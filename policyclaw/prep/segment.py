from __future__ import annotations

import re
from typing import List

SEGMENTER_VERSION = "section_paragraph_v15_exact_spans"
METHOD_ID = f"v4-{SEGMENTER_VERSION}-verified_context-one_prompt"
CHUNK_CHARS = 4000
BULLET_PREFIX = re.compile(r"^\s*(?:[-·•●*]|\([a-z0-9]+\))\s+", re.IGNORECASE)
BULLET_ONLY = re.compile(r"^\s*(?:[-·•●*]|\([a-z0-9]+\))\s*$", re.IGNORECASE)
SECTION_PATTERNS = [
    r'\n\s*\d+\.\s+[A-Z][^\n]+',
    r'\n\s*[A-Z][A-Z\s]+[A-Z]\s*\n',
    r'\n\s*#{1,3}\s+[^\n]+',
]


def merge_lines(text: str) -> str:
    raw_lines = [str(line or "").strip() for line in str(text or "").splitlines() if str(line or "").strip()]
    if not raw_lines:
        return ""
    normalized_lines: List[str] = []
    idx = 0
    while idx < len(raw_lines):
        line = raw_lines[idx]
        if BULLET_ONLY.match(line) and idx + 1 < len(raw_lines):
            normalized_lines.append(f"{line} {raw_lines[idx + 1]}".strip())
            idx += 2
            continue
        normalized_lines.append(line)
        idx += 1
    merged: List[str] = []
    for line in normalized_lines:
        if BULLET_PREFIX.match(line) and merged:
            merged[-1] = merged[-1] + "\n" + line
        else:
            merged.append(line)
    return "\n".join(merged).strip()


def is_fragment(para: str) -> bool:
    text = merge_lines(para)
    if not text:
        return False
    stripped = text.strip()
    line_count = len([ln for ln in stripped.splitlines() if ln.strip()])
    last_line = stripped.splitlines()[-1].strip() if stripped.splitlines() else stripped
    word_count = len(re.findall(r"\b\w+\b", stripped))
    has_terminal_punct = bool(re.search(r"[.!?:;]$", last_line))
    starts_bullet = bool(BULLET_PREFIX.match(stripped))
    if starts_bullet:
        return True
    if line_count <= 2 and word_count <= 8 and not has_terminal_punct:
        return True
    return False


def is_list_continuation(para: str) -> bool:
    text = merge_lines(para)
    if not text:
        return False
    return bool(BULLET_PREFIX.match(text))


def chunk_long_segment(segment: str, max_len: int = CHUNK_CHARS) -> List[str]:
    segment = str(segment or "").strip()
    if not segment:
        return []
    if len(segment) <= max_len:
        return [segment]
    parts = re.split(r'([.!?]\s+)', segment)
    chunked: List[str] = []
    current = ""
    for i in range(0, len(parts), 2):
        piece = parts[i] + (parts[i + 1] if i + 1 < len(parts) else "")
        while len(piece) > max_len:
            if current:
                chunked.append(current.strip())
                current = ""
            cut = piece.rfind(" ", 0, max_len + 1)
            cut = cut if cut > 0 else max_len
            chunked.append(piece[:cut].strip())
            piece = piece[cut:].strip()
        if len(current) + len(piece) > max_len and current:
            chunked.append(current.strip())
            current = piece
        else:
            current += piece
    if current.strip():
        chunked.append(current.strip())
    return chunked


def split_sections(text: str) -> List[str]:
    boundaries = []
    for pattern in SECTION_PATTERNS:
        for match in re.finditer(pattern, text):
            if text[: match.start()].rstrip().endswith(("(", "[", "{")):
                continue
            boundaries.append((match.start(), match.end()))
    boundaries.sort()
    if not boundaries:
        stripped = str(text or "").strip()
        return [stripped] if stripped else []
    sections: List[str] = []
    last_pos = 0
    for start, _end in boundaries:
        if start > last_pos:
            segment = text[last_pos:start].strip()
            if segment:
                sections.append(segment)
        last_pos = start
    if last_pos < len(text):
        segment = text[last_pos:].strip()
        if segment:
            sections.append(segment)
    return sections


def split_paragraphs(section: str) -> List[str]:
    raw_paragraphs = [merge_lines(p.strip()) for p in re.split(r'\n\s*\n', section)]
    paragraphs: List[str] = []
    pending_lead = ""
    list_block_open = False
    for para in raw_paragraphs:
        if not para:
            continue
        if pending_lead:
            if is_fragment(para):
                pending_lead += "\n" + para
                continue
            para = pending_lead + "\n\n" + para
            pending_lead = ""
        if is_fragment(para):
            if paragraphs:
                paragraphs[-1] = paragraphs[-1] + "\n" + para
            else:
                pending_lead = para
            continue
        if paragraphs and paragraphs[-1].rstrip().endswith(":"):
            paragraphs[-1] = paragraphs[-1] + "\n\n" + para
            list_block_open = True
            continue
        if list_block_open and is_list_continuation(para):
            paragraphs[-1] = paragraphs[-1] + "\n\n" + para
            continue
        list_block_open = False
        paragraphs.append(para)
        list_block_open = paragraphs[-1].rstrip().endswith(":")
    if pending_lead:
        if paragraphs:
            paragraphs[-1] = paragraphs[-1] + "\n" + pending_lead
        else:
            paragraphs.append(pending_lead)
    return [p.strip() for p in paragraphs if p.strip()]


def locate_segment_ranges(source: str, segments: list[str]) -> list[list[int]]:
    source_chars = [(index, char) for index, char in enumerate(source) if not char.isspace()]
    compact_source = "".join(char for _, char in source_chars)
    ranges = []
    cursor = 0
    for index, segment in enumerate(segments):
        compact_segment = "".join(char for char in segment if not char.isspace())
        if not compact_segment:
            raise ValueError(f"empty segment at index {index}")
        compact_start = compact_source.find(compact_segment, cursor)
        if compact_start < 0:
            raise ValueError(f"segment {index} changes non-whitespace source text")
        compact_end = compact_start + len(compact_segment)
        start = source_chars[compact_start][0]
        end = source_chars[compact_end - 1][0] + 1
        ranges.append([start, end])
        cursor = compact_end
    return ranges


def segment_policy(text: str) -> tuple[List[str], list[list[int]]]:
    segments: List[str] = []
    for section in split_sections(text):
        for paragraph in split_paragraphs(section):
            segments.append(paragraph)
    cleaned_segments = [chunk for segment in segments for chunk in chunk_long_segment(merge_lines(segment))]
    if cleaned_segments:
        ranges = locate_segment_ranges(text, cleaned_segments)
        cleaned_segments = [text[start:end] for start, end in ranges]
    else:
        ranges = []
    return cleaned_segments, ranges


def segment_document(policy_id: str, text: str) -> dict:
    segments, spans = segment_policy(text)
    assert len(segments) == len(spans)
    assert all(text[a:b] == s for s, (a, b) in zip(segments, spans))
    return {
        "policy": policy_id,
        "method_id": METHOD_ID,
        "source_chars": len(text),
        "segment_count": len(segments),
        "segments": [{"segment_id": i, "source_char_range": list(span), "text": s}
                     for i, (s, span) in enumerate(zip(segments, spans), 1)],
    }
