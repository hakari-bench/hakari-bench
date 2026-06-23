# NanoMTEB-Korean / ko_strategy_qa

## Overview

`ko_strategy_qa` is a Korean StrategyQA-style evidence retrieval task. Queries
are short Korean implicit-reasoning questions, and documents are Korean evidence
passages. The Nano split contains 200 queries, 9,251 documents, and 378
positive qrels. It is multi-positive: each query has 1.89 positives on average,
the median is two, and 61.5% of queries have more than one positive. Queries
average only 22.43 characters, while documents average 321.26 characters. The
task tests whether a retriever can find evidence needed for hidden reasoning
steps, not just match surface wording in the question.

## Details

### What the Original Data Measures

[Did Aristotle Use a Laptop? A Question Answering Benchmark with Implicit Reasoning Strategies](https://arxiv.org/abs/2101.02235)
introduced StrategyQA, a Boolean question-answering benchmark where the
reasoning strategy is implicit in the question. The paper emphasizes that
questions often require decomposition into evidence-seeking steps and that
supporting evidence may have limited lexical overlap with the question.

[taeminlee/Ko-StrategyQA](https://huggingface.co/datasets/taeminlee/Ko-StrategyQA)
adapts this setting into Korean and BEIR/MTEB-style retrieval. The Nano task
evaluates evidence retrieval rather than final yes/no answering: a model must
retrieve the passages that supply the facts needed by the hidden reasoning
chain.

### Observed Data Profile

The split has 200 Korean queries, 9,251 documents, and 378 positive judgments.
Many queries have multiple evidence passages, with a maximum of five positives.
Queries are short and sometimes under-specified because the reasoning step is
implicit. Documents are short evidence passages, often with title prefixes and
entity-centered factual content.

Examples include evidence about Snowdon's annual precipitation, Joan Crawford's
career, Elton John's knighthood, halal dietary restrictions, and the inventor of
the polio vaccine. The relevant passage may not answer the query directly; it
may provide one intermediate fact needed for reasoning.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.4740, hit@10 of 0.7550, and recall@100 of 0.7804.
This is a solid but limited lexical baseline. It works when the question
contains an entity or term that appears in the evidence passage, but it loses
ground when the implicit reasoning step changes the vocabulary needed for
retrieval.

The result matches the core StrategyQA challenge. A query can require evidence
about a related entity, property, date, or definition that is not directly named
in the question. Lexical frequency alone is therefore incomplete.

### Dense Evaluation Profile

Dense retrieval is strongest for top-10 ranking, with nDCG@10 of 0.7084,
hit@10 of 0.8350, and recall@100 of 0.8413. The dense model better connects
short implicit questions to semantically relevant evidence passages. It can
retrieve evidence even when the query and passage share fewer terms than a
direct QA task would.

Dense retrieval still leaves room for improvement. Multi-hop evidence can
require several distinct passages, and a dense model may retrieve only one
obvious fact while missing another supporting step. Better decomposition-aware
retrieval should improve this split.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` profile reaches nDCG@10 of 0.6476, hit@10 of 0.8400,
and recall@100 of 0.8704. It has the best recall@100 and slightly higher
hit@10 than dense retrieval, while dense keeps the best nDCG@10. Candidate
lists contain 100 to 101 rows, with 14 safeguard-positive rows.

This is a useful hybrid pattern: dense retrieval provides strong semantic
ranking, while hybrid search exposes more supporting evidence passages for
reranking. Since many queries have multiple positives, broader candidate
coverage is especially valuable.

### Metric Interpretation for Model Researchers

`ko_strategy_qa` is dense-favorable for early ranking and hybrid-favorable for
evidence coverage. BM25 is useful but cannot fully handle implicit reasoning.
nDCG@10 measures whether useful evidence appears early, hit@10 measures whether
at least one supporting passage is found, and recall@100 measures how much of
the multi-positive evidence set is available to a downstream reasoner.

Because the task has multiple positives for most queries, a model should not be
evaluated as if there is only one correct passage. Retrieving several evidence
pieces can matter for final reasoning even when one positive is already present.

### Query and Relevance Type Tendencies

Queries are short Korean implicit-reasoning questions. Positive documents are
evidence passages about entities, definitions, dates, properties, or facts that
support the hidden decomposition. The evidence may be indirect: the passage can
provide a necessary fact rather than a final answer.

Relevance is reasoning-step evidence. A passage with shared topic words can be
irrelevant if it does not support the needed inference, while a passage with
limited overlap can be positive if it supplies the missing fact.

### Representative Failure Modes

BM25 fails when the evidence vocabulary differs from the question. Dense
retrieval can fail by selecting a semantically related passage that does not
support the specific reasoning step. Hybrid retrieval can improve coverage but
still over-rank obvious entity matches while missing less direct evidence.

Multi-positive queries add another risk: a retriever may find one evidence
passage and miss the rest, limiting a downstream reasoning model.

### Training Data That May Help

Useful training data includes non-overlapping Ko-StrategyQA train evidence
pairs, StrategyQA evidence retrieval and decomposition-step pairs, Korean
multi-hop QA evidence retrieval data, and hard negatives sharing entities but
supporting different reasoning steps. Training should exclude Ko-StrategyQA dev
examples, Nano queries, qrels, and positive evidence passages.

Synthetic data should create short Korean evidence passages about entities,
dates, definitions, and properties, then generate implicit reasoning questions
that require one or more evidence passages. Multi-positive objectives are
appropriate because the benchmark often expects multiple supporting facts.

### Model Improvement Notes

Models should learn decomposition-aware retrieval. Dense encoders need to map a
short question to the evidence implied by its hidden reasoning path. Rerankers
should judge whether a passage supports a reasoning step rather than merely
sharing an entity or topic with the query.

## Example Data

| Query | Positive document |
| --- | --- |
| 스노우다운의 연간 강수량은 얼마나 되나요? [23 chars] | Snowdon "스노우던"이라는 영어 이름은 "눈 언덕"을 의미하는 고대 영어 스노 던에서 유래되었으며, 스노우던은 종종 눈으로 덮여 있기 때문입니다. 겨울철 스노우던에 내리는 눈의 양은 매우 다양하지만, 2004년에는 1994년에 비해 55%나 적었습니다. 스노든의 경사면은 영국에서 가장 습한 기후 중 하나이며 연평균 200인치(5,100mm) 이상의 강수량을 기록합니다. [211 chars] |
| 조안 크로포드의 텔레비전 배우로서의 경력은 언제 끝났나요? [32 chars] | Joan Crawford 크로포드는 1930년대 중반까지 인기 영화 배우로서 명성을 이어갔습니다. 노 모어 레이디스(1935)는 로버트 몽고메리, 당시 남편 프랜쇼 톤과 공동 주연을 맡아 큰 성공을 거두었습니다. 크로포드는 오랫동안 MGM의 수장 루이스 B. 메이어에게 더 극적인 역할에 캐스팅해 달라고 간청했고, 메이어는 주저했지만 W.S. 반 다이크 감독의 세련된 코미디 드라마 <나는 내 인생을 산다>(1935)에 그녀를 캐스팅해 평론가들의 호평을 받았죠. [259 chars] |
| 엘튼 존이 기사 작위를 받았나요? [18 chars] | Elton John 존은 그래미상 5회, 브릿 어워드 5회, 아카데미상 2회, 골든 글로브상 2회, 토니상, 디즈니 레전드상, 케네디 센터 아너상 등을 수상했습니다. 2004년 롤링스톤은 로큰롤 시대의 영향력 있는 뮤지션 100인 명단에서 그를 49위로 선정했습니다. 2013년 빌보드는 그를 '빌보드 핫 100 톱 올타임 아티스트'에서 가장 성공한 남성 솔로 아티스트로 선정했으며, 비틀즈와 마돈나에 이어 전체 3위를 차지했습니다. 1994년에는 로큰롤 명예의 전당에, 1992년에는 작곡가 명예의 전당에 헌액되었으며 영국 작사, 작곡가 및 작가 아카데미의 펠로우입니다. 1998년 엘리자베스 2세로부터 "음악 및 자선 활동에 대한 공로"로 기사 작위를 받았습니다. 존은 1997년 웨스트민스터 사원에서 열린 다이애나 비의 장례식, 2002년 궁전에서의 파티, 2012년 버킹엄 궁전 밖에서 열린 여왕의 다이아몬드 주빌리 콘서트 등 수많은 왕실 행사에서 공연을 펼쳤습니다. [490 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Did Aristotle Use a Laptop? A Question Answering Benchmark with Implicit Reasoning Strategies | 2021 | Paper | [https://arxiv.org/abs/2101.02235](https://arxiv.org/abs/2101.02235) |
| taeminlee/Ko-StrategyQA | 2025 | Dataset card | [https://huggingface.co/datasets/taeminlee/Ko-StrategyQA](https://huggingface.co/datasets/taeminlee/Ko-StrategyQA) |

### Representative Snippets

| Query | Positive document excerpt |
| --- | --- |
| 스노우다운의 연간 강수량은 얼마나 되나요? | A Korean Snowdon passage describing very wet slopes and annual precipitation. |
| 조안 크로포드의 텔레비전 배우로서의 경력은 언제 끝났나요? | A Joan Crawford passage about her acting career and later roles. |
| 엘튼 존이 기사 작위를 받았나요? | An Elton John passage listing awards, honors, and recognition. |
| 1은 어떤 식단 제한을 부과합니까? | A Haram passage describing prohibited foods and emergency exceptions. |
| 소아마비 백신은 누가 만들었나요? | A polio vaccine passage naming Jonas Salk and collaborators. |
