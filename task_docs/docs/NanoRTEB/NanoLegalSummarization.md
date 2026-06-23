# NanoRTEB / NanoLegalSummarization

## Overview

`NanoLegalSummarization` is an English legal paraphrase retrieval task from NanoRTEB. The query is a short plain-English summary of a contract or terms-of-service clause, and the relevant documents are the formal legal text passages that express the same obligation, permission, or policy. Some queries have multiple positives. BM25, dense retrieval, and `reranking_hybrid` are all competitive, with `reranking_hybrid` the strongest overall because the task needs both shared legal terminology and semantic paraphrase matching.

## Details

### What the Original Data Measures

Plain English Summarization of Contracts introduced a corpus of contract clauses paired with plain-English summaries. The original task focuses on making legal text easier to understand.

RTEB repurposes the alignment as retrieval. The simplified summary becomes the query, and the formal clause text becomes the document to retrieve. This tests whether a model can connect informal explanations to legal language.

### Observed Data Profile

The Nano split contains 200 queries, 438 documents, and 345 positive qrel rows. Queries average 103.06 characters, while documents average 606.16 characters. Positives per query average 1.73, with a minimum of 1, a median of 1, and a maximum of 11. Fifty-six queries, or 28.0%, have multiple positives.

Example summaries describe location data collection, permission to modify a game but not distribute hacked clients, deletion of inactive virtual goods, unilateral terms changes, and access to files stored in a cloud service.

### BM25 Evaluation Profile

The BM25 candidate subset uses the full 438-document pool and reaches nDCG@10 of 0.5678, hit@10 of 0.7800, and recall@100 of 0.8667. BM25 is strong because summaries and clauses often share names, legal concepts, service terms, or domain words.

Its limitation is paraphrase. Informal summaries can express clauses in lay language, such as describing liability, termination, or content access without using the exact legal phrasing found in the document.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses the full 438-document pool and reaches nDCG@10 of 0.5861, hit@10 of 0.7850, and recall@100 of 0.9159. Dense retrieval slightly improves over BM25 on early rank quality and clearly improves recall@100.

This indicates that semantic similarity helps bridge plain-English explanations and formal legal text. It is useful when the query summarizes the effect of a clause rather than quoting it.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates, with 13 rows receiving the optional rank-101 safeguard. It reaches nDCG@10 of 0.6085, hit@10 of 0.8100, and recall@100 of 0.9246. Hybrid retrieval is the strongest profile on all reported metrics.

The result reflects the task structure. Sparse matching preserves service names and legal terms, while dense retrieval captures paraphrase between plain-English summaries and formal clauses.

### Metric Interpretation for Model Researchers

Because some queries have multiple positives, nDCG@10 rewards placing several matching clauses early, hit@10 measures whether at least one relevant clause appears in the first ten, and recall@100 measures broader candidate availability.

For `NanoLegalSummarization`, nDCG@10 is the most useful top-rank signal. A good model should retrieve the correct clause family, not just one document with a shared service name.

### Query and Relevance Type Tendencies

Queries are plain-English legal summaries, often short and informal. Relevant documents are formal contract or terms-of-service passages. They may include permissions, restrictions, data-use policies, account termination rules, or liability language.

Relevance is semantic equivalence between the summary and clause. A nearby clause from the same contract can be wrong if it covers a different right or obligation.

### Representative Failure Modes

Common failures include retrieving the right contract but wrong clause, overmatching service names, missing informal paraphrases, and confusing similar policy areas such as data collection, content license, and account termination. BM25 can miss lay paraphrases; dense retrieval can blur neighboring legal provisions.

### Training Data That May Help

Useful training data includes legal simplification, clause-summary pairs, contract passage retrieval, terms-of-service QA, and hard negatives from nearby clauses in the same document. Evaluation summaries, clauses, and qrels should be excluded.

### Model Improvement Notes

Models should represent obligations, permissions, rights, and restrictions rather than only legal keywords. Hard negatives should come from the same contract and share names or legal terms while expressing a different policy. Hybrid retrieval is the best first-stage profile for this split.

## Example Data

| Query | Positive document |
| --- | --- |
| this service may collect use and share location data. [53 chars] | apple and our partners and licensees may collect use and share precise location data including the real time geographic location of your apple computer or device. where available location based servic... [200 / 740 chars] |
| you may mod the game but don t distribute hacked clients. [57 chars] | if you ve bought the game you may play around with it and modify it. we d appreciate it if you didn t use this for griefing though and remember not to distribute the changed versions of our software.... [200 / 349 chars] |
| if you haven t played for a year you mess up or we mess up we can delete all of your virtual goods.... [100 / 245 chars] | we may cancel suspend or terminate your account and your access to your trading items virtual money virtual goods the content or the services in our sole discretion and without prior notice including... [200 / 1,441 chars] |
| the service makes critical changes to its terms without user involvement. [73 chars] | gitlab reserves the right at its sole discretion to modify or replace any part of this agreement. it is your responsibility to check this agreement periodically for changes. your continued use of or a... [200 / 624 chars] |
| dropbox along with their third parties are allowed to access scan store and duplicate content that y... [100 / 122 chars] | when you use our services you provide us with things like your files content email messages contacts and so on your stuff. your stuff is yours. these terms don t give us any rights to your stuff excep... [200 / 714 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Plain English Summarization of Contracts | 2019 | task paper | [https://aclanthology.org/W19-2201/](https://aclanthology.org/W19-2201/) |
| mteb/legal_summarization |  | dataset card | [https://huggingface.co/datasets/mteb/legal_summarization](https://huggingface.co/datasets/mteb/legal_summarization) |
| Introducing RTEB: A New Standard for Retrieval Evaluation | 2025 | benchmark article | [https://huggingface.co/blog/rteb](https://huggingface.co/blog/rteb) |

### Representative Snippets

| Query | Relevant document excerpt |
| --- | --- |
| This service may collect, use, and share location data. | A clause says Apple and partners may collect and share precise location data. |
| You may mod the game, but do not distribute hacked clients. | A game clause permits modifications but restricts distributing changed software. |
| Inactive accounts or mistakes can lead to deleted virtual goods. | A clause allows cancellation, suspension, or termination of virtual goods and access. |
| The service can make critical terms changes without user involvement. | A clause reserves the right to modify or replace agreement terms. |
| Dropbox and third parties may access and duplicate content on the service. | A clause explains limited rights needed to host, scan, and provide stored files. |
