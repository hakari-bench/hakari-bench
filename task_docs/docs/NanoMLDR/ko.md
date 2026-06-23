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
| 자신의 마법 능력에 대해 인식하지 못하는 이유는 무엇인가요? [33 chars] | 테일즈위버(Talesweaver)는 넥슨과 소프트맥스가 소설 룬의 아이들을 원작으로 공동개발한 엠엠오알피지(MMORPG)다. 2003년 6월부터 정식 서비스를 개시한 이후 꾸준히 사랑받고 있다. 개요 원작은 전민희의 룬의 아이들로, 이것에서 비롯되었다. 시스템 일본에서는 2004년 9월부터 정식 서비스 중이다. 중화인민공화국에서는 2004년 5월에 처음 정식 서비스를 시작했다. 캐릭터 주인공(테일즈위버의 14 캐릭터) 시벨린 우 (Sivelin Uoo) 12월 30일 탄생(염소자리), 20살 정도, O형, 남자, 키 187cm 추정 연령 20대. 본인은 24세 정도로 기억하고 있다. 용병들의 국가로 알려진 레코르다블에 기반을 두고 있는 다국적 용병 길드 섀도우&애쉬(Shadow&Ash)에서 최근 명성을 날리고 있는 젊은 용병. 자신의 키보다도 큰 거대한 창을 주무기로 사용하며 황금빛 눈동자와 타오르는 듯한 붉은 머리카락의 강렬한 인상으로 인해 "진홍(眞紅)의 사신(死神)"이라는 호칭으로 널리 알려져 있다. 과거에 있었던 사건의 충격으로 인하여 자신의 이름은 물론, 국적이나 출생지, 나이등 자신의 신상과 관련된 모든 과거의 기억을 잊어버린 상태이다. 현재의 그와 그의 과거를 이어주는 단서는 선상(船上)에서의 전투 도중 거대한 검을 사용하는 흑의 검사(黑衣劍士)에게 공격 당했다는 단편적인 기억과 가슴에 남겨진 거대한 상흔, 그리고 발견되었을 당시 지니고 있었던 작은 팬던트(Pendant)와 유래를 알 수 없는 낡은 건틀렛(Gauntlet) 뿐이다. 그가 사용하고 있는 시벨린이라는 이름은 예전에 그와 함께 페어(Pair)를 짜서 활동했던 늙은 용병 케렌스 우(Kerence Uoo)가 지어준 것으로, 3년 전 임무 수행 도중 시벨린을 대신해 그가 죽은 이후로 그의 성을 이어받아 사용하고 있으며 그의 유언을 지키고 자신의 기억을 되찾기 위해서 전 대륙을 돌아다니며 흑의검사에 대한 정보를 조사하고 있다. 얼마 되지 않는 기억마저도 결코 즐겁고 밝은 일들로만 채워지지는 않... [1,000 / 12,131 chars] |
| 왕조 시대에 존재한 김숙검과 김희삼은 어떤 역할을 했으며, 그들의 기여는 어떤 영향을 미쳤을까요? [54 chars] | 의성 김씨(義城 金氏)는 경상북도 의성군을 본관으로 하는 한국의 성씨이다. 의성의 고호가 문소인 관계로 혹칭 문소 김씨(聞韶 金氏)라고도 한다. 역사 초기 족보인 1530년 계축보 부터 1801년 신유보 까지 3백여 년간에 걸쳐 고려 말 태자첨사를 지낸 김용비(金龍庇)를 시조로 하고, 관향을 의성으로 하여 세계를 이어왔다. 상계는 실전되어 전하지 않는다고 하였다. 시조 김용비(金龍庇)의 생몰 및 행적은 알려지지 않고 있으나, 신라 경순왕 김부의 후예로 고려 말 공민왕 때 홍건적이 쳐들어와 공민왕이 안동으로 몽진할 때 의성 일원에서 날뛰는 도적들의 무리를 물리쳐 민심을 수습한 공으로 금자 광록대부 태자첨사 의성군에 봉해졌다고 한다. 사후 백성들이 그의 공덕을 기려 의성읍 중리리에 『진민사(鎭民祠)』를 세우고 향사해 왔는데 1868년 오토재로 옮겼다고 한다. 《김은열 묘지명》 등장 조선 후기 1784년 개성 어느 산기슭에서 우연히 발견되었다는 『김은열 묘지석』을 바탕으로 김노규가 기사(記事)한 《김은열 묘지명》에 935년 경순왕이 고려에 항복 후 낙랑공주 왕씨를 맞이하여 8자(子)를 두었는데, 5자(子)가 김중석(金重錫)이라 한다. 이후 1785년 김은열의 후손이라 자처하는 경주 김씨 김사목이 족보를 수보하면서 《고려평장사 보국대안군 김은열 묘지명》을 추기하였는데, 2자 『굉(鍠)』을 『황(湟)』으로, 3자 『명(鳴)』을 『명종(鳴鍾)』으로 개명하고, 4자 은열(殷說)의 시호를 보국대안군으로 작호하는 등 가필을 심하게 하였다. 이후부터 경주 김씨 일문 족보류에 경순왕의 8자(子)들이 등재되기 시작하였다. 그러나 《김은열 묘지명》에 나오는 경순왕의 8자(子)들은 《고려사》 등의 문헌은 물론이고, 그 어떤 금석문에서도 찾아볼 수가 없다는 것이다. 또 묘지명 형태도 배위 관계 및 생애 등도 누락되어 있고 단지 형제 서차만 기술되어 있을 뿐 완전하지 않다는 것이다. 시조 소원 경순왕이 고려에 항복 후 맞아들인 고려 태조의 장녀인 낙랑공주 왕씨 소생의 아들이자 고려 태조의... [1,000 / 8,969 chars] |
| 의 안전성을 평가하기 위해 추가적인 임상시험이 필요하다. 이러한 비용과 시간 소요를 고려할 때, 신약 개발 프로세스에서 임상시험 단계를 최적화하거나 대체할 수 있는 방법이 있는지 궁금합니다? [106 chars] | 임상시험(臨床試驗, ) 또는 임상연구는 사람을 직접 대상으로, 사람에게서 추출(또는 적출)된 검체나 사람에 대한 정보를 이용하여 이루어지는 모든 시험 또는 연구이자 개발중인 신약의 사용 허가 전에 그 약의 효과와 안전성을 증명하는 과정이다. 참가자에 대한 이러한 전향적 생의학이나 행동 치료는 새로운 치료법 (신규 백신, 약물, 식이 선택, 식이 보충제 및 의료 기기 등) 및 추가 연구와 비교가 필요한 이미 알려진 치료를 포함하여, 생의학 또는 행동 치료에 관한 특정 질문에 답하도록 설계되었다. 임상시험 단계는 비임상, 1상, 2상, 3상, 4상 시험으로 구분된다. 과거, 임상실험이라는 용어와 혼용되었던 적이 있으나, 현재는 임상시험으로 통일하여 사용하며 임상실험이라는 용어는 사용하지 않는다. 임상시험은 수많은 요인에 따라 비용이 꽤 들 수 있다. 임상시험은 치료의 승인이 필요한 국가에서 보건 당국과 윤리 위원회 (IRB)의 승인을 받은 후에만 실시 될 수 있다. 이 기관들은 시험의 유익성/위험성 비율을 조사 할 책임이 있다. 이 기관들의 승인이 치료가 안전하거나 유효성이 있음을 나타내는 것은 아니며, 임상시험이 수행될 수 있음을 의미한다. 제품 유형 및 개발 단계에 따라 조사자는 처음에 자원 봉사자 또는 환자를 소규모 파일럿 연구에 등록한 다음 점차적으로 대규모 비교 연구를 수행한다. 임상시험의 규모와 비용은 다양 할 수 있으며, 단일 국가 또는 여러 국가를 포함하거나 단일 연구 센터 또는 여러 센터를 포함 할 수 있다. 임상시험 설계는 결과의 과학적 타당성과 재현성을 보장하는 것을 목표로 한다. 임상시험 비용은 승인 된 약물 당 수십억 달러에 이를 수 있다. 정부 단체나 제약, 생명공학기술, 의료기기 기업이 이를 후원한다. 모니터링 및 실험실 작업과 같은 시험에 필요한 특정 기능은 임상시험 수탁 기관 (CRO) 또는 중앙 실험실과 같은 외주 파트너가 관리 할 수 있다. 인간을 대상으로 한 임상시험을 시작한 모든 약들 가운데 10%정도만이 승인된 약으로 된다.... [1,000 / 13,280 chars] |

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
