# NanoMLDR / ko

## Overview

`NanoMLDR / ko` is the Korean split of NanoMLDR, a multilingual long-document
retrieval benchmark derived from MLDR. Korean paragraph-grounded questions
retrieve full Korean articles, so the model must connect a local answer-bearing
paragraph to its complete document. The Nano split has 177 queries, 3,087
documents, and 177 positive qrel rows, with exactly one positive document per
query. Current diagnostics show BM25 as the strongest top-rank profile, dense
retrieval as much weaker, and `reranking_hybrid` as improving coverage beyond
BM25 while still below BM25 on nDCG@10.

## Details

### What the Original Data Measures

MLDR was introduced with the M3-Embedding work as a multilingual long-document
retrieval benchmark. The dataset card describes sampling long documents,
selecting a paragraph, and generating a specific question from that paragraph.
The retrieval target is the full article containing the answer-bearing
paragraph.

For Korean, this creates a document-scale retrieval task rather than a short
passage task. The question may focus on a narrow statement, character, event,
place, medical concept, or historical detail, while the indexed candidate is a
long Korean article.

### Observed Data Profile

The Nano split contains 177 queries, 3,087 documents, and 177 positive qrel
rows. Every query has exactly one positive document. Queries average 55.27
characters, while documents average 5,915.24 characters.

Observed examples include questions about fictional characters, Korean family
lineages, clinical trials, Novosibirsk daylight, voice actor roles,
superconductivity, fantasy novels, Netherlands history, and apartment history.
The positive documents are long Korean articles containing the paragraph that
generated the question.

### BM25 Evaluation Profile

The dataset-provided BM25 candidate subset contains 500 candidates per query and
achieves nDCG@10 = 0.6868, hit@10 = 0.7740, and recall@100 = 0.8870. BM25 is
the strongest observed top-rank profile. Korean questions often retain
distinctive names, transliterated terms, article titles, technical vocabulary,
or proper nouns from the source paragraph.

This lexical signal is valuable for long-document retrieval because a rare
entity or phrase can point to the correct full article. BM25 can still struggle
when Korean morphology, spacing, or shared names create competing matches, but
it remains the best observed ranker at the top of the list.

### Dense Evaluation Profile

The dense `harrier_oss_v1_270m` candidate subset contains 500 candidates per
query and achieves nDCG@10 = 0.4120, hit@10 = 0.5311, and recall@100 = 0.7797.
Dense retrieval captures broad embedding similarity but loses a large amount of
top-rank precision relative to BM25.

This is consistent with the long-document setting. A single dense vector for a
long Korean article can blur the local paragraph evidence. Articles about
related games, historical regions, scientific concepts, public figures, or
medical topics can be semantically close even when only one contains the exact
answer-bearing paragraph.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset contains mostly 100 candidates per
query, with 17 queries using a rank-101 safeguard row. It achieves nDCG@10 =
0.5925, hit@10 = 0.7345, and recall@100 = 0.9040. Hybrid retrieval improves
clearly over dense retrieval and slightly exceeds BM25 on recall@100, but BM25
still has stronger top-rank quality.

This profile suggests that hybrid search is useful as a candidate generator for
reranking: it recovers positives that BM25 misses while preserving many lexical
hits. The remaining gap in nDCG@10 means the reranker must learn when to trust
Korean lexical anchors over broad semantic similarity.

### Metric Interpretation for Model Researchers

This task is single-positive: each query has exactly one relevant long
document. Hit@10 measures whether that document appears near the top. nDCG@10
is sensitive to the exact rank of the positive, and recall@100 measures whether
the positive remains available to a downstream reranker.

The Korean profile is a strong test of lexical-entity preservation in a
long-document setting. Dense models should not be evaluated only by semantic
coverage; they must also separate the exact article from related Korean
documents that share entities, genres, or topical vocabulary.

### Query and Relevance Type Tendencies

Queries are Korean paragraph-grounded questions about fiction, genealogy,
medicine, geography, biography, science, history, entertainment, and social
topics. They often mention a specific named entity, role, event, method, place,
or object from the source paragraph.

Relevant documents are long Korean articles. The answer-bearing information may
be local, while the rest of the document introduces many unrelated lexical and
semantic signals. This makes paragraph-aware evidence especially important.

### Representative Failure Modes

Dense retrieval can return a thematically similar Korean article but miss the
one containing the generated-question paragraph. BM25 can fail when several
articles share a name, title, or technical term, or when Korean spacing and
morphology reduce exact-match reliability.

Hybrid retrieval can increase recall but still place a semantically related
negative above the positive. Rerankers should compare local evidence spans and
not rely only on article titles or global document embeddings.

### Training Data That May Help

Useful training data includes Korean long-document QA retrieval pairs, Korean
Wikipedia article retrieval, multilingual MLDR training data outside this Nano
split, and Korean hard negatives that share entities, genres, or technical
terminology. Training should include full-article positives selected from a
single answer-bearing paragraph.

Synthetic data can help when it samples paragraphs from long Korean
encyclopedic articles, generates grounded Korean questions, and uses the full
article as the positive. Negatives should be related Korean articles that share
names, categories, or topical labels but do not answer the question.

### Model Improvement Notes

Dense retrievers should consider chunked indexing, late interaction,
paragraph-aware pooling, or multi-vector document representations. Sparse
systems should preserve Korean lexical anchors while handling morphology and
spacing variation. Rerankers should be trained with same-entity and same-topic
long-document hard negatives.

