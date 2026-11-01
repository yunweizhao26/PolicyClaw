#!/usr/bin/env python3
from __future__ import annotations

import argparse
import random
import sys
import time
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("store", choices=C.STORES)
    ap.add_argument("n", type=int)
    ap.add_argument("seed", type=int)
    C.add_data_dir(ap)
    a = ap.parse_args()
    t0 = time.time()
    sdir = C.store_dir(a.data_dir, a.store)
    ids = sorted(set(C.column_values(sdir / "ids", "app_id")))
    pick = random.Random(a.seed).sample(ids, min(a.n, len(ids)))
    table = pa.table({"store": [a.store] * len(pick), "app_id": pick, "draw_order": list(range(len(pick)))})
    out = sdir / "sample" / "part-00000.parquet"
    out.parent.mkdir(exist_ok=True)
    tmp = out.with_name("." + out.name + ".tmp")
    pq.write_table(table, tmp, compression="zstd", compression_level=C.ZSTD_LEVEL)
    tmp.replace(out)
    C.write_step_report(sdir, "sample", t0, {"population": len(ids), "n": len(pick), "seed": a.seed,
                                             "first_ids": pick[:5]})


if __name__ == "__main__":
    main()
