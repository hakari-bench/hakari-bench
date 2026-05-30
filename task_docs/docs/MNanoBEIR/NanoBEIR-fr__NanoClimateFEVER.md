# MNanoBEIR / NanoBEIR-fr / NanoClimateFEVER

## Overview

This task is the French NanoBEIR version of Climate-FEVER, a climate claim verification retrieval benchmark. The original Climate-FEVER dataset uses real-world climate claims and Wikipedia evidence to test whether systems can retrieve documents that support careful verification. In this NanoBEIR slice, French translated climate claims must retrieve French translated Wikipedia-style evidence documents from 3,408 candidates. The task contains 50 queries and 148 positive relevance judgments, with an average of 2.96 positives per query. Most claims have multiple relevant documents. It is a compact diagnostic for climate-science evidence retrieval, where models must connect claim wording to scientific context, temporal framing, mechanisms, records, and broad encyclopedia pages that may not repeat the claim exactly.

## Details

### What the Original Data Measures

Climate-FEVER measures evidence retrieval for climate-related claims. A claim may refer to sea-level variability, greenhouse gases, historical temperature periods, extreme weather, solar activity, or climate attribution. The retrieval task is to find evidence pages that help verify the claim before any final label is assigned. This requires more than recognizing climate vocabulary; the document must contain relevant scientific or historical context.

### Observed Data Profile

The French Nano task has 50 queries, 3,408 documents, and 148 positives. Positives per query average 2.96, and 44 of 50 queries have multiple positives. Queries average about 159 characters, while documents are long, averaging about 1,827 characters. The examples include claims about warming from 1970 to 1998, downward trends, local and regional sea-level variation, Hurricane Harvey, and the CERN CLOUD experiment. Positive documents are translated Wikipedia-style evidence pages.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.306, Hit@10 of 0.700, and Recall@100 of 0.615. Sparse retrieval helps when climate terms such as CO2, sea level, solar cycle, or named experiments recur in both claim and evidence page. However, many positives are broader context pages or use different wording from the claim. BM25 can retrieve topically climate-related pages while missing the specific evidence needed for verification.

### Dense Evaluation Profile

The dense harrier-oss-270m baseline is slightly stronger than BM25, with nDCG@10 of 0.311, Hit@10 of 0.720, and Recall@100 of 0.635. Dense retrieval helps connect claims to semantically related evidence pages, especially when evidence is explanatory rather than phrase-matched. The small margin over BM25 indicates that exact climate terminology remains important, while general semantic similarity alone does not fully solve claim-specific evidence retrieval.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid profile is clearly strongest, with nDCG@10 of 0.353, Hit@10 of 0.780, and Recall@100 of 0.696, with two safeguard rows at 101 candidates. This is a strong hybrid-search pattern: BM25 contributes exact scientific terms and names, while dense retrieval contributes broader evidence-page matching. The hybrid profile improves both top-10 ranking and candidate coverage, making it the most useful first-stage retriever for this French Climate-FEVER slice.

### Metric Interpretation for Model Researchers

Because most queries have several positives, Hit@10 should be treated as only a first-evidence signal. Recall@100 matters for verification pipelines because claims may need several evidence pages or because different pages capture different aspects of the claim. nDCG@10 measures whether evidence appears early enough for practical use. The hybrid gains show that both lexical and semantic signals are needed.

### Query and Relevance Type Tendencies

Queries are declarative French climate claims, often with numeric, temporal, or causal framing. Relevant documents are encyclopedia-style evidence pages, not short answers. Some positives are narrow mechanism pages, while others are broad background pages. The task is sensitive to scientific terminology, named institutions, time periods, and translation choices.

### Representative Failure Modes

BM25 can retrieve a page that shares a climate term but does not verify the claim. Dense retrieval can retrieve generally related climate pages that lack the required evidence. Hybrid retrieval reduces both errors but may still rank broad climate pages above the most directly useful evidence. Failure analysis should ask whether the document would help verify the specific claim.

### Training and Leakage Considerations

Training should exclude Climate-FEVER, BEIR, NanoBEIR, and translated records likely to overlap with these claims or evidence pages. Useful non-overlapping data includes climate fact-checking data, scientific claim-evidence retrieval pairs, French or multilingual Wikipedia verification data, and hard negatives from related climate pages. Multi-positive training is recommended because most claims have several evidence documents.

### Model Improvement Signals

Strong models should improve climate evidence recall without losing claim specificity. Useful training signals include temporal and numeric claim variants, related climate hard negatives, scientific term normalization, and multilingual claim verification pairs. Hybrid systems should preserve exact scientific terms while using dense similarity to recover broader explanatory evidence.

## Example Data

| Query | Positive Document |
|---|---|
| De 1970 à 1998, il y a eu une période de réchauffement qui a fait augmenter les températures d'environ 0,7 degré Fahrenheit... | Le Paléocène, qui signifie « ancien récent », est une époque géologique qui a duré d'environ 66 à 56 millions d'années... |
| En réalité, la tendance, bien qu'elle ne soit pas statistiquement significative, baisse. | Le cycle solaire ou cycle d'activité magnétique solaire est le cycle quasi périodique d'environ 11 ans des variations de l'activité du Soleil... |
| Les niveaux de la mer locaux et régionaux continuent de varier naturellement, montant dans certaines régions et baissant dans d'autres. | Le niveau moyen de la mer est un niveau moyen de la surface d'un ou plusieurs des océans de la Terre... |
| Les scientifiques du climat disent que certains aspects de l'ouragan Harvey suggèrent que le réchauffement climatique rend une situation déjà mauvaise encore plus difficile. | Les effets du réchauffement climatique sont les changements environnementaux et sociaux causés par les émissions humaines de gaz à effet de serre... |
| L'expérience CLOUD du CERN n'a testé qu'un tiers d'une des quatre exigences nécessaires pour attribuer le réchauffement climatique aux rayons cosmiques... | L'attribution des changements climatiques récents consiste à déterminer scientifiquement les mécanismes responsables des changements climatiques observés sur Terre... |

## Public Sources

- [Climate-FEVER paper](https://arxiv.org/abs/2012.00614)
- [BEIR benchmark](https://github.com/beir-cellar/beir)
- [MMTEB benchmark](https://arxiv.org/abs/2502.13595)
- [NanoBEIR dataset](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

## Source Reference Table

| Label | URL |
|---|---|
| Climate-FEVER paper | https://arxiv.org/abs/2012.00614 |
| BEIR benchmark | https://github.com/beir-cellar/beir |
| MMTEB benchmark | https://arxiv.org/abs/2502.13595 |
| NanoBEIR dataset | https://huggingface.co/collections/zeta-alpha-ai/nanobeir |
