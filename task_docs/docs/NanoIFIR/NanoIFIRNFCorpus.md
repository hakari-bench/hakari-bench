# NanoIFIR / NanoIFIRNFCorpus

## Overview

`NanoIFIRNFCorpus` is an English medical and nutrition literature retrieval task in NanoIFIR. The queries are layperson-style health and nutrition topics, and the documents are medical research article titles and abstracts.

This task evaluates retrieval across the lay-to-biomedical vocabulary gap. The user-facing query may use accessible health language, while relevant documents use PubMed-style scientific terminology, mechanisms, exposures, endpoints, and trial language.

## Details

### What the Original Data Measures

IFIR uses NFCorpus in a health-related expert retrieval setting, where the goal is to retrieve scientific literature tailored to a research or information need.

NFCorpus is a medical learning-to-rank dataset built from NutritionFacts.org pages written in lay English and linked to PubMed or PMC research articles. The original task emphasizes the lexical gap between consumer health topics and biomedical literature, with graded or multi-positive relevance derived from links between health content and scientific articles.

### Observed Data Profile

This Nano split contains 86 queries, 3,593 documents, and 242 positive qrels. Queries have 2.81 positives on average, with a minimum of 1, a median of 3.0, and a maximum of 8. There are 64 multi-positive queries, or 74.42% of the split. Queries average 37.84 characters, and documents average 1,589.52 characters.

Observed queries include topics such as curcumin safety, ulcerative colitis prevention with diet, autophagy and longevity, the Swank diet for multiple sclerosis, and curcumin bioavailability. Documents are PubMed-like titles and abstracts.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.3338, hit@10 of 0.6628, and recall@100 of 0.6488 with a top-500 candidate pool. Lexical matching is useful when consumer and biomedical wording overlaps, such as curcumin, ulcerative colitis, multiple sclerosis, or diet.

The task remains difficult for BM25 because many relevant abstracts use technical terms that differ from the lay query. A consumer phrase such as "live longer" may correspond to mechanisms involving mTOR, autophagy, aging, or nutrient signaling rather than exact phrase overlap.

### Dense Evaluation Profile

The dense harrier-oss-270m profile reaches nDCG@10 of 0.4580, hit@10 of 0.7326, and recall@100 of 0.8306. Dense retrieval is the strongest profile across the main metrics.

This shows that embedding similarity helps bridge lay health wording and scientific abstracts. Dense retrieval can connect consumer topics to biomedical mechanisms, trial endpoints, disease categories, and molecular terminology that are not obvious lexical matches.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate subset reaches nDCG@10 of 0.4108, hit@10 of 0.7209, and recall@100 of 0.7975. It uses 100 candidates per query, with nine rank-101 safeguard positives.

Hybrid retrieval is strong but below dense retrieval. Lexical anchors help for named nutrients or diseases, but dense semantic matching is more important overall. The hybrid pool remains useful for reranking because it combines term precision with broad biomedical semantic coverage.

### Metric Interpretation for Model Researchers

`NanoIFIRNFCorpus` is a dense-favored health literature retrieval task. The main benchmark signal is whether a model can bridge lay topics to biomedical evidence. BM25 is a useful baseline, but dense retrieval provides much better relevant coverage.

Because most queries have multiple positives, recall@100 matters. nDCG@10 measures whether the model ranks scientifically useful abstracts early enough for evidence review.

### Query and Relevance Type Tendencies

Queries are short health or nutrition titles written in accessible language. Documents are longer biomedical abstracts with scientific terminology, methods, results, and mechanistic claims.

The relevance relation is scientific support for the health topic. A relevant abstract may discuss a nutrient, disease, mechanism, trial, or epidemiological association related to the query.

### Representative Failure Modes

BM25 may miss relevant abstracts that use different scientific terms from the lay query. Dense retrieval may retrieve medically adjacent abstracts that do not actually address the consumer health topic. Hybrid retrieval can still over-rank articles that share a nutrient or disease but answer a different mechanistic question.

