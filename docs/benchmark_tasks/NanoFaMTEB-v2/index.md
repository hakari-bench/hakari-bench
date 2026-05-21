# NanoFaMTEB-v2

## Overview

NanoFaMTEB-v2 is the Nano task group for Persian retrieval in FaMTEB. It covers
seventeen Persian natural-language retrieval settings: argument retrieval,
fact-verification evidence retrieval, finance QA, multi-hop QA, MIRACL and
Natural Questions style retrieval, MS MARCO-style passage search, NeuCLIR news
retrieval, Persian web search, duplicate-question retrieval, scientific and
biomedical evidence search, synthetic QA, synthetic chatbot RAG FAQ retrieval,
WebFAQ, and Wikipedia question answering.

The group is useful because it does not treat Persian retrieval as one uniform
problem. Some tasks are short keyword-to-snippet searches, some are long
argument or dialogue queries, and several tasks have dozens of relevant
documents per query. A model must handle Persian script and morphology,
translated benchmark data, native web material, synthetic Persian data, and
domain vocabulary from finance, medicine, science, news, and general Wikipedia.

## Details

### What the Original Group Measures

[FaMTEB: Massive Text Embedding Benchmark in Persian Language](https://arxiv.org/abs/2502.11571)
introduces a Persian text embedding benchmark built in the MTEB style. It
combines Persian datasets, translated retrieval benchmarks, and synthetic
Persian data so that embedding models can be evaluated on Persian semantic
similarity, classification, clustering, reranking, and retrieval. NanoFaMTEB-v2
is the compact retrieval subset for that broader Persian benchmark.

The group follows the retrieval interface from
[MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316):
queries, corpus documents, qrels, and a BM25 candidate ranking are exposed per
task split. In this Nano group, those tasks come from `MCINext` Persian variants,
MTEB hard-negative datasets, MIRACL, NeuCLIR, WebFAQ, and synthetic Persian QA
or chatbot resources. The resulting suite is best read as a Persian retrieval
coverage test rather than as a single BEIR translation.

### Subtask Coverage

The seventeen subtasks cover six retrieval families:

- **Argument and question matching:** `argu_ana_fa` retrieves paired
  counterargument-style texts, while `quora_fa` retrieves duplicate or closely
  related Persian questions.
- **Open-domain QA and evidence retrieval:** `fever_fa`, `hotpot_qa_fa`,
  `miracl_fa`, `nq_fa`, `msmarco_fa`, `wikipedia_multilingual_fa`, and
  `syn_per_qa` map claims or questions to evidence passages, answer passages, or
  Wikipedia-style answers.
- **Domain retrieval:** `fi_qa2018_fa`, `sci_fact_fa`, `scidocs_fa`, and
  `treccovid_fa` cover finance, scientific claim evidence, related-paper
  retrieval, and biomedical COVID-19 literature.
- **News and CLIR-style retrieval:** `neu_clir2023_fas` uses Persian news or web
  documents with many relevant judgments per information need.
- **Web and FAQ retrieval:** `persian_web_document` and `web_faq_fas` test short
  Persian web queries, snippets, and FAQ question-answer matching.
- **Conversational RAG retrieval:** `syn_per_chatbot_ragfaq` maps long
  multi-turn Persian conversations to concise FAQ entries.

All observed tasks are Persian-labeled natural-language retrieval splits. The
qrel structure varies sharply: five tasks are single-positive for every query,
while twelve tasks have at least some multi-positive queries. `treccovid_fa`,
`neu_clir2023_fas`, `msmarco_fa`, and `persian_web_document` account for most of
the multi-positive judgments.

### Observed Group Profile

Across the seventeen splits, NanoFaMTEB-v2 contains 2,966 queries, 17,925
positive qrels, and 161,314 split-local candidate documents. The document count
is a sum across subtasks, not a deduplicated group-wide corpus size. Queries
average 161.54 characters when weighted by query count, and documents average
694.08 characters when weighted by split-local document count.

The query and document lengths show the main diversity of the group.
`persian_web_document` has extremely short web-search queries averaging 16.35
characters, while `argu_ana_fa` has paragraph-length argument queries averaging
1,100.98 characters. Documents range from very short Quora-style paired
questions in `quora_fa` to long NeuCLIR documents averaging 3,121.94 characters.
The sampled records include Persian argument paragraphs, Wikipedia evidence,
FAQ answers, scientific abstracts, COVID-19 biomedical abstracts, web snippets,
and multi-turn chatbot logs.

### BM25 Difficulty

Query-weighted BM25 nDCG@10 is 0.6570 and query-weighted hit@10 is 0.7984. The
task-level range is wide: `treccovid_fa` reaches nDCG@10 = 0.9490 and hit@10 =
0.9800, while `argu_ana_fa` reaches nDCG@10 = 0.2860 and
`syn_per_chatbot_ragfaq` reaches hit@10 = 0.4150.

BM25 is strongest on tasks with short lexical queries, many relevant documents,
or distinctive terms: TREC-COVID biomedical topics, HotpotQA-style evidence,
Wikipedia QA, WebFAQ, Quora duplicates, synthetic QA, Persian web search, MS
MARCO, and NeuCLIR. It is much weaker where the relation is stance-sensitive,
conceptual, or conversational. ArguAna requires matching an argument to a paired
counterargument, SCIDOCS requires related scientific-paper retrieval beyond exact
title overlap, FiQA contains finance wording that may not repeat exactly in the
answer, and chatbot RAG FAQ retrieval compresses long dialogue histories into a
short FAQ target.

### Training Data That May Help

Useful training data should preserve the task-family differences. For Persian
web and QA tasks, Persian search logs, mMARCO-style query-passage pairs,
Wikipedia QA, MIRACL-style hard negatives, and FAQ retrieval data are directly
relevant. For domain tasks, use Persian or translated scientific, biomedical,
finance, and news retrieval data with hard negatives from the same domain. For
argument and dialogue tasks, use stance-aware argument-pair retrieval,
conversation-to-knowledge-base matching, Persian query rewriting, and
chatbot-RAG examples.

Training should exclude NanoFaMTEB-v2 evaluation queries, qrels, positive
documents, and source rows used in the Nano splits. Because several tasks are
translated or derived from public benchmark test splits, using upstream test
sets without an overlap audit can inflate scores. Multi-positive tasks should
also preserve their qrel structure: treating one judged document as the only
positive would distort TREC-COVID, NeuCLIR, MS MARCO, Persian web retrieval, and
SCIDOCS.

### Synthetic Data Guidance

Synthetic data can help if it keeps Persian retrieval phenomena intact. Generated
queries should preserve Persian script, right-to-left punctuation, Persian named
entities, domain terminology, and natural Persian morphology. Synthetic
documents should match the expected target shape: counterarguments for ArguAna,
evidence passages for FEVER and SciFact, answer passages for QA, related
abstracts for SCIDOCS, FAQ answers for WebFAQ and chatbot RAG, and long news or
biomedical passages for NeuCLIR and TREC-COVID.

Hard negatives should be close in topic and vocabulary but wrong in the task
relation. For example, an argument negative can share the policy topic but not
the counterargument relation; a chatbot FAQ negative can mention the same product
or service but answer a different user need; and a scientific negative can use
the same field terminology while describing a different method or finding.
Evaluation queries and positive documents from NanoFaMTEB-v2 should not be used
as generation seeds.

## Task Summary

| Task | Retrieval shape | Queries | Docs | BM25 nDCG@10 | BM25 hit@10 | Query avg chars | Doc avg chars | Source status |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| [argu_ana_fa](argu_ana_fa.md) | argument to paired counterargument | 199 | 8,669 | 0.2860 | 0.6432 | 1,100.98 | 973.15 | FaMTEB + MCINext dataset card |
| [fever_fa](fever_fa.md) | claim to fact-verification evidence | 200 | 10,000 | 0.8240 | 0.9000 | 47.09 | 523.29 | FaMTEB + MCINext dataset card |
| [fi_qa2018_fa](fi_qa2018_fa.md) | finance question to answer passage | 200 | 10,000 | 0.3888 | 0.5300 | 65.78 | 763.49 | FaMTEB + MCINext dataset card |
| [hotpot_qa_fa](hotpot_qa_fa.md) | multi-hop question to evidence passages | 200 | 10,000 | 0.9102 | 0.9650 | 87.89 | 394.90 | FaMTEB + MCINext dataset card |
| [miracl_fa](miracl_fa.md) | Persian MIRACL query to Wikipedia passage | 200 | 10,000 | 0.5509 | 0.8000 | 39.99 | 413.55 | FaMTEB + MIRACL/MTEB source |
| [msmarco_fa](msmarco_fa.md) | web query to passage answer | 43 | 8,766 | 0.8161 | 0.9535 | 31.49 | 326.20 | FaMTEB + MCINext dataset card |
| [neu_clir2023_fas](neu_clir2023_fas.md) | information need to news/web documents | 74 | 10,000 | 0.7761 | 0.9324 | 65.82 | 3,121.94 | FaMTEB + NeuCLIR/MTEB source |
| [nq_fa](nq_fa.md) | natural question to evidence passage | 200 | 10,000 | 0.4683 | 0.7000 | 46.72 | 556.82 | FaMTEB + MCINext dataset card |
| [persian_web_document](persian_web_document.md) | short web query to web document/snippet | 200 | 10,000 | 0.8210 | 0.9500 | 16.35 | 228.31 | FaMTEB + MCINext dataset card |
| [quora_fa](quora_fa.md) | question to duplicate question | 200 | 10,000 | 0.8832 | 0.9550 | 48.67 | 60.81 | FaMTEB + MCINext dataset card |
| [sci_fact_fa](sci_fact_fa.md) | scientific claim to evidence abstract | 200 | 5,183 | 0.6374 | 0.7900 | 84.48 | 1,361.31 | FaMTEB + MCINext dataset card |
| [scidocs_fa](scidocs_fa.md) | paper title to related scientific document | 200 | 10,000 | 0.3664 | 0.5650 | 61.56 | 1,092.04 | FaMTEB + MCINext dataset card |
| [syn_per_chatbot_ragfaq](syn_per_chatbot_ragfaq.md) | multi-turn chatbot dialogue to FAQ entry | 200 | 8,696 | 0.2882 | 0.4150 | 597.44 | 145.69 | FaMTEB + MCINext dataset card |
| [syn_per_qa](syn_per_qa.md) | synthetic Persian question to answer | 200 | 10,000 | 0.8609 | 0.9400 | 59.81 | 306.22 | FaMTEB + MCINext dataset card |
| [treccovid_fa](treccovid_fa.md) | COVID-19 topic to biomedical abstract | 50 | 10,000 | 0.9490 | 0.9800 | 64.58 | 1,210.70 | FaMTEB + MCINext dataset card |
| [web_faq_fas](web_faq_fas.md) | FAQ question to answer passage | 200 | 10,000 | 0.8680 | 0.9350 | 48.01 | 209.60 | FaMTEB + WebFAQ/MTEB source |
| [wikipedia_multilingual_fa](wikipedia_multilingual_fa.md) | Wikipedia-style question to answer passage | 200 | 10,000 | 0.8915 | 0.9600 | 49.17 | 352.93 | FaMTEB + MCINext dataset card |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoFaMTEB-v2 |
| Backing dataset | NanoFaMTEB-v2 |
| Hugging Face dataset | [hakari-bench/NanoFaMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoFaMTEB-v2) |
| Language | fa |
| Category | natural_language |
| Subtasks | 17 |
| Total queries | 2,966 |
| Split-local documents | 161,314 |
| Positive qrels | 17,925 |
| Positives per query | avg 6.04, min 1, median 1.0, max 100 |
| Multi-positive tasks | 12 |
| Query-weighted BM25 nDCG@10 | 0.6570 |
| Query-weighted BM25 hit@10 | 0.7984 |
| Mean query length | 161.54 chars, weighted by query count |
| Mean document length | 694.08 chars, weighted by split-local document count |

### Public Sources

- [FaMTEB: Massive Text Embedding Benchmark in Persian Language](https://arxiv.org/abs/2502.11571); 2025; Kasra Kowsari et al.
- [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316); 2023; Niklas Muennighoff et al.
- [MIRACL project](http://miracl.ai/); multilingual information retrieval benchmark.
- [NeuCLIR project](https://neuclir.github.io/); cross-language information retrieval benchmark.
- [mteb/WebFAQRetrieval](https://huggingface.co/datasets/mteb/WebFAQRetrieval); source dataset card.
- `MCINext` Persian source dataset cards for ArguAna, FEVER, FiQA, HotpotQA,
  MS MARCO, NQ, Persian web retrieval, Quora, SciFact, SCIDOCS, synthetic QA,
  synthetic chatbot RAG FAQ, TREC-COVID, and Wikipedia-style retrieval.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoFaMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoFaMTEB-v2)
- Source datasets:
  [MCINext/arguana-fa-v2](https://huggingface.co/datasets/MCINext/arguana-fa-v2),
  [MCINext/FEVER_FA_test_top_250_only_w_correct-v2](https://huggingface.co/datasets/MCINext/FEVER_FA_test_top_250_only_w_correct-v2),
  [MCINext/fiqa-fa-v2](https://huggingface.co/datasets/MCINext/fiqa-fa-v2),
  [MCINext/HotpotQA_FA_test_top_250_only_w_correct-v2](https://huggingface.co/datasets/MCINext/HotpotQA_FA_test_top_250_only_w_correct-v2),
  [mteb/MIRACLRetrievalHardNegatives](https://huggingface.co/datasets/mteb/MIRACLRetrievalHardNegatives),
  [MCINext/MSMARCO_FA_test_top_250_only_w_correct-v2](https://huggingface.co/datasets/MCINext/MSMARCO_FA_test_top_250_only_w_correct-v2),
  [mteb/NeuCLIR2023RetrievalHardNegatives](https://huggingface.co/datasets/mteb/NeuCLIR2023RetrievalHardNegatives),
  [MCINext/nq-fa-v2](https://huggingface.co/datasets/MCINext/nq-fa-v2),
  [MCINext/persian-web-document-retrieval](https://huggingface.co/datasets/MCINext/persian-web-document-retrieval),
  [MCINext/quora-fa-v2](https://huggingface.co/datasets/MCINext/quora-fa-v2),
  [MCINext/scifact-fa-v2](https://huggingface.co/datasets/MCINext/scifact-fa-v2),
  [MCINext/scidocs-fa-v2](https://huggingface.co/datasets/MCINext/scidocs-fa-v2),
  [MCINext/synthetic-persian-chatbot-rag-faq-retrieval](https://huggingface.co/datasets/MCINext/synthetic-persian-chatbot-rag-faq-retrieval),
  [MCINext/synthetic-persian-qa-retrieval](https://huggingface.co/datasets/MCINext/synthetic-persian-qa-retrieval),
  [MCINext/trec-covid-fa-v2](https://huggingface.co/datasets/MCINext/trec-covid-fa-v2),
  [mteb/WebFAQRetrieval](https://huggingface.co/datasets/mteb/WebFAQRetrieval),
  and [MCINext/wikipedia-persian-qa-retrieval](https://huggingface.co/datasets/MCINext/wikipedia-persian-qa-retrieval).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| FaMTEB: Massive Text Embedding Benchmark in Persian Language | 2025 | benchmark paper | https://arxiv.org/abs/2502.11571 |
| MTEB: Massive Text Embedding Benchmark | 2023 | benchmark paper | https://arxiv.org/abs/2210.07316 |
| MIRACL | 2022 | benchmark project | http://miracl.ai/ |
| NeuCLIR | 2023 | benchmark project | https://neuclir.github.io/ |
| WebFAQRetrieval | 2024 | dataset card | https://huggingface.co/datasets/mteb/WebFAQRetrieval |
| PersianWebDocumentRetrieval source reference | 2024 | IEEE record | https://ieeexplore.ieee.org/document/10553090 |

## Machine-Readable Metadata

<!-- benchmark-task-group-metadata:v1 -->

```yaml
benchmark_task_group_metadata:
  schema_version: 1
  document_status: reviewed_manual
  nano_set: NanoFaMTEB-v2
  backing_dataset: NanoFaMTEB-v2
  dataset_id: hakari-bench/NanoFaMTEB-v2
  language: fa
  category: natural_language
  document_path: docs/benchmark_tasks/NanoFaMTEB-v2/index.md
  source_research:
    primary_source_type: benchmark_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    tasks: 17
    queries: 2966
    split_local_documents: 161314
    positive_qrels: 17925
  positives_per_query:
    average: 6.043492919757249
    min: 1
    median: 1.0
    max: 100
    multi_positive_tasks: 12
    multi_positive_queries: 1176
  text_stats_chars:
    query_mean_weighted_by_queries: 161.54484153742413
    document_mean_weighted_by_documents: 694.0769059102124
  bm25:
    ndcg_at_10_query_weighted: 0.6569951786918409
    hit_at_10_query_weighted: 0.7983799393122051
    ndcg_at_10_unweighted_task_mean: 0.6815294117647059
    hit_at_10_unweighted_task_mean: 0.8184764705882352
    source: dataset_bm25_column
    easiest_task_by_ndcg_at_10: treccovid_fa
    hardest_task_by_ndcg_at_10: argu_ana_fa
  tasks:
    - name: argu_ana_fa
      path: docs/benchmark_tasks/NanoFaMTEB-v2/argu_ana_fa.md
      retrieval_shape: argument_to_paired_counterargument
      queries: 199
      documents: 8669
      positive_qrels: 199
      bm25_ndcg_at_10: 0.286
      bm25_hit_at_10: 0.6432
    - name: fever_fa
      path: docs/benchmark_tasks/NanoFaMTEB-v2/fever_fa.md
      retrieval_shape: claim_to_fact_verification_evidence
      queries: 200
      documents: 10000
      positive_qrels: 229
      bm25_ndcg_at_10: 0.824
      bm25_hit_at_10: 0.9
    - name: fi_qa2018_fa
      path: docs/benchmark_tasks/NanoFaMTEB-v2/fi_qa2018_fa.md
      retrieval_shape: finance_question_to_answer_passage
      queries: 200
      documents: 10000
      positive_qrels: 534
      bm25_ndcg_at_10: 0.3888
      bm25_hit_at_10: 0.53
    - name: hotpot_qa_fa
      path: docs/benchmark_tasks/NanoFaMTEB-v2/hotpot_qa_fa.md
      retrieval_shape: multi_hop_question_to_evidence_passages
      queries: 200
      documents: 10000
      positive_qrels: 400
      bm25_ndcg_at_10: 0.9102
      bm25_hit_at_10: 0.965
    - name: miracl_fa
      path: docs/benchmark_tasks/NanoFaMTEB-v2/miracl_fa.md
      retrieval_shape: persian_miracl_query_to_wikipedia_passage
      queries: 200
      documents: 10000
      positive_qrels: 427
      bm25_ndcg_at_10: 0.5509
      bm25_hit_at_10: 0.8
    - name: msmarco_fa
      path: docs/benchmark_tasks/NanoFaMTEB-v2/msmarco_fa.md
      retrieval_shape: web_query_to_passage_answer
      queries: 43
      documents: 8766
      positive_qrels: 2826
      bm25_ndcg_at_10: 0.8161
      bm25_hit_at_10: 0.9535
    - name: neu_clir2023_fas
      path: docs/benchmark_tasks/NanoFaMTEB-v2/neu_clir2023_fas.md
      retrieval_shape: information_need_to_news_web_documents
      queries: 74
      documents: 10000
      positive_qrels: 3669
      bm25_ndcg_at_10: 0.7761
      bm25_hit_at_10: 0.9324
    - name: nq_fa
      path: docs/benchmark_tasks/NanoFaMTEB-v2/nq_fa.md
      retrieval_shape: natural_question_to_evidence_passage
      queries: 200
      documents: 10000
      positive_qrels: 251
      bm25_ndcg_at_10: 0.4683
      bm25_hit_at_10: 0.7
    - name: persian_web_document
      path: docs/benchmark_tasks/NanoFaMTEB-v2/persian_web_document.md
      retrieval_shape: short_web_query_to_web_document_snippet
      queries: 200
      documents: 10000
      positive_qrels: 2186
      bm25_ndcg_at_10: 0.821
      bm25_hit_at_10: 0.95
    - name: quora_fa
      path: docs/benchmark_tasks/NanoFaMTEB-v2/quora_fa.md
      retrieval_shape: question_to_duplicate_question
      queries: 200
      documents: 10000
      positive_qrels: 570
      bm25_ndcg_at_10: 0.8832
      bm25_hit_at_10: 0.955
    - name: sci_fact_fa
      path: docs/benchmark_tasks/NanoFaMTEB-v2/sci_fact_fa.md
      retrieval_shape: scientific_claim_to_evidence_abstract
      queries: 200
      documents: 5183
      positive_qrels: 225
      bm25_ndcg_at_10: 0.6374
      bm25_hit_at_10: 0.79
    - name: scidocs_fa
      path: docs/benchmark_tasks/NanoFaMTEB-v2/scidocs_fa.md
      retrieval_shape: paper_title_to_related_scientific_document
      queries: 200
      documents: 10000
      positive_qrels: 986
      bm25_ndcg_at_10: 0.3664
      bm25_hit_at_10: 0.565
    - name: syn_per_chatbot_ragfaq
      path: docs/benchmark_tasks/NanoFaMTEB-v2/syn_per_chatbot_ragfaq.md
      retrieval_shape: multi_turn_chatbot_dialogue_to_faq_entry
      queries: 200
      documents: 8696
      positive_qrels: 200
      bm25_ndcg_at_10: 0.2882
      bm25_hit_at_10: 0.415
    - name: syn_per_qa
      path: docs/benchmark_tasks/NanoFaMTEB-v2/syn_per_qa.md
      retrieval_shape: synthetic_persian_question_to_answer
      queries: 200
      documents: 10000
      positive_qrels: 200
      bm25_ndcg_at_10: 0.8609
      bm25_hit_at_10: 0.94
    - name: treccovid_fa
      path: docs/benchmark_tasks/NanoFaMTEB-v2/treccovid_fa.md
      retrieval_shape: covid19_topic_to_biomedical_abstract
      queries: 50
      documents: 10000
      positive_qrels: 4623
      bm25_ndcg_at_10: 0.949
      bm25_hit_at_10: 0.98
    - name: web_faq_fas
      path: docs/benchmark_tasks/NanoFaMTEB-v2/web_faq_fas.md
      retrieval_shape: faq_question_to_answer_passage
      queries: 200
      documents: 10000
      positive_qrels: 200
      bm25_ndcg_at_10: 0.868
      bm25_hit_at_10: 0.935
    - name: wikipedia_multilingual_fa
      path: docs/benchmark_tasks/NanoFaMTEB-v2/wikipedia_multilingual_fa.md
      retrieval_shape: wikipedia_style_question_to_answer_passage
      queries: 200
      documents: 10000
      positive_qrels: 200
      bm25_ndcg_at_10: 0.8915
      bm25_hit_at_10: 0.96
  learning:
    leakage_note: exclude NanoFaMTEB-v2 evaluation queries, qrels, positive documents, and upstream source rows used in the Nano splits; audit public FaMTEB and MCINext source splits before using them for training
    useful_training_data:
      - Persian web search, FAQ, Wikipedia QA, and mMARCO-style query-passage retrieval data
      - Persian MIRACL, Natural Questions, FEVER, HotpotQA, and hard-negative evidence retrieval data
      - Persian or translated finance, scientific, biomedical, and news retrieval data
      - stance-aware Persian argument-pair and duplicate-question retrieval data
      - Persian chatbot RAG, conversation-to-FAQ, and query-rewriting data
    synthetic_data:
      document_generation: Persian counterarguments, evidence passages, answer passages, web snippets, scientific abstracts, biomedical abstracts, news articles, FAQ answers, and chatbot knowledge-base entries
      question_generation: Persian claims, web queries, information needs, scientific titles, FAQ questions, multi-turn dialogues, and domain-specific QA prompts grounded in selected documents
      answerability: each positive must satisfy the task relation, not only share Persian surface terms with the query
    multi_positive_training: preserve many-positive qrel structure for TREC-COVID, NeuCLIR, MS MARCO, Persian web retrieval, SCIDOCS, Quora, and MIRACL-style tasks
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoFaMTEB-v2
    source_urls:
      - label: FaMTEB arXiv
        url: https://arxiv.org/abs/2502.11571
      - label: MTEB arXiv
        url: https://arxiv.org/abs/2210.07316
      - label: MIRACL project
        url: http://miracl.ai/
      - label: NeuCLIR project
        url: https://neuclir.github.io/
      - label: mteb/WebFAQRetrieval
        url: https://huggingface.co/datasets/mteb/WebFAQRetrieval
      - label: MCINext Hugging Face organization
        url: https://huggingface.co/MCINext
    source_notes: []
  references:
    - title: "FaMTEB: Massive Text Embedding Benchmark in Persian Language"
      url: https://arxiv.org/abs/2502.11571
      year: 2025
      is_paper: true
      source_confidence: definitive_paper_link
    - title: "MTEB: Massive Text Embedding Benchmark"
      url: https://arxiv.org/abs/2210.07316
      year: 2023
      is_paper: true
      source_confidence: definitive_paper_link
    - title: MIRACL
      url: http://miracl.ai/
      year: 2022
      is_paper: false
      source_confidence: probably_correct
    - title: NeuCLIR
      url: https://neuclir.github.io/
      year: 2023
      is_paper: false
      source_confidence: probably_correct
    - title: mteb/WebFAQRetrieval
      url: https://huggingface.co/datasets/mteb/WebFAQRetrieval
      year: 2024
      is_paper: false
      source_confidence: probably_correct
```
