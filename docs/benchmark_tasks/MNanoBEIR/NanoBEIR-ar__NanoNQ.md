# MNanoBEIR / NanoBEIR-ar / NanoNQ

## Overview

Natural Questions is an open-domain question answering benchmark built from
real Google search questions and Wikipedia evidence. `NanoBEIR-ar__NanoNQ` is
the Arabic MNanoBEIR version: each query is an Arabic translated natural
question, and the system must retrieve Arabic translated Wikipedia evidence
passages that contain the answer. The task tests everyday question-to-evidence
retrieval.

## Details

### What the Original Data Measures

[Natural Questions: A Benchmark for Question Answering
Research](https://aclanthology.org/Q19-1026/) introduces NQ as a dataset of
real anonymized Google queries. Annotators were shown a question and a
Wikipedia page from the top Google results, then selected a long answer, usually
a paragraph or table region, and a short answer when present. The paper
emphasizes that the questions are naturally occurring information needs rather
than questions written after seeing the answer passage.

[BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information
Retrieval Models](https://arxiv.org/abs/2104.08663) includes NQ as a
question-answering retrieval task over Wikipedia. [MMTEB: Massive Multilingual
Text Embedding Benchmark](https://arxiv.org/abs/2502.13595) provides the
multilingual benchmark context for this Arabic Nano split. The retrieval target
is the answer-bearing evidence passage, not the final answer string.

### Observed Data Profile

The sampled Arabic Nano task has 50 queries, 5,035 documents, and 57 positive
qrel rows. Most queries have one positive, while 7 of 50 have two positives.
The average query length is 40.16 characters, and the average document length
is 447.30 characters.

The inspected queries ask ordinary factual questions: who appoints members of
relevant branches in the United States, when a film was released, the
difference between RON and MON, where cones are located in the eye, and how long
one rotation of Earth takes. Positive documents are translated Wikipedia
passages containing the answer evidence. The task is less multi-hop than
HotpotQA and less paraphrase-like than Quora; it is relation-specific evidence
retrieval.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.2885 and hit@10 = 0.5200. Only 4 of 50 queries have a positive ranked first,
and the median first-positive rank is 8. Every query has a positive within the
top 100.

BM25 can struggle because the query asks for a relation while candidate
passages may share the same topic but not the answer. A question about where
cones are in the eye should retrieve the retina/fovea evidence; a question
about RON and MON needs the octane-rating distinction; a film release question
needs the passage with release dates. Strong retrievers should preserve the
entity and the requested relation, especially when Arabic translation changes
surface overlap.

### Training Data That May Help

Useful training data includes non-overlapping Natural Questions training
examples, Wikipedia question-to-passage retrieval data, KILT-style
question-to-Wikipedia evidence supervision, and Arabic or multilingual
open-domain QA retrieval pairs. Hard negatives should share entities or topics
without answering the relation.

Training should exclude NQ dev/test, BEIR, NanoBEIR, or translated records
likely to overlap with the evaluation questions or evidence passages.

### Synthetic Data Guidance

For document-to-query generation, start from non-evaluation Wikipedia passages
and generate Arabic search-style questions answerable from the passage. Include
`who`, `where`, `when`, `what`, `how long`, definition, release-date,
location, and relation questions.

For joint generation, create Arabic Wikipedia-style paragraphs with entities,
dates, offices, locations, and definitions, then generate questions whose
positive passage contains the answer evidence. Avoid questions answerable from
generic entity mentions alone.

## Example Data

| Query | Positive document |
| --- | --- |
| أين تقام أربع النهائي هذا العام؟ (32 chars) | بطولة كرة السلة للرجال في القسم الأول من الاتحاد الوطني للرياضات الجامعية لعام 2018 كانت بطولة إقصاء فردي تضم 68 فريقًا لتحديد بطل كرة السلة الجامعية للرجال في القسم الأول للاتحاد الوطني للرياضات الجامعية للعام الدراسي 2017–1 ... [truncated 225 chars](349 chars) |
| هل كان فيلم "ليلة مرعبة قبل عيد الميلاد" من إنتاج ديزني في البداية؟ (67 chars) | بدأ فكرة فيلم ليلة مرعبة في عيد الميلاد بقصيدة كتبها تيم بورتون في عام 1982، وهو يعمل كرسام متحرك في استوديوهات والت ديزني للرسوم المتحركة. بعد نجاح فيلم فينسنت في نفس العام، بدأت استوديوهات والت ديزني في التفكير في تطوير فيل ... [truncated 225 chars](556 chars) |
| لماذا يوجد تمثال الملاك الشمالي هناك؟ (37 chars) | وفقًا لـ غورملي، كان لمعنى التمثال الملاك ثلاثة جوانب: أولاً، لإظهار أن تحت موقع بنائه عمل عمال المناجم على مدى قرنين؛ ثانيًا، لاستيعاب الانتقال من عصر صناعي إلى عصر المعلومات؛ وثالثًا، لأن يكون مركزًا لأملنا وخوفنا المتطور. (224 chars) |
| أين تم ذكر تعويض الثلاثي الخامس في الدستور لأول مرة؟ (52 chars) | توجد اتفاقية الثلاثة أخماس في المادة الأولى، القسم الثاني، البند الثالث من دستور الولايات المتحدة الأمريكية، والتي تنص على: (123 chars) |
| من يغني أغنية "أحد يراقبني" مع مايكل جاكسون (43 chars) | "Somebody's Watching Me" هي أغنية للمغني الأمريكي روكويل من ألبومه الأول Somebody's Watching Me (1984). أصدرت الأغنية كأغنية أولية وأغنية رئيسية من الألبوم في 14 يناير 1984 بواسطة موتاون. شارك فيها أعضاء سابقين من فرقة جاكسون ... [truncated 225 chars](300 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-ar |
| Task / split | NanoNQ |
| Hugging Face dataset | [hakari-bench/NanoBEIR-ar](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ar) |
| Language | ar |
| Category | natural_language |
| Queries | 50 |
| Documents | 5,035 |
| Positive qrels | 57 |
| Avg positives / query | 1.14 |
| Positives per query (min / median / max) | 1 / 1.00 / 2 |
| Queries with multiple positives | 7 (14.0%) |
| BM25 nDCG@10 | 0.2885 |
| BM25 hit@10 | 0.5200 |
| Query length avg chars | 40.16 |
| Document length avg chars | 447.30 |

### Public Sources

- [Natural Questions: A Benchmark for Question Answering Research](https://aclanthology.org/Q19-1026/); 2019; Tom Kwiatkowski, Jennimaria Palomaki, Olivia Redfield, Michael Collins, Ankur Parikh, Chris Alberti, Danielle Epstein, Illia Polosukhin, Jacob Devlin, Kenton Lee, Kristina Toutanova, Llion Jones, Matthew Kelcey, Ming-Wei Chang, Andrew M. Dai, Jakob Uszkoreit, Quoc Le, Slav Petrov; DOI: `10.1162/tacl_a_00276`.
- [Google Research Natural Questions publication page](https://research.google/pubs/natural-questions-a-benchmark-for-question-answering-research/).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663); 2021; Nandan Thakur, Nils Reimers, Andreas Rueckle, Abhishek Srivastava, Iryna Gurevych; DOI: `10.48550/arXiv.2104.08663`.
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595); 2025; Kenneth Enevoldsen, Isaac Chung, Imene Kerboua, Marton Kardos, Ashwin Mathur, and others; DOI: `10.48550/arXiv.2502.13595`.
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-ar](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ar)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Natural Questions: A Benchmark for Question Answering Research | 2019 | task paper | https://aclanthology.org/Q19-1026/ |
| Google Research Natural Questions publication page |  | project page | https://research.google/pubs/natural-questions-a-benchmark-for-question-answering-research/ |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | https://arxiv.org/abs/2104.08663 |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | https://arxiv.org/abs/2502.13595 |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | https://huggingface.co/collections/zeta-alpha-ai/nanobeir |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: MNanoBEIR
  backing_dataset: NanoBEIR-ar
  dataset_id: hakari-bench/NanoBEIR-ar
  task_name: NanoNQ
  split_name: NanoNQ
  language: ar
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-ar__NanoNQ.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 50
    documents: 5035
    positive_qrels: 57
  positives_per_query:
    average: 1.14
    min: 1
    median: 1.0
    max: 2
    multi_positive_queries: 7
    multi_positive_query_percent: 14.0
  text_stats_chars:
    query_mean: 40.16
    document_mean: 447.302681
  bm25:
    ndcg_at_10: 0.288525414
    hit_at_10: 0.52
    source: dataset_bm25_column
  learning:
    original_train_split: available
    evaluation_split_origin: MNanoBEIR Arabic NanoBEIR task split from hakari-bench/NanoBEIR-ar
    train_eval_overlap_audit: not_audited
    leakage_note: prefer excluding NQ, BEIR, or NanoBEIR records likely to overlap with these evaluation questions or evidence passages
    useful_training_data:
      - non-overlapping Natural Questions train examples
      - Arabic or multilingual open-domain QA retrieval pairs
      - Wikipedia question-to-passage evidence supervision
      - KILT-style question-to-Wikipedia evidence pairs
    synthetic_data:
      document_generation: Arabic Wikipedia-style passages with factual answer-bearing statements
      question_generation: Arabic natural search-style fact questions answerable from a single passage
      answerability: positives should contain the requested relation and answer evidence, not just the same entity
    multi_positive_training: single_positive_question_document_focus
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoBEIR-ar
    source_urls:
      - label: Natural Questions paper
        url: https://aclanthology.org/Q19-1026/
      - label: Google Research Natural Questions page
        url: https://research.google/pubs/natural-questions-a-benchmark-for-question-answering-research/
      - label: BEIR paper
        url: https://arxiv.org/abs/2104.08663
      - label: MMTEB paper
        url: https://arxiv.org/abs/2502.13595
      - label: Zeta Alpha NanoBEIR collection
        url: https://huggingface.co/collections/zeta-alpha-ai/nanobeir
    source_notes:
      - Arabic task is a multilingual NanoBEIR adaptation of the original English BEIR task
  references:
    - title: "Natural Questions: A Benchmark for Question Answering Research"
      url: https://aclanthology.org/Q19-1026/
      year: 2019
      doi: 10.1162/tacl_a_00276
      is_paper: true
      source_confidence: definitive_paper_link
    - title: Google Research Natural Questions publication page
      url: https://research.google/pubs/natural-questions-a-benchmark-for-question-answering-research/
      year: null
      doi: null
      is_paper: false
      source_confidence: definitive_project_page
    - title: "BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models"
      url: https://arxiv.org/abs/2104.08663
      year: 2021
      doi: 10.48550/arXiv.2104.08663
      is_paper: true
      source_confidence: benchmark_context_paper
    - title: "MMTEB: Massive Multilingual Text Embedding Benchmark"
      url: https://arxiv.org/abs/2502.13595
      year: 2025
      doi: 10.48550/arXiv.2502.13595
      is_paper: true
      source_confidence: benchmark_context_paper
    - title: "NanoBEIR: Smaller BEIR dataset subsets"
      url: https://huggingface.co/collections/zeta-alpha-ai/nanobeir
      year: 2024
      doi: null
      is_paper: false
      source_confidence: dataset_collection
```
