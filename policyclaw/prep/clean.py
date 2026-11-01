from __future__ import annotations

import json

from ..extract import load_prompt
from ..llm import LLM

SELECT = load_prompt("clean_select.txt")
VERIFY = load_prompt("clean_verify.txt")
MAX_TOKENS = 8192
MAX_CHUNK_CHARS = 24_000
CORE_CHUNK_CHARS = 20_000
OVERLAP_LINES = 5
SELECT_ATTEMPTS = 3
MAX_VERIFICATION_ATTEMPTS = 8
REQUIRED_APPROVALS = 2

RANGES = {"type": "array", "items": {"type": "array", "items": {"type": "integer", "minimum": 1},
                                     "minItems": 2, "maxItems": 2}}
LINES = {"type": "array", "items": {"type": "integer", "minimum": 1}}
SELECT_SCHEMA = {"type": "object", "properties": {"keep_line_ranges": RANGES, "mixed_lines": LINES},
                 "required": ["keep_line_ranges", "mixed_lines"], "additionalProperties": False}
VERIFY_SCHEMA = {"type": "object",
                 "properties": {"missing_policy_ranges": RANGES, "extraneous_selected_ranges": RANGES, "mixed_lines": LINES},
                 "required": ["missing_policy_ranges", "extraneous_selected_ranges", "mixed_lines"],
                 "additionalProperties": False}


def split_cores(lines, max_chars=CORE_CHUNK_CHARS):
    cores = []
    start = 0
    chars = 0
    for end, line in enumerate(lines):
        if end > start and chars + len(line) > max_chars:
            cores.append((start, end))
            start = end
            chars = 0
        chars += len(line)
    if start < len(lines):
        cores.append((start, len(lines)))
    return cores


def add_bounded_overlap(lines, start, end, max_chars=MAX_CHUNK_CHARS):
    sent_start, sent_end = start, end
    chars = sum(map(len, lines[start:end]))
    budget = max(max_chars, chars)
    for _ in range(OVERLAP_LINES):
        if sent_start and chars + len(lines[sent_start - 1]) <= budget:
            sent_start -= 1
            chars += len(lines[sent_start])
        if sent_end < len(lines) and chars + len(lines[sent_end]) <= budget:
            chars += len(lines[sent_end])
            sent_end += 1
    return sent_start, sent_end


def preserve_nonempty(first_pass, second_pass):
    return first_pass if first_pass.strip() and not second_pass.strip() else second_pass


def validation_error(result, line_count):
    if not isinstance(result, dict) or set(result) != {"keep_line_ranges", "mixed_lines"}:
        return "response must contain exactly keep_line_ranges and mixed_lines"
    value = result["keep_line_ranges"]
    previous_end = 0
    if not isinstance(value, list):
        return "keep_line_ranges must be an array"
    for line_range in value:
        if not isinstance(line_range, list) or len(line_range) != 2:
            return "each line range must contain two integers"
        start, end = line_range
        if type(start) is not int or type(end) is not int or not 1 <= start <= end <= line_count:
            return f"line ranges must stay between 1 and {line_count}"
        if start <= previous_end:
            return "line ranges must be ordered and non-overlapping"
        previous_end = end
    mixed_lines = result["mixed_lines"]
    if not isinstance(mixed_lines, list) or any(
        type(line) is not int or not 1 <= line <= line_count for line in mixed_lines
    ):
        return f"mixed_lines must contain integers between 1 and {line_count}"
    return None


def lines_from_ranges(ranges):
    return {line for start, end in ranges for line in range(start, end + 1)}


def verification_error(result, current, line_count):
    if not isinstance(result, dict) or set(result) != {
        "missing_policy_ranges",
        "extraneous_selected_ranges",
        "mixed_lines",
    }:
        return "response must contain exactly missing_policy_ranges, extraneous_selected_ranges, and mixed_lines"
    for key in ("missing_policy_ranges", "extraneous_selected_ranges"):
        error = validation_error({"keep_line_ranges": result[key], "mixed_lines": []}, line_count)
        if error:
            return f"{key}: {error}"
    error = validation_error({"keep_line_ranges": [], "mixed_lines": result["mixed_lines"]}, line_count)
    if error:
        return error
    return None


def call_model(llm: LLM, messages, schema):
    content = llm.complete(messages, MAX_TOKENS, schema=schema)
    try:
        return json.loads(content)
    except json.JSONDecodeError as error:
        raise RuntimeError(f"invalid model JSON: chars={len(content)} tail={content[-300:]!r}") from error


def selected_lines(result):
    selected = lines_from_ranges(result["keep_line_ranges"])
    selected.update(result["mixed_lines"])
    return selected


def materialize(lines, result):
    selected = selected_lines(result)
    return "".join(lines[line - 1] for line in sorted(selected))


def selection_from_lines(selected, mixed=()):
    mixed = set(mixed)
    kept = set(selected) - mixed
    ranges = []
    for line in sorted(kept):
        if ranges and line == ranges[-1][1] + 1:
            ranges[-1][1] = line
        else:
            ranges.append([line, line])
    return {"keep_line_ranges": ranges, "mixed_lines": sorted(mixed)}


def conservative_union(candidates):
    mixed = set().union(*(candidate["mixed_lines"] for candidate in candidates))
    selected = set().union(*(selected_lines(candidate) for candidate in candidates))
    return selection_from_lines(selected, mixed)


def tagged_source(lines, current):
    selected = selected_lines(current)
    return "".join(
        f"[{'KEEP' if number in selected else 'REST'} {number:04d}] {line}"
        for number, line in enumerate(lines, 1)
    )


