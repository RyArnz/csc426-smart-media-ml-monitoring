import argparse
from pathlib import Path
import requests
import pandas as pd
from datetime import datetime, timedelta, timezone


DEFAULT_QUERIES = {
    "server_cpu_percent": '100 - (avg(rate(node_cpu_seconds_total{job="node_exporter",mode="idle"}[1m])) * 100)',
    "server_ram_percent": '100 * (1 - (node_memory_MemAvailable_bytes{job="node_exporter"} / node_memory_MemTotal_bytes{job="node_exporter"}))',
    "disk_usage_percent": '100 * (1 - (max by(instance) (node_filesystem_avail_bytes{job="node_exporter",mountpoint="/",fstype!="tmpfs"}) / max by(instance) (node_filesystem_size_bytes{job="node_exporter",mountpoint="/",fstype!="tmpfs"})))',
    "container_ram_mb": 'sum(container_memory_usage_bytes{job="cadvisor",image!=""}) / 1024 / 1024',
    "container_cpu_cores": 'sum(rate(container_cpu_usage_seconds_total{job="cadvisor",image!=""}[1m]))',
    "container_count": 'count(container_memory_usage_bytes{job="cadvisor",image!=""})',
}


def parse_args():
    parser = argparse.ArgumentParser(
        description="Export Prometheus range-query metrics to CSV."
    )
    parser.add_argument(
        "--base-url",
        type=str,
        default="http://192.168.1.11:9090",
        help="Prometheus base URL, for example http://192.168.1.11:9090",
    )
    parser.add_argument(
        "--start",
        type=str,
        default=None,
        help='Start time in ISO format, for example "2026-04-13T00:00:00Z"',
    )
    parser.add_argument(
        "--end",
        type=str,
        default=None,
        help='End time in ISO format, for example "2026-04-14T00:00:00Z"',
    )
    parser.add_argument(
        "--step",
        type=str,
        default="60",
        help='Prometheus step interval. Examples: "60", "60s", "1m"',
    )
    parser.add_argument(
        "--output",
        type=str,
        default="server_metrics_dataset.csv",
        help="Output CSV path",
    )
    return parser.parse_args()


def parse_iso_utc(dt_str: str) -> datetime:
    dt_str = dt_str.strip()
    if dt_str.endswith("Z"):
        dt_str = dt_str[:-1] + "+00:00"
    dt = datetime.fromisoformat(dt_str)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def format_prometheus_time(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def run_query_range(base_url: str, query: str, start: str, end: str, step: str) -> pd.DataFrame:
    response = requests.get(
        f"{base_url.rstrip('/')}/api/v1/query_range",
        params={
            "query": query,
            "start": start,
            "end": end,
            "step": step,
        },
        timeout=60,
    )
    response.raise_for_status()

    payload = response.json()
    if payload.get("status") != "success":
        raise RuntimeError(f"Prometheus returned non-success payload: {payload}")

    result = payload["data"]["result"]

    print("Series returned:", len(result))

    if not result:
        return pd.DataFrame(columns=["timestamp"])

    values = result[0]["values"]
    df = pd.DataFrame(values, columns=["timestamp", "value"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s", utc=True)
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    return df


def main():
    args = parse_args()

    if args.start and args.end:
        start_dt = parse_iso_utc(args.start)
        end_dt = parse_iso_utc(args.end)
    else:
        end_dt = datetime.now(timezone.utc)
        start_dt = end_dt - timedelta(hours=2)

    if start_dt >= end_dt:
        raise ValueError("Start time must be earlier than end time.")

    start = format_prometheus_time(start_dt)
    end = format_prometheus_time(end_dt)
    step = args.step
    base_url = args.base_url

    print("Base URL:", base_url)
    print("Start:   ", start)
    print("End:     ", end)
    print("Step:    ", step)

    frames = []

    for name, query in DEFAULT_QUERIES.items():
        print(f"\nRunning query: {name}")
        print(query)

        df = run_query_range(base_url, query, start, end, step)

        if df.empty:
            print(f"No data returned for {name}")
            continue

        df = df.rename(columns={"value": name})
        frames.append(df)

    if not frames:
        raise RuntimeError("No data returned from Prometheus for any query.")

    dataset = frames[0]
    for frame in frames[1:]:
        dataset = dataset.merge(frame, on="timestamp", how="outer")

    dataset = dataset.sort_values("timestamp").reset_index(drop=True)
    dataset = dataset.dropna(how="all")

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    dataset.to_csv(output_path, index=False)

    print(f"\nDataset exported to {output_path}")
    print(dataset.head())
    print("\nColumns:", list(dataset.columns))
    print("Rows:", len(dataset))


if __name__ == "__main__":
    main()