For hybrid systems, `NanoMLDR / ko` is a useful reminder that better
recall@100 does not automatically mean better nDCG@10. The current
`reranking_hybrid` profile gives a strong reranking candidate pool, but top-rank
ordering still needs improvement.

## Example Data

| Query | Positive document |
| --- | --- |
| 자신의 마법 능력에 대해 인식하지 못하는 이유는 무엇인가요? [33 chars] | 테일즈위버(Talesweaver)는 넥슨과 소프트맥스가 소설 룬의 아이들을 원작으로 공동개발한 엠엠오알피지(MMORPG)다. 2003년 6월부터 정식 서비스를 개시한 이후 꾸준히 사랑받고 있다. 개요 원작은 전민희의 룬의 아이들로, 이것에서 비롯되었다. 시스템 일본에서는 2004년 9월부터 정식 서비스 중이다. 중화인민공화국에서는 2004년 5월에 처음 정... [200 / 12,131 chars] |
| 왕조 시대에 존재한 김숙검과 김희삼은 어떤 역할을 했으며, 그들의 기여는 어떤 영향을 미쳤을까요? [54 chars] | 의성 김씨(義城 金氏)는 경상북도 의성군을 본관으로 하는 한국의 성씨이다. 의성의 고호가 문소인 관계로 혹칭 문소 김씨(聞韶 金氏)라고도 한다. 역사 초기 족보인 1530년 계축보 부터 1801년 신유보 까지 3백여 년간에 걸쳐 고려 말 태자첨사를 지낸 김용비(金龍庇)를 시조로 하고, 관향을 의성으로 하여 세계를 이어왔다. 상계는 실전되어 전하지 않는다고... [200 / 8,969 chars] |
| 의 안전성을 평가하기 위해 추가적인 임상시험이 필요하다. 이러한 비용과 시간 소요를 고려할 때, 신약 개발 프로세스에서 임상시험 단계를 최적화하거나 대체할 수 있는 방법이 있는지... [100 / 106 chars] | 임상시험(臨床試驗, ) 또는 임상연구는 사람을 직접 대상으로, 사람에게서 추출(또는 적출)된 검체나 사람에 대한 정보를 이용하여 이루어지는 모든 시험 또는 연구이자 개발중인 신약의 사용 허가 전에 그 약의 효과와 안전성을 증명하는 과정이다. 참가자에 대한 이러한 전향적 생의학이나 행동 치료는 새로운 치료법 (신규 백신, 약물, 식이 선택, 식이 보충제 및... [200 / 13,280 chars] |
| 노보시비르스크에서 겨울과 여름에는 어떻게 해가 떠 있는 시간이 변하는가? [40 chars] | 노보시비르스크(, )는 인구 수 기준으로 러시아 제3의 도시이며 시베리아 제1의 도시다. 시베리아 연방관구, 노보시비르스크주, 노보시비르스크구의 행정수도(주도)이며 서시베리아경제구역의 중심지이다. 노보시비르스크는 의의가 있는 도시로서, 도시구의 지위를 가진 시市 구성체 노보시비르스크시를 구성하는데, 이는 러시아에서 가장 인구가 많은 시 구성체이다. 또한 노... [200 / 12,930 chars] |
| 이 작품에서 주인공들은 어떤 역할을 맡고 있나요? [27 chars] | 최원형(1968년 1월 3일 ~ )은 한국의 남자 성우다. 1993년 문화방송 11기 공채 성우로 데뷔했다. 출연 작품 굵은 글씨는 메인 캐릭터. TV 애니메이션 3x3 아이즈 : 성마전설 ova - 나파르바 DNA^2 (애니맥스) - 모모나리 준타 S.A 스페셜 에이 (애니맥스) - 타키시마 케이 가이스터즈 (MBC) - 딘 호너스 고미의 만화 호기심 천... [200 / 9,813 chars] |

### Public Sources

- [M3-Embedding: Multi-Linguality, Multi-Functionality, Multi-Granularity Text Embeddings Through Self-Knowledge Distillation](https://arxiv.org/abs/2402.03216),
  2024.
- [M3-Embedding ACL Anthology version](https://aclanthology.org/2024.findings-acl.137/),
  2024.
- [Shitao/MLDR dataset card](https://huggingface.co/datasets/Shitao/MLDR).
- [hakari-bench/NanoMLDR](https://huggingface.co/datasets/hakari-bench/NanoMLDR),
  Nano benchmark dataset.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| M3-Embedding: Multi-Linguality, Multi-Functionality, Multi-Granularity Text Embeddings Through Self-Knowledge Distillation | 2024 | benchmark paper | [https://arxiv.org/abs/2402.03216](https://arxiv.org/abs/2402.03216) |
| M3-Embedding ACL Anthology version | 2024 | paper | [https://aclanthology.org/2024.findings-acl.137/](https://aclanthology.org/2024.findings-acl.137/) |
| MLDR: Multilingual Long-Document Retrieval dataset | 2024 | dataset card | [https://huggingface.co/datasets/Shitao/MLDR](https://huggingface.co/datasets/Shitao/MLDR) |

### Representative Snippets

| Query pattern | Positive document pattern |
| --- | --- |
| A Korean question about a character's unrecognized magical ability. | A long article about a Korean-served online role-playing game or related fiction. |
| A question about historical lineage members and their contributions. | A long article about a Korean family lineage. |
| A question about optimizing or replacing clinical-trial stages. | A long article about clinical trials. |
| A question about seasonal daylight in Novosibirsk. | A long article about the Russian city. |
| A question about roles played by main characters in a work. | A long article about a Korean voice actor and credited roles. |
