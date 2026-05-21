# NanoMIRACL / ar

## Overview

The MIRACL paper frames Arabic as one of its monolingual ad hoc retrieval
settings: native-language Arabic questions are judged against Arabic Wikipedia
passages, not translated evidence. This Nano split keeps that
question-to-passage setup in a compact single-positive form. The observed
queries are short Arabic fact questions, often beginning with forms such as
`ما`, `من`, `متى`, or `أين`, so the task emphasizes precise entity, date,
location, and definition matching within Arabic encyclopedia prose.

## Details

### What the Original Data Measures

[Making a MIRACL: Multilingual Information Retrieval Across a Continuum of
Languages](https://arxiv.org/abs/2210.09984) describes MIRACL as monolingual
ad hoc retrieval across 18 languages. The paper states that queries and corpora
are in the same language, so Arabic queries retrieve Arabic Wikipedia passages
rather than translated evidence. It also reports more than 700k manual relevance
judgments for about 77k queries, with assessments performed by native speakers.

The paper matters for this Arabic task because MIRACL was built directly for
retrieval. The corpora come from Wikipedia dumps segmented into passages, and
the retrieval unit is a passage even though the source is an encyclopedia
article. For the languages inherited from Mr. TyDi, including Arabic, MIRACL
keeps the broad split alignment but adds denser passage relevance judgments and
addresses inconsistent passage segmentation from the earlier pipeline.

MIRACL's annotation design also shapes how the task should be read. The authors
say annotators first generated well-formed questions from Wikipedia prompts and
then judged candidate passages retrieved by an ensemble of BM25, mDPR, and
mColBERT. For Arabic, the original paper reports development-set BM25 nDCG@10 of
0.481 and hybrid BM25+mDPR nDCG@10 of 0.673. That gap suggests that exact Arabic
lexical matching is useful on the full benchmark, but neural or hybrid models
can improve evidence selection.

### Observed Data Profile

The sampled Nano task has 200 queries, 1,854 documents, and 200 positive qrel
rows. Every query has exactly one positive passage. Queries average 30.14
characters and are mostly compact Arabic fact questions. The most common first
tokens are `ما`, `من`, `متى`, `أين`, `كم`, and `هل`, which matches the visible
question styles: definitions, people, dates, locations, counts, and yes/no
properties. Documents average 680.47 characters and are Arabic Wikipedia
passages that usually begin with an article title followed by explanatory text.

The examples show a broad encyclopedia mix: public figures, geography, sports
competitions, historical events, companies, religious history, medical topics,
and abstract definitions. Many positives contain the answer in a single
sentence, but the passage often includes additional context around the entity or
topic. A retriever therefore needs to connect a short Arabic information need to
the right article and passage, not merely retrieve any passage about a related
entity family.

Arabic-specific surface form issues are visible in the sample and BM25 ranking.
Queries vary between spellings such as `أين` and `اين`, and between fused forms
such as `ماهي` and separated forms such as `ما هي`. Named entities can be
transliterated, inflected, or embedded in longer article titles. These details
make sparse matching sensitive to normalization, tokenization, hamza variants,
and whether a short function word is attached to the following token.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.5445
and hit@10 = 0.8100 on this Nano split. BM25 places 60 of 200 positives at rank
1 and 162 of 200 positives in the top 10. This is a useful baseline because many
queries contain distinctive Arabic names or titles, such as organizations,
historical figures, cities, and competitions.

The misses show several concrete sparse-retrieval weaknesses. For "متى هاجر
الرسول محمد من مكة إلى المدينة ؟", BM25 retrieves passages mentioning the
Prophet, Mecca, Medina, and campaigns, but the positive passage about the Hijra
is only rank 11. For "ماهي مساحة بلجيكا؟" and "ماهي مساحة مصر؟", top candidates
include the Indian place name `ماهي`, showing how the fused question form can
distract lexical matching from the intended area question. For "اين توجد مدينة
لينتس؟", BM25 ranks a French commune named `أين` first because the query uses
the location word `اين`, while the positive Linz passage is much lower. These
are not topic-absence failures; they are normalization, entity disambiguation,
and relation-selection failures.

Because every query has one positive passage in this Nano split, hit@10 is easy
to interpret: BM25 fails to surface the labeled answer passage for 38 queries.
nDCG@10 still matters because many correct positives appear below rank 1. A
strong model should retain BM25's rare-term anchoring while improving cases
where the Arabic question word, spelling variant, or entity neighbor changes the
ranking.

### Training Data That May Help

The first existing data to inspect is non-overlapping Arabic MIRACL training
data. Since this Nano task is MIRACL-derived, upstream development or test
queries, qrels, and positive passages likely to overlap with the benchmark
should preferably be excluded from training. Other useful sources include Arabic
Wikipedia question-to-passage retrieval pairs, Arabic QA evidence retrieval
datasets, and native Arabic entity-centric supervision for dates, places,
definitions, counts, and yes/no facts.

Training data should emphasize passage evidence rather than question
paraphrase. The model needs to learn that a short question such as "where was X
born" or "when did Y begin" should retrieve an Arabic encyclopedia passage that
contains the answer-bearing evidence, even when the passage title is broader or
the wording uses a different spelling.

### Synthetic Data Guidance

For document-to-question generation, use non-evaluation Arabic Wikipedia-style
passages and generate short Arabic questions grounded in one selected passage.
The questions should cover `ما`, `من`, `متى`, `أين`, `كم`, and `هل` intents,
with realistic spelling variation, attached and separated question forms, named
entities, dates, locations, and definitions. The generated positives should be
evidence passages, not direct answer strings.

For joint document-and-question generation, create Arabic encyclopedia-style
passages with article titles, entity aliases, dates, places, and factual
sentences, then create Arabic questions answerable from those passages. Do not
seed generation with Nano evaluation queries or positive passages. Synthetic
data is most useful when it teaches Arabic normalization and entity-specific
evidence retrieval while preserving exact answer grounding.

## Example Data

| Query | Positive document |
| --- | --- |
| ما هي اول دار للنشر في لبنان ؟ (30 chars) | لبنان ويشتهر لبنان بدور النشر التي تصدر الكتب المتنوعة العربية منها والمترجمة من لغات أخرى. وأول دار للنشر في لبنان أنشئت بهدف النشر والتوزيع والتأليف هي دار العلم للملايين في سنة 1945، وكان معظم المشتغلين في إنتاج الكتاب قبل ... [truncated 225 chars](721 chars) |
| ما أول أبحاث ماري سكوودوفسكا كوري؟ (34 chars) | ماري كوري خلال الحرب العالمية الأولى، أسست أول مراكز إشعاعية عسكرية. ورغم حصولها على الجنسية الفرنسية، لم تفقد ماري سكوودوفسكا كوري إحساسها بهويتها البولندية، فقد علمت بناتها اللغة البولندية، واصطحبتهم في زيارات لبولندا. كما ... [truncated 225 chars](548 chars) |
| كم عدد أعضاء مجلس الأمة الكويتي؟ (32 chars) | سياسة الكويت لدى مجلس الأمة 65 عضو، 50 عضو منهم منتخبين لفترة تستمر لأربعة سنوات، ويكون الوزراء في الحكومة أعضاء في البرلمان، وبالرغم من أن الأمير لديه الأمر الأخير في جميع قضايا الدولة، إلا أن مجلس الأمة لديه سلطة كبيرة في ص ... [truncated 225 chars](488 chars) |
| من مؤسس الإمبراطورية الهابسبورغية ؟ (35 chars) | هابسبورغ الفترة من القرن الحادي عشر إلى القرن الثاني عشر فترة انحدار للإمبراطورية والملكية الألمانية إلى أدنى مستوياتها حيث سقطت أسرة هوهنشتاوفن وسادت الفوضى والمنازعات وادعى ريتشارد كورونولى أحقيته في الحكم، لكن بعد وفاته تم ... [truncated 225 chars](1026 chars) |
| متى بدأت شركة امازون بتقديم خدمة الحوسبة السحابية ؟ (51 chars) | حوسبة سحابية هذا ولعب موقع أمازون الإلكتروني دوراً جوهرياً في تنمية الحوسبة السحابية من خلال تحديث مراكز البيانات بعد فقاعة الدوت كوم، والتي، مثل غالبية شبكات الحاسوب، كانت تستخدم قدراً ضئيلاً يُقَدَّرُ بنحو 10% من إمكانياتها ... [truncated 225 chars](663 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMIRACL |
| Backing dataset | NanoMIRACL |
| Task / split | ar |
| Hugging Face dataset | [hakari-bench/NanoMIRACL](https://huggingface.co/datasets/hakari-bench/NanoMIRACL) |
| Language | ar |
| Category | natural_language |
| Queries | 200 |
| Documents | 1,854 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.5445 |
| BM25 hit@10 | 0.8100 |
| Query length avg chars | 30.14 |
| Document length avg chars | 680.47 |

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
  task_name: ar
  split_name: ar
  language: ar
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMIRACL/ar.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 200
    documents: 1854
    positive_qrels: 200
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 30.14
    document_mean: 680.473571
  bm25:
    ndcg_at_10: 0.5444900265
    hit_at_10: 0.81
    source: dataset_bm25_column
  learning:
    original_train_split: available
    evaluation_split_origin: unknown
    train_eval_overlap_audit: not_audited
    leakage_note: prefer excluding upstream development/test data or other MIRACL-derived data likely to overlap with the NanoMIRACL evaluation questions and passages
    useful_training_data:
      - non-overlapping MIRACL Arabic train split data
      - native Arabic Wikipedia question-to-passage retrieval pairs
      - Arabic entity-centric QA evidence retrieval pairs
    synthetic_data:
      document_generation: Arabic Wikipedia-style passages with titles, aliases, dates, names, places, definitions, and factual evidence
      question_generation: short native Arabic fact questions using varied question words, spelling variants, and attached or separated forms
      answerability: questions should be grounded in explicit facts or relations in the generated or selected passage
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
    - title: 'Making a MIRACL: Multilingual Information Retrieval Across a Continuum of Languages'
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
```
