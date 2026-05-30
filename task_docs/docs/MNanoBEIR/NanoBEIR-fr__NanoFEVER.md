# MNanoBEIR / NanoBEIR-fr / NanoFEVER

## Overview

This task is the French NanoBEIR version of FEVER, a Wikipedia fact verification retrieval benchmark. The original FEVER dataset contains claims generated from Wikipedia and annotated with evidence that supports or refutes each claim. In this NanoBEIR slice, French translated claims must retrieve French translated Wikipedia-style evidence documents from 4,996 candidates. The task contains 50 queries and 57 positive relevance judgments. Most claims have one positive document, while six have multiple positives. It is a compact diagnostic for entity-centric evidence retrieval, where models must find the page or passage that contains the facts needed for verification, including cases where the evidence contradicts the claim rather than repeating it.

## Details

### What the Original Data Measures

FEVER measures fact extraction and verification over Wikipedia. In retrieval form, the first-stage task is evidence discovery. A positive document is one that contains the evidence needed to verify a claim, whether the final label is support or refute. Claims often involve entities, works, places, people, dates, roles, or membership relations, so retrieval must combine entity matching with relation awareness.

### Observed Data Profile

The French Nano task has 50 queries, 4,996 documents, and 57 positives. Positives per query average 1.14, with a maximum of three. Queries average about 51 characters, while documents average about 1,325 characters. Example claims mention Keith Godchaux and the Grateful Dead, Taarak Mehta Ka Ooltah Chashmah, aircraft in Burbank, Nero, and Scream 2. Positive documents are translated Wikipedia-style pages containing verification evidence.

### BM25 Evaluation Profile

BM25 is strong, with nDCG@10 of 0.747, Hit@10 of 0.920, and Recall@100 of 0.965. This reflects the entity-heavy nature of FEVER claims: names, titles, and locations often appear directly in the evidence document. Sparse retrieval provides excellent candidate coverage. The remaining difficulty is relation precision, especially when a claim is false or when several pages share the same entity name but only one contains the verifying fact.

### Dense Evaluation Profile

The dense harrier-oss-270m baseline is the best direct ranker, with nDCG@10 of 0.819, Hit@10 of 0.940, and Recall@100 of 0.930. Dense retrieval improves early ordering by recognizing semantic relation between the claim and the evidence page, even when wording differs. Its lower Recall@100 compared with BM25 shows that exact entity anchoring is still important for broad coverage, but dense retrieval is better at placing the positive evidence high.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid profile reaches nDCG@10 of 0.780, Hit@10 of 0.920, and Recall@100 of 1.000. It gives perfect evidence coverage in the top 100, while dense retrieval gives the best top-10 ranking. This split is important for pipeline design: hybrid search is the safest candidate generator, while dense ranking may be better for direct first-page use. A downstream verifier or reranker benefits from the hybrid pool because it does not miss any annotated positive in this sample.

### Metric Interpretation for Model Researchers

With mostly one positive per claim, Hit@10 and Recall@100 are meaningful evidence discovery measures. nDCG@10 reflects whether the evidence appears early enough for practical use. The dense and hybrid profiles should be read together: dense optimizes the first page, while hybrid optimizes candidate coverage. Retrieval success should not be confused with verification success; a refuting evidence page is still a correct retrieval target.

### Query and Relevance Type Tendencies

Queries are short French factual claims. Relevant documents are Wikipedia-style evidence pages. Hard negatives often share an entity name, title family, or topic but do not contain the required relation. The task rewards entity normalization, alias handling, relation sensitivity, and the ability to retrieve contradictory evidence.

### Representative Failure Modes

BM25 can retrieve pages with high name overlap but no verifying relation. Dense retrieval can rank a semantically related page that does not contain the exact evidence. Hybrid retrieval improves coverage but may still put related lexical pages above the annotated evidence. Failure analysis should ask whether the retrieved document actually verifies the claim.

### Training and Leakage Considerations

Training should exclude FEVER, BEIR, NanoBEIR, and translated Wikipedia claim records likely to overlap with these claims or evidence pages. Useful non-overlapping data includes FEVER-style evidence retrieval pairs, French or multilingual Wikipedia claim verification data, entity-centric QA evidence pairs, and hard negatives from similar entity pages. Synthetic data should generate both supported and contradicted French claims from non-evaluation Wikipedia passages.

### Model Improvement Signals

Strong models should preserve exact entity recall while improving relation-aware evidence ranking. Useful signals include title and alias normalization, relation paraphrase examples, same-entity hard negatives, and multilingual fact verification supervision. Hybrid systems should use BM25 for names and dense retrieval for semantic evidence matching.

## Example Data

| Query | Positive Document |
|---|---|
| Keith Godchaux connaissait les Grateful Dead. | Les Grateful Dead étaient un groupe de rock américain formé en 1965 à Palo Alto, en Californie... |
| Taarak Mehta Ka Ooltah Chashmah est une sitcom. | Taarak Mehta Ka Ooltah Chashmah est la sitcom la plus longue en cours de diffusion en Inde... |
| Des avions de pointe et secrets ont été fabriqués à Burbank, en Californie. | Burbank est une ville située dans le comté de Los Angeles, en Californie du Sud... |
| Nero est une personne. | La dynastie julio-claudienne désigne les cinq premiers empereurs romains, dont Néron... |
| Scream 2 est un film exclusivement allemand. | Scream 2 est un film d'horreur américain de 1997 réalisé par Wes Craven... |

## Public Sources

- [FEVER paper](https://arxiv.org/abs/1803.05355)
- [FEVER shared task](https://fever.ai/)
- [BEIR benchmark](https://github.com/beir-cellar/beir)
- [MMTEB benchmark](https://arxiv.org/abs/2502.13595)
- [NanoBEIR dataset](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

## Source Reference Table

| Label | URL |
|---|---|
| FEVER paper | https://arxiv.org/abs/1803.05355 |
| FEVER shared task | https://fever.ai/ |
| BEIR benchmark | https://github.com/beir-cellar/beir |
| MMTEB benchmark | https://arxiv.org/abs/2502.13595 |
| NanoBEIR dataset | https://huggingface.co/collections/zeta-alpha-ai/nanobeir |
