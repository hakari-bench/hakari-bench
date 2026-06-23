# NanoJMTEB-v2 / miracl_ja

## Overview

NanoJMTEB-v2 / miracl_ja is the Japanese MIRACL retrieval task packaged inside
the Japanese MTEB-style Nano set. Like NanoMIRACL / ja, it is a monolingual
Japanese Wikipedia passage retrieval task: short Japanese questions retrieve
Japanese passages that contain the answer evidence. The metadata records 200
queries, 10,000 passages, and 373 positive qrels, with 78 queries having
multiple positives. The task is entity-centered and fact-oriented, but it is not
only a title lookup. A strong system must preserve exact Japanese names and
article-title cues while choosing the passage that answers the requested
relation. BM25 has strong top-100 coverage, dense retrieval gives the strongest
top-rank ordering, and reranking hybrid creates the most reliable top-100
candidate pool for downstream reranking.

## Details

### What the Original Data Measures

[Making a MIRACL: Multilingual Information Retrieval Across a Continuum of
Languages](https://arxiv.org/abs/2210.09984) introduced MIRACL as a multilingual
monolingual retrieval benchmark over Wikipedia passages. Japanese queries are
matched to Japanese passages, with native-language questions and relevance
judgments. The task measures passage retrieval: the system must retrieve a text
passage that provides evidence for the information need, not merely classify the
question or generate an answer.

JMTEB adapts Japanese retrieval tasks for embedding evaluation. This Nano task
keeps MIRACL's Japanese Wikipedia evidence-finding shape but places it inside a
Japanese embedding benchmark family. That context matters for model comparison:
the task is useful for evaluating Japanese dense encoders, sparse retrievers,
and reranking pipelines on the same entity-and-evidence behavior that MIRACL was
designed to test.

### Observed Data Profile

The sampled Nano task has 200 queries and 10,000 documents. Positive relevance
is not always one-to-one: the average is 1.865 positives per query, and the
maximum is 8. Queries are short, averaging 17.50 characters. They ask about
birth dates, opening dates, country membership, licenses, definitions, office
holders, fictional properties, media figures, sports, and historical entities.
Documents are Japanese Wikipedia passages averaging 194.29 characters, usually
starting with the article title and then a concise explanatory paragraph.

The main retrieval challenge is passage-level evidence selection among plausible
entity neighbors. For many queries, the title or entity name gives a strong
lexical anchor. The harder cases require selecting the passage that answers the
relation asked by the query: date, role, membership, property, category, or
requirement. Because this task is part of a Japanese embedding benchmark, it is
especially useful for checking whether dense models improve top-rank ordering
without losing the exact Japanese lexical anchors that sparse retrieval keeps.

### BM25 Evaluation Profile

The BM25 candidate subset reaches nDCG@10 = 0.5361, hit@10 = 0.8550, and
Recall@100 = 0.9759. BM25 is a strong candidate generator because many queries
contain names, titles, date-like expressions, and other surface forms that occur
in Wikipedia passages. Its limitation is shallow ordering: it can retrieve the
right article or topic family while ranking a non-answering passage above the
judged evidence.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` reaches nDCG@10 = 0.6923,
hit@10 = 0.8800, and Recall@100 = 0.9223. Dense retrieval is the strongest
top-rank signal for this task, indicating that embedding similarity helps map
short Japanese questions to passages expressing the requested fact or relation.
Its weakness is candidate coverage: it misses more judged positives by top 100
than BM25 does.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset reaches nDCG@10 = 0.6252, hit@10 =
0.8600, and Recall@100 = 0.9973. Hybrid is not the best top-rank ordering signal
because dense has higher nDCG@10, but it is the best candidate-coverage view.
For reranker research, this is the most useful pool: nearly every judged
positive is available in the top 100, while the candidate set still contains
real lexical and semantic distractors.

### Metric Interpretation for Model Researchers

This task is a good example of why nDCG@10 and Recall@100 should be read
separately. Dense retrieval winning nDCG@10 means it usually orders answer-like
passages better near the top. BM25 winning over dense on Recall@100 means exact
Japanese surface anchors are still critical for candidate coverage. Reranking
hybrid approaching complete Recall@100 means the remaining challenge is mostly
evidence ordering, not whether a relevant passage exists in the candidate pool.
For encoder research, a useful improvement would preserve BM25's high recall
while matching or exceeding dense top-rank ordering. For reranker research, this
task tests whether the model can identify the passage that answers the relation
instead of merely matching the same entity.

### Query and Relevance Type Tendencies

The query set is dominated by short factual questions about named entities.
Lexical-heavy queries include exact person names, organization names, place
names, country names, works, and fictional entities. Semantic-heavy queries ask
about relations that may not share words with the passage, such as whether a
license is required, where a territory belongs, or what capability a fictional
group has. A passage is relevant when it contains enough evidence to answer the
question; a passage about the same entity is not automatically relevant. Hybrid
retrieval helps when the entity must be preserved lexically but the relevant
passage is chosen by relation semantics.

### Representative Failure Modes

BM25-style failures tend to be same-entity or same-topic ordering mistakes. The
retriever may find the right article family but rank an adjacent passage that
does not contain the answer. Dense failures tend to be semantically plausible
but under-anchored: the model retrieves a passage about a nearby location,
person, organization, or concept while missing the exact title or named entity.
For example, queries about dates, country membership, licenses, and fictional
properties can attract passages that are topically related but do not answer the
specific relation. These errors are useful hard negatives for reranking.

### Japanese-Specific Notes

Japanese retrieval quality depends on tokenization, script normalization, and
proper-noun preservation. Queries include kanji names, katakana names,
full-width punctuation, romanized names, date expressions, and short particles
that determine the relation. Sparse retrieval can fail when segmentation breaks
or over-splits entity names. Dense retrieval can fail when it smooths away exact
titles or orthographic variants. Strong Japanese models should normalize
surface variation while preserving entity-distinguishing strings.

### Training and Leakage Notes

Training should avoid evaluation queries, qrels, and positive passages from this
Nano split, as well as upstream MIRACL examples that overlap with the same
Japanese evaluation material. Useful training exposure should be disclosed,
especially if the model saw MIRACL, JMTEB, Mr. TyDi, Japanese Wikipedia QA, or
synthetic data generated from Japanese Wikipedia evidence. Because this is a
public benchmark-derived task, overlap auditing is important for both dense
encoder training and reranker fine-tuning.

### Model Improvement Hints

A strong first-stage retriever should combine exact Japanese entity anchoring
with semantic relation matching. Rerankers should be trained on hard negatives
from the same article, same title family, same entity type, or same relation
family. Multi-positive training is useful because many queries have more than
one judged passage. Synthetic data should create short Japanese factual
questions from non-evaluation Wikipedia passages and include near-entity
distractors that are plausible but do not answer the question.

### Training Data That May Help

Relevant training data includes Japanese MIRACL train material, Mr. TyDi-style
Japanese retrieval pairs, Japanese Wikipedia question-to-passage supervision,
and Japanese entity-centric QA retrieval. For reranking, examples should include
same-article or same-topic negatives rather than only random negatives. Training
should keep passage-level labels because the task is about finding evidence
passages, not just predicting answer strings.

### Synthetic Data Guidance

Generate short Japanese questions from non-evaluation Wikipedia passages. Cover
`いつ`, `どこ`, `誰`, `何`, country-membership questions, license/requirement
questions, definition questions, and yes/no property questions. Synthetic
documents should remain passage-shaped, with titles and factual explanatory
sentences. Hard negatives should share the same entity, article family, or
domain but omit the specific evidence needed to answer the generated question.

## Example Data

| Query | Positive document |
| --- | --- |
| 神戸港が開港したのはいつ [12 chars] | 神戸港: 「神戸」は当時、開港場一帯の村の名前でしかなかったが、公文書には、開港直後の1868年（慶応4年、明治元年）には「神戸港」の名称がすでに現れている。やがて外国人の手によって居留地ができ始め、西洋文化の入り口として発展して「神戸」の名が著名になっていった。1872年（明治5年）、和田岬に和田岬灯台が設置されて1892年（明治25年）に勅令により、旧生田川（現フラワーロード）河口から和田岬ま... [200 / 214 chars] |
| レーシングドライバーになるには免許が必要ですか？ [24 chars] | モータースポーツライセンス: 世界的に通用する国際ライセンスの発行は以下の団体が行っている。下記団体が開催する競技に参戦するためには、これらの団体が発行したライセンスが必要となる。ただし発給申請自体は、傘下の国内ライセンスの発行団体を通じて行えることが多い。日本の法律ではモータースポーツを行うのに資格は必要ないが、参加するモータースポーツ主催の団体（FIAやJAF等）が発行するモータースポーツライ... [200 / 564 chars] |
| ウェールズはどこの国に属する？ [15 chars] | ウェールズ: ウェールズ（、 カムリ）は、グレートブリテンおよび北アイルランド連合王国（イギリス）を構成する4つの「国（イギリスのカントリー）」（country）のひとつである。ウェールズはグレートブリテン島の南西に位置し、南にブリストル海峡、東にイングランド、西と北にはアイリッシュ海が存在する。 [149 chars] |
| パメラ・コールマン・スミスはいつ生まれた？ [21 chars] | パメラ・コールマン・スミス: パメラ・コールマン・スミス（Pamela Colman Smith、1878年2月16日 - 1951年9月18日）は、画家、イラストレーター、作家。ニックネームは「ピクシー」だった。スミスは、占いに使用するタロット・カードの一つ、「ウェイト＝スミス・デッキ」（ライダー＝ウェイト、あるいはライダー＝ウェイト＝スミス・デッキとも呼ばれる。）を、アーサー・エドワード・ウェ... [200 / 223 chars] |
| マーベル・コミックのミュータントは特殊能力を持つ？ [25 chars] | マグニートー (マーベル・コミック): マグニートーは磁場を操り、幅広い種類の影響を及ぼすことができるミュータントである。彼の主要な能力は、磁力を支配し、鉄を含む金属と非鉄の金属を操ることである。彼が一度に操ることのできる量の最大値は不明で、彼は何度か、大きな小惑星を動かし、3万トンの原子力潜水艦を容易く空中に浮かせたことがある。彼は自分の力を原子レベルにまで拡張し、（電磁力が化学結合の要因である... [200 / 831 chars] |

### Public Sources

- [Making a MIRACL: Multilingual Information Retrieval Across a Continuum of Languages](https://arxiv.org/abs/2210.09984), 2022.
- [MIRACL project page](http://miracl.ai/).
- [sbintuitions/JMTEB](https://huggingface.co/datasets/sbintuitions/JMTEB), Japanese embedding benchmark card.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoJMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoJMTEB-v2)
- Source task dataset: [mteb/MIRACLRetrieval](https://huggingface.co/datasets/mteb/MIRACLRetrieval)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Making a MIRACL: Multilingual Information Retrieval Across a Continuum of Languages | 2022 | paper | [https://arxiv.org/abs/2210.09984](https://arxiv.org/abs/2210.09984) |
| MIRACL project page |  | project page | [http://miracl.ai/](http://miracl.ai/) |
| sbintuitions/JMTEB | 2024 | dataset card | [https://huggingface.co/datasets/sbintuitions/JMTEB](https://huggingface.co/datasets/sbintuitions/JMTEB) |
