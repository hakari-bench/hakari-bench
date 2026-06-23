# MNanoBEIR / NanoBEIR-ja / NanoNFCorpus

## Overview

NanoBEIR-ja / NanoNFCorpus is a Japanese biomedical retrieval task derived from
NFCorpus, the full-text medical information retrieval dataset introduced for
learning-to-rank research and later used in BEIR. The original NFCorpus task is
not a single-answer encyclopedia search problem. It asks a retrieval system to
surface biomedical abstracts relevant to short health, nutrition, and medical
information needs, often with many relevant documents for the same query. This
Nano task keeps that broad relevance structure in Japanese translated form: 50
short Japanese health queries retrieve from 2,953 Japanese biomedical abstracts,
with 1,651 positive qrel rows. The task is therefore useful for studying
biomedical candidate discovery under heavy multi-positive relevance. BM25
captures literal biomedical terminology, dense retrieval captures broader
embedding similarity, and `reranking_hybrid` gives the strongest combined view
by preserving both exact terms and semantic near matches.

## Details

### What the Original Data Measures

[NFCorpus: A Full-Text Learning to Rank Dataset for Medical Information
Retrieval](https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf)
introduced NFCorpus for medical information retrieval over full-text and
abstract-like biomedical material. BEIR later included NFCorpus as one of its
heterogeneous zero-shot retrieval tasks. In that setting, the system retrieves
documents relevant to health claims, nutrition questions, diseases, chemicals,
interventions, and biomedical findings.

The task measures relevance to an information need rather than answer extraction
from a known article. A relevant abstract may discuss a matching intervention,
condition, exposure, population, or outcome, and there can be many relevant
documents for a single query. The Japanese NanoBEIR version keeps this task
shape while translating the query/document surface into Japanese, so it tests
both biomedical terminology preservation and Japanese semantic matching.

### Observed Data Profile

The task metadata records 50 queries, 2,953 documents, and 1,651 positive qrels.
It is highly multi-positive: 47 of 50 queries have more than one positive
document, with an average of 33.02 positives per query and a maximum of 100.
Queries are very short, averaging 11.16 characters. Documents are much longer
than the MIRACL-style Japanese passage tasks, averaging 655.83 characters, and
usually read like translated biomedical abstracts with objectives, methods,
results, and conclusions.

This shape changes how the scores should be interpreted. A top-100 ranking can
contain useful relevant abstracts while still covering only a modest fraction of
all judged positives. The task is less about finding one exact page and more
about ranking a diverse set of biomedical evidence. The strongest systems need
to keep exact food, nutrient, disease, chemical, and study names, while also
matching lay health phrases to technical abstract language.

### BM25 Evaluation Profile

The BM25 candidate subset reaches nDCG@10 = 0.2414, hit@10 = 0.5800, and
Recall@100 = 0.1514. BM25 is useful because many queries contain visible
biomedical anchors: foods, nutrients, compounds, diseases, toxins, named
studies, and short clinical phrases. When those strings appear in the abstract,
term-frequency and exact-match signals can recover relevant documents directly.

