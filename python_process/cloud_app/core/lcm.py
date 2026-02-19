import math


def calculate_lcm_from_rows(rows: list[dict]) -> int:
    bundle_counts: set[int] = set()
    for row in rows:
        bundle_counts.add(int(row["bundles_per_truckload"]))
    return int(math.lcm(*sorted(bundle_counts)))

