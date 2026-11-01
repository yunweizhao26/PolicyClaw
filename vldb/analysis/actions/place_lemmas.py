import collections, concurrent.futures as cf, json, os, sys

sys.path.insert(0, "/scratch/yz5944/nlp+privacy/PolicyClaw")
from policyclaw.llm import make_llm
from policyclaw.schema import SCHEMA

COVERED = """You organise the verbs that privacy policies use for operations on personal data.

The operation tree, from GDPR Article 4(2):
{tree}

A privacy policy uses the verb "{lemma}" for the operation "{op}" in these extracted practices:
{examples}

Relate the verb, as used here, to the operation "{op}":
- "same": the verb names this operation.
- "narrower": the verb names a specific kind of this operation.
- "not a data operation": the verb names no operation on personal data.
Return only JSON: {{"relation": "same" or "narrower" or "not a data operation", "reason": "one short sentence"}}"""

UNCOVERED = """You organise the verbs that privacy policies use for operations on personal data.

The operation tree, from GDPR Article 4(2):
{tree}

A privacy policy uses the verb "{lemma}" in these extracted practices, and the extractor found no operation of the tree for it:
{examples}

Decide, as the verb is used here:
- "same" or "narrower": an operation of the tree does fit after all; name it.
- "new operation": the verb names an operation on personal data that no operation of the tree describes; propose a short name for it.
- "not a data operation": the verb names no operation on personal data.
Return only JSON: {{"relation": one of the four, "operation": the operation name for "same" or "narrower", otherwise "", "proposed_name": a short name for "new operation", otherwise "", "reason": "one short sentence"}}"""


def main(nodes_path, out_prefix):
    nodes = json.load(open(nodes_path))
    tree = SCHEMA.operations_prompt()
    other = SCHEMA.uncovered["label"]
    llms = [make_llm(os.environ["LLM_MODEL_NAME"], os.path.join(os.path.dirname(out_prefix), "llm_cache"), seed=s) for s in (1, 2, 3)]

    def place(x):
        examples = "\n".join(f"- {e}" for e in x["examples"])
        votes = []
        for llm in llms:
            if x["operation"] == other:
                v = llm.json(UNCOVERED.format(tree=tree, lemma=x["lemma"], examples=examples), max_tokens=1024)
                rel = v.get("relation") if v.get("relation") in ("same", "narrower", "new operation", "not a data operation") else "invalid"
                op = v.get("operation", "") if rel in ("same", "narrower") and v.get("operation") in SCHEMA.operations else ""
                if rel in ("same", "narrower") and not op:
                    rel = "invalid"
                votes.append((rel, op, str(v.get("proposed_name") or "").lower() if rel == "new operation" else ""))
            else:
                v = llm.json(COVERED.format(tree=tree, lemma=x["lemma"], op=x["operation"], examples=examples), max_tokens=1024)
                rel = v.get("relation") if v.get("relation") in ("same", "narrower", "not a data operation") else "invalid"
                votes.append((rel, x["operation"] if rel in ("same", "narrower") else "", ""))
        key = collections.Counter((r, o) for r, o, _ in votes).most_common(1)[0]
        (rel, op), n = key
        names = [p for r, _, p in votes if r == "new operation" and p]
        return {**x, "relation": rel if n >= 2 else "no majority", "placed_under": op if n >= 2 else "",
                "proposed_names": names, "agreement": n, "votes": votes}

    with cf.ThreadPoolExecutor(int(os.environ.get("THREADS", 8))) as ex:
        placed = list(ex.map(place, nodes))
    json.dump(placed, open(f"{out_prefix}.json", "w"), indent=1, ensure_ascii=False)

    total = sum(x["count"] for x in placed)
    agree = collections.Counter(x["agreement"] for x in placed)
    lines = [f"{len(placed)} verb-operation nodes covering {total} rules; unanimous {agree[3]}, two of three {agree[2]}, split {agree[1]}",
             f"usage: {[l.usage.as_dict() for l in llms]}", ""]
    unc = [x for x in placed if x["operation"] == other]
    lines.append(f"COVERAGE: the extractor marked {sum(x['count'] for x in unc)} of {total} rules ({100 * sum(x['count'] for x in unc) / max(1, total):.2f}%) "
                 f"as an operation outside the tree, over {len(unc)} verbs")
    for rel in ("same", "narrower", "new operation", "not a data operation", "no majority", "invalid"):
        xs = sorted((x for x in unc if x["relation"] == rel), key=lambda x: -x["count"])
        if xs:
            lines.append(f"  {rel}: {sum(x['count'] for x in xs)} rules: " + "; ".join(
                f"{x['lemma']} ({x['count']}{', under ' + x['placed_under'] if x['placed_under'] else ''}"
                f"{', proposed: ' + '/'.join(sorted(set(x['proposed_names']))) if x['proposed_names'] else ''})" for x in xs[:40]))
    lines.append("")
    for op in SCHEMA.operations:
        mine = [x for x in placed if x["placed_under"] == op]
        same = sorted((x for x in mine if x["relation"] == "same"), key=lambda x: -x["count"])
        narrow = sorted((x for x in mine if x["relation"] == "narrower"), key=lambda x: -x["count"])
        if same or narrow:
            lines.append(f"{op}\n    same as: " + ", ".join(f"{x['lemma']} ({x['count']})" for x in same[:25])
                         + "\n    narrower: " + ", ".join(f"{x['lemma']} ({x['count']})" for x in narrow[:25]))
    bad = sorted((x for x in placed if x["operation"] != other and x["relation"] in ("not a data operation", "no majority", "invalid")),
                 key=lambda x: -x["count"])
    lines.append("[covered operation, but the verb names no data operation or had no majority] "
                 + ", ".join(f"{x['lemma']}@{x['operation']} ({x['count']}, {x['relation']})" for x in bad[:40]))
    open(f"{out_prefix}.txt", "w").write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
