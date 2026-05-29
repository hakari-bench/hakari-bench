# NanoMIRACL / bn

## Overview

MIRACL treats Bengali retrieval as same-language Wikipedia passage search with
native questions and relevance judgments. In this Nano split, Bengali questions
must retrieve the single answer-bearing Bengali passage from a compact corpus.
The observed queries are often topic-first rather than question-word-first,
with intent signaled later by forms such as `কী`, `কোথায়`, `কত`, or `কবে`,
so the task tests entity-centered Bengali retrieval where the model must bind a
specific factual attribute to the right passage.

## Details

### What the Original Data Measures

[Making a MIRACL: Multilingual Information Retrieval Across a Continuum of
Languages](https://arxiv.org/abs/2210.09984) presents MIRACL as a monolingual
ad hoc retrieval benchmark across 18 languages. In this setting, Bengali
queries search Bengali Wikipedia passages; the task is not cross-lingual search
or translated English retrieval. The paper reports that MIRACL covers Wikipedia
passages, well-formed natural-language questions, and native-speaker relevance
judgments.

The Bengali split belongs to the group of MIRACL languages inherited from Mr.
TyDi. The paper explains that for these languages, MIRACL aligns with the
existing Mr. TyDi split structure but provides richer relevance judgments over a
newly prepared Wikipedia passage corpus. This matters because the task evaluates
retrieval over all relevant Bengali Wikipedia passages, not extraction from a
single preselected article.

The MIRACL paper also describes a two-phase annotation workflow: annotators
generated questions from Wikipedia prompts, then judged candidate passages from
an ensemble of BM25, mDPR, and mColBERT retrieval. For Bengali, the paper reports
development-set BM25 nDCG@10 of 0.508 and hybrid BM25+mDPR nDCG@10 of 0.654.
The full benchmark therefore rewards both lexical matching and semantic passage
selection, especially when the correct answer is in a broader article section.

### Observed Data Profile

The sampled Nano task has 200 queries, 1,731 documents, and 200 positive qrel
rows. Every query has exactly one positive passage. Queries average 47.23
characters, longer than the Japanese and Arabic NanoMIRACL examples already
inspected. Many Bengali queries begin with the topic rather than a question word:
common openings include `বাংলাদেশের`, `ভারতীয়`, `ব্রিটিশ`, `মার্কিন`, and
proper names. The question intent often appears later through phrases such as
`কী`, `কোথায়`, `কত`, `কোন`, or `কবে`.

Documents average 717.88 characters and are Bengali Wikipedia passages. The
retrieval unit is usually an article-title-prefixed passage with enough context
to answer a factual question. The sampled positives cover religious concepts,
Bangladeshi and Indian public figures, rivers, prisons, country statistics,
software support, literary works, films, and sports organizations. Several
queries ask for one specific attribute of an entity, so the model must retrieve
the passage containing that attribute rather than any passage about the same
entity family.

The observed data has a practical Bengali retrieval challenge: a query can carry
many topical words before the actual relation is clear. For example, questions
about an author's work, a film actor's first film, or a country's rank by
population contain enough lexical anchors to find related pages, but the positive
depends on the exact attribute requested. This makes passage-level evidence
selection more important than title matching alone.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.5103
and hit@10 = 0.7750 on this Nano split. BM25 places 57 of 200 positives at rank
1 and 155 of 200 positives in the top 10. The baseline is useful when the query
contains rare names such as `ড্রপবক্স`, `সেলুলার জেল`, or `গঙ্গা নদী`, but it
misses 45 labeled positives from the top 10.

The failure cases show entity-neighbor confusion. For "মতিউর রহমান নিজামীর
বাবার নাম কী ?", BM25 retrieves passages about other people named মতিউর রহমান
before the positive passage for মতিউর রহমান নিজামী. For "লালন সাঁই বা ফকির
লালনের আখড়া কোথায় ছিল ?", it retrieves pages about related singers, films, and
performers before the positive passage that names the আখড়া location. For
"মুসলমানদের পবিত্র ধর্মীয় গ্রন্থ কুরআনের মোট কয়টি সূরা রয়েছে ?", BM25 ranks
individual sura pages above the general Qur'an passage that states the total
number of suras. These examples show that lexical overlap finds the topic, but
not always the requested relation.

Because the Nano split is single-positive, hit@10 captures whether the labeled
evidence passage appears at all, while nDCG@10 captures how high it appears.
Strong models should preserve Bengali rare-term matching but improve relation
resolution for "name of", "how many", "where", "which work", and "first film"
questions.

### Training Data That May Help

Non-overlapping Bengali MIRACL training data is the first source to inspect.
Because this task is MIRACL-derived, upstream development or test queries, qrels,
and positive passages likely to overlap with the benchmark should preferably be
excluded from training. Other useful data includes Bengali Wikipedia
question-to-passage pairs, Bengali QA evidence retrieval datasets, and
entity-attribute supervision over people, places, organizations, books, films,
religion, and country facts.

Training should focus on evidence retrieval rather than paraphrase alone. The
model needs to learn that a Bengali question about an entity's father, founding
year, location, count, or work title should retrieve the passage containing that
attribute, even when other passages share more surface words.

### Synthetic Data Guidance

For document-to-question generation, use non-evaluation Bengali
Wikipedia-style passages and generate Bengali questions whose answer is
explicitly grounded in one passage. Useful synthetic intents include `কী`,
`কোথায়`, `কত`, `কোন`, `কবে`, `কার`, and `কে` questions about names, places,
dates, counts, first works, founders, definitions, and rankings. Generated
questions should vary whether the topic appears first or after the question
word.

For joint document-and-question generation, create Bengali encyclopedia-style
passages with article titles, aliases, dates, person names, places, and
attribute-bearing sentences, then create questions answerable from those
passages. Do not seed generation with Nano evaluation queries or positive
passages. Synthetic positives should be the evidence passage, not a short answer
or a loosely related article.

## Example Data

| Query | Positive document |
| --- | --- |
| শ্রীনিবাস রামানুজনের বাবার নাম কি ছিল ? (39 chars) | শ্রীনিবাস রামানুজন রামানুজন ১৮৮৭ খ্রিস্টাব্দের ২২ ডিসেম্বর প্রাচীন ভারতের মাদ্রাজ প্রদেশের তাঞ্জোর জেলার ইরেভদ শহরের এক দরিদ্র ব্রাহ্মণ পরিবারে জন্মগ্রহণ করেন। তাঁর পিতা "কে শ্রীনিবাস ইয়েঙ্গার" ছিলেন শহরের একটি কাপড়ের দোকান ... [truncated 225 chars](588 chars) |
| জে কে রাউলিং রচিত হ্যারি পটার উপন্যাসের প্রকাশক কে ? (52 chars) | হ্যারি পটার এই বইয়ের সাফল্য রাউলিংকে ইতিহাসে সবচেয়ে বেশী উপার্জন করা লেখকের তালিকায় শীর্ষস্থান দিয়েছে। বইগুলোর ইংরেজি সংস্করণণ প্রকাশ করে ব্লুমসবারি যুক্তরাজ্যে, স্কলাস্টিক প্রেস যুক্তরাষ্ট্রে, অ্যালেন ও আনউইন অস্ট্রেলিয় ... [truncated 225 chars](255 chars) |
| খেজুর গাছে খেজুর ফল আসতে কতদিন সময় লাগে ? (41 chars) | খেজুর গাছে ফল উৎপাদনের জন্য সচরাচর ৪ থেকে ৮ বছর পর্যন্ত অপেক্ষা করতে হয়। তবে বাণিজ্যিকভাবে ফসল উৎপাদন উপযোগী খেজুর গাছে ফল আসতে ৭ থেকে ১০ বছর সময় লেগে যায়। পূর্ণাঙ্গ খেজুর গাছে প্রতি মৌসুমে গড়ে ৮০-১২০ কিলোগ্রাম (১৭৬-২৬৪ প ... [truncated 225 chars](416 chars) |
| ওড়িশার কোন শহরে জগন্নাথের প্রধান মন্দিরটি অবস্থিত ? (51 chars) | জগন্নাথ জগন্নাথের মূর্তি সাধারণত কাঠে তৈরি করা হয়। এই মূর্তির চোখদুটি বড়ো বড়ো ও গোলাকার। হাত অসম্পূর্ণ। মূর্তিতে কোনো পা দেখা যায় না। জগন্নাথের পূজাপদ্ধতিও অন্যান্য হিন্দু দেবতাদের পূজাপদ্ধতির চেয়ে আলাদা। ওড়িশা রাজ্যের ... [truncated 225 chars](309 chars) |
| সাদ্দাম হোসেন আবদুল মাজিদ আল তিকরিতি কবে নিহত হন ? (50 chars) | সাদ্দাম হুসাইন প্রথমে সাদ্দাম হোসেন জেনারেল আহমেদ হাসান আল বকরের উপ-রাষ্ট্রপতি ছিলেন। সেই সময় সাদ্দাম দৃঃঢ় ভাবে সরকার ও সামরিক বাহিনীর মধ্যকার বিরোধের অবসান ঘটান। এই উদ্দেশ্যে তিনি নিরাপত্তা বাহিনী গঠন করেন। ইরাকের রাষ্ট্রপ ... [truncated 225 chars](1236 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMIRACL |
| Backing dataset | NanoMIRACL |
| Task / split | bn |
| Hugging Face dataset | [hakari-bench/NanoMIRACL](https://huggingface.co/datasets/hakari-bench/NanoMIRACL) |
| Language | bn |
| Category | natural_language |
| Queries | 200 |
| Documents | 1,731 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.5033 |
| BM25 hit@10 | 0.7800 |
| BM25 Recall@100 | 0.9582 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.7661 |
| Dense hit@10 | 0.9450 |
| Dense Recall@100 | 0.9484 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.6537 |
| Reranking hybrid hit@10 | 0.9350 |
| Reranking hybrid Recall@100 | 0.9975 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100 |
| Reranking hybrid safeguard rows | 0 |
| Query length avg chars | 47.23 |
| Document length avg chars | 717.88 |

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
  task_name: bn
  split_name: bn
  language: bn
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMIRACL/bn.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 200
    documents: 1731
    positive_qrels: 200
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 47.225
    document_mean: 717.879261
  bm25:
    ndcg_at_10: 0.5033141888103525
    hit_at_10: 0.78
    source: dataset_candidate_subset
  learning:
    original_train_split: available
    evaluation_split_origin: unknown
    train_eval_overlap_audit: not_audited
    leakage_note: prefer excluding upstream development/test data or other MIRACL-derived
      data likely to overlap with the NanoMIRACL evaluation questions and passages
    useful_training_data:
    - non-overlapping MIRACL Bengali train split data
    - native Bengali Wikipedia question-to-passage retrieval pairs
    - Bengali entity-attribute QA evidence retrieval pairs
    synthetic_data:
      document_generation: Bengali Wikipedia-style passages with titles, aliases,
        dates, names, places, definitions, counts, and factual evidence
      question_generation: Bengali fact questions with varied topic-first and question-word-first
        forms
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
      ndcg_at_10: 0.5033141888
      hit_at_10: 0.78
      recall_at_100: 0.9582309582
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9582309582
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.7660762
      hit_at_10: 0.945
      recall_at_100: 0.9484029484
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9484029484
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.653704251
      hit_at_10: 0.935
      recall_at_100: 0.9975429975
      candidate_count_min: 100
      candidate_count_max: 100
      candidate_count_mean: 100.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9975429975
      safeguard_positive_rows: 0
      rows_with_101_candidates: 0
```
