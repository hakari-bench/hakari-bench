# NanoBEIR-en / NanoNFCorpus

## Overview

NanoNFCorpus is the compact English NanoBEIR version of NFCorpus, a medical and nutrition information retrieval task. Queries are short layperson health, food, drug, disease, or nutrition topics, and the corpus contains biomedical abstracts or abstract-like scientific passages. The retrieval goal is to connect consumer-facing health topics to relevant medical evidence. This makes the task useful for evaluating biomedical domain transfer, multi-positive retrieval, and the gap between everyday health wording and technical scientific text.

## Details

### What the Original Data Measures

NFCorpus was built as a learning-to-rank dataset for medical information retrieval. Its queries come from NutritionFacts.org-style lay health topics, while its documents are mainly PubMed and PMC titles or abstracts. Relevance can be derived from direct citations, indirect links, and topic relations, so many queries have broad evidence sets.

The BEIR version places NFCorpus in biomedical information retrieval. The NanoBEIR version exposes binary positive qrels, but the original graded and link-derived nature of the source remains important for interpretation. The task is not ordinary clinical QA; it is health-topic-to-scientific-evidence retrieval.

### Observed Data Profile

The task contains 50 queries, 2,953 documents, and 1,651 relevance judgments. It is highly multi-positive, with an average of 33.02 positives per query. The minimum is 1, the median is 23.5, the maximum is 100, and 47 queries are multi-positive, or 94.0% of the set.

Queries average only 21.04 characters, while documents average 1,512.73 characters. This is one of the strongest query-document length mismatches in the NanoBEIR set. A few lay terms must retrieve long biomedical abstracts that may use study-design language, biochemical terminology, disease names, or statistical reporting.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.3060, hit@10 of 0.6800, and recall@100 of 0.1690 using the top-500 BM25 candidate subset. Lexical matching works when a query contains distinctive disease, food, drug, or scientific terms, but it covers only a small fraction of the broad relevant set.

The low recall@100 is partly a consequence of the many positives per query. BM25 may find one relevant abstract while missing most of the linked evidence pool. It also struggles when a consumer topic maps to technical terminology that does not repeat the query phrase.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.3135, hit@10 of 0.7200, and recall@100 of 0.2447. Dense retrieval improves all three reported metrics over BM25. The largest gain is recall@100, showing that embedding similarity broadens coverage across the scientific evidence set.

This indicates that semantic matching helps bridge consumer health wording and biomedical abstracts. However, the absolute recall remains low because each query can have dozens of positives and because biomedical concepts require specialized terminology. A general dense model helps but does not fully solve domain evidence coverage.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.3178, hit@10 of 0.6800, and recall@100 of 0.2332. It uses a top-100 candidate range with an optional rank-101 safeguard; this slice has 6 safeguard rows, candidate counts from 100 to 101, and a mean of 100.12 candidates. It has the best nDCG@10, while dense retrieval has the best hit@10 and recall@100.

The hybrid result suggests that adding lexical anchors improves the top ordering of some evidence passages, even though dense retrieval covers slightly more positives overall. BM25 contributes exact food, disease, drug, and biomedical terms, while dense retrieval contributes broader health-topic similarity.

### Metric Interpretation for Model Researchers

Because most queries have many positives, hit@10 is only a weak signal. A system can retrieve one relevant abstract and still miss the majority of the evidence set. nDCG@10 measures whether the highest ranks are useful, while recall@100 measures how much evidence is available for reranking.

The comparison shows that BM25 is limited by vocabulary mismatch, dense retrieval improves coverage, and reranking_hybrid slightly improves top-rank quality. This task is a good diagnostic for biomedical domain adaptation and multi-positive retrieval objectives.

### Query and Relevance Type Tendencies

Queries include health topics such as healthy chocolate milkshakes, medical ethics, fava beans, what is actually in chicken nuggets, and saturated fat. Relevant documents are scientific abstracts with methods, results, background, and outcome descriptions. Many positives are linked by health topic rather than by exact word overlap.

The task rewards mapping lay health topics to scientific evidence. A relevant abstract may discuss a nutrient, pathway, disease, exposure, or study outcome without using the exact consumer phrase. Same-domain but wrong-outcome abstracts are common hard negatives.

### Representative Failure Modes

Likely failures include retrieving generic health abstracts that share a food or disease term, missing abstracts that use technical synonyms, under-covering large relevant sets, and ranking broad background text above directly linked evidence. BM25 may be too literal, while dense retrieval may be too broad without biomedical specialization.

### Training Data That May Help

