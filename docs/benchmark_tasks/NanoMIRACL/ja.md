# NanoMIRACL / ja

## Overview

MIRACL frames Japanese as monolingual retrieval: Japanese questions are judged
against Japanese Wikipedia passages, not translated evidence. The Nano split
keeps a compact one-positive version of this passage search problem. Its
queries are especially short, often asking when an organization was founded,
where a person was born, whether an entity has a property, or how many people
were affected by an event, so success depends on using sparse Japanese entity,
date, place, and event cues to find the relevant passage.

## Details

### What the Original Data Measures

[Making a MIRACL: Multilingual Information Retrieval Across a Continuum of
Languages](https://arxiv.org/abs/2210.09984) describes MIRACL as a monolingual
ad hoc retrieval dataset across 18 languages. The query and corpus language are
the same, so Japanese queries retrieve Japanese Wikipedia passages rather than
translated or cross-lingual evidence. The paper states that MIRACL was built to
support retrieval research across a continuum of high-resource and lower-resource
languages, with native-speaker relevance judgments over Wikipedia passages.

The paper is important for interpreting this task because MIRACL was designed as
a retrieval benchmark, not as a reading-comprehension dataset converted into
search. Its corpora are created from Wikipedia dumps, plain text is retained,
images and tables are discarded, and articles are segmented into passages using
natural discourse units. For the languages inherited from Mr. TyDi, including
Japanese, MIRACL reuses the general split structure but adds richer passage
annotations and fixes inconsistent passage segmentation. This makes the task
closer to practical passage retrieval over a full encyclopedia than to finding an
answer inside a preselected article.

MIRACL's annotation workflow also matters. The authors hired native speakers,
asked them to generate well-formed questions from Wikipedia prompts, and then had
them judge retrieved candidate passages. Candidate passages were drawn from an
ensemble of BM25, mDPR, and mColBERT, which means the relevance judgments were
formed against plausible lexical and neural candidates rather than only random
documents. For Japanese, the original paper reports development-set BM25 nDCG@10
of 0.369 and hybrid BM25+mDPR nDCG@10 of 0.576, showing that lexical retrieval is
useful but not sufficient on the full task.

### Observed Data Profile

The sampled Nano task has 200 queries, 1,846 documents, and 200 positive qrel
rows. Every query in this Nano split has exactly one positive passage. Queries
are very short, with an average length of 17.47 characters. They are usually
natural Japanese fact questions such as asking when an organization was founded,
where a person was born, whether an entity has a property, or how many people
were affected by an event. The documents are Japanese Wikipedia passages with an
average length of 297.91 characters, typically beginning with the article title
followed by an explanatory paragraph.

The actual samples are strongly entity-centered. Queries ask about specific
people, organizations, historical events, sports, vehicles, companies, and
places. Many answer passages put the needed answer in a compact factual sentence:
birthplace, foundation year, death date, sport type, or definition. This makes
the task easy to understand but not trivial. A retriever must map a short query
to the correct article and passage, often with only a few lexical anchors.
Japanese tokenization, era/date expressions, katakana names, romanized names, and
article-title variants all affect retrieval quality.

The task differs from duplicate-question or web FAQ retrieval because the
document is not another question; it is an encyclopedia passage. The query asks
for a fact, and the positive is the passage that contains enough context to
answer it. The retrieval unit may include more information than the query asks
for, so a model should treat the relevant passage as evidence-bearing context,
not as a direct paraphrase.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.5956
and hit@10 = 0.9400 on this Nano split. BM25 places 60 of 200 positives at rank
1, and 188 of 200 positives somewhere in the top 10. This is a strong sparse
baseline because the task has many short entity queries and Wikipedia passages
often repeat the exact entity name from the query.

The harder cases show where lexical matching is not enough. For "メジロライアンはいつ
生まれた？", BM25 ranks several other `メジロ` racehorse passages above the correct
`メジロライアン` passage. For "ＮＨＫは有料テレビ局？", it is distracted by passages
about paid television services and NHK-related topics rather than the precise
license-fee evidence. For "皇族用車両は英国にもありますか？", BM25 finds Japanese
royal train and British railway passages but misses the passage that explicitly
answers the cross-country royal-carriage question. These failures are
entity-neighbor and intent-resolution failures: the right topic family is found,
but the exact relation asked by the short query is not ranked high enough.

This means nDCG@10 should be read as a mixture of lexical anchoring and
fine-grained evidence selection. A strong retriever should preserve BM25's
ability to use rare names, dates, and titles while improving cases where the
query's relation is short and implicit.

### Training Data That May Help

The best existing training data is non-overlapping Japanese question-to-passage
retrieval data with Wikipedia-style evidence. MIRACL train data is the first
source to inspect for the Japanese domain, but data likely to overlap with the
benchmark split, such as upstream development or test queries, should preferably
be excluded from training. Other useful data includes Japanese QA retrieval
pairs from encyclopedic corpora, native Japanese entity-centric question/passage
pairs, and retrieval supervision over Japanese Wikipedia passages where the
positive passage explicitly contains the answer.

Generic paraphrase data is less directly useful than evidence retrieval data.
The model needs to learn that a short question like "when was X founded" should
retrieve a passage containing the founding event, not a similar question or a
general article about the same entity. Training should therefore emphasize
question intent, article-title grounding, passage-level evidence, and Japanese
text normalization.

### Synthetic Data Guidance

For document-to-question generation, use non-evaluation Japanese Wikipedia
passages and generate short Japanese questions whose answer is explicitly
grounded in one passage. The generated questions should cover birthplace,
foundation date, definition, role, event casualty count, organization type,
sport rule, and entity-property questions. They should vary surface form:
plain-form questions, `いつ`, `どこ`, `何`, `誰`, `何人`, yes/no questions, and
queries that omit part of the official article title.

For joint document-and-question generation, create Wikipedia-style Japanese
passages with realistic titles, dates, names, locations, and concise factual
sentences, then create short questions answerable from those passages. The
documents should look like encyclopedia text rather than QA answers. Do not seed
generation with Nano evaluation queries or positive passages. Synthetic data is
most useful when it teaches the model to connect compact Japanese information
needs to answer-bearing passages while handling near-entity confusions.

## Example Data

| Query | Positive document |
| --- | --- |
| ノートン・モーターサイクルは自動車の製造をしたことはある？ (29 chars) | ノートン・モーターサイクル ノートンは、1898年にバーミンガムのによって設立された。当初は自転車メーカーであったが1902年1.5馬力のエンジンを積んだオートバイ一号車を製造しオートバイ製造に参入した。その後もフランスやスイスからエンジンを調達してオートバイの製造を続け、1907年にはプジョーから購入した726ccV2サイドバルブエンジンを搭載したオートバイで（新競技方式での）第1回マン島TTレース2気筒クラスを制した。1908年には自社製72 ... [truncated 225 chars](651 chars) |
| チャールズ・ディケンズの出身はどこ (17 chars) | チャールズ・ディケンズ 海軍の会計吏ジョン・ディケンズとエリザベスの長男として、ハンプシャー州のポーツマス郊外のランドポートに生まれた。2歳のときにロンドンに、5歳のときにケント州（現在は独立行政区メドウェイ）の港町チャタムに移る。チャタムでは6年間を過ごし、ディケンズの心の故郷となった。少年期は病弱であり、フィールディング、デフォー、セルバンテスなどを濫読した。 ディケンズの家は中流階級の家庭であったが、父親ジョンは金銭感覚に乏しい人物であり、 ... [truncated 225 chars](636 chars) |
| FIA GT1世界選手権は何の競技？ (18 chars) | FIA GT1世界選手権 FIA GT1世界選手権（エフアイエー ジーティーワンせかいせんしゅけん、FIA GT1 World Championship）は、ステファン・ラテル・オルガニザシオンが主催し、国際自動車連盟（FIA）が管轄する、FIA GTカーによるレースの名称。2010年より開催されていたが2012年にFIA GT世界選手権としては終了した。翌年の2013年からFIA GTシリーズ、2014年からはブランパンスプリントシリーズとして ... [truncated 225 chars](233 chars) |
| ヘンリー2世はいつ死去した？ (14 chars) | ヘンリー2世 (イングランド王) ヘンリー2世（, 1133年3月5日 - 1189年7月6日）は、プランタジネット朝（あるいはアンジュー朝）初代のイングランド王国の国王（在位：1154年 - 1189年）である。 (107 chars) |
| アメリカン・エキスプレスはいつ設立した？ (20 chars) | アメリカン・エキスプレス 1850年に、ウェルズ・ファーゴの創設者でもあるヘンリー・ウェルズとウィリアム・ファーゴ、ジョン・バターフィールドの3人によって、荷馬車により貨物を運ぶ宅配便業者（）として、ニューヨーク州バッファローを本社に運輸業を開始した。事業は好調に推移し、輸送網を全米、および隣国のカナダやメキシコにも広げた。 (163 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMIRACL |
| Backing dataset | NanoMIRACL |
| Task / split | ja |
| Hugging Face dataset | [hakari-bench/NanoMIRACL](https://huggingface.co/datasets/hakari-bench/NanoMIRACL) |
| Language | ja |
| Category | natural_language |
| Queries | 200 |
| Documents | 1,846 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.5956 |
| BM25 hit@10 | 0.9400 |
| Query length avg chars | 17.47 |
| Document length avg chars | 297.91 |

### Public Sources

- [Making a MIRACL: Multilingual Information Retrieval Across a Continuum of Languages](https://arxiv.org/abs/2210.09984); 2022; Xinyu Zhang, Nandan Thakur, Odunayo Ogundepo, Ehsan Kamalloo, David Alfonso-Hermelo, Xiaoguang Li, Qun Liu, Mehdi Rezagholizadeh, Jimmy Lin; DOI: `10.48550/arXiv.2210.09984`.
- [MIRACL: A Multilingual Retrieval Dataset Covering 18 Diverse Languages](https://aclanthology.org/2023.tacl-1.63/); 2023 TACL version; DOI: `10.1162/tacl_a_00595`.
- [MIRACL GitHub repository](https://github.com/project-miracl/miracl).
- [MIRACL corpus dataset card](https://huggingface.co/datasets/miracl/miracl-corpus).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMIRACL](https://huggingface.co/datasets/hakari-bench/NanoMIRACL)
- Source corpus: [miracl/miracl-corpus](https://huggingface.co/datasets/miracl/miracl-corpus)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Making a MIRACL: Multilingual Information Retrieval Across a Continuum of Languages | 2022 | paper | https://arxiv.org/abs/2210.09984 |
| MIRACL: A Multilingual Retrieval Dataset Covering 18 Diverse Languages | 2023 | paper | https://aclanthology.org/2023.tacl-1.63/ |
| MIRACL GitHub repository |  | project repository | https://github.com/project-miracl/miracl |
| miracl/miracl-corpus |  | dataset card | https://huggingface.co/datasets/miracl/miracl-corpus |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMIRACL
  backing_dataset: NanoMIRACL
  dataset_id: hakari-bench/NanoMIRACL
  task_name: ja
  split_name: ja
  language: ja
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMIRACL/ja.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 200
    documents: 1846
    positive_qrels: 200
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 17.47
    document_mean: 297.912784
  bm25:
    ndcg_at_10: 0.5956231823
    hit_at_10: 0.94
    source: dataset_bm25_column
  learning:
    original_train_split: available
    evaluation_split_origin: unknown
    train_eval_overlap_audit: not_audited
    leakage_note: prefer excluding upstream development/test data or other MIRACL-derived data likely to overlap with the NanoMIRACL evaluation questions and passages
    useful_training_data:
      - non-overlapping MIRACL Japanese train split data
      - native Japanese Wikipedia question-to-passage retrieval pairs
      - Japanese entity-centric QA evidence retrieval pairs
    synthetic_data:
      document_generation: Japanese Wikipedia-style passages with titles, dates, names, places, and factual evidence
      question_generation: short native Japanese fact questions answerable from one selected passage
      answerability: questions should be grounded in explicit facts or relations in the generated or selected passage
    multi_positive_training: single_positive_question_document_focus
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMIRACL
    source_urls:
      - label: MIRACL corpus dataset
        url: https://huggingface.co/datasets/miracl/miracl-corpus
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
