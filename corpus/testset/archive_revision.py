import json
import shutil

from base import OUT, now, require_compute, sha, write_json

PROTECTED = ('DESIGN.md', 'pipeline_inputs.py', 'run_pipeline.s')


def main():
    require_compute()
    dest = OUT/'v1'
    dest.mkdir(exist_ok=True)
    marker = dest/'archive_manifest.json'
    if marker.exists():
        record = json.loads(marker.read_text())
        for name, digest in record['protected_files'].items():
            assert sha((OUT/name).read_bytes()) == digest, f'Protected file changed: {name}'
        return
    patterns = ('selection.*', 'selection_state.json', 'texts', 'rejected.*', 'report.md', 'report.json',
        'audit.json', 'cross_arm_organizations.*', 'candidates_*.parquet', 'frame_*.json', 'frame_rejected_*.parquet',
        'exclusions.json', 'exclusions.parquet', 'policyie_source_audit.json', 'code_provenance.json',
        'development_sites_audit.json', 'package_versions.json', 'verify.jsonl', 'verify_input.tsv',
        'verification_config.json', 'run_status.json', 'failure.json')
    pending = dest/'archive_pending.json'
    if pending.exists():
        record = json.loads(pending.read_text())
    else:
        paths = sorted({p for pattern in patterns for p in OUT.glob(pattern)})
        assert (OUT/'selection.parquet') in paths, 'No first-run selection to archive'
        files = {str(f.relative_to(OUT)): sha(f.read_bytes()) for p in paths
                 for f in (sorted(p.rglob('*')) if p.is_dir() else [p]) if f.is_file()}
        record = dict(at=now(), paths=[p.name for p in paths], sha256=files,
                      protected_files={name:sha((OUT/name).read_bytes()) for name in PROTECTED})
        write_json(pending, record)
    for name in record['paths']:
        source, target = OUT/name, dest/name
        if target.exists():
            assert not source.exists(), f'Archive destination already exists: {target}'
        else:
            shutil.move(str(source), str(target))
    for name, digest in record['sha256'].items():
        assert sha((dest/name).read_bytes()) == digest, f'Archive hash mismatch: {name}'
    pending.replace(marker)
    print('Archived first-run outputs:', len(record['paths']), flush=True)


if __name__ == '__main__':
    main()
