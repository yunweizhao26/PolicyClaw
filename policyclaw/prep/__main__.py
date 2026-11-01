import argparse, json, os, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from ..llm import make_llm
from .clean import clean
from .segment import segment_document

F01 = "01_frozen_plaintext_pipeline_input.txt"
F02 = "02_first_pass_cleaned.txt"
F03 = "03_qwen_complement_verified_cleaned_pipeline_input.txt"
F05 = "05_segments_v15_exact.json"


def write_new(path, text):
    with path.open("x", encoding="utf-8") as handle:
        handle.write(text)


def prepare(job, out, model, cache):
    policy_id, path, *stored03 = job
    folder = out / policy_id
    folder.mkdir()
    text = Path(path).read_text(encoding="utf-8")
    if not text:
        raise ValueError(f"empty input {path}")
    write_new(folder / F01, text)
    usage = {}
    if model is None:
        first = final = Path(stored03[0]).read_text(encoding="utf-8")
    else:
        llm = make_llm(model, cache)
        first, final, audit = clean(llm, text)
        usage = llm.usage.as_dict()
        write_new(folder / "cleanup_audit.json",
                  json.dumps({**audit, "model": llm.model, "variant": llm.variant, "usage": usage}) + "\n")
    write_new(folder / F02, first)
    write_new(folder / F03, final)
    if final.strip():
        write_new(folder / F05, json.dumps(segment_document(policy_id, final), indent=2, ensure_ascii=False) + "\n")
    return final, usage


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("tsv", type=Path)
    parser.add_argument("out", type=Path)
    parser.add_argument("--no-model", action="store_true")
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    out = args.out.resolve()
    jobs = [line.rstrip("\n").split("\t") for line in args.tsv.read_text().splitlines() if line.strip()]
    for policy_id, *_ in jobs:
        if "/" in policy_id or policy_id in ("", ".", "..", "llm_cache", ".partial"):
            raise SystemExit(f"bad id {policy_id!r}")
        if (out / policy_id).exists() and not args.resume:
            raise SystemExit(f"refusing to overwrite {out / policy_id}")
    if args.resume:
        done = [j for j in jobs if (out / j[0] / F03).exists()]
        for policy_id, *_ in jobs:
            folder = out / policy_id
            if folder.exists() and not (folder / F03).exists():
                (out / ".partial").mkdir(parents=True, exist_ok=True)
                folder.rename(out / ".partial" / f"{policy_id}.{len(list((out / '.partial').glob(policy_id + '.*')))}")
        jobs = [j for j in jobs if j not in done]
        print(f"resume: {len(done)} done, {len(jobs)} to prepare", flush=True)
    if not args.no_model and not os.environ.get("LLM_MODEL_NAME"):
        raise SystemExit("LLM_MODEL_NAME is required unless --no-model is given")
    model = None if args.no_model else os.environ["LLM_MODEL_NAME"]
    cache = os.environ.get("LLM_CACHE") or str(out / "llm_cache")
    out.mkdir(parents=True, exist_ok=True)
    failed, total = 0, {}
    with ThreadPoolExecutor(int(os.environ.get("THREADS", 8))) as pool:
        for job, future in [(j, pool.submit(prepare, j, out, model, cache)) for j in jobs]:
            try:
                final, usage = future.result()
            except Exception as error:
                failed += 1
                print(f"FAILED {job[0]}: {error!r}", flush=True)
                continue
            total = {k: total.get(k, 0) + v for k, v in usage.items()}
            print(f"done {job[0]} cleaned_chars={len(final)} {json.dumps(usage)}", flush=True)
    print(f"policies={len(jobs)} failed={failed} usage={json.dumps(total)}", flush=True)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
