# NanoMuPLeR / pl

## Overview

`NanoMuPLeR / pl` is the Polish split of MuPLeR-retrieval, a multilingual legal retrieval task based on European Union legal passages. Queries are synthetic Polish legal questions, and documents are Polish DGT-Acquis passages. Each query has exactly one relevant passage, so the task evaluates precise passage retrieval under formal legal language. The split is useful because BM25 and dense retrieval are close, while the hybrid pool improves substantially, showing that Polish legal search benefits from both exact lexical anchors and semantic matching.

## Details

### What the Original Data Measures

MuPLeR-retrieval measures legal passage retrieval across multiple European languages using DGT-Acquis passages and synthetic aligned queries. The source dataset card describes 10,000 passages and 200 queries per language. DGT-Acquis is one of the European Union's multilingual parallel legal resources.

In this Polish split, retrieval is same-language and single-positive. The model must identify the passage that grounds a legal question about a committee request, right of access, court decision, trademark reasoning, or policy-making body.

### Observed Data Profile

The Nano split contains 200 queries, 10,000 documents, and 200 positive qrel rows. Each query has one positive. Queries average 143.97 characters, while documents average 686.12 characters.

Examples include appointment of experienced specialists, Charter-protected access to services of general economic interest, judicial shaping of corporate taxation, criticism of trademark reasoning, and the creation of a body involving technical practitioners in policy. The passage style is formal, argumentative, and institution-heavy.

### BM25 Evaluation Profile

The BM25 candidate subset uses top-500 candidates and reaches nDCG@10 of 0.8400, hit@10 of 0.9050, and recall@100 of 0.9600. BM25 is slightly stronger than dense retrieval by nDCG@10 and equal on hit@10 and recall@100. Polish legal queries contain many exact anchors: institutional names, legal rights, court actions, trademark terms, and policy phrases.

This means sparse lexical evidence is a serious baseline. Term frequency and exact phrase overlap capture much of the task, but the score gap to hybrid retrieval shows that lexical matching alone still leaves difficult paraphrase and ranking cases.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses top-500 candidates and reaches nDCG@10 of 0.8299, hit@10 of 0.9050, and recall@100 of 0.9600. Dense retrieval is nearly tied with BM25, but it places positives slightly lower on average.

The close result suggests that Polish MuPLeR balances lexical and semantic signals. Dense retrieval helps with argumentative or paraphrased questions, while exact legal vocabulary remains important for distinguishing similar EU provisions and court or committee contexts.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates, with two rows receiving the optional rank-101 safeguard. It reaches nDCG@10 of 0.8909, hit@10 of 0.9500, and recall@100 of 0.9900. Hybrid retrieval is clearly strongest.

This profile shows that BM25 and dense retrieval retrieve many of the same positives but not always with the same rank or coverage. Combining them gives a reranker more complete access to the exact answer passage and better early ranking.

### Metric Interpretation for Model Researchers

With one positive per query, nDCG@10 measures how early the answer passage appears, hit@10 is the success rate within the first ten results, and recall@100 indicates reranking coverage. For Polish MuPLeR, BM25 and dense are both strong first-stage baselines, but the hybrid pool is the practical target for reranking experiments.

Researchers should avoid treating this split as purely lexical or purely semantic. The important behavior is the interaction between exact Polish legal terms and paraphrased legal reasoning.

### Query and Relevance Type Tendencies

Queries are formal Polish questions about EU institutions, rights, court reasoning, trademark interpretation, taxation, and policy development. Relevant documents are translated EU legal or advisory passages with dense legal argumentation.

The relevance relation is strict. A document must answer the exact legal or institutional point, not merely mention the same right, court, tax topic, or policy area.

### Representative Failure Modes

Failures include choosing a passage with the same right but not the requested analysis, matching the same court topic but a different decision, confusing trademark reasoning across cases, and retrieving broad policy language instead of the specific body or recommendation. Dense retrieval can overgeneralize; sparse retrieval can miss paraphrased legal framing.

### Training Data That May Help

Useful training data includes non-overlapping Polish EUR-Lex and DGT-Acquis retrieval pairs, Polish legal QA, multilingual legal bitext, and hard negatives from related EU legal passages. Evaluation queries and exact positives should be excluded.

### Model Improvement Notes

Models should jointly preserve Polish legal morphology, exact institutional names, and semantic paraphrase of legal reasoning. Hard negatives should come from the same legal topic and share terminology while failing the requested actor, decision, right, or consequence. The hybrid result indicates that reranking over combined sparse-dense candidates is the most informative setting.

## Example Data

### Public Sources

- [mteb/MuPLeR-retrieval](https://huggingface.co/datasets/mteb/MuPLeR-retrieval), source dataset card.
- [An overview of the European Union's highly multilingual parallel corpora](https://link.springer.com/article/10.1007/s10579-014-9277-0), DGT-Acquis source reference.
- [DGT-Acquis](https://joint-research-centre.ec.europa.eu/language-technology-resources/dgt-acquis_en), European Commission source-corpus page.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| MuPLeR: Multilingual Parallel Legal Retrieval |  | dataset card | https://huggingface.co/datasets/mteb/MuPLeR-retrieval |
| An overview of the European Union's highly multilingual parallel corpora | 2014 | source paper | https://link.springer.com/article/10.1007/s10579-014-9277-0 |
| DGT-Acquis |  | source corpus | https://joint-research-centre.ec.europa.eu/language-technology-resources/dgt-acquis_en |

### Representative Snippets

| Query | Relevant document excerpt |
| --- | --- |
| Who again called for appointing experienced specialists, citing audit rules, decision-makers' discretion, and legal-liability risk? | A passage about the committee's awareness of the tradeoff between transparency, Court of Auditors rules, and room for decision-makers. |
| Which Charter-protected right of access to services of general economic interest requires analysis under Article 16 TEU and its protocol? | A passage explaining that specific analysis may be needed to preserve the right of access to services of general economic interest. |
| Which court decision recently showed courts reshaping national corporate taxation when political bodies failed to agree on a common tax framework? | A passage warning that lack of agreement on a common corporate tax base may leave necessary decisions to judicial rulings. |
| Which judgment criticized a lower court for overstating phonetic differences and understating the dominance of words over image in trademark registration? | A passage stating that the court erred in assuming sufficient phonetic difference between disputed marks. |
| Which body's creation was treated as an encouraging first step toward including experienced technical practitioners in policy-making? | A passage supporting greater inclusion of experienced experts and representatives of science and technology in administrative and policy processes. |
