import json
from collections import defaultdict

def read_records(filename):
    with open(filename, encoding="utf-8") as f:
        for line in f:
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                yield None

def main():
    filename = input("Enter JSONL file path: ").strip()
    data = defaultdict(lambda: {
        "count": 0,
        "min": float("inf"),
        "max": float("-inf"),
        "sum": 0.0,
        "corrupted": 0
    })

    try:
        for record in read_records(filename):
            if not isinstance(record, dict):
                continue

            device = record.get("device_id")
            temperature = record.get("temperature_c")

            if not device or not isinstance(temperature, (int, float)):
                if device:
                    data[device]["corrupted"] += 1
                continue

            d = data[device]
            d["count"] += 1
            d["min"] = min(d["min"], temperature)
            d["max"] = max(d["max"], temperature)
            d["sum"] += temperature

        for device in sorted(data):
            d = data[device]
            if d["count"]:
                avg = d["sum"] / d["count"]
                print(
                    f"{device} count={d['count']} "
                    f"min={d['min']} max={d['max']} "
                    f"avg={avg:.2f} corrupted={d['corrupted']}"
                )
            else:
                print(f"{device} count=0 corrupted={d['corrupted']}")

    except FileNotFoundError:
        print("File not found.")

if __name__ == "__main__":
    main()