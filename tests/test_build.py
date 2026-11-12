"""Smoke tests for the build pipeline."""

from src.index.build import plan_shards


def test_plan_shards_covers_all_rows():
    spans = plan_shards(2_500_000, rows_per_shard=500_000)
    assert spans[0] == (0, 500_000)
    assert spans[-1][1] == 2_500_000


def test_plan_shards_empty():
    # TODO: assert the shard planner returns no spans for an empty corpus
    assert plan_shards(0) == []
