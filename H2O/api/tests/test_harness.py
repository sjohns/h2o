from api.tests.harness.run_harness import run_harness


def test_solver_harness_has_zero_mismatches():
    summary = run_harness()
    assert summary["mismatches"] == 0, summary
