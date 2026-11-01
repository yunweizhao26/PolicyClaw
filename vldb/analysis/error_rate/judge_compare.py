import concurrent.futures as cf, csv, json, os, random, sys

sys.path.insert(0, os.path.dirname(__file__))
import estimate_error as ee
from policyclaw.llm import make_llm

out, n, judges = sys.argv[1], int(sys.argv[2]), sys.argv[3:]
rows = list(csv.DictReader(open(f"{ee.FINAL}/review/e1_ann.csv")))
random.Random(7).shuffle(rows)
w = {r["record_id"]: float(r["sample_weight"]) for r in csv.DictReader(open(f"{ee.FINAL}/e1/source.csv"))}
items = []
for r in rows[:n]:
    rec = json.loads(r["record"])
    items.append({"id": r["record_id"], "human": r["fidelity"], "claim": {
        "record_id": r["record_id"], **{k: rec.get(k, "") for k in
                                        ("polarity", "actor", "action", "attribute", "counterparty", "condition", "condition_predicate")},
        "source_segment": r["source_segment"], "policy_context": ""}})
sub = lambda f: f == "substantial"
print(f"{len(items)} E1 items, human substantial {sum(sub(x['human']) for x in items)}")
for spec in judges:
    model, thinking = spec.split(":")
    llm = make_llm(model, os.path.join(out, f"cache_{model}_{thinking}"), seed=42)
    if hasattr(llm, "thinking_level"):
        llm.thinking_level = thinking
    with cf.ThreadPoolExecutor(int(os.environ.get("THREADS", 8))) as ex:
        verdicts = list(ex.map(lambda x: ee.judge(llm, x["claim"]), items))
    with open(os.path.join(out, f"judged_{model}_{thinking}.jsonl"), "w") as f:
        for x, v in zip(items, verdicts):
            f.write(json.dumps({**x, "judge": v}, ensure_ascii=False) + "\n")
    tp = sum(sub(x["human"]) and sub(v["fidelity"]) for x, v in zip(items, verdicts))
    pos = sum(sub(x["human"]) for x in items)
    tn = sum(not sub(x["human"]) and not sub(v["fidelity"]) for x, v in zip(items, verdicts))
    neg = len(items) - pos
    wrate = lambda f: sum(w[x["id"]] for x, v in zip(items, verdicts) if f(x, v)) / sum(w[x["id"]] for x in items)
    u = llm.usage.as_dict()
    print(f"{model} {thinking}: sensitivity {tp / pos:.3f}, specificity {tn / neg:.3f}, Youden {tp / pos + tn / neg - 1:.3f}, "
          f"weighted substantial human {wrate(lambda x, v: sub(x['human'])):.3f} judge {wrate(lambda x, v: sub(v['fidelity'])):.3f}, "
          f"exact agreement {sum(x['human'] == v['fidelity'] for x, v in zip(items, verdicts)) / len(items):.3f}; "
          f"tokens in {u['prompt_tokens']:,} out {u['completion_tokens']:,} thinking {u['thinking_tokens']:,}", flush=True)
