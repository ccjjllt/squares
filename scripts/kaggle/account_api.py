"""Run Kaggle operations with an explicitly selected account, without global changes.

Use a Python environment containing the official kaggle CLI package. The access
token is read locally and is never written into the notebook bundle or reports.
"""

import argparse
import json
import os
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--account", default="qingyu1232")
    parser.add_argument("--receipt", type=Path)
    sub = parser.add_subparsers(dest="action", required=True)
    sub.add_parser("quota")
    push = sub.add_parser("push")
    push.add_argument("folder", type=Path)
    push.add_argument("--timeout", type=int, default=1800)
    push.add_argument("--accelerator", default="NvidiaTeslaT4")
    for name in ("status", "logs", "output"):
        action = sub.add_parser(name)
        action.add_argument("kernel")
        if name == "output":
            action.add_argument("directory", type=Path)
            action.add_argument(
                "--pattern",
                default=(
                    r"(summary\.json|events\.jsonl|improved_groups\.csv|per_n_gains\.json|"
                    r"submission\.csv|environment\.json|"
                    r"(?:near_misses|winners|donors)\.(json|npz))$"
                ),
            )
    args = parser.parse_args()
    if not args.account.replace("_", "").isalnum():
        raise ValueError("Invalid account name")
    token_path = Path.home() / ".kaggle" / f"access_token_{args.account}"
    os.environ["KAGGLE_API_TOKEN"] = token_path.read_text().strip()
    from kaggle.api.kaggle_api_extended import KaggleApi

    api = KaggleApi()
    api.authenticate()
    actual = api.get_config_value(api.CONFIG_NAME_USER)
    if actual != args.account:
        raise RuntimeError("Selected credential does not belong to requested account")
    if args.action == "quota":
        quota = api.quota_view()
        # SDK to_dict serializes timedelta.seconds without days (30h becomes 6h).
        result = {"quota_refresh_time": quota.quota_refresh_time.isoformat()}
        for name, resource in (("gpu", quota.gpu_quota), ("tpu", quota.tpu_quota)):
            if resource is not None:
                used = resource.time_used.total_seconds()
                reserved = resource.time_reserved.total_seconds()
                total = resource.total_time_allowed.total_seconds()
                result[name] = {
                    "used_seconds": used,
                    "reserved_seconds": reserved,
                    "total_seconds": total,
                    "available_seconds": max(0.0, total - used - reserved),
                }
    elif args.action == "push":
        meta = json.loads((args.folder / "kernel-metadata.json").read_text())
        if not meta["id"].startswith(args.account + "/") or not meta.get("is_private"):
            raise ValueError("Pilot must be private and owned by the selected account")
        try:
            result = api.kernels_push(
                str(args.folder), timeout=args.timeout, acc=args.accelerator
            ).to_dict()
        except Exception as exc:
            response = getattr(exc, "response", None)
            if response is None:
                raise
            result = {
                "error": type(exc).__name__,
                "status_code": response.status_code,
                "server_message": response.text[:4000],
            }
    else:
        if not args.kernel.startswith(args.account + "/"):
            raise ValueError("Only operate on the selected account's notebook")
        if args.action == "status":
            result = api.kernels_status(args.kernel).to_dict()
        elif args.action == "logs":
            raw = api.kernels_logs(args.kernel)
            result = {"log": json.loads(raw) if raw else []}
        else:
            files, token = api.kernels_output(
                args.kernel,
                str(args.directory),
                file_pattern=args.pattern,
                force=True,
                quiet=True,
                page_size=100,
            )
            result = {"files": files, "next_page_token": token}
    report = {"account": actual, "action": args.action, "result": result}
    if args.receipt:
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(json.dumps(report, indent=2, default=str) + "\n")
    display = report
    if args.action == "logs" and args.receipt:
        display = {
            **report,
            "result": {
                "log_entries": len(result["log"]),
                "tail": result["log"][-6:],
                "full_log": str(args.receipt),
            },
        }
    print(json.dumps(display, indent=2, default=str))
    if result.get("error"):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
