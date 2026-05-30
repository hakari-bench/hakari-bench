# NanoMIRACL / ja

## Overview

MIRACL is a multilingual ad hoc retrieval benchmark introduced in the
`Making a MIRACL` paper and later expanded in the TACL version. The Japanese
task is monolingual: Japanese questions are judged against Japanese Wikipedia
passages, not translated evidence or cross-lingual documents. The benchmark was
designed around native-speaker question writing and passage relevance judgments,
with candidate passages drawn from lexical and neural retrievers, so it measures
practical passage retrieval rather than answer extraction from a preselected
article.

This NanoMIRACL Japanese split keeps a compact version of that Wikipedia passage
search problem. It has 200 short fact-seeking queries over a 10,000-passage
Japanese corpus, with 373 positive qrel rows. Questions often ask when an
organization was founded, where a person was born, whether an entity has a
property, what kind of sport or object something is, or how many people were
affected by an event. The task is therefore strongly entity-centered, but not
purely lexical: a good system must preserve rare names, titles, dates, and
places while also resolving the relation asked by the short query. The BM25,
dense, and reranking-hybrid candidate profiles expose how much of the dataset is
driven by exact surface overlap, embedding-level semantic similarity, and the
combination of both.

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

The sampled Nano task has 200 queries, 10,000 documents, and 373 positive qrel
rows. Most queries have one positive passage, but 78 queries have multiple
positive passages; the average is 1.865 positives per query, with a maximum of
8. Queries are very short, with an average length of 17.50 characters. They are
usually natural Japanese fact questions such as asking when an organization was
founded, where a person was born, whether an entity has a property, or how many
people were affected by an event. The documents are Japanese Wikipedia passages
with an average length of 173.39 characters, typically beginning with the
article title followed by an explanatory paragraph.

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

### BM25 Evaluation Profile

BM25 is the lexical view of this task: it rewards exact or near-exact overlap
between the short Japanese question and a Wikipedia passage. On this NanoMIRACL
Japanese split, the dataset-provided BM25 top-500 candidate subset reaches
nDCG@10 = 0.6601, hit@10 = 0.9350, and Recall@100 = 0.9705. It is strong because
many queries contain rare entity names, article titles, organization names,
vehicles, games, dates, or Japanese Wikipedia surface strings. BM25 is therefore
a high-coverage first-stage retriever for this split, especially for top-100
candidate recall. Its weakness is relation resolution: lexical overlap can put
near-entity passages above the passage that actually answers the short question.

### Dense Evaluation Profile

The dense candidate subset, produced by `harrier_oss_v1_270m`, measures a
different tendency. Instead of relying mainly on term frequency and exact
Japanese string overlap, it ranks passages by embedding similarity. On this
split it reaches nDCG@10 = 0.7745 and hit@10 = 0.9150, while Recall@100 is
0.9303. Dense is the best top-rank ordering signal among the three candidate
views, but it is not the best top-100 coverage signal. It helps when the query
asks for a relation rather than only naming an entity, or when the evidence
passage uses a different surface form from the query. The cost is rare-string
anchoring: katakana spellings, romanized names, product titles, and exact
article titles can be smoothed into nearby topics.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset emulates a hybrid search result by
combining the lexical strengths of BM25 and the embedding-similarity strengths
of dense retrieval. On this split it reaches nDCG@10 = 0.7223, hit@10 = 0.9700,
and Recall@100 = 1.0000. Hybrid is not the best pure top-rank sorter because
dense has higher nDCG@10, but it is the safest candidate-generation view. It
finds a positive in the top 10 for 194 of 200 queries and covers all 373 judged
positives in the top 100. For reranker research, this means the candidate stage
is already strong enough to test evidence selection rather than only missing
document recovery.

### Metric Interpretation for Model Researchers

The most important distinction is nDCG@10 versus Recall@100. Dense leading
nDCG@10 means embedding similarity often orders the answer-bearing passage
better at the very top. BM25 leading dense on Recall@100 means exact lexical
anchors still recover positives that dense retrieval can miss. Reranking hybrid
reaching Recall@100 = 1.0000 means top-100 candidate loss is largely removed for
this split; the remaining challenge for a reranker is ordering the best evidence
above near-entity or topic-adjacent passages. A model that improves only nDCG@10
without preserving Recall@100 may be learning semantic ranking at the cost of
lexical coverage. A model that improves Recall@100 but not nDCG@10 may be a
better first-stage retriever but not necessarily a better final ranker.

### Query Type Tendencies

The task is dominated by short entity-centered fact questions. Common query
types include birthplace, death date, founding date, organization type, sport or
vehicle classification, yes/no property questions, and event-count questions.
The lexical winner cases usually contain rare entity strings, exact titles, or
unusual katakana and romanized forms. Dense tends to help when the query asks a
relation that is not expressed in the same words as the passage, such as whether
a broadcaster is paid television, whether a license is required, or where a
person came from. Hybrid is most useful for questions where both signals are
needed: the entity string must be preserved, but the correct passage is the one
that satisfies the relation.

### Representative Failure Modes

Failures often happen inside the correct topic family. BM25 may retrieve other
`メジロ` racehorse passages before the one that states the birth date of
`メジロライアン`. It may also retrieve passages about paid television services or
NHK-related topics before the passage that answers "ＮＨＫは有料テレビ局？". Dense can
make the opposite mistake: it can rank a semantically coherent passage about a
nearby person, work, organization, or product above the judged evidence because
the exact rare string is not strongly anchored. These are not broad topical
misses; they are passage-level evidence selection errors among plausible
neighbors.

### Japanese-Specific Notes

Japanese tokenization and normalization matter. Query strings include kanji,
hiragana, katakana, full-width Latin letters, romanized titles, punctuation,
variant article-title forms, and date expressions. BM25 quality depends on
whether proper nouns and compounds are segmented in a way that preserves useful
lexical anchors. Dense retrieval is less sensitive to segmentation, but it can
blur rare names, long katakana titles, and full-width/half-width variants. Strong
systems should normalize harmless orthographic variation while preserving
entity-distinguishing characters.

### Training and Leakage Notes

MIRACL Japanese train data and other Japanese Wikipedia question-to-passage
retrieval data are natural training sources, but evaluation queries, qrels, and
positive passages from this Nano split should be excluded. Upstream MIRACL
development or test material and other MIRACL-derived data should be audited for
overlap before training. For model comparison, it is useful to report whether a
system was trained on MIRACL, Mr. TyDi, Japanese Wikipedia QA, or synthetic
question-generation data, because those sources can directly teach this
question-to-evidence style.

### Model Improvement Hints

The most useful improvements are lexical-semantic balance, relation-aware
reranking, and Japanese entity grounding. First-stage retrievers should preserve
BM25-like rare-name recall while using dense similarity to rank relation matches
near the top. Rerankers should be trained with hard negatives from the same
entity family, the same article title neighborhood, or passages that share the
entity but answer a different relation. Synthetic data is most valuable when it
creates short Japanese fact questions from non-evaluation Wikipedia-style
passages and pairs them with near-entity negatives.

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
