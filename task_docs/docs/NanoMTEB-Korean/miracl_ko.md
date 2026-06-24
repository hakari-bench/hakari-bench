# NanoMTEB-Korean / miracl_ko

## Overview

`miracl_ko` is the Korean MIRACL retrieval task. Queries are Korean information
needs, and documents are Korean Wikipedia passages. The Nano split contains 200
queries, 10,000 documents, and 508 positive qrels. It is multi-positive: each
query has 2.54 positives on average, the median is two, and 51.5% of queries
have more than one relevant passage. Queries average 21.71 characters, while
documents average 193.24 characters. The task tests Korean passage retrieval
over short encyclopedic passages with native-language queries, aliases,
morphology, and multiple answer-bearing contexts.

## Details

### What the Original Data Measures

[MIRACL: A Multilingual Retrieval Dataset Covering 18 Diverse Languages](https://arxiv.org/abs/2210.09984)
introduced a multilingual retrieval benchmark with human-annotated
passage-level relevance judgments over Wikipedia. MIRACL includes Korean and
provides native-language queries, passage corpora, and relevance annotations.
The dataset was designed to improve multilingual retrieval coverage beyond
English-centric benchmarks.

The Korean split is a same-language Wikipedia retrieval task. The model must
rank answer-bearing or contextually relevant Korean passages for a Korean
query, often with more than one positive passage.

### Observed Data Profile

The Nano split has 200 Korean queries, 10,000 documents, and 508 positive
judgments. Documents are short Korean Wikipedia passages with title prefixes.
Queries are compact fact-oriented questions, often asking about people, places,
religion, science, history, and definitions.

Examples include questions about Hercules, King Sukjong, Catholic canon law,
RNA structure, and the origin of Buddhism. Passage segmentation means several
passages can be relevant to one query, and some positives may provide
supporting context rather than a single direct answer sentence.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.5069, hit@10 of 0.8050, and recall@100 of 0.9606.
This is a strong lexical baseline for Korean Wikipedia retrieval. Named
entities, titles, and direct fact terms often provide enough overlap for BM25
to retrieve relevant passages.

BM25 is not the best top-rank method, however. Korean morphology, aliases,
synonyms, and short query length can make exact term matching fragile. BM25 has
high recall but can place the most useful passage below semantically related
distractors.

### Dense Evaluation Profile

Dense retrieval is stronger at early ranking, with nDCG@10 of 0.6997, hit@10
of 0.9150, and recall@100 of 0.9291. Dense retrieval better captures semantic
relationships between compact Korean questions and answer-bearing passages. It
can handle paraphrase and entity context more effectively than pure lexical
matching.

Dense recall@100 is lower than BM25, which shows the tradeoff: dense retrieval
often ranks better when it finds the right evidence, but may miss some lexical
positives in the first 100. This is important for reranking pipeline design.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` profile is strongest overall, with nDCG@10 of 0.7121,
hit@10 of 0.9550, and recall@100 of 0.9902. It combines the dense model's
semantic ranking advantage with BM25's lexical coverage. Candidate lists
contain 100 to 101 entries, with three safeguard-positive rows.

This is the ideal hybrid pattern: hybrid search improves both early ranking and
candidate coverage relative to the individual methods. It is a strong candidate
source for downstream reranking in Korean Wikipedia retrieval.

### Metric Interpretation for Model Researchers

`miracl_ko` is hybrid-favorable, with dense retrieval strong at top-10 and BM25
strong for recall. The task is useful for evaluating whether a model can
balance Korean lexical anchors with semantic matching. Since many queries have
multiple positives, recall@100 should be interpreted as coverage across all
useful evidence passages, not only one answer.

nDCG@10 measures whether the most useful relevant passages appear early. Hit@10
measures whether at least one relevant passage is retrieved for a user or QA
system. The hybrid score indicates that combining lexical and dense evidence is
especially valuable here.

### Query and Relevance Type Tendencies

Queries are short Korean information needs, often asking who, what, where, or
whether a statement is true. Positive documents are Korean Wikipedia passages
with answer evidence or necessary background. Topics range from mythology and
history to biology, religion, politics, and geography.

Relevance can be multi-passage. A query may have several passages that answer
or support the information need, so training and evaluation should allow
multiple positives.

### Representative Failure Modes

BM25 can fail on aliases, inflection, and paraphrase. Dense retrieval can miss
rare names or exact Korean title matches when semantic similarity is too broad.
Hybrid retrieval reduces both risks, but can still rank a related passage above
the most directly answer-bearing one.

Passage segmentation is another challenge: a passage may contain context but
not the answer sentence, while another passage from the same article gives the
direct answer.

### Training Data That May Help

Useful training data includes non-overlapping MIRACL Korean train pairs, Mr.
TyDi Korean retrieval pairs, Korean Wikipedia question-to-passage retrieval
pairs, and native Korean hard negatives from the same Wikipedia topic. Training
should exclude MIRACL Korean dev/test queries, qrels, and positive passages
likely to overlap with the Nano split.

Synthetic data should create Korean Wikipedia-style passages with titles,
aliases, dates, places, organizations, and definitions, then generate Korean
fact questions grounded in one or more source passages. Multi-positive training
is appropriate.

### Model Improvement Notes

Models should combine Korean lexical fidelity with semantic passage matching.
Dense encoders need stronger handling of aliases, title variants, and rare
entities. Hybrid and reranking systems should preserve multiple relevant
passages while prioritizing the most answer-bearing one.

## Example Data

| Query | Positive document |
| --- | --- |
| 헤라클레스는 그리스 신들 중 한 명인가? [22 chars] | 그리스 신화 헤라클레스는 에트루리아와 로마의 신화 및 숭배에도 등장하며, 로마인이 쓰던 라틴어 감탄사 "mehercule"은 그리스어인 "Herakleis"에서 유래한 것이었다. 이탈리아에서는 헤라클레스를 상인의 신으로 숭배하였는데, 다른 나라에서는 그의 특징적인 재능인 행운이나 위험에서의 구조를 염원하기도 하였다. [178 chars] |
| 숙종은 몇 번째 왕인가? [13 chars] | 조선 숙종 숙종(肅宗, 1661년 10월 7일(음력 8월 15일) ~ 1720년 7월 12일(음력 6월 8일))은 조선의 제19대 왕이다. 성은 이(李), 휘는 돈(焞), 본관은 전주(全州)., 초명은 용상(龍祥), 광(爌), 자는 명보(明譜), 사후 시호는 숙종현의광륜예성영렬장문헌무경명원효대왕(肅宗顯義光倫睿聖英烈章文憲武敬明元孝大王)이며 이후 존호가 더해져 정식 시호는 숙종현의광륜예성영렬유모영운홍인준덕배천합도계휴독경정중협극신의대훈장문헌무경명원효대왕(肅宗顯義光倫睿聖英烈裕謨永運洪仁峻德配天合道啓休篤慶正中恊極神毅大勳章文憲武敬明元孝大王)이다. 현종과 명성왕후의 외아들로 비는 김만기의 딸 인경왕후, 계비는 민유중의 딸 인현왕후, 제2계비는 김주신의 딸 인원왕후이다. [371 chars] |
| 가톨릭교회의 교회법(CIC)은 교회의 고유한 조직과 운영, 그리고 신자들이 교회의 목적을 좇아 이루도록 합법적인 교회의 권위로 제정한 법을 말하나요? [83 chars] | 로마 가톨릭교회 가톨릭교회의 교회법(CIC)은 교회의 고유한 조직과 운영, 그리고 신자들이 교회의 목적을 좇아 이루도록 합법적인 교회의 권위로 제정한 법을 말한다. 가톨릭교회는 영신적이면서도 가시적인 형태로 존재하며, 신적인 것과 인간적인 것이 함께 존재한다. 그러므로 교회법도 자연히 신약성경과 성전 안에 나오는 신법과, 교회와 인간이 제정한 실정법으로 이루어진다. 이러한 법의 제정 및 공표는 교황만이 할 수 있다. 교황은 보편 교회의 최고 목자로서 자기 임무에 의하여 교회에서 최고의 완전하고 직접적이며 보편적인 직권을 가지며 이를 언제나 자유로이 행사할 수 있다. [320 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| MIRACL: A Multilingual Retrieval Dataset Covering 18 Diverse Languages | 2023 | Paper | [https://arxiv.org/abs/2210.09984](https://arxiv.org/abs/2210.09984) |
| MIRACL project page | 2023 | Project page | [http://miracl.ai/](http://miracl.ai/) |
| mteb/MIRACLRetrieval | 2025 | Dataset card | [https://huggingface.co/datasets/mteb/MIRACLRetrieval](https://huggingface.co/datasets/mteb/MIRACLRetrieval) |

### Representative Snippets

| Query | Positive document excerpt |
| --- | --- |
| 헤라클레스는 그리스 신들 중 한 명인가? | A Korean passage about Hercules in Greek, Etruscan, and Roman mythology. |
| 숙종은 몇 번째 왕인가? | A Korean passage identifying Sukjong as the 19th king of Joseon. |
| 가톨릭교회의 교회법은 무엇을 말하나요? | A Roman Catholic Church passage describing canon law and church authority. |
| RNA는 오탄당인 리보스를 기반으로 사슬구조를 이루나요? | An RNA passage explaining ribose, bases, phosphate, and chain structure. |
| 불교의 시작은 어느 나라인가? | A history of Buddhism passage discussing India and early spread. |
