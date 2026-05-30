# MNanoBEIR / NanoBEIR-ja / NanoNFCorpus

## Overview

NFCorpus is a biomedical and nutrition-focused retrieval benchmark introduced as
a full-text learning-to-rank dataset for medical information retrieval. BEIR
uses it as a biomedical retrieval task, and MMTEB provides the multilingual
benchmark context in which this Japanese NanoBEIR variant is evaluated. The
original task is not a single-answer encyclopedia search problem: it asks a
system to retrieve biomedical abstracts relevant to short health, nutrition, and
medical information needs, often with many relevant documents per query.

`NanoBEIR-ja__NanoNFCorpus` applies that task shape to Japanese translated
queries and Japanese translated biomedical documents. The sampled Nano task has
50 very short health queries, 2,953 biomedical abstracts, and 1,651 positive
qrel rows, averaging 33.02 positives per query. This makes the task a useful
contrast to single-positive entity retrieval. Exact terms such as nutrients,
foods, chemicals, study names, and disease names still matter, but many relevant
abstracts express the same health concept with different wording. The BM25,
dense, and reranking-hybrid profiles therefore reveal whether a search method is
primarily finding literal terminology, broader biomedical semantic similarity,
or a balanced candidate pool that preserves both.

## Details

### What the Original Data Measures