def normalize_review(reviewed, line_count):
    normalized = dict(reviewed)
    for key in ("missing_policy_ranges", "extraneous_selected_ranges"):
        selected = set()
        for start, end in reviewed[key]:
            start, end = sorted((start, end))
            start, end = max(1, start), min(line_count, end)
            if start <= end:
                selected.update(range(start, end + 1))
        normalized[key] = selection_from_lines(selected)["keep_line_ranges"]
    normalized["mixed_lines"] = sorted({line for line in reviewed["mixed_lines"] if 1 <= line <= line_count})
    return normalized


def apply_review(current, reviewed):
    selected = selected_lines(current)
    missing = lines_from_ranges(reviewed["missing_policy_ranges"]) - selected
    extraneous = lines_from_ranges(reviewed["extraneous_selected_ranges"]) & selected
    selected.update(missing)
    selected.difference_update(extraneous)
    selected.update(reviewed["mixed_lines"])
    return selection_from_lines(selected, reviewed["mixed_lines"])


def verify_selection(llm: LLM, lines, initial):
    current = initial
    history = [current]
    attempts = []
    approvals = 0
    cycle_resolution = None
    for _ in range(MAX_VERIFICATION_ATTEMPTS):
        raw_reviewed = call_model(llm, [{"role": "system", "content": VERIFY},
                                        {"role": "user", "content": tagged_source(lines, current)}], VERIFY_SCHEMA)
        reviewed = normalize_review(raw_reviewed, len(lines))
        error = verification_error(reviewed, current, len(lines))
        if error:
            raise RuntimeError(f"invalid complement audit: {error}")
        proposed = apply_review(current, reviewed)
        attempts.append({"response": raw_reviewed, "normalized_response": reviewed, "error": None, "proposed": proposed})
        if proposed == current:
            approvals += 1
            if approvals == REQUIRED_APPROVALS:
                return current, {"attempts": attempts, "success": True, "cycle_resolution": cycle_resolution}
            continue
        approvals = 0
        if proposed in history:
            proposed = conservative_union([*history, proposed])
            cycle_resolution = "conservative_union"
            attempts[-1]["proposed"] = proposed
            return proposed, {"attempts": attempts, "success": True, "cycle_resolution": cycle_resolution}
        history.append(proposed)
        current = proposed
    raise RuntimeError(f"complement audit did not converge after {MAX_VERIFICATION_ATTEMPTS} attempts: "
                       f"{json.dumps(attempts)}")


def clean_segment(llm: LLM, original, numbered):
    lines = original.splitlines(keepends=True)
    messages = [
        {"role": "system", "content": SELECT},
        {"role": "user", "content": "Numbered website text follows.\n\n" + numbered},
    ]
    attempts = []
    for _ in range(SELECT_ATTEMPTS):
        result = call_model(llm, messages, SELECT_SCHEMA)
        error = validation_error(result, len(lines))
        attempts.append({"response": result, "error": error})
        if error is None:
            break
        messages.extend([
            {"role": "assistant", "content": json.dumps(result)},
            {"role": "user", "content": f"That response is invalid: {error}. Correct it."},
        ])
    if error is not None:
        raise RuntimeError(f"line-range selection stayed invalid after {SELECT_ATTEMPTS} attempts")
    current = {key: result[key] for key in ("keep_line_ranges", "mixed_lines")}
    result, verification = verify_selection(llm, lines, current)
    return materialize(lines, result), {"attempts": attempts, "verification": verification, "response": result,
                                        "valid": True}


def clean_pass(llm: LLM, source):
    lines = source.splitlines(keepends=True)
    selected = set()
    mixed = set()
    chunk_audits = []
    for index, (core_start, core_end) in enumerate(split_cores(lines), 1):
        sent_start, sent_end = add_bounded_overlap(lines, core_start, core_end)
        chunk_lines = lines[sent_start:sent_end]
        chunk = "".join(chunk_lines)
        numbered = "".join(f"[{number:04d}] {line}" for number, line in enumerate(chunk_lines, 1))
        _, audit = clean_segment(llm, chunk, numbered)
        ranges = audit["response"]["keep_line_ranges"]
        mixed_lines = audit["response"]["mixed_lines"]
        for start, end in ranges:
            selected.update(range(sent_start + start, sent_start + end + 1))
        mixed.update(sent_start + line for line in mixed_lines)
        selected.update(sent_start + line for line in mixed_lines)
        chunk_audits.append({
            "chunk": index,
            "core_global_lines": [core_start + 1, core_end],
            "sent_global_lines": [sent_start + 1, sent_end],
            "sent_chars": len(chunk),
            "selected_local_ranges": ranges,
            "selected_global_lines": sorted({sent_start + line for start, end in ranges for line in range(start, end + 1)}
                                            | {sent_start + line for line in mixed_lines}),
            "mixed_global_lines": [sent_start + line for line in mixed_lines],
            "model_audit": audit,
        })
    initial = selection_from_lines(selected, mixed)
    if lines:
        final, global_verification = verify_selection(llm, lines, initial)
    else:
        final = initial
        global_verification = {"attempts": [], "success": True, "empty_source": True}
    return materialize(lines, final), {
        "source_lines": len(lines),
        "source_chars": len(source),
        "cleaned_lines": len(selected_lines(final)),
        "mixed_global_lines": final["mixed_lines"],
        "chunks": chunk_audits,
        "global_verification": global_verification,
    }


def clean(llm: LLM, text):
    first, audit1 = clean_pass(llm, text)
    second, audit2 = clean_pass(llm, first)
    return first, preserve_nonempty(first, second), {"first": audit1, "second": audit2}
