# NanoMIRACL / ja

## Overview

NanoMIRACL / ja is a compact Japanese passage-retrieval task derived from
MIRACL, the multilingual ad hoc retrieval benchmark introduced in the
`Making a MIRACL` paper and later expanded in TACL. The task is monolingual:
Japanese questions retrieve Japanese Wikipedia passages. It is not a translated
cross-lingual benchmark and not a reading-comprehension task with a preselected
article. The Nano split contains 200 short fact-seeking queries, 10,000
Wikipedia-style passages, and 373 positive qrels. Most queries have one positive
passage, but a substantial minority have multiple positives. The strongest
retrieval signal is a mixture of rare Japanese entity strings, article-title
matching, and relation-aware passage selection. BM25 gives strong top-100
coverage, dense retrieval gives the best top-rank ordering, and reranking hybrid
nearly eliminates candidate loss for reranker experiments.

## Details

### What the Original Data Measures

[Making a MIRACL: Multilingual Information Retrieval Across a Continuum of
Languages](https://arxiv.org/abs/2210.09984) describes MIRACL as a multilingual
retrieval benchmark covering 18 languages. Each language is evaluated
monolingually, so the Japanese task asks Japanese questions over Japanese
Wikipedia passages. The paper emphasizes native-speaker question writing and
native-speaker relevance judgments, with candidate passages gathered from
lexical and neural retrieval systems. That design matters: the benchmark
measures open-domain passage retrieval over plausible answer-bearing evidence,
not answer extraction from a fixed document.

For Japanese, the source task inherits the Wikipedia passage style also seen in
Mr. TyDi-like retrieval: short natural questions, article-title cues, compact
factual passages, and relevance labels over passages rather than whole pages.
Images and tables are outside the retrieval target; systems retrieve text
passages. The result is an evidence-finding benchmark where correct retrieval
requires both finding the right article neighborhood and selecting the passage
that answers the relation asked by the query.

### Observed Data Profile

The task metadata records 200 queries, 10,000 documents, and 373 positive qrels.
There are 78 multi-positive queries, so the task is mostly single-positive but
not purely one-answer. Query text is very short, averaging 17.50 characters,
while passages average 173.39 characters. Many queries ask entity-centered fact
questions: when an organization was founded, where a person was born, whether an
entity has a property, what kind of object or sport something is, or how many
people were affected by an event.

The documents are compact Japanese Wikipedia passages, usually beginning with a
title or title-like phrase followed by explanatory text. Because the query is
short, many errors happen among plausible neighbors: the correct entity family
is retrieved, but the passage does not answer the specific relation. This makes
the task useful for studying whether a retriever can preserve exact Japanese
entity anchors while still ranking answer-bearing evidence above nearby article
fragments.

### BM25 Evaluation Profile

The BM25 candidate subset reaches nDCG@10 = 0.6601, hit@10 = 0.9350, and
Recall@100 = 0.9705. This is a strong sparse baseline because short Japanese
queries often contain rare names, article titles, dates, organizations, or
katakana strings that appear in the relevant passage. Its main limitation is
relation selection: term overlap can retrieve the right topic family while
placing the actually answer-bearing passage lower.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` reaches nDCG@10 = 0.7745,
hit@10 = 0.9150, and Recall@100 = 0.9303. Dense retrieval is the best top-rank
ordering signal here, suggesting that embedding similarity helps connect short
Japanese questions to passages that express the requested relation. Its weakness
is coverage: it can smooth away rare spellings, exact titles, or katakana names
that BM25 preserves.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset reaches nDCG@10 = 0.7223, hit@10 =
0.9700, and Recall@100 = 1.0000. It is not the best top-rank sorter because
dense has higher nDCG@10, but it is the safest candidate-generation view. The
hybrid pool preserves BM25's lexical anchors while adding dense semantic matches,
so reranker evaluation can focus on evidence ordering rather than missing
candidate recovery.

### Metric Interpretation for Model Researchers

This task separates top-rank ordering from candidate coverage. Dense retrieval
leading nDCG@10 means semantic similarity often places a good evidence passage
near the top. BM25 leading dense on Recall@100 means exact Japanese lexical
anchors still recover positives that dense retrieval can miss. Reranking hybrid
at Recall@100 = 1.0000 means the candidate pool contains every judged positive
within the top 100, so a reranker tested on this pool is mainly being evaluated
on passage-level evidence selection. A model that improves nDCG@10 but loses
Recall@100 may be too semantic and insufficiently anchored. A model that
improves Recall@100 but not nDCG@10 may be useful as a first-stage retriever but
not necessarily as a final ranker.

### Query and Relevance Type Tendencies

Common queries ask about people, organizations, historical events, vehicles,
sports, media properties, companies, and places. Lexical-heavy cases contain
rare entity strings, exact article titles, unusual katakana forms, romanized
names, or explicit dates. Semantic-heavy cases ask a relation that may be
phrased differently in the passage, such as whether a service is paid, whether a
license is required, or where a person came from. Relevance means the passage
contains enough evidence to answer the question, not merely that the passage is
topically related to the named entity. Hybrid retrieval is strongest when the
entity string must be preserved but the correct passage is determined by the
relation.

### Representative Failure Modes

Failures are usually near misses rather than broad topical misses. BM25 can rank
other passages from the same entity family above the judged evidence, such as
retrieving related racehorse passages before the one that states the birth date
of a specific horse. It can also retrieve passages that share terms with the
query but answer a different relation, such as television-service passages that
do not settle whether NHK is a paid television broadcaster. Dense retrieval can
make the opposite mistake by ranking semantically plausible passages about a
nearby person, organization, product, or event while losing the exact rare
string that identifies the judged evidence. Strong rerankers need hard negatives
from the same article family and same entity neighborhood.

### Japanese-Specific Notes

Japanese tokenization and normalization directly affect this task. Queries mix
kanji, hiragana, katakana, punctuation, full-width Latin letters, romanized
titles, date expressions, and article-title variants. Sparse retrieval depends
on whether proper nouns and compounds are segmented in a way that preserves
entity anchors. Dense retrieval is less sensitive to segmentation but can blur
rare names and orthographic variants. Good systems should normalize harmless
surface variation without collapsing entity-distinguishing characters, product
titles, organization names, or date strings.

### Training and Leakage Notes

MIRACL Japanese training data, Mr. TyDi-style Japanese retrieval pairs, and
Japanese Wikipedia question-to-passage data are relevant training sources, but
the evaluation queries, qrels, and positive passages from this Nano split should
not be used. Upstream MIRACL development/test material and MIRACL-derived
synthetic data should be audited for overlap before training. Model reports
should disclose whether the system saw MIRACL, Japanese Wikipedia QA, Mr. TyDi,
or synthetic question-generation data based on related Wikipedia passages.

### Model Improvement Hints

The main improvement target is lexical-semantic balance. First-stage retrievers
should keep BM25-like rare-name recall while improving top-rank semantic
ordering for short relation questions. Rerankers should learn to distinguish
same-entity wrong-relation passages, same-title neighboring passages, and
article-family distractors. Synthetic training should generate short Japanese
fact questions from non-evaluation Wikipedia passages and include hard negatives
that share the entity but do not answer the question.

### Training Data That May Help

Useful non-evaluation data includes Japanese MIRACL train data, Japanese
Wikipedia QA retrieval pairs, Mr. TyDi-style monolingual retrieval data, and
native Japanese entity-centric question/passage pairs. Training examples should
keep passage-level positives rather than only answer strings. Hard negatives
from the same article, same entity family, or same topic cluster are especially
valuable because the benchmark's mistakes often occur inside a plausible
neighborhood rather than among unrelated passages.

### Synthetic Data Guidance

For document-to-question generation, use non-evaluation Japanese Wikipedia
passages and generate short Japanese questions answerable from one passage.
Cover birthplace, foundation date, definition, role, event count, organization
type, sport category, and yes/no property questions. For joint generation,
create realistic Wikipedia-style passages with titles, names, dates, places, and
compact factual statements, then generate questions grounded in those passages.
Do not seed generation with Nano evaluation queries or positive passages.

## Example Data

| Query | Positive document |
| --- | --- |
| ノートン・モーターサイクルは自動車の製造をしたことはある？ [29 chars] | ノートン・モーターサイクル ノートンは、1898年にバーミンガムのによって設立された。当初は自転車メーカーであったが1902年1.5馬力のエンジンを積んだオートバイ一号車を製造しオートバイ製造に参入した。その後もフランスやスイスからエンジンを調達してオートバイの製造を続け、1907年にはプジョーから購入した726ccV2サイドバルブエンジンを搭載したオートバイで（新競技方式での）第1回マン島TTレース2気筒クラスを制した。1908年には自社製726ccV2エンジンを製造している。マン島TTレースでは以後戦時中を挟んで1954年までの間に通算10勝を挙げた。ジェームス・ノートンは1925年に56歳で世を去ったが、その前年にあたる1924年にはセニアTTレースとサイドカーレースでの勝利を見届けることが出来た。1927年に開発され1930年に改良が施されたシングル・カムシャフトのCS1エンジンは、1932年から第二次世界大戦勃発の影響で中断される1939年までのセニアTTで7度の優勝を飾るなど、レース界でのノートン伝説を創り上げた。 単気筒エンジンとギアボックス間に隙間を設けるレイアウトは高い信頼性と良好な操作性をもたらし、一般のライダーからも高く評価された。戦時中ノートンはイギリス軍にオートバイを供給し、1937年から1945年の期間に使用されたオートバイのうち四分の一、数にして10万台以上を占めた。主なモデルは単座の『WD 16H』やサイドカー『WD Big Four』などがあった。 [652 chars] |
| 被災者生活再建支援法が制定されたのはいつ [20 chars] | 被災者生活再建支援法 浪江町では、(1)自然災害に起因する今回の原子力発電所の事故を支給対象とせねば支援法が死に法となる。(2)法解釈は現場を知る福島県が被災者に寄り添い、柔軟に運用する義務がある。(3)東京電力原子力事故により被災した子どもをはじめとする住民等の生活を守り支えるための被災者の生活支援等に関する施策の推進に関する法律の趣旨を踏まえ被災者生活再建支援法を適用すべき。(4)長期避難世帯の認定は、被災自治体や社会福祉士会、弁護士会などの専門家の意見を参考にすべき。(5)復興予算をまず被災者の生活再建資金に使うべき。(6)被災者生活再建支援法は、平成7年の阪神大震災の教訓を受け誕生し、様々な災害を乗り越え改良を積み重ねてきた法律であるとし、被災地は、その精神を受け継ぎ、次につなげる義務がある。などと主張している。（浪江町HP参照） [375 chars] |
| アメリカに西欧人が入植したのはいつ？ [18 chars] | ペンサコーラ (フロリダ州) この一帯にヨーロッパ人が訪れるようになったのは16世紀中盤にさしかかった頃であった。1528年にはスペインのパンフィロ・デ・ナルバエスの一行が、1539年には同じくスペインのエルナンド・デ・ソトの一行がその探検の中でこの地を訪れた。そして1559年、トリスタン・デ・ルナ・イ・アレヤーノがメキシコのベラクルスから11隻の船を率いて、1,400人の入植者と共にこの地に降り立ち、現在のアメリカ合衆国本土で最初のスペイン人入植地を創設した。しかし、同年9月19日にハリケーンがこの地を襲い、何百人もの死者を出し、5隻の船が沈没し、キャラベル船が座礁し、食料やその他生活用品も傷み、この入植地は壊滅した。1,000人ほどの生存者は別の場所に入植地を再設したが、飢饉や原住民の攻撃により、1561年には放棄された。240人ほどはこの地を離れ、サンタエレナ（現在のサウスカロライナ州パリスアイランド）へと向かったが、その航海の最中に別の嵐に遭い、キューバへと行先を変え、散り散りになった。この地に最終的に残った50人ほどの入植者はメキシコに戻り、西フロリダは危険すぎて入植できないと結論付けた。こうした西フロリダ観はその後135年にわたって、当地のスペイン人入植者の間に残った。 [550 chars] |

### Public Sources

- [Making a MIRACL: Multilingual Information Retrieval Across a Continuum of Languages](https://arxiv.org/abs/2210.09984); 2022; DOI: `10.48550/arXiv.2210.09984`.
- [MIRACL: A Multilingual Retrieval Dataset Covering 18 Diverse Languages](https://aclanthology.org/2023.tacl-1.63/); 2023; DOI: `10.1162/tacl_a_00595`.
- [MIRACL GitHub repository](https://github.com/project-miracl/miracl).
- [MIRACL corpus dataset card](https://huggingface.co/datasets/miracl/miracl-corpus).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMIRACL](https://huggingface.co/datasets/hakari-bench/NanoMIRACL)
- Source corpus: [miracl/miracl-corpus](https://huggingface.co/datasets/miracl/miracl-corpus)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Making a MIRACL: Multilingual Information Retrieval Across a Continuum of Languages | 2022 | paper | [https://arxiv.org/abs/2210.09984](https://arxiv.org/abs/2210.09984) |
| MIRACL: A Multilingual Retrieval Dataset Covering 18 Diverse Languages | 2023 | paper | [https://aclanthology.org/2023.tacl-1.63/](https://aclanthology.org/2023.tacl-1.63/) |
| MIRACL GitHub repository |  | project repository | [https://github.com/project-miracl/miracl](https://github.com/project-miracl/miracl) |
| miracl/miracl-corpus |  | dataset card | [https://huggingface.co/datasets/miracl/miracl-corpus](https://huggingface.co/datasets/miracl/miracl-corpus) |
