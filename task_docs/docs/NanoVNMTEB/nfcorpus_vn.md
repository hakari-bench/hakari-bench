# NanoVNMTEB / nfcorpus_vn

## Overview

`nfcorpus_vn` is the Vietnamese NanoVNMTEB version of NFCorpus, a medical information retrieval benchmark built to connect lay health information needs with scientific literature. The original NFCorpus links NutritionFacts.org topics and questions to medical research articles, especially PubMed-style abstracts. In this VN-MTEB split, translated lay health or nutrition queries retrieve translated biomedical abstracts.

The split contains 166 queries, 3,618 documents, and 4,571 positive qrels. Queries are very short, averaging 24.722892 characters, while documents are long biomedical abstracts averaging 1,584.25152 characters. It is strongly multi-positive: the average query has 27.536145 positives, and the median has 14. `reranking_hybrid` is strongest, but all absolute scores are low. The task is difficult because everyday health terms must be mapped to technical biomedical evidence, often across a large lexical and conceptual gap.

## Details

### What the Original Data Measures

NFCorpus was designed for medical information retrieval from lay health content to scientific articles. The original dataset links consumer-facing NutritionFacts.org pages to research literature at several relevance levels. In retrieval form, a query may be a disease, food, nutrient, intervention, or health concept, and relevant documents are abstracts with biomedical terminology.

The Vietnamese version translates the source data, though the language field is marked multilingual and some queries may remain very short or non-Vietnamese-like. Documents are mostly Vietnamese-translated abstracts but preserve scientific terms, intervention names, disease names, measurement language, and study outcomes. This makes the task different from ordinary QA: a relevant abstract may not directly answer in lay language but is scientifically connected to the topic.

### Observed Data Profile

The task has 4,571 positives for 166 queries. The average positive count is 27.536145, the median is 14, and 156 queries have multiple positives, giving a multi-positive rate of 93.975904%. The maximum positive count is 100. This is a set-retrieval and ranking task over many potentially relevant biomedical abstracts.

Queries are often extremely short, such as a food, nutrient, disease, or broad health concept. Documents are long abstracts with methods, outcomes, populations, and scientific framing. The task therefore combines query expansion, lay-to-technical vocabulary mapping, and multi-positive ranking.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.2551666290, hit@10 of 0.5963855422, and recall@100 of 0.1817982936 with a top-500 candidate set. The hit rate shows that lexical retrieval often finds at least one related abstract, especially when a disease, nutrient, or food term appears directly.

The low nDCG and recall reveal the harder problem. A short query such as milk, pork, vitamin K, Stevia, or a cooking method can have many relevant abstracts using technical vocabulary. BM25 may rank exact-term documents but miss broader biomedical relevance or fail to order the most useful abstracts above same-term weak matches.

### Dense Evaluation Profile

Dense retrieval with `harrier-oss-270m` reaches nDCG@10 of 0.2827302811, hit@10 of 0.6385542169, and recall@100 of 0.2168015751. It improves over BM25 on all metrics, indicating that semantic similarity helps bridge some lay-to-scientific wording gaps.

The improvement is modest, not transformative. Biomedical abstracts contain specialized terminology, study designs, and measured outcomes, while queries can be only one or two words. Dense models may connect related concepts but still struggle to rank many relevant abstracts when the query lacks context. Domain-specific biomedical training and multilingual medical vocabulary are likely important.

### Reranking Hybrid Evaluation Profile

`reranking_hybrid` is the strongest condition: nDCG@10 is 0.2901899855, hit@10 is 0.6506024096, and recall@100 is 0.2194268213. The top-100 candidate pool has mean candidate count 100.180723, with 30 safeguard-positive rows and 30 rows containing 101 candidates. The gain over dense is small but consistent.

Hybrid retrieval helps because sparse matching preserves exact disease, nutrient, and food names, while dense retrieval captures broader biomedical relatedness. The small absolute recall@100 shows that even the hybrid pool retrieves only a fraction of all positives for many queries. This benchmark remains challenging despite many positives because the relevant set is broad and scientifically varied.

### Metric Interpretation for Model Researchers

