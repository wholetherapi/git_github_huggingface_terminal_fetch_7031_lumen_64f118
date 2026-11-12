# Lumen Index Backlog Atlas

Project: lumen-index
Upstream corpus: allenai/c4
Corpus license: apache-2.0
Atlas revision: 2026.09

The backlog atlas is a curated index of maintenance items that the triage
rotation has reviewed and accepted into sprint scope. It is deliberately not
an inventory of every marker in the source tree: reviewers close items that
are out of scope, folded into other work, or deferred past the current
milestone.

## Reviewed backlog items

- `src/export/checksums.py:18` -- TODO: sort by shard index parsed from the file name rather than by raw lexicographic order
- `src/export/writer.py:51` -- TODO: include the shard sequence number in the file name to make reruns auditable
- `src/export/writer.py:67` -- TODO: flush the current shard on a byte budget rather than a fixed row count
- `src/export/writer.py:86` -- TODO: record a per-shard digest manifest next to the export root
- `src/index/build.py:29` -- TODO: derive rows per shard from the host memory budget rather than a constant
- `src/index/compact.py:13` -- TODO: clamp the fanout to the largest power of two that fits the memory budget
- `src/index/segment.py:48` -- TODO: stream the digest in fixed-size blocks instead of building one buffer
- `src/index/segment.py:60` -- TODO: short-circuit the merge when tombstone density stays below five percent
- `src/index/segment.py:87` -- TODO: recompute the digest field in place without rewriting the payload
- `src/ingest/dedup.py:23` -- TODO: swap pairwise bloom filter for a stable cuckoo filter
- `src/ingest/fetch.py:13` -- TODO: support resumable downloads with HTTP range requests
- `src/ingest/parse.py:22` -- TODO: validate UTF-8 boundaries before splitting the concatenated payload
- `src/ingest/parse.py:50` -- TODO: preserve the original field order when serialising back to JSON
- `src/util/logging.py:36` -- TODO: tag every event with the build generation

## Review policy

Entries are ordered by file path and then by line number. Reviewers keep the
wording of an entry stable once it is accepted; the wording is the record of
what was agreed, not a copy of the source comment. Owners named in source
annotations are tracked in the rotation log and are intentionally left out of
the atlas text.

When implementation lands, the entry is removed from the atlas in the same
change set that deletes the marker. If a change moves a surviving marker, only
its line reference is refreshed. Entries for untouched files are never
re-derived.

## Out of scope

Items marked as deferred, duplicated, or superseded are not listed here. The
rotation log records the reasons and is retained with the sprint archive.
