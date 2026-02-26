def calculate_target_weights(rows: list[dict]) -> dict:
    popularity_scores: list[int] = []
    seen: set[int] = set()

    for row in rows:
        score = int(row["popularity_score"])
        if score not in seen:
            seen.add(score)
            popularity_scores.append(score)

    inverse_weights = [1.0 / score for score in popularity_scores]
    total_weight = sum(inverse_weights)
    normalized_weights = [weight / total_weight for weight in inverse_weights]

    score_to_weight: dict = {}
    for idx, score in enumerate(popularity_scores):
        score_to_weight[score] = normalized_weights[idx]

    weights_by_sku: dict = {}
    for row in rows:
        weights_by_sku[row["sku_id"]] = score_to_weight[int(row["popularity_score"])]

    return weights_by_sku


def score_solution(solution: list[dict], rows_by_id: dict, target_weights: dict) -> tuple[int, int]:
    total_sticks_per_sku: dict = {}
    for item in solution:
        sku_id = item["sku_id"]
        sticks_per_bundle = int(rows_by_id[sku_id]["sticks_per_bundle"])
        number_of_bundles = int(item["number_of_bundles"])
        total_sticks_per_sku[sku_id] = sticks_per_bundle * number_of_bundles

    total_sticks = sum(total_sticks_per_sku.values())
    if total_sticks <= 0:
        return 10**12, 0

    difference_sum = 0
    for sku_id, sticks in total_sticks_per_sku.items():
        actual_weight = sticks / total_sticks
        target_weight = target_weights[sku_id]
        popularity_score = int(rows_by_id[sku_id]["popularity_score"])
        difference = round(abs(actual_weight - target_weight) * popularity_score * 10000)
        difference_sum += int(difference)

    return int(difference_sum), int(total_sticks)

