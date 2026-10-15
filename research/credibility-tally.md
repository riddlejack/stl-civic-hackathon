# What we analysed: the credibility tally

Counted 14 Oct 2026, about 11:55 p.m. Central, from the files on disk, for the "what I analysed" moment in v6. Everything is **observed** unless marked.

## Summary

The entry rests on these sources:
- **the city's full public 311 file:** 1.45 million requests, 2008–2026;
- **every closing since January 2025, classified:** 175,876 closings, read by their closing words (252 distinct phrases);
- **the Forestry billing ledger:** 2.25 million rows, 1.13 million billed grass cuts;
- **the city's own Cityworks records, read with permission:** 19,291 open requests and 29,018 work orders;
- **1,440 of the city's public status pages,** read one by one, plus 223 lists of attached items;
- **9 CityStat measures rebuilt from scratch,** within 0.2% of the published figure on 8 of 9;
- **11 other cities' 311 practices compared;**
- **10 public statements by officials,** checked live.

| Figure | Value | Source |
|---|---|---|
| 311 requests in the public file | 1,454,222 (filed 2008–2026) | `requests` table, build/stl.duckdb ([311 data](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=5)) |
| Requests filed since 1 Jan 2025 | 216,532 | same |
| Closings since 2025 classified by their words | 175,876 (252 distinct closing texts) | `closure_class`, `closure_text_class` |
| Forestry billing-ledger rows | 2,252,031 (1,126,751 billed cuts) | `ledger`, `cuts` |
| Parcels joined | 134,919 | `parcels` |
| Cityworks open requests (Active SRs) | 19,291 | research/cityworks-active-queues.md |
| Cityworks work orders | 29,018 | research/cityworks-gap-review.md |
| Public status pages read | 1,440 (plus 223 attached-item lists) | research/status-page-linkage.md |
| CityStat measures rebuilt | 9; within 0.2% on 8 | research/chapters/R1-trace.md, N4 |
| Cities compared | 11 | research/precedents-closed-loop.md |
| Officials' statements checked live | 10 | research/chapters/R3-voices.md |
| Public datasets in the manifest | 15 city sources (plus withheld extracts listed) | site/data.html, data/MANIFEST.csv |