Useful training data includes non-overlapping NFCorpus training data, consumer-health-question to PubMed evidence pairs, biomedical abstract retrieval, BioASQ-style medical question-to-article retrieval, and citation or link supervision connecting lay health pages to scientific papers. Multi-positive training is important.

### Model Improvement Notes

A model targeting this task should improve lay-to-biomedical vocabulary bridging and evidence-set coverage. Sparse systems need synonym expansion and biomedical tokenization. Dense systems need domain adaptation on scientific abstracts and health topics. Hybrid systems can help when exact biomedical terms and semantic topic matching both matter.

## Example Data

| Query | Positive document |
| --- | --- |
| Healthy Chocolate Milkshakes [28 chars] | Objective To study the relation between cherry intake and the risk of recurrent gout attacks among individuals with gout. Methods We conducted a case-crossover study to examine associations of a set of putative risk factors with recurrent gout attacks. Individuals with gout were prospectively recruited and followed online for one year. Participants were asked about the following information when experiencing a gout attack: the onset date of the gout attack, symptoms and signs, medications (including anti-gout medications), and potential risk factors (including daily intake of cherries and cherry extract) during the 2-day period prior to the gout attack. We assessed the same exposure information over 2-day control periods. We estimated the risk of recurrent gout attacks related to cherry intake using conditional logistic regression. Results Our study included 633 individuals with gout. Cherry intake over a 2-day period was associated with a 35% lower risk of gout attacks compared with n... [1,000 / 1,586 chars] |
| medical ethics [14 chars] | BACKGROUND: One of the major issues in controlling serum cholesterol through dietetic intervention appears to be the need to improve patient adherence. AIMS: To explore the many questions regarding barriers to, and motivators for, cholesterol-lowering diet adherence. METHODS: We surveyed French general practitioners' dietetic practices for patients with hypercholesterolaemia, and looked at their patients' attitudes towards such an approach. RESULTS: We analysed 234 doctors' personal questionnaires and 356 patient self-survey questionnaires. Patients' reasons for not complying with the prescribed diet included: 'already having satisfactory food habits' (34.7%), 'unwillingness to suffer nutritional deprivation' (33.3%), 'difficulties to conciliate a diet with family life' (27.8%) and 'taking cholesterol-lowering drugs' (22.2%). Despite a generally good understanding by patients of doctors' recommendations, some discrepancies were seen between their respective declarations. While doctors... [1,000 / 1,831 chars] |
| fava beans [10 chars] | Over the past 20 years, growing interest in the biochemistry, nutrition, and pharmacology of L-arginine has led to extensive studies to explore its nutritional and therapeutic roles in treating and preventing human metabolic disorders. Emerging evidence shows that dietary L-arginine supplementation reduces adiposity in genetically obese rats, diet-induced obese rats, finishing pigs, and obese human subjects with Type-2 diabetes mellitus. The mechanisms responsible for the beneficial effects of L-arginine are likely complex, but ultimately involve altering the balance of energy intake and expenditure in favor of fat loss or reduced growth of white adipose tissue. Recent studies indicate that L-arginine supplementation stimulates mitochondrial biogenesis and brown adipose tissue development possibly through the enhanced synthesis of cell-signaling molecules (e.g., nitric oxide, carbon monoxide, polyamines, cGMP, and cAMP) as well as the increased expression of genes that promote whole-bo... [1,000 / 1,240 chars] |

### Source Reference Table

| Item | Reference |
| --- | --- |
| Original dataset paper | [NFCorpus](https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf) |
| Project page | [NFCorpus project page](https://www.cl.uni-heidelberg.de/statnlpgroup/nfcorpus/) |
| Retrieval benchmark framing | [BEIR](https://arxiv.org/abs/2104.08663) |
| Source dataset card | [mteb/nfcorpus](https://huggingface.co/datasets/mteb/nfcorpus) |
| NanoBEIR-en dataset | [hakari-bench/NanoBEIR-en](https://huggingface.co/datasets/hakari-bench/NanoBEIR-en) |

Representative query and positive evidence snippets:

| Query | Positive document snippet |
| --- | --- |
| Healthy Chocolate Milkshakes | A study examines cherry intake and risk of recurrent gout attacks among individuals with gout. |
| medical ethics | An abstract discusses patient adherence and barriers in controlling serum cholesterol through diet. |
| fava beans | A passage discusses L-arginine biochemistry, nutrition, and therapeutic roles. |
| What is Actually in Chicken Nuggets? | A study determines the contents of chicken nuggets from two national food chains. |
| saturated fat | A prospective study examines associations between maternal diet and allergic disorders in children. |
