# NanoMTEB-Dutch / nfcorpus_nl

## Overview

`nfcorpus_nl` is the Dutch NFCorpus retrieval task from BEIR-NL. Queries are
short consumer-health or nutrition topics, and documents are translated medical
or biomedical passages. The Nano split contains 199 queries, 3,593 documents,
and 5,880 positive qrel rows. It is strongly multi-positive: the average query
has 29.55 positives, the median is 15, and 181 of 199 queries have more than
one positive.

This task is very different from single-positive retrieval. Queries are often
extremely short, averaging only 18.51 characters, while documents average
1,743.72 characters and can contain technical biomedical terminology. BM25 has
the best nDCG@10, dense retrieval has better recall@100 than BM25, and
`reranking_hybrid` has the best hit@10 and recall@100. Because each query can
map to many relevant medical documents, recall should be interpreted as
coverage over a relevance set rather than success on one target passage.

## Details

### What the Original Data Measures

[NFCorpus: A Full-Text Learning to Rank Dataset for Medical Information Retrieval](https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf)
describes a medical information retrieval dataset built from NutritionFacts.org
topics linked to PubMed and PubMed Central evidence. The original task focuses
on the gap between lay health information needs and biomedical literature,
using relevance signals that can connect one topic to many documents.

BEIR includes NFCorpus as a medical retrieval task, and BEIR-NL translates
public BEIR datasets into Dutch. This Nano task should therefore be read as
translated medical retrieval. Some technical names, biomedical terms, and
English or multilingual artifacts can remain visible, while the surrounding
text is Dutch-translated.

### Observed Data Profile

The split has 199 queries and 3,593 documents. It contains 5,880 positive qrels,
which is much denser than most Nano retrieval tasks. The maximum number of
positives for a single query is 100. Documents are long biomedical or health
passages, often resembling translated abstracts with exposure, outcome, method,
or population details.

Representative queries include short topics such as bagels, grapes, Dr. Walter
Willett, chronic headache and pork parasites, and Native Americans. The
positive documents cover topics such as poppy seeds and opiate testing,
plant polyphenols and cognition, coconut oil and lipid profiles,
neurocysticercosis, and diet-related disease. The query-to-document bridge is
often conceptual rather than a direct wording match.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 = 0.2683, hit@10 = 0.6181, and recall@100 = 0.1371 over
top-500 candidate lists. BM25 is the best nDCG@10 source, which shows that exact
medical, nutrition, and food terms are valuable when they appear in both query
and document. It can rank some highly relevant documents near the top when
there is direct term overlap.

The low recall@100 is the more important warning. Because each query can have
many relevant documents, recovering one or a few lexical matches does not cover
the full relevance set. Short lay queries often do not share terminology with
technical biomedical abstracts, and translations can introduce additional
variation. BM25 is useful but incomplete.

### Dense Evaluation Profile

Dense retrieval with `harrier_oss_v1_270m` reaches nDCG@10 = 0.2590, hit@10 =
0.6181, and recall@100 = 0.1757. Dense retrieval has slightly lower nDCG@10
than BM25 but better recall@100. This suggests that dense similarity helps
recover medically related documents that do not share exact query terms, even
if its top ranking is not as sharp as BM25 for lexical matches.

Dense retrieval should be especially useful for lay-to-technical mappings:
food names to biomedical exposures, symptoms to diseases, or health topics to
research abstracts. Its failure mode is broad concept matching. It may retrieve
documents that are medically related but not relevant under the original
NFCorpus relevance judgments.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate column reaches nDCG@10 = 0.2656, hit@10 =
0.6231, and recall@100 = 0.1815, with 100 to 101 candidates per query and 37
rank-101 safeguard rows. It has the best hit@10 and recall@100, while BM25 has
the highest nDCG@10. This pattern shows the tradeoff between sharp lexical top
ranking and broader semantic coverage.

Hybrid search is useful because medical retrieval needs both exact terminology
and concept matching. BM25 can preserve precise biomedical terms, while dense
retrieval can bridge lay wording and technical passages. A reranker can then
decide which medically related candidates are genuinely relevant.

