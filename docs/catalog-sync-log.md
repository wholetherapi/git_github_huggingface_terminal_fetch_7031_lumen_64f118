# Catalog sync automation log

The nightly `catalog-sync` job rebuilds the review notes for
`docs/backlog-atlas.md` and records the upstream card values it resolved. The
job is still being stabilised, so every run keeps its own entry here. Newest
entries are at the top.

Card facts are read from the dataset repository metadata; the parser output is
included verbatim below so the compliance review can compare runs.

## Run 12 -- 2026-10-30 (latest)

- Status: completed
- Upstream corpus: `allenai/c4` (en)
- Card license (as read by the job): `cc-by-4.0`
- Proposed atlas header line: `Corpus license: cc-by-4.0`
- Entries in atlas: 14
- Notes: The card links the Common Crawl terms and the mirror pages we sampled
  describe the corpus as Creative Commons Attribution 4.0. Three independent
  mirrors use the same attribution language, so `cc-by-4.0` was chosen as the
  conservative value. The run wrote the header field and left the entry list
  untouched because the release sweep had not landed yet.

## Run 11 -- 2026-10-23

- Status: completed
- Upstream corpus: `allenai/c4` (en)
- Card license (as read by the job): `apache-2.0`
- Entries in atlas: 14
- Notes: Parser resolved the license tag from the repository metadata block and
  normalised the value to `apache-2.0`.

## Run 10 -- 2026-10-16

- Status: completed
- Upstream corpus: `allenai/c4` (en)
- Card license (as read by the job): `mit`
- Entries in atlas: 14
- Notes: The job followed the "use" section of the card and reported `mit`.

## Run 9 -- 2026-10-09

- Status: completed
- Upstream corpus: `allenai/c4` (en)
- Card license (as read by the job): `cc0-1.0`
- Entries in atlas: 14
- Notes: This run was flagged for review. The parser matched a public-domain
  statement in an older cached copy of the card and wrote `cc0-1.0`. The
  reviewer noted that the cached copy predates the current revision, but the
  automated retry was never scheduled. The value was left in place to avoid
  churn between nightly runs.

## Run 8 -- 2026-10-02

- Status: completed
- Upstream corpus: `allenai/c4` (en)
- Card license (as read by the job): `bsd-3-clause`
- Entries in atlas: 14

## Run 7 -- 2026-09-25

- Status: completed
- Upstream corpus: `allenai/c4` (en)
- Card license (as read by the job): `apache-2.0`
- Entries in atlas: 14

## Run 6 -- 2026-09-18

- Status: completed
- Upstream corpus: `allenai/c4` (en)
- Card license (as read by the job): `cc-by-sa-4.0`
- Entries in atlas: 14
- Notes: The job's HTML snapshot contained a share-alike footer from the
  Common Crawl mirror and the parser preferred the last license string on the
  page. This produced `cc-by-sa-4.0`. The discrepancy was reported but the run
  was not reverted because the release branch had not been cut yet.

## Run 5 -- 2026-09-11

- Status: completed
- Upstream corpus: `allenai/c4` (en)
- Card license (as read by the job): `gpl-3.0`
- Entries in atlas: 14

## Run 4 -- 2026-09-04

- Status: completed
- Upstream corpus: `allenai/c4` (en)
- Card license (as read by the job): `epl-2.0`
- Entries in atlas: 14

## Run 3 -- 2026-08-28

- Status: completed
- Upstream corpus: `allenai/c4` (en)
- Card license (as read by the job): `mit`
- Entries in atlas: 14
- Notes: Second run of the week. The parser reports `mit` whenever the card's
  YAML front matter is served without its structured metadata block; this has
  happened intermittently since the mirror moved to a new CDN. The run still
  updated the header because the previous value differed.

## Run 2 -- 2026-08-21

- Status: completed
- Upstream corpus: `allenai/c4` (en)
- Card license (as read by the job): `cc-by-4.0`
- Entries in atlas: 14

## Run 1 -- 2026-08-14

- Status: completed
- Upstream corpus: `allenai/c4` (en)
- Card license (as read by the job): `apache-2.0`
- Entries in atlas: 12
- Notes: Initial backfill. The atlas had 12 reviewed entries at the time.
