# NanoMLDR / ko

## Overview

`ko` is the Korean split of NanoMLDR. It evaluates retrieval of long Korean
articles from Korean paragraph-grounded questions.

## Details

### What the Original Data Measures

[M3-Embedding](https://arxiv.org/abs/2402.03216) uses MLDR as a multilingual
long-document retrieval benchmark for evaluating models on document-scale
inputs. The [MLDR dataset card](https://huggingface.co/datasets/Shitao/MLDR)
lists Korean as Wikipedia-sourced and explains that questions are generated
from sampled paragraphs while the full article is the retrieval target.

### Observed Data Profile

The Nano split has 177 queries, 3,087 documents, and 177 positive qrels. Each
query has one positive. Queries average 55.27 characters and documents average
5,915.24 characters. Examples include superconductivity, fictional characters,
fantasy novels, Netherlands history, and apartment history.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.7010 and hit@10 = 0.7740. It ranks 111 positives first. Korean lexical
matching is often effective for article titles and proper nouns, but short
queries and broad article topics still leave many positives outside the top 10.

### Training Data That May Help

Useful training data includes Korean Wikipedia question-article retrieval,
Korean long-document QA, multilingual MLDR training data, and hard negatives
from articles sharing names, genres, or technical terminology.

### Synthetic Data Guidance

Synthetic data should generate Korean questions from a paragraph inside a long
article. Hard negatives should be related Korean articles that share entities or
topic labels without answering the question.

## Example Data

| Query | Positive document |
| --- | --- |
| 자신의 마법 능력에 대해 인식하지 못하는 이유는 무엇인가요? (33 chars) | 테일즈위버(Talesweaver)는 넥슨과 소프트맥스가 소설 룬의 아이들을 원작으로 공동개발한 엠엠오알피지(MMORPG)다. 2003년 6월부터 정식 서비스를 개시한 이후 꾸준히 사랑받고 있다. 개요 원작은 전민희의 룬의 아이들로, 이것에서 비롯되었다. 시스템 일본에서는 2004년 9월부터 정식 서비스 중이다. 중화인민공화국에서는 2004년 5월에 처음 정식 서비스를 시작했다. 캐릭터 주인공(테일즈위 ... [truncated 225 chars](12131 chars) |
| 왕조 시대에 존재한 김숙검과 김희삼은 어떤 역할을 했으며, 그들의 기여는 어떤 영향을 미쳤을까요? (54 chars) | 의성 김씨(義城 金氏)는 경상북도 의성군을 본관으로 하는 한국의 성씨이다. 의성의 고호가 문소인 관계로 혹칭 문소 김씨(聞韶 金氏)라고도 한다. 역사 초기 족보인 1530년 계축보 부터 1801년 신유보 까지 3백여 년간에 걸쳐 고려 말 태자첨사를 지낸 김용비(金龍庇)를 시조로 하고, 관향을 의성으로 하여 세계를 이어왔다. 상계는 실전되어 전하지 않는다고 하였다. 시조 김용비(金龍庇)의 생몰 및 행적 ... [truncated 225 chars](8969 chars) |
| 의 안전성을 평가하기 위해 추가적인 임상시험이 필요하다. 이러한 비용과 시간 소요를 고려할 때, 신약 개발 프로세스에서 임상시험 단계를 최적화하거나 대체할 수 있는 방법이 있는지 궁금합니다? (106 chars) | 임상시험(臨床試驗, ) 또는 임상연구는 사람을 직접 대상으로, 사람에게서 추출(또는 적출)된 검체나 사람에 대한 정보를 이용하여 이루어지는 모든 시험 또는 연구이자 개발중인 신약의 사용 허가 전에 그 약의 효과와 안전성을 증명하는 과정이다. 참가자에 대한 이러한 전향적 생의학이나 행동 치료는 새로운 치료법 (신규 백신, 약물, 식이 선택, 식이 보충제 및 의료 기기 등) 및 추가 연구와 비교가 필요한 ... [truncated 225 chars](13280 chars) |
| 노보시비르스크에서 겨울과 여름에는 어떻게 해가 떠 있는 시간이 변하는가? (40 chars) | 노보시비르스크(, )는 인구 수 기준으로 러시아 제3의 도시이며 시베리아 제1의 도시다. 시베리아 연방관구, 노보시비르스크주, 노보시비르스크구의 행정수도(주도)이며 서시베리아경제구역의 중심지이다. 노보시비르스크는 의의가 있는 도시로서, 도시구의 지위를 가진 시市 구성체 노보시비르스크시를 구성하는데, 이는 러시아에서 가장 인구가 많은 시 구성체이다. 또한 노보시비르스크에는 서시베리아철도 관리국, 시베리 ... [truncated 225 chars](12930 chars) |
| 이 작품에서 주인공들은 어떤 역할을 맡고 있나요? (27 chars) | 최원형(1968년 1월 3일 ~ )은 한국의 남자 성우다. 1993년 문화방송 11기 공채 성우로 데뷔했다. 출연 작품 굵은 글씨는 메인 캐릭터. TV 애니메이션 3x3 아이즈 : 성마전설 ova - 나파르바 DNA^2 (애니맥스) - 모모나리 준타 S.A 스페셜 에이 (애니맥스) - 타키시마 케이 가이스터즈 (MBC) - 딘 호너스 고미의 만화 호기심 천국 (SBS) - 고미 그 남자! 그 여자! ... [truncated 225 chars](9813 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMLDR |
| Backing dataset | NanoMLDR |
| Task / split | ko |
| Hugging Face dataset | [hakari-bench/NanoMLDR](https://huggingface.co/datasets/hakari-bench/NanoMLDR) |
| Language | ko |
| Category | natural_language |
| Queries | 177 |
| Documents | 3087 |
| Positive qrels | 177 |
| BM25 nDCG@10 | 0.7010 |
| BM25 hit@10 | 0.7740 |
| Query length avg chars | 55.27 |
| Document length avg chars | 5915.24 |

### Public Sources

- [M3-Embedding](https://arxiv.org/abs/2402.03216); 2024; Jianlv Chen et al.
- [MLDR dataset card](https://huggingface.co/datasets/Shitao/MLDR).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMLDR](https://huggingface.co/datasets/hakari-bench/NanoMLDR)
- Source dataset: [Shitao/MLDR](https://huggingface.co/datasets/Shitao/MLDR)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| M3-Embedding: Multi-Linguality, Multi-Functionality, Multi-Granularity Text Embeddings Through Self-Knowledge Distillation | 2024 | benchmark paper | https://arxiv.org/abs/2402.03216 |
| MLDR: Multilingual Long-Document Retrieval dataset | 2024 | dataset card | https://huggingface.co/datasets/Shitao/MLDR |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMLDR
  backing_dataset: NanoMLDR
  dataset_id: hakari-bench/NanoMLDR
  task_name: ko
  split_name: ko
  language: ko
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMLDR/ko.md
  source_research:
    primary_source_type: benchmark_paper_and_dataset_card
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 177
    documents: 3087
    positive_qrels: 177
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 55.271186440677965
    document_mean: 5915.235827664399
  bm25:
    ndcg_at_10: 0.7010081474034279
    hit_at_10: 0.7740112994350282
    source: dataset_bm25_column
  learning:
    original_train_split: available
    evaluation_split_origin: MLDR Korean split
    train_eval_overlap_audit: not_audited
    leakage_note: exclude NanoMLDR ko queries, qrels, and positive documents
    useful_training_data:
      - Korean long-document QA retrieval pairs
      - Korean Wikipedia article retrieval
      - multilingual MLDR training data outside this Nano split
      - same-entity Korean hard negatives
    synthetic_data:
      document_generation: long Korean encyclopedic articles
      question_generation: paragraph-grounded Korean questions
      answerability: positives should be full articles containing the answer-bearing paragraph
    multi_positive_training: single_positive
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMLDR
    source_urls:
      - label: M3-Embedding arXiv
        url: https://arxiv.org/abs/2402.03216
      - label: Shitao/MLDR
        url: https://huggingface.co/datasets/Shitao/MLDR
    source_notes: []
  references:
    - title: "M3-Embedding: Multi-Linguality, Multi-Functionality, Multi-Granularity Text Embeddings Through Self-Knowledge Distillation"
      url: https://arxiv.org/abs/2402.03216
      year: 2024
      is_paper: true
      source_confidence: definitive_paper_link
```
