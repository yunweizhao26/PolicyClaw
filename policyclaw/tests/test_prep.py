import json

from policyclaw.prep import clean
from policyclaw.prep.clean import (apply_review, clean_segment, conservative_union, normalize_review, preserve_nonempty,
                                   split_cores, validation_error, verification_error)

APPROVE = '{"missing_policy_ranges":[],"extraneous_selected_ranges":[],"mixed_lines":[]}'


class Replies:

    def __init__(self, *replies):
        self.replies, self.requests = list(replies), []

    def complete(self, messages, max_tokens, schema=None):
        self.requests.append(messages)
        return self.replies.pop(0)


def raises(fn, text):
    try:
        fn()
    except RuntimeError as e:
        assert text in str(e), str(e)
        return
    raise AssertionError(f"no RuntimeError mentioning {text!r}")


def test_original_self_checks():
    assert split_cores(["a" * 6, "b" * 6, "c"], 10) == [(0, 1), (1, 3)]
    assert split_cores(["x" * 20, "y"], 10) == [(0, 1), (1, 2)]
    assert preserve_nonempty("policy\n", "") == "policy\n"
    assert preserve_nonempty("policy\n", "cleaner\n") == "cleaner\n"
    assert validation_error({"keep_line_ranges": [[1, 1], [3, 4]], "mixed_lines": []}, 4) is None
    assert validation_error({"keep_line_ranges": [[0, 1]], "mixed_lines": []}, 4)
    assert verification_error({"missing_policy_ranges": [], "extraneous_selected_ranges": [], "mixed_lines": []},
                              {"keep_line_ranges": [[1, 2]], "mixed_lines": []}, 2) is None
    assert conservative_union([{"keep_line_ranges": [[1, 2]], "mixed_lines": []},
                               {"keep_line_ranges": [[1, 1]], "mixed_lines": [3]}]) == {"keep_line_ranges": [[1, 2]], "mixed_lines": [3]}
    assert normalize_review({"missing_policy_ranges": [[3, 8], [2, 2]], "extraneous_selected_ranges": [[4, 3]], "mixed_lines": [1, 9]}, 4) \
        == {"missing_policy_ranges": [[2, 4]], "extraneous_selected_ranges": [[3, 4]], "mixed_lines": [1]}
    assert apply_review({"keep_line_ranges": [[1, 2]], "mixed_lines": []},
                        {"missing_policy_ranges": [[2, 3]], "extraneous_selected_ranges": [[2, 3]], "mixed_lines": []}) \
        == {"keep_line_ranges": [[1, 1], [3, 3]], "mixed_lines": []}


def test_invalid_selection_is_returned_with_its_error():
    model = Replies('{"keep_line_ranges":[[0,9]],"mixed_lines":[]}', '{"keep_line_ranges":[[1,1]],"mixed_lines":[]}', APPROVE, APPROVE)
    cleaned, audit = clean_segment(model, "policy\nfooter\n", "[0001] policy\n[0002] footer\n")
    assert cleaned == "policy\n" and len(audit["attempts"]) == 2 and len(audit["verification"]["attempts"]) == 2
    retry = model.requests[1]
    assert retry[0] == {"role": "system", "content": clean.SELECT}
    assert retry[2] == {"role": "assistant", "content": json.dumps({"keep_line_ranges": [[0, 9]], "mixed_lines": []})}
    assert retry[3]["content"] == "That response is invalid: line ranges must stay between 1 and 2. Correct it."


def test_three_invalid_selections_or_a_reply_that_is_not_json_fail():
    bad = '{"keep_line_ranges":[[2,1]],"mixed_lines":[]}'
    raises(lambda: clean_segment(Replies(bad, bad, bad), "policy\n", "[0001] policy\n"), "after 3 attempts")
    raises(lambda: clean_segment(Replies(""), "policy\n", "[0001] policy\n"), "invalid model JSON")


def test_audit_needs_two_consecutive_approvals_and_resolves_a_cycle_by_union():
    drop = '{"missing_policy_ranges":[],"extraneous_selected_ranges":[[2,2]],"mixed_lines":[]}'
    add = '{"missing_policy_ranges":[[2,2]],"extraneous_selected_ranges":[],"mixed_lines":[]}'
    final, audit = clean.verify_selection(Replies(APPROVE, drop, APPROVE, APPROVE), ["a\n", "b\n"], {"keep_line_ranges": [[1, 2]], "mixed_lines": []})
    assert final == {"keep_line_ranges": [[1, 1]], "mixed_lines": []} and len(audit["attempts"]) == 4
    final, audit = clean.verify_selection(Replies(drop, add), ["a\n", "b\n"], {"keep_line_ranges": [[1, 2]], "mixed_lines": []})
    assert final == {"keep_line_ranges": [[1, 2]], "mixed_lines": []} and audit["cycle_resolution"] == "conservative_union"
