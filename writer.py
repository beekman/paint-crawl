import json
import os
from datetime import datetime, timezone


def write_medium(medium, paints, output_dir="data"):
    os.makedirs(output_dir, exist_ok=True)
    payload = {
        "medium": medium,
        "crawled_at": datetime.now(timezone.utc).isoformat(),
        "paints": paints,
    }
    path = os.path.join(output_dir, f"{medium}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
