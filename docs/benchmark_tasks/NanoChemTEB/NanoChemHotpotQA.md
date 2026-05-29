# NanoChemTEB / NanoChemHotpotQA

## Overview

`NanoChemHotpotQA` is the chemistry-filtered HotpotQA retrieval task from
ChemTEB. Queries are English multi-hop questions whose answer requires finding
supporting Wikipedia passages, and the corpus is a chemistry-focused subset of
English Wikipedia-derived retrieval documents. The task tests whether a retriever
can follow entity bridges and chemical or scientific clues rather than only
matching one prominent surface term.

## Details

### What the Original Data Measures

[ChemTEB: Chemical Text Embedding Benchmark, an Overview of Embedding Models
Performance & Efficiency on a Specific Domain](https://arxiv.org/abs/2412.00532)
introduces ChemTEB as a chemistry-specific embedding benchmark and includes
`ChemHotpotQARetrieval` in its retrieval category. The paper says ChemTEB uses a
chemistry-related subset of HotpotQA and evaluates retrieval tasks with nDCG@10.
The BASF dataset card states that the subset was created from `mteb/hotpotqa` by
starting from the Wikipedia chemistry category and traversing linked articles up
to three levels deep.

[HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering](https://aclanthology.org/D18-1259/)
introduced 113k Wikipedia-based question-answer pairs whose questions require
finding and reasoning over multiple supporting documents. That matters here
because the chemistry filter does not remove the original multi-hop shape:
questions can ask for a company, year, field, dish, or related entity that is
connected through a chemical, biological, or scientific clue.

### Observed Data Profile

The Nano split has 18 queries, 10,000 documents, and 18 positive qrel rows. Each
query has one positive. Queries average 104.22 characters and often contain
multi-clause HotpotQA-style wording such as "the Swiss physicist who had a
geometrical representation named after him" or a company associated with a
chemical preservation method. Documents average 402.40 characters and are
Wikipedia passages about scientists, fungi, food preservation, journals,
plumbing traps, and other chemistry-adjacent topics.

The sampled data shows that "chemistry-focused" is broad. Some positives are
directly chemical or biological, such as basidiomycete fungi or nuclear magnetic
precision measurements. Others are adjacent through preservation, physics, food,
or scientific publishing. Readers should interpret this split as a small
chemistry-filtered multi-hop retrieval task rather than a dense literature-search
benchmark.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.6496
and hit@10 = 0.7222. With only 18 queries, the score is sensitive to a few hard
examples. BM25 ranks 10 positives first and finds 13 of 18 positives in the top
10, usually when the query includes a rare entity or phrase repeated in the
positive.

The failures are typical HotpotQA retrieval failures. For a question about a
Swiss physicist and a geometrical representation, BM25 retrieves another
scientist page before Felix Bloch. For a basidiomycete fungus query, it retrieves
a different basidiomycete page before the Boletus edulis passage. These cases
require resolving the bridge or requested property, not just retrieving a page
with one shared scientific term.

### Training Data That May Help

Useful training data includes the non-overlapping ChemHotpotQA train split,
HotpotQA retrieval pairs, multi-hop Wikipedia QA with supporting facts, and
chemistry-filtered Wikipedia passage retrieval. Training should exclude the
ChemHotpotQA test queries, qrels, and positive passages used by this Nano split.

The task is single-positive in Nano, but source HotpotQA was designed around
multiple supporting documents. Training data that preserves bridge entities,
comparison questions, and supporting-fact supervision is likely more useful than
simple query-document paraphrase data.

### Synthetic Data Guidance

For document-to-question generation, use non-evaluation chemistry-related
Wikipedia passages and generate multi-hop questions that require connecting a
scientist, compound, method, journal, organism, or application through another
entity. The answer passage should contain the final fact, while hard negatives
can share the bridge entity or scientific term.

For joint generation, create paired Wikipedia-style passages with an explicit
bridge relation and write a natural HotpotQA-like question over them. Do not use
the Nano evaluation queries or positive passages as seeds.

## Example Data

| Query | Positive document |
| --- | --- |
| In what field did a Swiss physicist who had a geometrical representation named after him work in? (97 chars) | Felix Bloch Felix Bloch (23 October 1905 – 10 September 1983) was a Swiss physicist, working mainly in the U.S. He and Edward Mills Purcell were awarded the 1952 Nobel Prize for Physics for "their development of new ways and ... [truncated 225 chars](354 chars) |
| What company claims to manufacture one out of every three objects that provide a shelf life typically ranging from one to five years? (133 chars) | Canning Canning is a method of preserving food in which the food contents are processed and sealed in an airtight container. Canning provides a shelf life typically ranging from one to five years, although under specific circ ... [truncated 225 chars](715 chars) |
| WHat dish is Dacryopinax spathularia included in that is also sometimes called Luóhàn cài? (91 chars) | Dacryopinax spathularia Dacryopinax spathularia (syn. Guepinia spathularia) is an edible jelly fungus. It is orange in color. In Chinese culture, it is called "guìhuā'ěr" (桂花耳; literally "sweet osmanthus ear," referring to it ... [truncated 225 chars](339 chars) |
| What is another name for basidiomycete fungus? (46 chars) | Boletus edulis Boletus edulis (English: penny bun, cep, porcino or porcini) is a basidiomycete fungus, and the type species of the genus "Boletus". Widely distributed in the Northern Hemisphere across Europe, Asia, and North ... [truncated 225 chars](821 chars) |
| What substance is always in a trap to prevent the passage of anything from either direction, even sewer gases? (111 chars) | Trap (plumbing) In plumbing, a trap is a device which has a shape that uses a bending path to capture water to prevent sewer gases from entering buildings, while allowing waste to pass through. In refinery applications, traps ... [truncated 225 chars](322 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoChemTEB |
| Backing dataset | NanoChemTEB |
| Task / split | NanoChemHotpotQA |
| Hugging Face dataset | [hakari-bench/NanoChemTEB](https://huggingface.co/datasets/hakari-bench/NanoChemTEB) |
| Language | en |
| Category | natural_language |
| Queries | 18 |
| Documents | 10,000 |
| Positive qrels | 18 |
| BM25 nDCG@10 | 0.7178 |
| BM25 hit@10 | 0.7778 |
| BM25 Recall@100 | 0.8889 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.7748 |
| Dense hit@10 | 0.8333 |
| Dense Recall@100 | 1.0000 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.7923 |
| Reranking hybrid hit@10 | 0.8333 |
| Reranking hybrid Recall@100 | 1.0000 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100 |
| Reranking hybrid safeguard rows | 0 |
| Query length avg chars | 104.22 |
| Document length avg chars | 402.40 |

### Public Sources

- [ChemTEB: Chemical Text Embedding Benchmark, an Overview of Embedding Models Performance & Efficiency on a Specific Domain](https://arxiv.org/abs/2412.00532); 2024; Ali Shiraee Kasmaee, Mohammad Khodadad, Mohammad Arshi Saloot, Nicholas Sherck, Stephen Dokas, Hamidreza Mahyar, and Soheila Samiee; DOI: `10.48550/arXiv.2412.00532`.
- [HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering](https://aclanthology.org/D18-1259/); 2018; Zhilin Yang et al.; DOI: `10.18653/v1/D18-1259`.
- [BASF-AI/ChemHotpotQARetrieval dataset card](https://huggingface.co/datasets/BASF-AI/ChemHotpotQARetrieval).
- [ChemTEB retrieval datasets collection](https://huggingface.co/collections/BASF-AI/chemteb-retrieval-datasets).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoChemTEB](https://huggingface.co/datasets/hakari-bench/NanoChemTEB)
- Source dataset: [BASF-AI/ChemHotpotQARetrieval](https://huggingface.co/datasets/BASF-AI/ChemHotpotQARetrieval)
- MTEB mirror: [mteb/ChemHotpotQARetrieval](https://huggingface.co/datasets/mteb/ChemHotpotQARetrieval)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| ChemTEB: Chemical Text Embedding Benchmark, an Overview of Embedding Models Performance & Efficiency on a Specific Domain | 2024 | arXiv paper | https://arxiv.org/abs/2412.00532 |
| HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering | 2018 | ACL paper | https://aclanthology.org/D18-1259/ |
| BASF-AI/ChemHotpotQARetrieval | 2024 | dataset card | https://huggingface.co/datasets/BASF-AI/ChemHotpotQARetrieval |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoChemTEB
  backing_dataset: NanoChemTEB
  dataset_id: hakari-bench/NanoChemTEB
  task_name: NanoChemHotpotQA
  split_name: NanoChemHotpotQA
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoChemTEB/NanoChemHotpotQA.md
  source_research:
    primary_source_type: benchmark_paper
    paper_pdf_or_html_checked: true
    paper_url: https://arxiv.org/abs/2412.00532
    additional_source_urls:
    - https://proceedings.mlr.press/v262/shiraee-kasmaee24a.html
    - https://aclanthology.org/D18-1259/
    - https://huggingface.co/datasets/BASF-AI/ChemHotpotQARetrieval
  counts:
    queries: 18
    documents: 10000
    positive_qrels: 18
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 104.2222222222
    document_mean: 402.3997
  bm25:
    ndcg_at_10: 0.7177774766605192
    hit_at_10: 0.7777777777777778
    source: dataset_candidate_subset
  learning:
    original_train_split: available
    evaluation_split_origin: ChemHotpotQARetrieval test split derived from HotpotQA
    train_eval_overlap_audit: not_audited
    leakage_note: exclude ChemHotpotQA test queries, qrels, and positive Wikipedia
      passages
    useful_training_data:
    - non-overlapping ChemHotpotQA train retrieval pairs
    - HotpotQA multi-hop retrieval with supporting facts
    - chemistry-filtered Wikipedia question-passage pairs
    - multi-hop scientific QA with bridge-entity hard negatives
    synthetic_data:
      document_generation: non-evaluation chemistry-related Wikipedia passages with
        bridge entities and scientific facts
      question_generation: HotpotQA-style multi-hop questions requiring a bridge from
        one entity or property to another
      answerability: the positive passage should contain the final answer fact and
        negatives may share only the bridge term
    multi_positive_training: single_positive_question_document_focus
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoChemTEB
    source_urls:
    - label: ChemTEB arXiv
      url: https://arxiv.org/abs/2412.00532
    - label: HotpotQA ACL Anthology
      url: https://aclanthology.org/D18-1259/
    - label: BASF-AI/ChemHotpotQARetrieval
      url: https://huggingface.co/datasets/BASF-AI/ChemHotpotQARetrieval
    source_notes: []
  references:
  - title: 'ChemTEB: Chemical Text Embedding Benchmark, an Overview of Embedding Models
      Performance & Efficiency on a Specific Domain'
    url: https://arxiv.org/abs/2412.00532
    year: 2024
    doi: 10.48550/arXiv.2412.00532
    is_paper: true
    source_confidence: definitive_paper_link
  - title: 'HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering'
    url: https://aclanthology.org/D18-1259/
    year: 2018
    doi: 10.18653/v1/D18-1259
    is_paper: true
    source_confidence: definitive_paper_link
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.7177774767
      hit_at_10: 0.7777777778
      recall_at_100: 0.8888888889
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 18
      query_coverage: 1.0
      relevant_coverage_at_100: 0.8888888889
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.7747997017
      hit_at_10: 0.8333333333
      recall_at_100: 1.0
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 18
      query_coverage: 1.0
      relevant_coverage_at_100: 1.0
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.7923255282
      hit_at_10: 0.8333333333
      recall_at_100: 1.0
      candidate_count_min: 100
      candidate_count_max: 100
      candidate_count_mean: 100.0
      query_count: 18
      query_coverage: 1.0
      relevant_coverage_at_100: 1.0
      safeguard_positive_rows: 0
      rows_with_101_candidates: 0
```
