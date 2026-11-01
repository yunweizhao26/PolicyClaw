import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time


def rss_tree(pid):
    seen, total, pending = set(), 0, [pid]
    while pending:
        child = pending.pop()
        if child in seen:
            continue
        seen.add(child)
        try:
            for line in Path(f'/proc/{child}/status').read_text().splitlines():
                if line.startswith('VmRSS:'):
                    total += int(line.split()[1]) * 1024
            for path in Path(f'/proc/{child}/task').glob('*/children'):
                pending.extend(map(int, path.read_text().split()))
        except (OSError, ValueError):
            pass
    return total


def main():
    assert os.environ.get('SLURM_JOB_ID'), 'Run through Slurm on a compute node'
    step, *command = sys.argv[1:]
    output = Path(__file__).resolve().parent / 'metrics'
    output.mkdir(exist_ok=True)
    started = time.time()
    process = subprocess.Popen(command)
    peak = 0
    while process.poll() is None:
        peak = max(peak, rss_tree(process.pid))
        time.sleep(0.5)
    usage = resource.getrusage(resource.RUSAGE_CHILDREN)
    record = dict(step=step, command=command, started_at=started, finished_at=time.time(),
                  elapsed_s=time.time()-started, cpu_user_s=usage.ru_utime, cpu_system_s=usage.ru_stime,
                  peak_process_rss_kib=usage.ru_maxrss, peak_tree_rss_bytes=peak,
                  peak_tree_sample_interval_s=0.5, exit_code=process.returncode,
                  slurm_job_id=os.environ['SLURM_JOB_ID'], hostname=os.uname().nodename)
    metric_path = output / f'{step}.json'
    if metric_path.exists():
        old = json.loads(metric_path.read_text())
        metric_path.rename(output / f'{step}.previous-{int(old["started_at"]*1_000_000)}.json')
    metric_path.write_text(json.dumps(record, indent=2)+'\n')
    if step in ('final_report', 'v2_report') and process.returncode == 0:
        folder = output.parent
        report = folder/'report.md'
        line = (f'| {step} | {record["slurm_job_id"]} | {usage.ru_utime+usage.ru_stime:.3f} | '
                f'{record["elapsed_s"]:.3f} | {usage.ru_maxrss/1024:.3f} | {peak/1048576:.3f} | 0 |')
        report.write_text(report.read_text().replace('<!-- REPORT_RESOURCE -->', line))
        summary_path = folder/'report.json'
        summary = json.loads(summary_path.read_text())
        summary['resources'].append(record)
        summary_path.write_text(json.dumps(summary, indent=2)+'\n')
    sys.exit(process.returncode)


if __name__ == '__main__':
    main()
