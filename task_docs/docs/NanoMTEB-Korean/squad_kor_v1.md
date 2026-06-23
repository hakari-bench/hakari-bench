# NanoMTEB-Korean / squad_kor_v1

## Overview

`squad_kor_v1` is a Korean SQuAD/KorQuAD-style passage retrieval task. Queries
are Korean extractive-QA questions, and documents are Korean Wikipedia passages.
The Nano split contains 200 queries, 960 documents, and 200 positive qrels,
with exactly one positive passage per query. Queries average 35.78 characters,
and documents average 546.20 characters. The task is a compact evidence
retrieval benchmark: the model must find the passage containing the answer span,
often among other passages from the same entity or article.

## Details

### What the Original Data Measures

[KorQuAD1.0: Korean QA Dataset for Machine Reading Comprehension](https://arxiv.org/abs/1909.07005)
introduced a Korean extractive machine-reading dataset built from Korean
Wikipedia. It follows the SQuAD-style setup with human-written questions and
answer spans, while addressing Korean-specific evaluation and language
properties. The retrieval version uses the question as the query and the
answer-bearing passage as the positive document.

This task evaluates Korean QA evidence retrieval rather than final answer
extraction. A model succeeds if it retrieves the passage containing enough local
context for the answer.

### Observed Data Profile

The split has 200 Korean queries, 960 documents, and 200 positive judgments.
Every query has one positive. Questions are direct Korean fact questions.
Documents are Korean Wikipedia passages with title prefixes and medium-length
context. Some passages support multiple questions, which is typical for
reading-comprehension datasets.

Examples include political figures, constitutional amendment discussions,
security-law events, Noah's Ark, Ban Ki-moon, and martial-arts biographical
details. The target passage often contains the answer sentence explicitly.

### BM25 Evaluation Profile

BM25 is the strongest top-ranking profile, with nDCG@10 of 0.9618, hit@10 of
0.9850, and recall@100 of 0.9950. This is one of the most lexically favorable
Korean tasks. Questions often reuse entities, phrases, or answer-bearing terms
from the positive passage, and the corpus is small enough that BM25 has very
high candidate coverage.

The small remaining error set is still useful. BM25 can be distracted by
passages that share the same person, title, or event but do not contain the
specific answer. These errors are fine-grained evidence-selection failures.

### Dense Evaluation Profile

Dense retrieval reaches nDCG@10 of 0.9158, hit@10 of 1.0000, and recall@100 of
1.0000. It has perfect hit and recall coverage but lower nDCG@10 than BM25,
meaning it almost always retrieves the positive passage but sometimes ranks it
slightly lower. Dense semantic matching is therefore robust for candidate
generation, even if exact lexical cues produce the best first-rank ordering.

This is a useful diagnostic for dense models: they should not miss the answer
passage, but they must also preserve Korean entity and phrase specificity to
match BM25 top-ordering.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` profile reaches nDCG@10 of 0.9585, hit@10 of 0.9950,
and recall@100 of 1.0000. It is almost tied with BM25 at top-10 and has full
top-100 coverage. There are no safeguard-positive rows.

Hybrid search works well here because the task benefits from both exact Korean
lexical anchors and semantic answer-passage matching. Still, BM25 remains
slightly stronger in nDCG@10, which reflects how direct the questions are.

### Metric Interpretation for Model Researchers

`squad_kor_v1` is BM25-favorable at top-10, while dense and hybrid methods
provide complete candidate coverage. Since every query has one positive,
nDCG@10 measures the rank of the answer-bearing passage directly, hit@10
measures early availability, and recall@100 measures whether reranking can
recover the passage.

Because scores are near ceiling, this task is most useful for detecting
regressions in Korean QA retrieval or for analyzing fine-grained ranking errors,
not for separating models on broad semantic ability alone.

### Query and Relevance Type Tendencies

Queries are Korean extractive QA questions asking for names, dates, offices,
events, definitions, or reasons. Positive documents are Korean Wikipedia
passages containing the answer span and surrounding context.

Relevance is answer-span evidence. A passage about the same entity is not
sufficient if it does not contain the answer to the specific question.

### Representative Failure Modes

BM25 can be confused by repeated entity names across adjacent passages. Dense
retrieval can rank a semantically related passage above the exact answer
context. Hybrid retrieval largely mitigates candidate loss, but still needs a
reranker to prioritize the precise answer-bearing paragraph when several
passages share a title or entity.

Same-article hard negatives are the most important failure source because they
look topically correct but omit the answer span.

### Training Data That May Help

Useful training data includes non-overlapping KorQuAD or SQuADKor train pairs,
Korean Wikipedia question-to-passage retrieval data, native Korean QA
reformulations, and same-article hard negatives. Training should exclude source
test data, Nano queries, qrels, and positive Korean Wikipedia passages likely to
overlap with the evaluation split.

Synthetic data should generate Korean Wikipedia-style paragraphs with titles,
named entities, dates, offices, locations, and numeric facts, then create Korean
extractive QA questions whose answer span is explicit in the passage.

### Model Improvement Notes

Models should preserve Korean named entities, answer phrases, and article-title
context. Dense encoders can improve top ordering with hard negatives from the
same article. Rerankers should focus on whether the candidate passage contains
the answer span, not only whether it is topically similar.

## Example Data

| Query | Positive document |
| --- | --- |
| '행보가 비서 본연의 역할을 벗어난다', '장관들과 내각이 소외되고 대통령비서실의 권한이 너무 크다'는 의견이 제기된 대표적인 예는? [74 chars] | 임종석 "내각과 장관들이 소외되고 대통령비서실의 권한이 너무 크다", "행보가 비서 본연의 역할을 벗어난다"는 의견이 제기되었다. 대표적인 예가 10차 개헌안 발표이다. 원로 헌법학자인 허영 경희대 석좌교수는 정부의 헌법개정안 준비 과정에 대해 "청와대 비서실이 아닌 국무회의 중심으로 이뤄졌어야 했다"고 지적했다. '국무회의의 심의를 거쳐야 한다'(제89조... [200 / 480 chars] |
| 임종석이 1989년 2월 15일에 지명수배 받은 혐의는 어떤 시위를 주도했다는 것인가? [48 chars] | 임종석 1989년 2월 15일 여의도 농민 폭력 시위를 주도한 혐의(폭력행위등처벌에관한법률위반)으로 지명수배되었다. 1989년 3월 12일 서울지방검찰청 공안부는 임종석의 사전구속영장을 발부받았다. 같은 해 6월 30일 평양축전에 임수경을 대표로 파견하여 국가보안법위반 혐의가 추가되었다. 경찰은 12월 18일~20일 사이 서울 경희대학교에서 임종석이 성명... [200 / 482 chars] |
| 유사지질학자들이 노아의 홍수를 증명하기 위해 성경 이외에 근거라고 주장한 것들은? [45 chars] | 노아의_방주 역사학과 과학의 발달이 더뎠던 고대사회에서는, 성경이 단순한 교리적인 부분 뿐 아니라 역사책으로서의 권위도 높았기에 노아의 방주를 역사적인 존재로서 다루고 있었다. 이는 제칠일안식교에서 비롯된 의사과학의 한 종류인 유사지질학인 홍수지질학과 같은 것에 영향을 주었으며, 과거 신학에서는 이러한 근본주의적 해석을 받아들여 역사와 사회적인 모든 부분에... [200 / 588 chars] |
| 반기문이 유엔 차기 사무총장 선거에 공식적으로 출마 선언을 한 날짜는? [39 chars] | 반기문 2006년 2월 14일에 유엔 차기 사무총장 선거에 공식적으로 출마 선언을 하여 선거운동을 시작했다. 반기문은 대한민국의 외교통상부 장관으로서 유엔 안전보장 이사회의 모든 나라를 순방할 수 있었다. 2006년 10월 14일에 한국인으로서는 최초로 유엔 사무총장에 당선되었다. 그러나 그가 출마를 선언했을 당시엔 그의 당선을 예상한 외신은 그다지 많지... [200 / 551 chars] |
| 중화민국 수립 후 임세영은 자신의 스승이었던 누구를 재조명하는 작업에 착수하였는가? [46 chars] | 린스룽 임세영은 자신의 제자들과 연극을 구경하러 갔다가 우연히 깡패들과 시비가 붙었는데 깡패들이 임세영의 무공이 고강한 것을 알고 물러갔으나 임세영이 홀로 있을 때 몰래 기습을 해왔다. 그러자 임세영은 그들의 무리수가 많아 방어만 하기에는 곤란한 것을 깨닫고 할 수 없이 공격을 하여 깡패들을 쓰러뜨렸으나 결국 광주 전역에 임세영을 체포한다는 수배령이 내려졌... [200 / 460 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| KorQuAD1.0: Korean QA Dataset for Machine Reading Comprehension | 2019 | Paper | [https://arxiv.org/abs/1909.07005](https://arxiv.org/abs/1909.07005) |
| yjoonjang/squad_kor_v1 | 2025 | Dataset card | [https://huggingface.co/datasets/yjoonjang/squad_kor_v1](https://huggingface.co/datasets/yjoonjang/squad_kor_v1) |

### Representative Snippets

| Query | Positive document excerpt |
| --- | --- |
| 대통령비서실 권한이 너무 크다는 의견의 대표적인 예를 묻는 질문. | A Korean passage on Im Jong-seok and criticism around the tenth constitutional amendment announcement. |
| 임종석이 1989년 2월 15일 지명수배된 혐의를 묻는 질문. | A passage describing a farmers' protest, wanted status, and later security-law allegations. |
| 유사지질학자들이 노아의 홍수를 증명하기 위해 주장한 근거를 묻는 질문. | A Noah's Ark passage discussing flood geology and fundamentalist interpretations. |
| 반기문이 유엔 사무총장 선거 출마를 선언한 날짜를 묻는 질문. | A Ban Ki-moon passage giving the February 14, 2006 declaration date. |
| 중화민국 수립 후 임세영이 재조명한 스승을 묻는 질문. | A Lin Shirong passage describing later events and biographical context. |