Short queries also create ambiguity. A title like a broad health claim may map to several mechanisms, interventions, or outcomes.

### Training Data That May Help

Useful training data includes non-overlapping NFCorpus train pairs, PubMed abstract retrieval pairs, consumer-health to biomedical query rewriting, and same-topic biomedical hard negatives.

Training should preserve multiple relevant medical abstracts where available and exclude `NanoIFIRNFCorpus` queries, qrels, and positive PubMed or PMC abstracts.

### Model Improvement Notes

Improving this task requires biomedical semantic matching and lay-language query understanding. Models should represent nutrients, diseases, mechanisms, clinical outcomes, and study designs, while also handling consumer phrasing.

For reranking, the model should verify that the abstract scientifically addresses the query topic, not merely that it mentions a related nutrient or disease.

## Example Data

| Query | Positive document |
| --- | --- |
| Who Should be Careful About Curcumin? [37 chars] | Curcumin as "Curecumin": from kitchen to clinic. Although turmeric (Curcuma longa; an Indian spice) has been described in Ayurveda, as a treatment for inflammatory diseases and is referred by differen... [200 / 1,773 chars] |
| Preventing Ulcerative Colitis with Diet [39 chars] | A diet high in fat and meat but low in dietary fibre increases the genotoxic potential of 'faecal water'. To determine the effects of different diets on the genotoxicity of human faecal water, a diet... [200 / 1,604 chars] |
| Exploiting Autophagy to Live Longer [35 chars] | mTOR: from growth signal integration to cancer, diabetes and ageing Preface In all eukaryotes, the target of rapamycin (TOR) signaling pathway couples energy and nutrient abundance to the execution of... [200 / 694 chars] |
| Treating Multiple Sclerosis With the Swank MS Diet [50 chars] | Effect of low saturated fat diet in early and late cases of multiple sclerosis. 144 multiple sclerosis patients took a low-fat diet for 34 years. For each of three categories of neurological disabilit... [200 / 683 chars] |
| Boosting the Bioavailability of Curcumin [40 chars] | Bioavailability of curcumin: problems and promises. Curcumin, a polyphenolic compound derived from dietary spice turmeric, possesses diverse pharmacologic effects including anti-inflammatory, antioxid... [200 / 1,418 chars] |

### Source Reference Table

| Source | Role |
| --- | --- |
| [IFIR: A Comprehensive Benchmark for Evaluating Instruction-Following in Expert-Domain Information Retrieval](https://arxiv.org/abs/2503.04644) | Expert-domain instruction-following IR benchmark paper. |
| [NFCorpus: A Full-Text Learning to Rank Dataset for Medical Information Retrieval](https://www.cl.uni-heidelberg.de/~sokolov/pubs/boteva16full.pdf) | Original NFCorpus medical retrieval paper. |
| [NFCorpus project page](https://www.cl.uni-heidelberg.de/statnlpgroup/nfcorpus/) | Original dataset project page. |
| [hakari-bench/NanoIFIR](https://huggingface.co/datasets/hakari-bench/NanoIFIR) | Nano benchmark dataset containing this split. |

### Representative Snippets

| Query Pattern | Positive Document Pattern |
| --- | --- |
| A lay health title asking who should be careful about curcumin. | A PubMed-style abstract discussing turmeric, curcumin, pharmacologic effects, and clinical use. |
| A query about preventing ulcerative colitis with diet. | An abstract about diet composition, fat, meat, fiber, and biological effects relevant to colitis risk. |
| A query about exploiting autophagy to live longer. | A scientific abstract about mTOR, nutrient signaling, growth, diabetes, cancer, or aging. |
| A query about treating multiple sclerosis with the Swank MS diet. | An abstract about low saturated fat diet in multiple sclerosis patients. |
| A query about boosting curcumin bioavailability. | An abstract discussing curcumin bioavailability, pharmacologic properties, problems, and promises. |
