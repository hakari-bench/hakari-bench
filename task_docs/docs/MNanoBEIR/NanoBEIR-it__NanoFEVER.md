# MNanoBEIR / NanoBEIR-it / NanoFEVER

## Overview

This task is the Italian NanoBEIR version of FEVER, a Wikipedia fact verification evidence retrieval benchmark. The original FEVER dataset contains claims paired with Wikipedia evidence for support, refute, or not-enough-information labels. In this NanoBEIR slice, Italian translated claims must retrieve Italian translated Wikipedia evidence passages from 4,996 candidate documents. The task contains 50 queries and 57 positive relevance judgments. Most queries have one positive document, while six queries have multiple positives. It is a compact benchmark for entity-centric fact-checking retrieval, where models must find the passage that verifies the claim, including cases where the evidence contradicts the claim rather than repeating it.

## Details

### What the Original Data Measures

FEVER measures fact extraction and verification over Wikipedia. In retrieval form, the task is evidence discovery before classification. Claims often mention entities, titles, roles, locations, or dates. A relevant document contains the information needed to support or refute the claim, so retrieval quality should be evaluated separately from the final verification decision.

### Observed Data Profile

The Italian Nano task has 50 queries, 4,996 documents, and 57 positives. Positives per query average 1.14, with a maximum of three. Queries are short, averaging about 50 characters, while documents average about 1,290 characters. Example claims involve Keith Godchaux and the Grateful Dead, Taarak Mehta Ka Ooltah Chashmah, aircraft made in Burbank, Nero, and Scream 2. Positive documents are Italian translated Wikipedia-style evidence passages.

### BM25 Evaluation Profile

BM25 is very strong, with nDCG@10 of 0.778, Hit@10 of 0.900, and Recall@100 of 0.947. This reflects the strong role of exact entity and title overlap in FEVER claims. Sparse retrieval usually finds the correct evidence page when the claim contains a distinctive name or work title. The remaining difficulty is relation precision: a page may share an entity but not contain the fact needed to verify the claim.

### Dense Evaluation Profile

The dense harrier-oss-270m baseline reaches nDCG@10 of 0.797, Hit@10 of 0.900, and Recall@100 of 0.895. Dense retrieval slightly improves top-10 ordering over BM25 but has lower candidate recall. This suggests that embeddings help rank evidence passages once the entity context is found, but exact lexical matching is still important for broad evidence discovery.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid profile is strongest overall, with nDCG@10 of 0.798, Hit@10 of 0.920, and Recall@100 of 0.982, with one safeguard row at 101 candidates. It combines BM25's entity anchoring with dense relation matching and gives the best first-page hit rate and candidate coverage. This makes hybrid search especially suitable as the first stage of an Italian FEVER verification pipeline.

### Metric Interpretation for Model Researchers

Because most claims have one positive, Hit@10 and Recall@100 are direct evidence discovery measures. nDCG@10 shows whether the evidence appears near the top. The hybrid profile's higher recall is important: a downstream verifier cannot recover evidence that is absent from the candidate set. Dense's strong nDCG shows that semantic relation matching can still improve the first page.

### Query and Relevance Type Tendencies

Queries are short Italian factual claims, often entity-heavy. Relevant documents are Wikipedia passages that verify the claim. Hard negatives may share a title, person, or location while lacking the verifying relation. The task rewards exact entity normalization, title matching, relation awareness, and retrieval of contradictory evidence.

### Representative Failure Modes

BM25 can retrieve a page with high name overlap but no verifying fact. Dense retrieval can retrieve a semantically related page that does not contain the evidence. Hybrid retrieval improves both but can still rank a closely related entity page above the annotated evidence. Failure analysis should ask whether the retrieved document actually verifies the claim.

### Training and Leakage Considerations

Training should exclude FEVER, BEIR, NanoBEIR, and overlapping translated Wikipedia evidence. Useful non-overlapping data includes FEVER-style claim-evidence pairs, Wikipedia evidence retrieval data, Italian or multilingual fact-checking examples, and same-entity hard negatives. Synthetic data should generate short Italian claims from non-evaluation Wikipedia passages, including supported and contradicted variants.

### Model Improvement Signals

Strong models should combine exact entity recall with relation-sensitive evidence ranking. Useful signals include alias handling, title normalization, same-entity hard negatives, and claim-evidence paraphrase training. Hybrid systems should use sparse retrieval for entity anchors and dense retrieval for semantic verification context.

## Example Data

| Query | Positive document |
| --- | --- |
| Keith Godchaux conosceva i Grateful Dead. [41 chars] | I Grateful Dead sono stati una band rock americana formata nel 1965 a Palo Alto, California. Con una formazione variabile da quintetto a settetto, la band è nota per il suo stile unico ed eclettico, c... [200 / 3,080 chars] |
| Taarak Mehta Ka Ooltah Chashmah è una sitcom. [45 chars] | Taarak Mehta Ka Ooltah Chashmah (In inglese: La Differente Prospettiva di Taarak Mehta) è la sitcom più longeva dell'India, prodotta da Neela Tele Films Private Limited. La serie è andata in onda il 2... [200 / 583 chars] |
| Aerei segreti e tecnologicamente avanzati sono stati prodotti a Burbank, in California. [87 chars] | Burbank è una città nella contea di Los Angeles, nella California meridionale, Stati Uniti, a 12 miglia a nord-ovest del centro di Los Angeles. Secondo il censimento del 2010, la popolazione era di 10... [200 / 1,410 chars] |
| Nero è una persona. [19 chars] | La dinastia giulio-claudia si riferisce ai primi cinque imperatori romani — Augusto, Tiberio, Caligola, Claudio e Nerone — o alla famiglia a cui appartenevano. Governarono l'Impero Romano dalla sua fo... [200 / 2,095 chars] |
| Scream 2 è un film esclusivamente tedesco. [42 chars] | Scream 2 è un film slasher americano del 1997 diretto da Wes Craven e scritto da Kevin Williamson. Vede la partecipazione di David Arquette, Neve Campbell, Courteney Cox, Sarah Michelle Gellar, Jamie... [200 / 2,802 chars] |

## Public Sources

- [FEVER paper](https://arxiv.org/abs/1803.05355)
- [BEIR benchmark](https://github.com/beir-cellar/beir)
- [MMTEB benchmark](https://arxiv.org/abs/2502.13595)
- [NanoBEIR dataset](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

## Source Reference Table

| Label | URL |
|---|---|
| FEVER paper (https://arxiv.org/abs/1803.05355) |
| BEIR benchmark (https://github.com/beir-cellar/beir) |
| MMTEB benchmark (https://arxiv.org/abs/2502.13595) |
| NanoBEIR dataset (https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
