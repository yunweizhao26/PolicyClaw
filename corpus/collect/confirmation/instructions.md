# Labeling instructions

You label web pages for a corpus of privacy policies. Your task names one batch, `batch_NN`. Every path below is under `/scratch/yz5944/nlp+privacy/PolicyClaw/corpus/collect/`.

## Steps

1. Read `rubric.md` in full. It defines the five labels, the two flags, and how cut pages are shown.
2. Read your batch file, `confirmation/batches/batch_NN.md`. The table at its top gives the line range of each page. Read every page completely, one page at a time, with the Read tool's `offset` and `limit`. If a read is refused as too large, read the page in smaller parts.
3. Label every page by the rubric, on its own. Use only what the batch shows: the URL, the word count and the text. Do not visit the URL.
4. Write all labels with the Write tool to `confirmation/labels/batch_NN.jsonl`: one JSON object per line, one line per page, in the order of the batch. The fields are:
   - `id`: the page id, for example `v017`;
   - `label`: one of `complete_policy`, `partial_policy`, `cookie_only`, `other_legal`, `not_policy`;
   - `flags`: `multiple_orgs` (true or false) and `language` (ISO 639-1 code, or `und` for no readable text);
   - `evidence`: one to three short passages, each at most 30 words, copied exactly from the page (an empty list only when the page has no readable text);
   - `reason`: one or two sentences. For a policy page, say which of the three required items (collection; use or sharing; rights, retention or contact) the page states or lacks.

   Example line:

   ```
   {"id": "v017", "label": "complete_policy", "flags": {"multiple_orgs": false, "language": "en"}, "evidence": ["We collect your name, email address and order history.", "You may ask us to delete your data by writing to privacy@example.com."], "reason": "A full policy of one shop: it states what it collects, how it uses and shares the data, and how to request deletion."}
   ```

5. Reply with the number of pages you labeled and the count of each label.

## Rules

- Use only the Read and Write tools.
- Open only `rubric.md`, this file, and your batch file. Do not open any other file or folder, including other batches, `key.json`, `sample.tsv`, `text/`, other labels, and any verifier output.
- Write only your own labels file.
- Every page in the batch gets exactly one line.
