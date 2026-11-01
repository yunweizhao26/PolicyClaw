#!/usr/bin/env python3
import collections, csv, json, re, sys
from pathlib import Path

from rapidfuzz import fuzz
from unidecode import unidecode

from poligrapher.annotators import CollectionAnnotator
from poligrapher.graph_utils import KGraph

BL = Path(__file__).resolve().parents[1]
W = BL / "work"
DIRS = W / "poligraph/workdirs"
CORPUS = BL.parent / "baseline_corpus"
OUT = BL / "poligraph"


def shard_status():
    statuses = [json.load(open(p)) for p in sorted((W / "poligraph/shards").glob("shard_*/status.json"))]
    assert statuses and len(statuses) == statuses[0]["nshards"], "missing shard status files"
    policies = sorted(p for s in statuses for p in s["policies"])
    assert len(policies) == len(set(policies)) == 200, len(policies)
    failed = {p: f for s in statuses for p, f in s["failed"].items()}
    done = [p for p in policies if p not in failed and (DIRS / p / "graph-extended.yml").is_file()]
    return statuses, policies, failed, done


REWRITES = [(re.compile(r"\be-mails?\b", re.I), "email"), (re.compile(r"\bwi-fi\b", re.I), "WiFi"),
            (re.compile(r"\bgeo-location\b", re.I), "geolocation"), (re.compile(r"\bid\b"), "ID"),
            (re.compile(r"\b(\w+)\(s\)"), r"\1s")]


def visible_index(text):
    chars, ptr = [], []
    for i, c in enumerate(text):
        for ch in unidecode(c):
            chars.append(ch)
            ptr.append(i)
    for regex, repl in REWRITES:
        s, new_chars, new_ptr, last = "".join(chars), [], [], 0
        for m in regex.finditer(s):
            new_chars += chars[last:m.start()]
            new_ptr += ptr[last:m.start()]
            r = m.expand(repl)
            new_chars += list(r)
            new_ptr += [ptr[m.start() + min(j, m.end() - m.start() - 1)] for j in range(len(r))]
            last = m.end()
        chars, ptr = new_chars + chars[last:], new_ptr + ptr[last:]
    keep = [k for k, ch in enumerate(chars) if not ch.isspace()]
    return "".join(chars[k].lower() for k in keep), [ptr[k] for k in keep]


def squash(s):
    return "".join(ch.lower() for ch in s if not ch.isspace())


def exact(needle, text, index):
    flat, ptr = index
    k = flat.find(needle) if needle else -1
    return text[ptr[k]:ptr[k + len(needle) - 1] + 1] if k >= 0 else None


def locate(sentence, text, index):
    flat, ptr = index
    needle = squash(sentence)
    if not needle:
        return "", "none"
    found = exact(needle, text, index)
    if found is not None:
        return found, "exact"
    lines = [squash(p) for p in sentence.split("\n") if p.strip()]
    if len(lines) > 1:
        parts = [exact(p, text, index) for p in lines]
        if all(p is not None for p in parts):
            return "\n".join(parts), "exact_lines"
    m = fuzz.partial_ratio_alignment(needle, flat, score_cutoff=90)
    if m is not None and m.dest_end > m.dest_start:
        return text[ptr[m.dest_start]:ptr[m.dest_end - 1] + 1], f"fuzzy:{m.score:.1f}"
    return "", "none"


def edge_texts(graph, label):
    found = {}
    for u, v, key, data in graph.edges(keys=True, data=True):
        name = f"{key}({u}, {v})"
        assert name not in found, (label, name)
        found[name] = data["text"]
    return found


def clean(texts):
    out = []
    for t in texts:
        t = t.strip()
        if t and t not in out:
            out.append(t)
    return out


def normalize():
    statuses, policies, failed, done = shard_status()
    rows = list(csv.DictReader(open(OUT / "contradictions.csv", newline="", encoding="utf-8")))
    fields = ["app_id", "pos_edge", "neg_edge", "pos_text", "neg_text"]
    graphs, texts = {}, {}
    out = []
    for n, r in enumerate(rows, 1):
        pid = r["app_id"]
        if pid not in graphs:
            kg = KGraph(str(DIRS / pid / "graph.yml"))
            graphs[pid] = (edge_texts(kg.positive_kgraph, pid), edge_texts(kg.negative_kgraph, pid))
            body = (CORPUS / "plaintext_policies" / f"{pid}.txt").read_text(encoding="utf-8")
            texts[pid] = (body, visible_index(body))
        pos_all, neg_all = graphs[pid][0][r["pos_edge"]], graphs[pid][1][r["neg_edge"]]
        assert "\n".join(pos_all) == r["pos_text"] and "\n".join(neg_all) == r["neg_text"], (pid, n)
        pos, neg = clean(pos_all), clean(neg_all)
        body, index = texts[pid]
        pos_vis = [locate(s, body, index) for s in pos]
        neg_vis = [locate(s, body, index) for s in neg]
        out.append({"policy_id": pid, "positive_sentence": "\n".join(pos), "negative_sentence": "\n".join(neg),
                    "n_positive_sentences": len(pos), "n_negative_sentences": len(neg),
                    "positive_sentence_visible": "\n".join(v for v, _ in pos_vis),
                    "negative_sentence_visible": "\n".join(v for v, _ in neg_vis),
                    "positive_visible_match": ";".join(m for _, m in pos_vis),
                    "negative_visible_match": ";".join(m for _, m in neg_vis),
                    **{k: r[k] for k in fields}, "official_row": n})
    with open(OUT / "contradictions_normalized.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0]) if out else ["policy_id", "positive_sentence", "negative_sentence", *fields])
        w.writeheader()
        w.writerows(out)

    matches = collections.Counter(m.split(":")[0] for x in out for side in ("positive_visible_match", "negative_visible_match")
                                  for m in x[side].split(";") if m)
    recl = list(csv.DictReader(open(OUT / "policylint_reclassified.csv", newline="", encoding="utf-8")))
    labels = collections.Counter(l for r in recl for l in r["labels"].splitlines() if l)
    log = (W / "logs" / "poligraph_reclassify.log").read_text(errors="replace")
    unique = re.findall(r"Number of unique PolicyLint tuples: (\d+)", log)
    summary = {
        "policies": len(policies),
        "completed_all_steps": len(done),
        "failed": {p: {"step": f["failed_step"], "rc": f.get("rc"), "log": f.get("log"), "tail": f.get("tail", [])[-3:]}
                   for p, f in sorted(failed.items())},
        "completed_without_graph": [p for p in policies if p not in failed and p not in done],
        "contradiction_rows": len(out),
        "policies_with_contradictions": len({x["policy_id"] for x in out}),
        "rows_with_several_sentences_on_a_side": sum(x["n_positive_sentences"] > 1 or x["n_negative_sentences"] > 1 for x in out),
        "distinct_policy_sentence_pairs": len({(x["policy_id"], x["positive_sentence"], x["negative_sentence"]) for x in out}),
        "visible_text_match_per_sentence": dict(matches),
        "reclassifier_rows": len(recl),
        "reclassifier_rows_by_label": dict(sorted(labels.items())),
        "reclassifier_unique_policylint_tuples": int(unique[-1]) if unique else None,
    }
    json.dump(summary, open(OUT / "summary.json", "w"), indent=1)
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    if sys.argv[1] == "list":
        print("\n".join(str(DIRS / p) for p in shard_status()[3]))
    elif sys.argv[1] == "normalize":
        normalize()
    else:
        sys.exit(__doc__)
