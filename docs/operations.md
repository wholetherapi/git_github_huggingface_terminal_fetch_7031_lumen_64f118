# Operations runbook

## Nightly index build

1. `scripts/nightly.sh` runs at 02:15 UTC on the builder host.
2. The job writes segments under `var/segments/<date>/`.
3. Export shards are mirrored to cold storage after the digest check passes.

## Incident: oversized segments

If a single segment exceeds the configured memory ceiling, stop the builder and
rerun compaction with a smaller fanout. Do not delete partially written
segments before the builder exits: the recovery job treats them as resumable.

## Incident: export drift

Export shards are content addressed by row order; a mismatch between the
manifest and the shard list usually means a partial upload.

# TODO(sol): add a recovery drill to the on-call checklist before the next audit