Its weakness is that biomedical relevance is rarely exhausted by literal word
overlap. Two abstracts can discuss the same health relationship with different
technical terms, and a query can be layperson-like while the document is
academic. BM25 can also over-rank abstracts that mention the same food,
chemical, or disease but answer a different intervention, population, or
outcome. In this task, BM25 should be understood as the lexical anchor signal:
important, but incomplete for broad biomedical relevance.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` reaches nDCG@10 = 0.2368,
hit@10 = 0.6600, and Recall@100 = 0.1787. Dense retrieval has slightly lower
nDCG@10 than BM25, but it finds at least one positive in the top 10 for more
queries and covers more positives by top 100. This indicates that embedding
similarity is better at broad biomedical candidate discovery for this Japanese
translation setting.

Dense retrieval is especially helpful when a short Japanese query maps to
abstract language with different wording: diet and disease relations, exposure
and risk, probiotic effects, nutrient intake, or study outcomes. Its failure
mode is under-anchoring. It can drift toward nearby medical topics while losing
the exact compound, organism, food, study name, or exposure that defines the
query. For model researchers, the dense profile shows the value of semantic
matching, but also the need to preserve rare biomedical surface forms.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset reaches nDCG@10 = 0.2757, hit@10 =
0.6800, and Recall@100 = 0.1926. It is the strongest of the three candidate
views on all visible aggregate metrics. The hybrid pool emulates practical
hybrid search: use BM25 to retain literal biomedical anchors and dense retrieval
to collect semantically related abstracts that lexical search can miss.

This is the most useful candidate set for reranker experiments. It still
contains realistic distractors from both retrieval families, but it gives the
reranker a better chance to see diverse relevant abstracts. The metadata also
shows a small rank-101 safeguard for some queries, which is expected in a
multi-positive dataset where preserving positives can matter even after
combining candidate sources.

### Metric Interpretation for Model Researchers

NanoNFCorpus should be read as multi-positive biomedical retrieval, not
single-positive fact lookup. nDCG@10 rewards systems that put useful relevant
abstracts near the top. Recall@100 is constrained by the large number of judged
positives per query, so absolute recall values are much lower than in
single-answer tasks. A model can be practically useful even when Recall@100
looks numerically modest, because there may be dozens of relevant abstracts.

The BM25 and dense contrast is informative. BM25 slightly leads dense on
nDCG@10, meaning literal terminology can place highly relevant abstracts near
the top. Dense leads BM25 on hit@10 and Recall@100, meaning semantic similarity
finds positives across more queries and broader terminology. The hybrid result
leading all three metrics suggests that this task rewards lexical-semantic
fusion. A strong retriever should not choose between exact biomedical terms and
embedding similarity; it should preserve both.

### Query and Relevance Type Tendencies

Queries are short Japanese health phrases. They include foods, nutrients,
diseases, toxic exposures, medical ethics, dietary claims, named studies,
probiotics, cancer-risk topics, and public-health burden concepts. Some queries
are technical, while others look like consumer health searches. Documents are
translated biomedical abstracts, so they often contain formal phrases,
measurement language, population descriptions, and study design terminology.

BM25 is strongest when the query contains a literal biomedical string that
appears in relevant abstracts. Dense is strongest when the same concept is
expressed with different wording or when a lay phrase needs to match technical
language. Hybrid is strongest when both constraints hold: the candidate must
preserve a visible food, compound, disease, or study anchor, but relevance
depends on a broader health relationship.

### Representative Failure Modes

BM25 can retrieve abstracts that share an obvious term but do not match the
judged claim. A query about a nutrient can attract many nutrition abstracts that
mention the term without addressing the same outcome. A query about a disease
can retrieve broad disease background material instead of the specific
intervention or exposure. Dense retrieval can make the opposite mistake by
ranking semantically nearby biomedical abstracts that omit the exact entity,
compound, food, or study name.

The hardest negatives are usually not unrelated documents. They are
near-domain abstracts: the same disease but a different treatment, the same food
but a different outcome, the same toxin family but a different exposure, or the
same study type but a different population. These are valuable hard negatives
for reranking and for training hybrid retrievers.

### Japanese-Specific Notes

The Japanese text is translated biomedical content, so it mixes consumer health
phrases, formal abstract style, transliterated terms, English study names,
chemical names, disease names, and domain-specific compounds. Tokenization
affects whether nutrient names and disease compounds remain searchable. Sparse
retrieval needs segmentation that preserves biomedical terms. Dense retrieval
helps bridge Japanese paraphrases and academic wording, but may smooth away
rare transliterations or English-like biomedical strings.

Good Japanese biomedical retrievers should normalize harmless surface variation
without collapsing important terminology. They also need to handle very short
queries whose intent is underspecified unless the model understands health
search conventions and biomedical context.

### Training and Leakage Notes

Training should avoid NFCorpus, BEIR/NanoBEIR evaluation material, and
overlapping translated biomedical abstracts. Because the task has many positives
per query, leakage can occur through either the query phrase or any of many
positive abstracts. Reports should disclose whether a model saw NFCorpus, BEIR,
NanoBEIR, biomedical abstracts from the same source pool, Japanese biomedical
QA, or synthetic data generated from related abstracts.

Non-overlapping biomedical retrieval data can still be useful, but source
overlap should be audited. In particular, synthetic question generation from
the same evaluation abstracts would make scores difficult to interpret.

### Model Improvement Hints

A strong first-stage retriever should combine biomedical exact matching with
semantic expansion. Sparse features should retain chemicals, foods, nutrients,
study names, disease names, and organisms. Dense features should connect short
Japanese health phrases to technical abstract language and to paraphrased
biomedical relationships. Rerankers should be trained on near-domain negatives
that share the visible term but differ in claim, population, intervention, or
outcome.

Because the task is highly multi-positive, training and evaluation should not
focus only on the first relevant document. Models should learn to rank multiple
relevant abstracts above plausible but non-relevant neighbors.

### Training Data That May Help

Useful training sources include non-overlapping Japanese biomedical retrieval,
clinical abstract retrieval, nutrition QA, multilingual medical IR, consumer
health search data, and Japanese biomedical question-to-abstract pairs. Data
should include both technical and layperson-style queries. For reranking,
same-topic hard negatives are more valuable than random negatives because the
benchmark's errors usually happen inside the biomedical neighborhood.

### Synthetic Data Guidance

Generate short Japanese health search phrases from non-evaluation biomedical
abstracts. Cover foods, nutrients, disease risk, interventions, exposures,
toxins, probiotics, study outcomes, and public-health concepts. Synthetic
documents should remain abstract-like and include objective, method, result, and
conclusion phrasing when appropriate. Hard negatives should share symptoms,
foods, diseases, chemicals, or organisms but address a different finding.

## Example Data

| Query | Positive document |
| --- | --- |
| ヘルシーなチョコレートミルクシェイク [18 chars] | 目的 痛風患者におけるサクランボの摂取と再発性痛風発作リスクとの関連を検討すること。 方法 一連の疑似的なリスク因子と再発性痛風発作との関連を調査するために、ケースクロスオーバー研究を実施した。痛風患者を前向きにオンラインで登録し、1年間追跡した。参加者には、痛風発作が発生した際に、発作の発症日、症状および徴候、薬物（痛風治療薬を含む）、および発作発生前の2日間における潜在的なリスク因子（サクランボおよびサクランボ抽出物の1日あたりの摂取を含む）に関する情報を報告してもらった。同じ曝露情報について、対照期間としての2日間についても評価した。条件付きロジスティック回帰を用いて、サクランボ摂取に関連した再発性痛風発作のリスクを推定した。 結果 本研究には633名の痛風患者が含まれた。2日間の期間におけるサクランボ摂取は、摂取なしと比較して痛風発作リスクを35％低下させる関連が認められた（多変量オッズ比[OR] = 0.65、95％信頼区間[CI]：0.50–0.85）。サクランボ抽出物の摂取も同様に逆相関を示した（多変量OR = 0.55、95％CI：0.30–0.98）。サクランボ摂取の効果は、性別、肥満の有無、プリン体摂取量、アルコール摂取、利尿薬の使用、痛風治療薬の使用といったサブグループ間で一貫して認められた。サクランボ摂取とアロプリノール使用を併用した場合、いずれの曝露もない期間と比較して痛風発作リスクは75％低下した（OR = 0.25、95％CI：0.15–0.42）。 結論 これらの知見は、サクランボの摂取が痛風発作リスクの低下と関連していることを示唆している。 [701 chars] |
| 医学倫理 [4 chars] | 背景：食事介入による血清コレステロールの管理において、主要な課題の一つは患者の服従性を高める必要性である。 目的：コレステロール低下食事の服従における障壁や動機に関する多くの疑問を検討すること。 方法：高コレステロール血症患者に対するフランスの一般医の食事指導実態を調査し、患者のそのようなアプローチに対する態度を検討した。 結果：医師234名の個人用アンケートおよび患者356名の自己記入式アンケートを分析した。患者が処方された食事に従わない理由には、「すでに満足のいく食習慣を持っている」（34.7％）、「栄養的制限を受けることを望まない」（33.3％）、「家族生活と食事療法の両立が難しい」（27.8％）、「コレステロール低下薬を服用している」（22.2％）などが挙げられた。患者は医師の指示を一般的によく理解しているにもかかわらず、双方の回答の間にいくつかの不一致が見られた。医師の多くは、患者が食事がコレステロールを低下させ（薬の服用を回避する）理由や方法についてより詳しい説明を必要としていると考えたが、実際にそのような情報が必要だと回答した患者は39.4％にとどまった。また、患者の服従に関する障壁や動機についても、同様の不一致が認められた。さらに、一部の食事指導は他のものより遵守が難しいようであった。例えば、「魚をもっと食べる」ことを82.6％の患者が覚えていたが、実際に実行しているのは51.3％に過ぎなかった。最後に、医師も患者も、脂質低下食の有効性に対して十分な信頼を示していなかった。 結論：患者教育の充実、特にリスクに対する認識の改善、および栄養士の関与の強化は、服従性を高めるために検討すべき動機である。 Copyright © 2012 Elsevier Masson SAS. All rights reserved. [786 chars] |
| ファバ豆 [4 chars] | 過去20年間、L-アルギニンの生化学、栄養学および薬理学に対する関心が高まり、その栄養的および治療的役割について、人間の代謝障害の予防および治療における広範な研究が行われてきた。最近の証拠は、食事によるL-アルギニンの補給が、遺伝的に肥満なラット、食餌誘導性肥満ラット、肥育用ブタ、および2型糖尿病を有する肥満人間において、体脂肪量を減少させることを示している。L-アルギニンの有益な効果をもたらすメカニズムはおそらく複雑であるが、最終的にはエネルギーの摂取と消費のバランスを、脂肪の減少または白色脂肪組織の成長抑制に有利な方向へと変化させることに関与していると考えられる。最近の研究では、L-アルギニンの補給が、細胞内シグナル伝達分子（例えば一酸化窒素、一酸化炭素、ポリアミン、cGMP、cAMPなど）の合成促進および全身のエネルギー基質（例えばグルコースおよび脂肪酸）の酸化を促進する遺伝子の発現増加を通じて、ミトコンドリアの新生および褐色脂肪組織の発達を刺激する可能性があることが示されている。したがって、L-アルギニンは、動物および人間において体脂肪を減少させ、筋肉量を増加させ、代謝プロファイルを改善する安全で費用対効果の高い栄養素として大きな可能性を秘めている。 [537 chars] |

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
| NFCorpus: A Full-Text Learning to Rank Dataset for Medical Information Retrieval | 2016 | task paper | [https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf](https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf) |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | [https://arxiv.org/abs/2104.08663](https://arxiv.org/abs/2104.08663) |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | [https://arxiv.org/abs/2502.13595](https://arxiv.org/abs/2502.13595) |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | [https://huggingface.co/collections/zeta-alpha-ai/nanobeir](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
