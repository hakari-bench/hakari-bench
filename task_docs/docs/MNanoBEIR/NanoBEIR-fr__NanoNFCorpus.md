# MNanoBEIR / NanoBEIR-fr / NanoNFCorpus

## Overview

This task is the French NanoBEIR version of NFCorpus, a medical information retrieval benchmark built from consumer health and nutrition information needs linked to biomedical articles. The original NFCorpus collection was designed to expose the vocabulary gap between lay health topics and medical literature. In this NanoBEIR slice, short French translated health queries must retrieve French translated medical or biomedical documents from 2,953 candidates. The task contains 50 queries and 1,651 positive relevance judgments, with an average of 33.02 positives per query. It is a many-positive biomedical retrieval benchmark where models must recover a set of relevant evidence documents, not just one answer passage.

## Details

### What the Original Data Measures

NFCorpus measures medical and nutrition retrieval where lay queries are linked to scientific evidence. Queries may be short food, diet, disease, supplement, or health-topic labels, while relevant documents are long biomedical abstracts or summaries. The task rewards models that bridge consumer wording to technical terminology, interventions, mechanisms, outcomes, and study contexts.

### Observed Data Profile

The French Nano task has 50 queries, 2,953 documents, and 1,651 positives. Positives per query average 33.02, with a median of 23.5 and a maximum of 100. Forty-seven queries are multi-positive. Queries are very short, averaging about 29 characters, while documents are long, averaging about 1,811 characters. Examples include healthy chocolate milkshakes, medical ethics, fava beans, chicken nuggets, and saturated fats. Documents are translated biomedical abstracts or scientific summaries.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.303, Hit@10 of 0.640, and Recall@100 of 0.167. Sparse retrieval often finds at least one relevant document when a query term directly appears in a medical abstract. However, recall is low because each query has many positives and because lay wording does not always match biomedical vocabulary. BM25 can also over-rank documents that share a food or disease term while studying a different outcome.

### Dense Evaluation Profile

The dense harrier-oss-270m baseline is slightly stronger in recall, with nDCG@10 of 0.305, Hit@10 of 0.620, and Recall@100 of 0.196. Dense retrieval helps bridge lay French health terms to scientific concepts, but the gains are modest. The task remains difficult because generic semantic similarity does not fully capture medical relevance, intervention-outcome specificity, or the diversity of the positive evidence set.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid profile reaches nDCG@10 of 0.310, Hit@10 of 0.580, and Recall@100 of 0.203, with eight safeguard rows at 101 candidates. It gives the best nDCG@10 and Recall@100 but the lowest Hit@10 among the three profiles. This suggests that hybrid search improves evidence-set coverage and graded ranking, while sometimes failing to place at least one positive in the top 10 for queries where BM25's direct term match works. For biomedical retrieval, both exact terminology and semantic expansion are necessary but insufficient.

### Metric Interpretation for Model Researchers

Hit@10 is not enough for NFCorpus because every query can have many relevant documents. A model can hit one abstract while missing most of the evidence set. Recall@100 is especially important and remains low across all methods. nDCG@10 measures whether the first page contains relevant medical evidence, but researchers should also inspect coverage across different evidence clusters for the same health topic.

### Query and Relevance Type Tendencies

Queries are short French health topics or lay questions. Relevant documents are long biomedical abstracts, clinical summaries, or article descriptions. A single query can map to studies about different populations, mechanisms, interventions, and outcomes. Hard negatives often share a disease or diet word but do not address the same medical relevance relation.

### Representative Failure Modes

BM25 can miss positives that use technical terminology instead of lay wording. Dense retrieval can retrieve medically adjacent abstracts that are not relevant to the specific topic. Hybrid retrieval improves coverage but still misses most positives for many queries. Failure analysis should focus on missing evidence clusters, not only the first retrieved document.

### Training and Leakage Considerations

Training should exclude NFCorpus, BEIR, NanoBEIR, and translated NutritionFacts records likely to overlap with these queries or linked medical documents. Useful non-overlapping data includes biomedical IR datasets, consumer-health question to abstract pairs, PubMed relevance ranking data, and French or multilingual medical retrieval supervision. Multi-positive training is recommended because most queries require multiple valid evidence documents.

### Model Improvement Signals

Strong models should improve lay-to-technical medical matching and evidence-set recall. Useful signals include biomedical synonym mapping, consumer health questions paired with abstracts, hard negatives sharing disease or food terms, and cluster-level positives. Hybrid systems should preserve exact medical terms while dense representations expand toward mechanisms, interventions, and outcomes.

## Example Data

| Query | Positive Document |
|---|---|
| Milkshakes au chocolat santé | Objectif : Étudier la relation entre la consommation de cerises et le risque de crises de goutte récidivantes... |
| éthique médicale | CONTEXTE : L'un des principaux défis dans la gestion du cholestérol sérique par l'intervention diététique... |
| fèves | Au cours des 20 dernières années, l'intérêt croissant pour la biochimie, la nutrition et la pharmacologie de la L-arginine... |
| Qu'est-ce qu'il y a vraiment dans les nuggets de poulet ? | But : Déterminer la composition des nuggets de poulet de deux chaînes de restauration nationales... |
| graisses saturées | L'intérêt pour la possibilité que l'alimentation maternelle pendant la grossesse puisse influencer le développement des troubles allergiques chez les enfants a augmenté... |

## Public Sources

- [NFCorpus paper](https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf)
- [NFCorpus project page](https://www.cl.uni-heidelberg.de/statnlpgroup/nfcorpus/)
- [BEIR benchmark](https://github.com/beir-cellar/beir)
- [MMTEB benchmark](https://arxiv.org/abs/2502.13595)
- [NanoBEIR dataset](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

## Source Reference Table

| Label | URL |
|---|---|
| NFCorpus paper | https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf |
| NFCorpus project page | https://www.cl.uni-heidelberg.de/statnlpgroup/nfcorpus/ |
| BEIR benchmark | https://github.com/beir-cellar/beir |
| MMTEB benchmark | https://arxiv.org/abs/2502.13595 |
| NanoBEIR dataset | https://huggingface.co/collections/zeta-alpha-ai/nanobeir |
