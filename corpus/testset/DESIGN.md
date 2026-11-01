# Evaluation set: 600 policies of large organizations

Goal: 200 privacy policies from websites, 200 from Google Play apps, and 200 from App Store apps, each from a large organization, no organization twice, all fetched with one fetcher in October 2026 and turned into text by one procedure. The set is the input for running and evaluating the PolicyClaw pipeline.

## Frames

| Arm | Frame | Size proxy |
|---|---|---|
| web | Registered domains that have at least one PrivaSeer URL and appear in the Tranco list | Tranco rank of the registered domain (lower is larger) |
| android | Google Play apps whose US details page (HTTP 200) gives a privacy policy URL | `realInstalls` (ties: `minInstalls`, then `ratings`) |
| apple | App Store apps found by the US iTunes lookup whose US app page gives a privacy policy URL | `userRatingCount` in the US storefront |

Tranco: one fixed list (its list id and date are recorded). The registered domain of a host follows the Public Suffix List, ICANN and private sections, from one pinned copy (date and SHA-256 recorded). The private section makes a user site on a hosting service (`user.github.io`, `shop.wixsite.com`) its own registered domain, so it is not ranked as the hosting company. An IP address is its own registered domain. App Store app pages are still being crawled; for the top-ranked apps that lack a US app page, the page is fetched now with the crawler's own code, so the ranking covers every app of the US lookup.

## Policy URL

- Apps: the privacy policy URL of the store listing.
- Websites: the privacy policy the site links from its current home page, which mirrors the store listing's link. The home page `https://<registered domain>/` is fetched (redirects followed). Its links whose anchor text or address contains "privacy" (case-insensitive) are the candidate links, in page order and without repeats. The first of at most three candidate links that is eligible (below) is the site's policy. A site whose home page cannot be fetched or has no such link is rejected with that reason. The PrivaSeer URL of the domain with the highest fastText score is kept in the metadata.

## Organizations

- Organization key within an arm: Google Play `developerId`, App Store `artistId`, web registered domain.
- Each organization enters its arm once, with its highest-ranked app.
- Development data of the extractor is excluded: every registered domain of the 290 development sites (`corpus/versions.jsonl`), the six PolicyIE test policies (apps `co.happybits.marcopolo`, `com.apps.go.clean.boost.master`, `com.blackout.word`; sites `codecademy.com`, `digg.com`, `entrepreneur.com`), and any candidate whose text contains at least half of the 5-word shingles of a PolicyIE policy. OPP-115 is not excluded, because no extractor development step used it (it was used only to validate the page verifier).

## Text

Every candidate's policy URL is fetched in October 2026 with `corpus/stores/common.fetch` (the store crawler's headers, redirects followed). App policies already fetched by the store crawl are reused. Each body is stored raw. Two texts are derived:
- the visible text (all text nodes outside script and style, as in `corpus/rebuild_versions.py`), which is the PolicyClaw input, and
- the trafilatura 2.0.0 text with the store crawl's settings (`corpus/stores/text.py`), kept for comparison.
PDF and plain-text bodies use the same rules as `corpus/stores/text.py`. The PrivaSeer text of a web candidate is kept in the metadata only.

## Eligibility

A candidate is eligible when
1. the fetch returned HTTP 2xx and a text of at least 100 characters,
2. the page verifier (`corpus/collect/verify.py`, prompt v1, Gemini 3.8 Flash at medium thinking; precision 97.8% on fresh pages, FINDINGS §29) labels it `complete_policy` and English, and
3. it duplicates no policy already selected in any arm: the registered domain of its final policy URL (and, for a website, the site's registered domain) is not the registered domain of a selected final policy URL or selected site, and its Jaccard similarity of 5-word shingle sets is below 0.5 with every selected text.

## Selection

The three rankings are walked in turns: web rank 1, android rank 1, apple rank 1, web rank 2, and so on. At each turn the arm takes its next eligible organization. An arm stops at 200. The order of turns decides which arm keeps an organization present in several arms. Every rejected candidate is recorded with its reason, so the report gives the funnel from frame to set.

## Outputs (`corpus/testset/`)

- `candidates_{web,android,apple}.parquet`: ranked organizations with metadata.
- `fetch/`: raw bodies and texts of the fetched candidates.
- `verify.jsonl`: verifier records.
- `selection.parquet` and `selection.tsv`: the 600 policies with arm, rank, organization, size proxy, app or site metadata, policy URL, final URL, fetch time, HTTP status, content type, text hashes and lengths, verifier label and evidence.
- `texts/<id>.visible.txt`, `texts/<id>.trafilatura.txt`.
- `report.md`: frame sizes, the funnel per arm with reasons, and the size proxy of the last selected organization per arm.
