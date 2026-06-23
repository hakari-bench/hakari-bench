# NanoMedical / NanoNFCorpus

## Overview

`NanoMedical / NanoNFCorpus` is an English consumer-health to biomedical-evidence retrieval task derived from NFCorpus. Queries are very short lay health topics, food names, disease labels, acronyms, or nutrition-related questions, and documents are PubMed or PubMed Central-style article titles and abstracts. The original NFCorpus dataset was built from NutritionFacts.org pages and the research articles cited by those pages, making it a benchmark for bridging consumer health language to technical biomedical literature. This Nano split is heavily multi-positive, so it evaluates both top-rank evidence quality and broad retrieval of many related abstracts.

## Details

### What the Original Data Measures

NFCorpus measures medical information retrieval where non-expert health topics must retrieve scientific articles. The original dataset uses links from NutritionFacts.org to cited research articles, with relevance signals derived from direct links, indirect links, and topic or tag relations.

This task is not medical FAQ answer retrieval. A query such as a food item, supplement, acronym, or health claim may correspond to many biomedical abstracts whose relevance depends on the cited evidence relationship, not only on shared words.

### Observed Data Profile

The Nano split contains 200 queries, 3,593 documents, and 3,718 positive qrel rows. Queries have 18.59 positives on average, with a median of 9 and a maximum of 97. There are 160 multi-positive queries, or 80.0% of the set. Queries average only 17.15 characters, while documents average 1,589.52 characters.

The examples include short topics such as avocados, grapes, Dr. Walter Willett, chlorophyll, and Native Americans. Documents are long technical abstracts with study background, methods, or biomedical mechanisms. This creates a large lexical and register gap between query and document.

### BM25 Evaluation Profile

The BM25 candidate subset uses top-500 candidates and reaches nDCG@10 of 0.2921, hit@10 of 0.6200, and recall@100 of 0.2066. BM25 can help when short queries contain exact biomedical terms, distinctive foods, or acronyms. However, recall is low because each query can have many relevant abstracts and because consumer phrasing may not appear in the abstract.

Sparse retrieval often reaches the right vocabulary cluster but misses the citation or health-claim relation. It can also over-rank abstracts that repeat a food or disease term while studying a different outcome, population, or mechanism.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses top-500 candidates and reaches nDCG@10 of 0.3070, hit@10 of 0.6150, and recall@100 of 0.2633. Dense retrieval improves nDCG@10 and recall@100 over BM25, although hit@10 is slightly lower.

This indicates that semantic matching helps bridge lay health topics and technical abstracts, but the task remains difficult. Many relevant documents are related through citation context, nutrition claims, or evidence roles that a general embedding model may not capture fully.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates, with 48 queries carrying a rank-101 safeguard positive. It reaches nDCG@10 of 0.3182, hit@10 of 0.6500, and recall@100 of 0.2604. Hybrid retrieval gives the best nDCG@10 and hit@10, while dense retrieval has slightly better recall@100.

The profile suggests that sparse and dense signals are complementary: exact food names and acronyms matter, but semantic evidence matching is also needed. A reranker should benefit from the hybrid pool if it can judge biomedical relevance rather than only topic overlap.

### Metric Interpretation for Model Researchers

Because 80.0% of queries are multi-positive and some have dozens of positives, recall@100 is a key metric. Hit@10 only shows whether at least one related abstract is found. nDCG@10 measures whether the first page of results contains highly relevant evidence.

The low recall values are not surprising given the many-positive structure and short queries. This task is better understood as consumer-health evidence retrieval than as ordinary question answering.

### Query and Relevance Type Tendencies

Queries are short lay topics, food names, health concerns, public-health labels, or acronyms. Relevant documents are biomedical abstracts. The relation may reflect a cited evidence link from a NutritionFacts.org page, not direct answer wording.

The relevance relation is evidence or citation affinity between a health topic and biomedical literature.

### Representative Failure Modes

Common failures include over-matching exact food or disease names, missing abstracts that use technical terminology for a lay topic, retrieving same-topic studies with different outcomes, and failing on ambiguous acronyms. Dense models may retrieve broad health-related abstracts; sparse models may miss semantically related evidence with little term overlap.

### Training Data That May Help

Useful training data includes non-overlapping consumer-health to biomedical retrieval pairs, nutrition article citation links, biomedical abstract retrieval with lay queries, and hard negatives from the same food, disease, exposure, or mechanism. Training should exclude overlapping NFCorpus test queries, source NutritionFacts page links, and positive PubMed or PMC qrels for clean evaluation.

### Model Improvement Notes

Models should learn both exact biomedical terminology and lay-to-technical bridging. Citation-informed training and hard negatives that share topic but differ in outcome or population are likely valuable. Multi-positive training is important because each query may have many evidence-bearing abstracts.

## Example Data

| Query | Positive document |
| --- | --- |
| avocados [8 chars] | Role of insulin in the pathogenesis of free fatty acid-induced insulin resistance in skeletal muscle. Insulin resistance is a pathophysiological link of obesity to type 2 diabetes. The initial cause o... [200 / 1,694 chars] |
| grapes [6 chars] | A berry thought-provoking idea: the potential role of plant polyphenols in the treatment of age-related cognitive disorders. Today, tens of millions of elderly individuals worldwide suffer from dement... [200 / 1,862 chars] |
| Dr. Walter Willett [18 chars] | Coconut oil predicts a beneficial lipid profile in pre-menopausal women in the Philippines Coconut oil is a common edible oil in many countries, and there is mixed evidence for its effects on lipid pr... [200 / 1,360 chars] |
| chlorophyll [11 chars] | Antimutagens and anticarcinogens: a survey of putative interceptor molecules. In this review recent publications are cited for a number of antimutagens. The molecules surveyed are potential or proven... [200 / 870 chars] |
| Native Americans [16 chars] | Western diseases and their emergence related to diet. Many of the commonest diseases in the economically more developed communities are characteristic of modern Western culture. Evidence is presented... [200 / 463 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| A Full-Text Learning to Rank Dataset for Medical Information Retrieval | 2016 | ECIR paper PDF | [https://www.cl.uni-heidelberg.de/~sokolov/pubs/boteva16full.pdf](https://www.cl.uni-heidelberg.de/~sokolov/pubs/boteva16full.pdf) |
| NFCorpus: A Full-Text Learning to Rank Dataset for Medical Information Retrieval | 2016 | official dataset page | [https://www.cl.uni-heidelberg.de/statnlpgroup/nfcorpus/](https://www.cl.uni-heidelberg.de/statnlpgroup/nfcorpus/) |
| A Full-Text Learning to Rank Dataset for Medical Information Retrieval | 2016 | DOI | [https://doi.org/10.1007/978-3-319-30671-1_58](https://doi.org/10.1007/978-3-319-30671-1_58) |
| mteb/nfcorpus |  | dataset card | [https://huggingface.co/datasets/mteb/nfcorpus](https://huggingface.co/datasets/mteb/nfcorpus) |

### Representative Snippets

| Query | Relevant document excerpt |
| --- | --- |
| avocados | A biomedical abstract about insulin resistance, free fatty acids, obesity, and type 2 diabetes mechanisms. |
| grapes | A paper discussing plant polyphenols and their possible role in age-related cognitive disorders. |
| Dr. Walter Willett | An abstract about coconut oil and lipid profiles among pre-menopausal women in the Philippines. |
| chlorophyll | A review of antimutagens and anticarcinogens, including putative interceptor molecules. |
| Native Americans | A passage discussing Western diseases and their emergence in relation to diet. |