Hit@10 is not enough for this task. With a median of 14 positives per query and many queries having far more, a model can hit one positive while missing most of the relevant literature. Recall@100 is low for every condition, so candidate coverage is a major bottleneck.

The metric ordering shows that dense helps and hybrid helps slightly more, but the task likely needs domain adaptation. General-purpose embeddings may not fully understand biomedical terminology, intervention-outcome relations, or lay-to-technical mappings. Evaluation should focus on listwise ranking and coverage, not only first positive retrieval.

### Query and Relevance Type Tendencies

Queries include foods, nutrients, disease names, health topics, and broad concepts such as cooking methods or memory. Relevant documents can be experimental studies, reviews, intervention studies, or toxicology abstracts. Some relevance is indirect because the original NFCorpus links lay health pages to scientific articles.

Relevance is graded-like and topic-rich rather than single-answer. A query about Stevia may retrieve abstracts about stevioside or steviol mutation assays. A query about milk may retrieve abstracts about processing, contamination, or nutritional outcomes. The model must infer biomedical connections from sparse query wording.

### Representative Failure Modes

BM25 can over-rank abstracts that repeat the query term but are less relevant to the health information need. Dense retrieval can retrieve broad biomedical neighbors without matching the specific intervention or outcome. Hybrid retrieval can still miss many relevant abstracts because the candidate pool is only a small slice of a large positive set.

Another failure mode is lay-to-scientific mismatch. Consumer terms may map to compounds, disease mechanisms, study populations, or measurement endpoints that do not share obvious words. Without medical domain knowledge, relevant abstracts may look unrelated.

### Training Data That May Help

Useful training data includes official NFCorpus training data with overlap removed, Vietnamese consumer-health QA, biomedical abstract retrieval pairs, PubMed-style query-document relevance data, and translated biomedical retrieval data. Multi-positive and listwise objectives are important because one-positive contrastive training would underrepresent the task.

Synthetic data should generate lay Vietnamese health queries from biomedical abstracts while preserving interventions, outcomes, populations, disease names, and measurements. Hard negatives should share a disease, food, nutrient, or intervention but differ in outcome or study focus.

### Model Improvement Notes

The main improvement direction is multilingual biomedical retrieval. Dense models need domain vocabulary and lay-to-technical alignment. Sparse retrieval should preserve exact medical terms, compounds, and disease names. Rerankers should compare intervention, outcome, population, and measurement context.

Error analysis should group failures by vocabulary mismatch, overly broad topic match, missing outcome, and insufficient recall over large positive sets. This task is a strong stress test for retrieval models intended for consumer health or biomedical literature search.

## Example Data

### Public Sources

- [NFCorpus paper](https://doi.org/10.1007/978-3-319-30671-1_58)
- [NFCorpus project page](https://www.cl.uni-heidelberg.de/statnlpgroup/nfcorpus/)
- [VN-MTEB paper](https://aclanthology.org/2026.findings-eacl.86/)
- [BEIR paper](https://arxiv.org/abs/2104.08663)
- [GreenNode/nfcorpus-vn](https://huggingface.co/datasets/GreenNode/nfcorpus-vn)

### Source Reference Table

| Source | Role |
|---|---|
| NFCorpus | Original medical information retrieval dataset |
| NFCorpus project page | Official dataset context |
| BEIR | Retrieval benchmark framing |
| VN-MTEB | Vietnamese benchmark collection using translated retrieval tasks |
| GreenNode dataset card | Public dataset entry for this Vietnamese split |

### Representative Snippets

- Query: `phương pháp nấu ăn`
  Relevant documents include biomedical abstracts about cooking-related exposures or food-processing effects.
- Query: `kí ức`
  Relevant documents may discuss compounds or mechanisms connected to memory-related health topics.
- Query: `ergothioneine`
  Relevant documents discuss nutrient sources and antioxidant effects of ergothioneine.
- Query: `vitamin K`
  Relevant documents include biomedical or food-processing abstracts connected to vitamin K or related nutrition contexts.
- Query: `Stevia`
  Relevant documents discuss stevioside, steviol, and toxicology or mutagenicity studies.