### Metric Interpretation for Model Researchers

This task should not be read like a single-positive benchmark. With 5,880
positive qrels for 199 queries, recall@100 can be low even when hit@10 is
moderate, because the system must cover many relevant documents. nDCG@10
reflects the quality of the top-ranked subset, while recall@100 reflects how
much of the broad relevance set is captured.

Multi-positive training objectives are a better match than single-positive
contrastive sampling. Models should learn to rank several relevant biomedical
documents for one lay topic, not only the nearest passage.

### Query and Relevance Type Tendencies

Queries are very short health, nutrition, food, symptom, or named-entity
topics. Documents are long biomedical passages or abstracts. Relevant documents
may vary in specificity: some are direct evidence for a topic, while others are
related medical sources connected through the original NFCorpus judgments.

The relevance type is topic-to-evidence coverage. A query such as a food name
or symptom can map to many relevant medical documents. Retrieval systems should
therefore handle broad but controlled semantic expansion.

### Representative Failure Modes

BM25 can fail when lay terms and biomedical terminology diverge, or when many
relevant documents do not repeat the short query token. Dense retrieval can
fail by retrieving broadly related medical passages that are not judged
relevant. Hybrid retrieval can still miss much of the positive set because only
100 candidates are retained for reranking.

Hard negatives should be concept-near: related diseases, compounds, foods, or
interventions that are medically adjacent but not relevant to the query's
topic.

### Training Data That May Help

Useful training data includes official NFCorpus training data with overlap
removed, Dutch biomedical QA and evidence retrieval pairs, non-overlapping
health topic to medical article pairs, and multilingual medical retrieval data
adapted to Dutch. Training should exclude translated NFCorpus test queries,
qrels, and medical documents used by this Nano split.

Synthetic data can be generated from Dutch biomedical abstracts or patient-
facing health passages outside the evaluation set. Generate short lay health
topics and questions that map to multiple technical passages. Include hard
negatives from adjacent conditions, compounds, interventions, or food topics.

### Model Improvement Notes

Improving this task requires lay-to-biomedical semantic bridging and multi-
positive ranking. Dense encoders should learn medical synonymy and concept
relations, while sparse signals should preserve exact terminology for top
precision. Rerankers should not assume one best answer; several documents may
be relevant to the same health topic.

The task is a good stress test for retrieval coverage. A model can look
acceptable by hit@10 while still covering only a small fraction of the relevant
medical evidence.

## Example Data

### Public Sources

- [NFCorpus: A Full-Text Learning to Rank Dataset for Medical Information Retrieval](https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf), 2016.
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663), 2021.
- [BEIR-NL: Zero-shot Information Retrieval Benchmark for the Dutch Language](https://aclanthology.org/2025.bucc-1.5/), 2025.
- [clips/beir-nl-nfcorpus](https://huggingface.co/datasets/clips/beir-nl-nfcorpus), source dataset card.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| NFCorpus: A Full-Text Learning to Rank Dataset for Medical Information Retrieval | 2016 | paper PDF | https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | arXiv paper | https://arxiv.org/abs/2104.08663 |
| BEIR-NL: Zero-shot Information Retrieval Benchmark for the Dutch Language | 2025 | ACL paper | https://aclanthology.org/2025.bucc-1.5/ |
| clips/beir-nl-nfcorpus |  | dataset card | https://huggingface.co/datasets/clips/beir-nl-nfcorpus |

### Representative Snippets

| Query | Positive passage |
| --- | --- |
| bagels | A translated biomedical passage discusses poppy seed products and opiate drug testing after possible contamination during harvest. |
| druiven | A translated passage discusses plant polyphenols and their potential role in age-related cognitive impairment. |
| Dr. Walter Willett | A translated passage discusses coconut oil and lipid profiles in premenopausal women in the Philippines. |
| Chronische hoofdpijn en varkens parasieten | A translated medical passage describes clinical manifestations, diagnosis, and treatment of neurocysticercosis. |
| Inheemse Amerikanen | A translated passage discusses Western diseases and their origins in relation to diet. |
