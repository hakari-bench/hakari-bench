# NanoMIRACL / en

## Overview

MIRACL's English split is a monolingual ad hoc retrieval task over English
Wikipedia passages, designed around natural questions and human passage
judgments rather than answer extraction from a fixed article. The Nano task
keeps the same passage-retrieval framing with one labeled positive per query.
Observed questions are short `When`, `What`, `How`, `Who`, and `Where`
information needs, so the model must retrieve the passage that contains the
requested fact across broad encyclopedia topics such as people, places,
organizations, politics, science, and definitions.

## Details

### What the Original Data Measures

[MIRACL: A Multilingual Retrieval Dataset Covering 18 Diverse
Languages](https://aclanthology.org/2023.tacl-1.63/) describes MIRACL as a
monolingual ad hoc retrieval dataset over Wikipedia passages. The paper
emphasizes natural questions, natural passages, and human labels across 18
languages; in the English split, both query and corpus are English. The task is
therefore passage retrieval, not answer extraction from a preselected article
and not multilingual translation.

The MIRACL paper reports that the dataset was built on top of Mr. TYDI for 11
languages, including English, and adds richer passage-level annotations. It also
describes MIRACL's two-phase annotation workflow: native speakers generated
well-formed questions from Wikipedia prompts, then assessed candidate passages
retrieved by an ensemble of BM25, mDPR, and mColBERT. This matters because the
positive labels are attached to evidence-bearing passages drawn from the corpus,
not to isolated short answers.

The TACL version includes an English question-word analysis. It shows that
English MIRACL contains a mixture of `what`, `when`, `how`, `who`, `where`,
`which`, and yes/no questions, with distribution shifts across splits. That
matches the Nano sample: the queries are not keyword searches, but short natural
questions that require the retriever to identify the passage expressing the
requested relation.

### Observed Data Profile

The sampled Nano task has 200 queries, 1,657 documents, and 200 positive qrel
rows. Every query has exactly one positive passage. Queries average 40.10
characters. The most common openings in the sample are `When`, `What`, `How`,
`Who`, `Where`, and `Is`, with smaller numbers of `Does`, `Do`, `Why`, `Can`,
and other forms. Documents average 760.23 characters and are English Wikipedia
passages that usually begin with the article title.

The sampled positives cover a wide encyclopedia range: video-game companies,
Brazilian demographics, Soviet language policy, international organizations,
religion, philosophy, Antarctica, WWE, Chinese piracy, Argentina, diabetes, and
fiction adaptations. Some questions are straightforward entity-attribute
queries, such as when the Commonwealth of Independent States was formed. Others
are more interpretive or time-sensitive, such as what happened to Silicon
Knights, who the CEO of WWE is, or what the fastest-growing religion in the
United States is. Those examples should be read as retrieval against the
Wikipedia snapshot, not as current factual answers.

The English split is useful even though English retrieval data is abundant,
because it stresses the same MIRACL passage formulation as the non-English
splits. A model must retrieve the passage that supports the answer. It is not
enough to rank a page about the same broad topic if the selected passage does
not contain the requested evidence.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.5432
and hit@10 = 0.8750 on this Nano split. BM25 places 51 of 200 positives at rank
1 and 175 of 200 positives in the top 10. This is a strong sparse baseline
because many English questions include distinctive entity names, such as
`Silicon Knights`, `Ukrainization`, `Commonwealth of Independent States`, or
`Dark Horse`.

The failures are still informative. For "Who proposed dualism?", BM25 retrieves
property-dualism and cognitive-dissonance passages before the positive human
brain passage that names René Descartes. For "Who is the CEO of the WWE?", it
retrieves pages with generic `CEO` wording before the Vince McMahon passage. For
"How large is Antarctica?", the top hits are unrelated high-overlap passages
rather than the Antarctica passage, showing that short common-word questions can
fail despite an obvious target entity. For "Does Christianity come from
Judaism?", BM25 ranks broad Christianity-and-Judaism pages above the positive
passage about origins of Judaism that directly states the historical relation.

Because this Nano split is single-positive, hit@10 indicates whether the labeled
evidence passage appears at all, while nDCG@10 captures whether it is placed
early enough to be useful. A stronger model should preserve BM25's exact entity
matching and improve relation-sensitive ranking for broad `what`, `who`, `how`,
and yes/no questions.

### Training Data That May Help

Non-overlapping English MIRACL training data is the first source to inspect, but
upstream development or test queries, qrels, and positive passages likely to
overlap with NanoMIRACL should preferably be excluded from training. Other
useful data includes English Wikipedia question-to-passage retrieval pairs,
open-domain QA evidence retrieval datasets, and supervised entity-attribute
retrieval examples from encyclopedic corpora.

Training should emphasize passage-level evidence, not just question answering or
sentence paraphrase. The model needs to learn to retrieve passages containing
dates, definitions, legal or political succession rules, demographic statements,
biographical events, and source-text evidence for yes/no or causal questions.

### Synthetic Data Guidance

For document-to-question generation, use non-evaluation English
Wikipedia-style passages and generate natural questions whose answers are
explicitly grounded in one passage. Useful synthetic questions include `when`,
`what`, `who`, `where`, `how many`, `how much`, `does`, and `is` forms about
organizations, events, people, geography, history, demography, and definitions.

For joint document-and-question generation, create English encyclopedia-style
passages with titles, aliases, dates, offices, places, population figures,
religious or historical relationships, and concise evidence sentences, then
create questions answerable from those passages. Do not seed generation with
Nano evaluation queries or positive passages. Include related but non-answering
passages as contrastive material so the model learns that topic overlap is not
enough for relevance.

## Example Data

| Query | Positive document |
| --- | --- |
| How many people visit the Eiffel Tower each year? (49 chars) | Tourism in Paris The Eiffel Tower is acknowledged as the universal symbol of Paris and France. It was originally designed by Émile Nouguier and Maurice Koechlin. In March 1885 Gustave Eiffel, known primarily as a successful i ... [truncated 225 chars](751 chars) |
| How long is the Omo River? (26 chars) | Omo River Its course is generally to the south, however with a major bend to the west at about 7° N 37° 30' E to about 36° E where it turns south until 5° 30' N where it makes a large S- bend then resumes its southerly course ... [truncated 225 chars](366 chars) |
| Where did Sun Yat-sen study medicine? (37 chars) | Sun Yat Sen Memorial House Whilst studying at the Hong Kong College of Medicine for Chinese, the young Dr. Sun constantly travelled between Hong Kong and Macau to criticise the corruption of the Qing regime and agitated for r ... [truncated 225 chars](536 chars) |
| What is the population of Lagos? (32 chars) | Lagos Colony Lagos Colony was a British colonial possession centred on the port of Lagos in what is now southern Nigeria. Lagos was annexed on 6 August 1861 under the threat of force by Commander Beddingfield of HMS Prometheu ... [truncated 225 chars](1091 chars) |
| When did Marxism develop? (25 chars) | Sophia N. Antonopoulou Sophia Antonopoulou developed this critique of Marx and Marxism in her book "The Marxist Theory of Development and its Convergence with the Bourgeois Theoretical Paradigm" (Papazissis, Athens, 1991) (in ... [truncated 225 chars](872 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMIRACL |
| Backing dataset | NanoMIRACL |
| Task / split | en |
| Hugging Face dataset | [hakari-bench/NanoMIRACL](https://huggingface.co/datasets/hakari-bench/NanoMIRACL) |
| Language | en |
| Category | natural_language |
| Queries | 200 |
| Documents | 1,657 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.6774 |
| BM25 hit@10 | 0.9950 |
| BM25 Recall@100 | 0.9929 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.7721 |
| Dense hit@10 | 0.9550 |
| Dense Recall@100 | 0.9482 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.7474 |
| Reranking hybrid hit@10 | 0.9850 |
| Reranking hybrid Recall@100 | 0.9964 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100 |
| Reranking hybrid safeguard rows | 0 |
| Query length avg chars | 40.10 |
| Document length avg chars | 760.23 |

### Public Sources

- [Making a MIRACL: Multilingual Information Retrieval Across a Continuum of Languages](https://arxiv.org/abs/2210.09984); 2022; Xinyu Zhang, Nandan Thakur, Odunayo Ogundepo, Ehsan Kamalloo, David Alfonso-Hermelo, Xiaoguang Li, Qun Liu, Mehdi Rezagholizadeh, Jimmy Lin; DOI: `10.48550/arXiv.2210.09984`.
- [MIRACL: A Multilingual Retrieval Dataset Covering 18 Diverse Languages](https://aclanthology.org/2023.tacl-1.63/); 2023 TACL version; DOI: `10.1162/tacl_a_00595`.
- [MIRACL GitHub repository](https://github.com/project-miracl/miracl).
- [MIRACL corpus dataset card](https://huggingface.co/datasets/miracl/miracl-corpus).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMIRACL](https://huggingface.co/datasets/hakari-bench/NanoMIRACL)
- Source corpus: [miracl/miracl-corpus](https://huggingface.co/datasets/miracl/miracl-corpus)
- Source queries and qrels: [miracl/miracl](https://huggingface.co/datasets/miracl/miracl)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Making a MIRACL: Multilingual Information Retrieval Across a Continuum of Languages | 2022 | paper | https://arxiv.org/abs/2210.09984 |
| MIRACL: A Multilingual Retrieval Dataset Covering 18 Diverse Languages | 2023 | paper | https://aclanthology.org/2023.tacl-1.63/ |
| MIRACL GitHub repository |  | project repository | https://github.com/project-miracl/miracl |
| miracl/miracl-corpus |  | dataset card | https://huggingface.co/datasets/miracl/miracl-corpus |
| miracl/miracl |  | dataset card | https://huggingface.co/datasets/miracl/miracl |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMIRACL
  backing_dataset: NanoMIRACL
  dataset_id: hakari-bench/NanoMIRACL
  task_name: en
  split_name: en
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMIRACL/en.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 200
    documents: 1657
    positive_qrels: 200
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 40.1
    document_mean: 760.228727
  bm25:
    ndcg_at_10: 0.6774072810398251
    hit_at_10: 0.995
    source: dataset_candidate_subset
  learning:
    original_train_split: available
    evaluation_split_origin: unknown
    train_eval_overlap_audit: not_audited
    leakage_note: prefer excluding upstream development/test data or other MIRACL-derived
      data likely to overlap with the NanoMIRACL evaluation questions and passages
    useful_training_data:
    - non-overlapping MIRACL English train split data
    - English Wikipedia question-to-passage retrieval pairs
    - English open-domain QA evidence retrieval datasets
    synthetic_data:
      document_generation: English Wikipedia-style passages with titles, dates, offices,
        places, population figures, definitions, and factual evidence
      question_generation: natural English fact questions using varied when, what,
        who, where, how many, how much, is, and does forms
      answerability: questions should be grounded in explicit facts or relations in
        the generated or selected passage
    multi_positive_training: single_positive_question_document_focus
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMIRACL
    source_urls:
    - label: MIRACL corpus dataset
      url: https://huggingface.co/datasets/miracl/miracl-corpus
    - label: MIRACL source queries and qrels
      url: https://huggingface.co/datasets/miracl/miracl
    - label: MIRACL GitHub repository
      url: https://github.com/project-miracl/miracl
    source_notes: []
  references:
  - title: 'Making a MIRACL: Multilingual Information Retrieval Across a Continuum
      of Languages'
    url: https://arxiv.org/abs/2210.09984
    year: 2022
    doi: 10.48550/arXiv.2210.09984
    is_paper: true
    source_confidence: definitive_paper_link
  - title: 'MIRACL: A Multilingual Retrieval Dataset Covering 18 Diverse Languages'
    url: https://aclanthology.org/2023.tacl-1.63/
    year: 2023
    doi: 10.1162/tacl_a_00595
    is_paper: true
    source_confidence: definitive_paper_link
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.677407281
      hit_at_10: 0.995
      recall_at_100: 0.9928571429
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9928571429
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.7721028257
      hit_at_10: 0.955
      recall_at_100: 0.9482142857
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9482142857
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.747376708
      hit_at_10: 0.985
      recall_at_100: 0.9964285714
      candidate_count_min: 100
      candidate_count_max: 100
      candidate_count_mean: 100.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9964285714
      safeguard_positive_rows: 0
      rows_with_101_candidates: 0
```