[NFCorpus](https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf)
was built for medical information retrieval over nutrition and health claims.
[BEIR](https://arxiv.org/abs/2104.08663) includes it as a biomedical retrieval
task, and [MMTEB](https://arxiv.org/abs/2502.13595) provides the multilingual
benchmark context.

### Observed Data Profile

The sampled Japanese Nano task has 50 queries, 2,953 documents, and 1,651
positive qrels. It is highly multi-positive, averaging 33.02 positives per
query. Queries are often very short health phrases, averaging 11.16 characters;
documents are biomedical abstracts averaging 655.83 characters.

### BM25 Evaluation Profile

BM25 represents the sparse lexical side of this Japanese NFCorpus task. It gives
high weight to the words that actually appear in the query and document: disease
names, nutrients, foods, chemical names, study names, and short health phrases.
On this split, the dataset-provided BM25 top-500 candidate subset reaches
nDCG@10 = 0.2414, hit@10 = 0.5800, and Recall@100 = 0.1514. The absolute numbers
are much lower than the Japanese MIRACL entity task because NFCorpus is
multi-positive and concept-heavy. There are 1,651 positive qrel rows for only 50
queries, with an average of 33.02 positives per query. A top-100 list can contain
many relevant abstracts and still cover only a modest fraction of all judged
positives. BM25 should therefore be read as exact terminology coverage over a
broad biomedical relevance set, not as a single-answer retrieval score. It is
most useful for queries such as "ラパマイシン" or "チアミン" where the literal
biomedical term should be preserved.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` captures embedding
similarity rather than raw word frequency. On this split it reaches nDCG@10 =
0.2368, hit@10 = 0.6600, and Recall@100 = 0.1787. Compared with BM25, dense has
slightly lower nDCG@10 but higher hit@10 and higher Recall@100. Query-level
averaging shows the same tendency: dense is the sole Recall@100 winner for 12
queries, while BM25 is the sole winner for 3. Dense also finds a top-10 positive
for 33 of 50 queries, compared with 29 for BM25. This indicates that embedding
similarity is better at broad candidate discovery for this Japanese biomedical
translation setting, even if it does not always put the very best positives at
the top. Dense is the signal for lay-health paraphrase and broad biomedical
similarity; its main weakness is drifting toward nearby health concepts that do
not match the specific food, compound, intervention, population, or outcome.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset is the hybrid-search view of this task:
it emulates taking the useful candidates from both BM25 and dense retrieval
rather than choosing one family. On this split it reaches nDCG@10 = 0.2757,
hit@10 = 0.6800, and Recall@100 = 0.1926, the best aggregate value among the
three candidate views for all three visible metrics. It also has the best
query-level top-100 tendency: reranking hybrid is the sole Recall@100 winner for
13 queries, dense for 12, and BM25 for 3, with the remaining queries tied. The
hybrid top-100 list includes an optional rank-101 safeguard for 7 queries,
showing that some queries still need explicit positive preservation even after
combining retrieval families. Hybrid is the best candidate view here because it
keeps literal anchors such as food names, study names, nutrients, and carcinogen
phrases while also collecting paraphrased biomedical abstracts.

### Metric Interpretation for Model Researchers

This task should be read as multi-positive biomedical candidate discovery, not
as single-answer search. nDCG@10 measures how well the top of the ranking
surfaces some of the many relevant abstracts. Recall@100 is stricter in a
different way: because the average query has 33.02 positives, even a useful
top-100 list may cover only a small fraction of all judged positives. Dense
beating BM25 on hit@10 and Recall@100 suggests that semantic similarity expands
coverage beyond literal term overlap. Reranking hybrid leading all three visible
metrics suggests that neither lexical nor dense retrieval alone is enough for
this task. A strong reranker should be judged not only by the first positive but
by whether it can order a diverse pool of relevant biomedical abstracts above
near misses.

### Query Type Tendencies

Queries are usually short Japanese health phrases, sometimes layperson-style and
sometimes technical. Common types include nutrients and foods, diseases,
chemicals, environmental toxins, named studies, medical ethics, diet claims,
probiotics, cancer-risk questions, and public-health burden terms. BM25 is most
valuable when the query contains a literal biomedical term or named study.
Dense is stronger when a short consumer phrase maps to technical abstract
language or when the same biomedical concept appears under different wording.
Hybrid matters for queries such as food-risk or intervention questions, where
both the visible term and the broader health relationship define relevance.

### Representative Failure Modes

BM25 can over-rank abstracts that merely mention a visible food, nutrient, or
disease without addressing the same clinical finding, population, intervention,
or outcome. Dense can over-rank abstracts in the same biomedical neighborhood
while losing the exact compound, organism, study name, or exposure. For example,
a query about "飽和脂肪" can attract many diet or cardiovascular abstracts, but
only some match the judged relevance set. A query about "有毒植物" or
"内分泌かく乱物質" can retrieve toxicity-related abstracts that are semantically
nearby but not qrels-positive. These failures are domain-neighbor errors rather
than random retrieval failures.

### Japanese-Specific Notes

The Japanese text is translated biomedical content, so systems must handle a
mixed register: short Japanese health phrases, transliterated biomedical terms,
English study names, chemical names, and formal abstract-style Japanese.
Tokenization affects compounds such as nutrient names and disease names. Dense
models help bridge lay terms to technical abstract language, but may smooth away
rare transliterations or English-like biomedical strings. Good systems should
preserve exact terms while still matching Japanese paraphrases of health
concepts.

### Training and Leakage Notes

Training should avoid NFCorpus, BEIR/NanoBEIR evaluation material, and
overlapping translated biomedical abstracts. Useful non-overlapping sources
include Japanese biomedical IR, clinical abstract retrieval, nutrition QA,
consumer-health search logs, and multilingual medical retrieval data. When
reporting model results, it is important to state whether the model saw NFCorpus,
BEIR, biomedical abstracts from the same source pool, or synthetic data derived
from those abstracts, because the query phrases and positives are highly
domain-specific.

### Model Improvement Hints

The task rewards biomedical lexical-semantic fusion. A first-stage retriever
should keep exact terminology for chemicals, foods, nutrients, study names, and
diseases, while dense similarity should broaden recall to abstracts that express
the same health relationship differently. Rerankers should be trained with hard
negatives that share the same food, disease, toxin, or intervention but differ
in outcome, population, or claim. Synthetic data is most useful when it creates
short Japanese health queries from non-evaluation abstracts and includes
near-topic biomedical negatives rather than generic unrelated negatives.

### Training Data That May Help

Useful training data includes non-overlapping biomedical IR, nutrition QA,
clinical abstract retrieval, and Japanese or multilingual health retrieval.
Training should exclude NFCorpus, BEIR, NanoBEIR, and overlapping medical
abstracts.

### Synthetic Data Guidance

Generate Japanese health search phrases from non-evaluation biomedical
abstracts. Include short layperson queries and technical queries, with hard
negatives that share symptoms, foods, or organisms but address a different
finding.

## Example Data

| Query | Positive document |
| --- | --- |
| ヘルシーなチョコレートミルクシェイク (18 chars) | 目的 痛風患者におけるサクランボの摂取と再発性痛風発作リスクとの関連を検討すること。 方法 一連の疑似的なリスク因子と再発性痛風発作との関連を調査するために、ケースクロスオーバー研究を実施した。痛風患者を前向きにオンラインで登録し、1年間追跡した。参加者には、痛風発作が発生した際に、発作の発症日、症状および徴候、薬物（痛風治療薬を含む）、および発作発生前の2日間における潜在的なリスク因子（サクランボおよびサクランボ抽出物の1日あたりの摂取を含む） ... [truncated 225 chars](701 chars) |
| 医学倫理 (4 chars) | 背景：食事介入による血清コレステロールの管理において、主要な課題の一つは患者の服従性を高める必要性である。 目的：コレステロール低下食事の服従における障壁や動機に関する多くの疑問を検討すること。 方法：高コレステロール血症患者に対するフランスの一般医の食事指導実態を調査し、患者のそのようなアプローチに対する態度を検討した。 結果：医師234名の個人用アンケートおよび患者356名の自己記入式アンケートを分析した。患者が処方された食事に従わない理由に ... [truncated 225 chars](786 chars) |
| ファバ豆 (4 chars) | 過去20年間、L-アルギニンの生化学、栄養学および薬理学に対する関心が高まり、その栄養的および治療的役割について、人間の代謝障害の予防および治療における広範な研究が行われてきた。最近の証拠は、食事によるL-アルギニンの補給が、遺伝的に肥満なラット、食餌誘導性肥満ラット、肥育用ブタ、および2型糖尿病を有する肥満人間において、体脂肪量を減少させることを示している。L-アルギニンの有益な効果をもたらすメカニズムはおそらく複雑であるが、最終的にはエネルギ ... [truncated 225 chars](537 chars) |
| チキンナゲットには実際に何が入っているのか？ (22 chars) | 目的：2つの全国的なフードチェーンで提供されるチキンナゲットの内容物を明らかにすること。 背景：チキンナゲットはアメリカ人の食生活の主要な構成要素となっている。我々は、この高度に加工された食品の現在の構成を明らかにすることを試みた。 方法：2つの異なる全国チェーンから無作為に選ばれたチキンナゲットをホルマリンで固定し、切片を作成して顕微鏡的分析のために染色した。 結果：どちらのナゲットにおいても、横紋筋（鶏肉）が主要な成分ではなかった。脂肪は同量 ... [truncated 225 chars](365 chars) |
| 飽和脂肪 (4 chars) | 妊娠中の母親の食事摂取が小児のアレルギー性疾患の発症に影響を与える可能性についての関心が高まっている。本研究は、妊娠中の特定の脂肪酸を多く含む食品および特定の脂肪酸の摂取が、3〜4か月齢の日本の乳児における疑わしいアトピー性皮膚炎のリスクに与える影響を前向きに検討したものである。対象は771組の母子である。妊娠中の母親の食事摂取に関する情報は、妥当性が確認された自己記入式の食歴調査票を用いて評価した。「疑わしいアトピー性皮膚炎」という用語は、出産 ... [truncated 225 chars](839 chars) |


### Public Sources

- [NFCorpus: A Full-Text Learning to Rank Dataset for Medical Information Retrieval](https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-ja](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ja)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| NFCorpus: A Full-Text Learning to Rank Dataset for Medical Information Retrieval | 2016 | task paper | https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | https://arxiv.org/abs/2104.08663 |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | https://arxiv.org/abs/2502.13595 |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | https://huggingface.co/collections/zeta-alpha-ai/nanobeir |
