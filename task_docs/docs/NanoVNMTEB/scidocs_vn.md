# NanoVNMTEB / scidocs_vn

## Overview

`scidocs_vn` is the Vietnamese NanoVNMTEB version of SciDocs retrieval. SciDocs was introduced with SPECTER as a scientific document-level benchmark using citation, co-citation, recommendation, and related-paper signals. In this VN-MTEB split, translated paper titles or short scientific descriptions are used as queries, and translated scientific abstracts are candidate documents.

The Nano split contains 200 queries, 10,000 documents, and 988 positive qrels. Every query has multiple positives: the average is 4.94, the median is 5, and each query has between 3 and 5 positives. Queries average 73.355 characters, while documents average 1,226.7277 characters. This is one of the hardest NanoVNMTEB retrieval tasks: absolute scores are low, and `reranking_hybrid` is only slightly ahead of dense on nDCG@10 and recall@100. The task measures related-paper retrieval, not answer lookup.

## Details

### What the Original Data Measures

SciDocs evaluates scientific document representations across document-level tasks. Citation and co-citation signals are used as proxies for relatedness, and the benchmark includes recommendation-style matching. Unlike QA retrieval, relevance is often based on scientific relationship: similar method, dataset, application, citation context, or topic.

The Vietnamese version translates scientific titles and abstracts. Technical terms, datasets, algorithms, software names, and domain phrases often remain partly unchanged. A relevant document may not share many exact words with the query, because citation-relatedness can reflect methodology or research context rather than direct wording.

### Observed Data Profile

The task has 988 positive qrels across 200 queries. Every query is multi-positive, with a minimum of 3 and maximum of 5 positives. This fixed small positive set makes the benchmark a related-paper ranking task: the system should retrieve several relevant scientific documents for each query.

Documents are long abstracts. Queries are short paper titles or short scientific descriptions. Examples include Android malware behavior analysis, semantic dictionary linkage to WordNet, cloud hardware reliability, daily activity recognition, and virtual learning environments. These topics span computing, language resources, systems, vision, education technology, and other scientific areas.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.1613400598, hit@10 of 0.5200, and recall@100 of 0.3805668016 with a top-500 candidate set. The low nDCG indicates that exact lexical matching is a weak signal for this task. Scientific abstracts can share terms without being citation-related, and related papers may use different terminology.

BM25 still provides some useful anchors, especially for rare technical terms, datasets, algorithms, and system names. However, it often retrieves same-field but non-relevant papers. Citation-style relevance requires matching research intent and context, not only keywords.

### Dense Evaluation Profile

Dense retrieval with `harrier-oss-270m` reaches nDCG@10 of 0.2028299676, hit@10 of 0.5800, and recall@100 of 0.4564777328. It improves over BM25, showing that semantic representations help with related-paper retrieval. The improvement is meaningful but still leaves low absolute performance.

Dense retrieval can connect papers with similar methods or application domains even when terms differ. Its limitation is that generic semantic similarity does not fully capture citation intent. Papers may be topically similar but not part of the same research context, or citation-related despite limited surface similarity.

### Reranking Hybrid Evaluation Profile

`reranking_hybrid` reaches nDCG@10 of 0.2038882997, hit@10 of 0.5650, and recall@100 of 0.4676113360. The top-100 candidate pool has mean candidate count 100.13, with 26 safeguard-positive rows and 26 rows containing 101 candidates. Hybrid retrieval is slightly best on nDCG@10 and recall@100, while dense has the best hit@10.

The small differences show that neither lexical nor general dense retrieval solves the task. Sparse evidence helps with technical anchors, and dense retrieval helps with semantic relatedness, but citation-style relevance likely requires domain-specific scientific document training. Hybrid search improves coverage a little, but the top ranks remain difficult.

### Metric Interpretation for Model Researchers

This task should be read as a low-score, high-difficulty related-paper benchmark. Every query has several positives, so recall@100 matters. However, because there are only 3 to 5 positives, nDCG@10 also reflects whether the model can place the most related papers near the top.

The relative ordering is modest: dense improves over BM25; hybrid barely improves over dense on nDCG and recall. Model researchers should not overinterpret small score gaps. The more important signal is that general retrieval methods struggle with citation and recommendation-style relevance.

### Query and Relevance Type Tendencies

Queries are scientific titles or concise research descriptions. Relevant documents are related scientific abstracts, often linked by method, task, domain, or citation context. Examples include malware analysis, Semantic Web vocabularies, cloud reliability, activity recognition, and virtual learning environments.

Relevance is not answerability or duplicate status. A relevant document may be a related work, a cited method, a paper in the same research cluster, or a paper useful for recommendation. This makes the task closer to scientific literature discovery than question answering.

### Representative Failure Modes

BM25 can retrieve papers sharing a keyword but unrelated in citation context. Dense retrieval can retrieve semantically similar abstracts that are not actually relevant by SciDocs signals. Hybrid retrieval can still fail when technical keywords and broad semantics point to same-field distractors.

Another failure mode is missing methodology. Two papers may be related because they share an evaluation setting, algorithmic approach, dataset, or citation neighborhood, even if abstracts use different surface vocabulary. General-purpose embeddings may not encode this structure.

### Training Data That May Help

Useful training data includes non-overlapping SciDocs signals, scientific citation pairs, co-citation pairs, paper recommendation logs, and translated scientific abstract retrieval data. Multi-positive training is appropriate because every query has multiple related documents.

Synthetic data should create related-paper queries from scientific abstracts, but it should include same-field hard negatives. Generated labels should reflect shared methods, datasets, applications, or citation rationale rather than only topical similarity.

### Model Improvement Notes

The main improvement direction is scientific document representation learning. Citation-informed or co-citation-informed training is likely more useful than generic QA data. Sparse features should preserve technical names, while dense representations should encode method, task, domain, and research context.

Error analysis should group failures by same-keyword distractors, same-domain but unrelated papers, missed method links, and translation of technical terms. This task is a strong diagnostic for research-paper recommendation quality.

## Example Data

### Public Sources

- [SPECTER / SciDocs paper](https://arxiv.org/abs/2004.07180)
- [SciDocs dataset page](https://allenai.org/data/scidocs)
- [VN-MTEB paper](https://aclanthology.org/2026.findings-eacl.86/)
- [BEIR paper](https://arxiv.org/abs/2104.08663)
- [GreenNode/scidocs-vn](https://huggingface.co/datasets/GreenNode/scidocs-vn)

### Source Reference Table

| Source | Role |
|---|---|
| SPECTER / SciDocs | Original scientific document representation and evaluation benchmark |
| SciDocs dataset page | Official dataset context |
| BEIR | Retrieval benchmark framing |
| VN-MTEB | Vietnamese benchmark collection using translated retrieval tasks |
| GreenNode dataset card | Public dataset entry for this Vietnamese split |

### Representative Snippets

- Query: `Phân tích hành vi của mã độc Android`
  Relevant documents include related mobile security or malware-analysis papers.
- Query: `Liên kết một từ điển ngữ nghĩa với Wordnet và chuyển đổi sang Wordnet-LMF`
  Relevant documents concern semantic resources, WordNet, or vocabulary mapping.
- Query: `Mô tả tính độ tin cậy của phần cứng điện toán đám mây`
  Relevant documents discuss reliability and failure trends in computing hardware.
- Query: `Nhận diện thói quen hàng ngày qua các hoạt động`
  Relevant documents include activity recognition or detection methods.
- Query: `VELNET (Môi trường ảo cho học tập mạng)`
  Relevant documents concern virtual learning environments or educational technology.
