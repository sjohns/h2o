from api.tests.harness.run_harness import (
    EXPECTED_HISTORICAL_PATH,
    ORDERS_HISTORICAL_PATH,
    run_harness,
)


def test_historical_solver_harness_has_zero_mismatches():
    summary = run_harness(
        orders_path=ORDERS_HISTORICAL_PATH,
        expected_path=EXPECTED_HISTORICAL_PATH,
    )
    assert summary["mismatches"] == 0, summary
