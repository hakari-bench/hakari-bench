# MNanoBEIR / NanoBEIR-ja / NanoSciFact

## Overview

`NanoBEIR-ja__NanoSciFact` is the Japanese NanoBEIR version of SciFact, a
scientific claim verification retrieval benchmark. The task uses Japanese
translated scientific claims as queries and asks a retriever to rank Japanese
translated abstracts that provide evidence for support or refutation. The Nano
split contains 50 queries, 2,919 documents, and 56 positive qrels. Most queries
have one positive, while 4 queries have multiple positives. This is a
claim-to-evidence task rather than a related-paper task: the model must find
the abstract whose experimental finding bears on a specific scientific claim.

## Details

### What the Original Data Measures

[Fact or Fiction: Verifying Scientific Claims](https://arxiv.org/abs/2004.14974)
introduced SciFact as expert-written scientific claims paired with evidence
abstracts, support/refute labels, and rationales. BEIR evaluates the retrieval
component: before a verifier can decide whether a claim is supported or refuted,
the system must retrieve the relevant abstract. In this Japanese NanoBEIR
version, the evidence retrieval problem is tested through translated
biomedical and scientific claims and translated abstracts.

### Observed Data Profile

The task has 50 queries and 2,919 documents. It contains 56 positive qrels,
with 1.12 positives per query on average. The positives-per-query distribution
is 1 minimum, 1.00 median, and 4 maximum, and only 8.0% of queries are
multi-positive. Queries average 40.58 characters, while documents average
633.08 characters. The examples cover neutrophil migration, antiretroviral
therapy, interferon-induced genes, cervical cancer screening, and TDP-43
interactions. Claims are concise but terminology-heavy, and abstracts contain
the experimental context needed for verification.

### BM25 Evaluation Profile

The BM25 top-500 subset reaches nDCG@10 = 0.7023, hit@10 = 0.8600, and
Recall@100 = 0.9464. BM25 is very strong because scientific claims often repeat
distinctive entities, proteins, diseases, interventions, or outcome terms that
also appear in the evidence abstract. Exact terminology is highly predictive in
this task. The limitation is that evidence may use abbreviations, different
phrasing, or broader experimental descriptions, so lexical matching alone does
not always produce the best ranked evidence.

### Dense Evaluation Profile

The dense `harrier-oss-270m` top-500 subset reaches nDCG@10 = 0.6751, hit@10 =
0.7800, and Recall@100 = 0.8750. Dense retrieval is competitive but below BM25
on all reported metrics. This suggests that general embedding similarity helps
with scientific paraphrase, but it can lose the precise biomedical anchors that
matter for claim verification. In SciFact, small entity and relation differences
can change whether an abstract verifies a claim, so broad semantic relatedness
is not enough.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses 100 to 101 candidates per query and reaches
nDCG@10 = 0.7232, hit@10 = 0.8400, and Recall@100 = 0.9286. Four queries use
the rank-101 safeguard. Hybrid retrieval has the best nDCG@10, while BM25 has
the best hit@10 and Recall@100. This means lexical retrieval gives the broadest
candidate coverage for this split, but hybrid fusion improves the ordering of
the highest-ranked evidence when lexical and semantic signals reinforce each
other.

### Metric Interpretation for Model Researchers

This task is a strong reminder that scientific claim retrieval is not always
dense-dominant. BM25 performs extremely well because exact biomedical terms are
central to relevance. Dense retrieval alone can underperform when it blurs
nearby scientific concepts. `reranking_hybrid` gives the best nDCG@10, so
combining exact terminology with semantic evidence matching is valuable, but
models should not discard lexical anchors. Improvements should preserve entity,
intervention, and outcome specificity.

### Query and Relevance Type Tendencies

Queries are atomic scientific claims. Relevant documents are abstracts that
describe experiments, observations, or findings related to the claim. Many
queries involve genes, proteins, viruses, therapies, or clinical endpoints.
Relevance depends on the exact scientific relation, not merely on topic
overlap. A passage about the same disease or molecule can be a hard negative if
it does not address the claim's assertion.

### Representative Failure Modes

BM25 can over-rank abstracts that repeat the right terms but describe a
different finding. Dense retrieval can over-rank semantically related abstracts
from the same biomedical area while missing the exact evidence. Hybrid retrieval
can improve nDCG but still miss candidate coverage compared with BM25 when the
semantic side adds noisy related documents. Retrieval errors are costly because
a downstream verifier cannot support or refute a claim without the evidence
abstract.

### Training Data That May Help

Useful training data includes non-overlapping scientific fact verification,
claim-evidence retrieval, biomedical abstract retrieval, and Japanese or
multilingual scientific NLI. Hard negatives should share terminology with the
claim but differ in the actual finding, intervention, or outcome. Training
should exclude SciFact, BEIR, NanoBEIR, and overlapping translated abstracts
from this benchmark.

### Model Improvement Notes

Strong systems should combine exact biomedical term handling with claim-level
semantic matching. Rerankers should attend to relation direction, experimental
context, and whether the abstract actually bears on the claim. For this task,
lexical recall is a high-value baseline, and dense models should be trained not
to smooth away scientific specificity.

## Example Data

| Query | Positive document |
| --- | --- |
| Ly49Qは、膜ラフト機能を制御することにより、好中球の炎症部位への移動の組織化を指示する。 [46 chars] | 好中球は感染部位や炎症部位へ迅速に浸潤するために、急速に偏極化し、方向性のある運動を行う。本研究では、阻害性MHC I受容体であるLy49Qが好中球の迅速な偏極化および組織への浸潤に不可欠であることを示した。恒常状態では、Ly49QはおそらくSrcキナーゼおよびPI3キナーゼの活性を阻害することにより、局在複合体の形成を妨げ、好中球の接着を抑制していた。しかし、炎症刺激が存在する状況では、Ly49QはITIMドメインに依存的に好中球の迅速な偏極化および組織浸潤を媒介した。これらの相反する機能は、エフェクターであるホスファターゼSHP-1およびSHP-2の異なる利用によって生じているようであった。Ly49Q依存的な偏極化および遊走は、Ly49Qによる膜ラフト機能の制御に影響されていた。我々は、Ly49Qが膜ラフトおよびそれに関連するシグナル伝達分子の時空間的制御を通じて、炎症時に好中球を偏極化形態および急速な遊走へと切り替える上で極めて重要であると提唱する。 [434 chars] |
| 抗レトロウイルス療法は、広範なCD4層において結核の発生率を低下させる。 [36 chars] | 背景 ヒト免疫不全ウイルス（HIV）感染は結核発症の最も強い危険因子であり、特にサブサハラ以南のアフリカで結核の再燃を助長している。2010年には、世界中でHIVに感染している推定3,400万人のうち、110万人が新たに結核を発症した。抗レトロウイルス療法（ART）はHIV関連結核の予防に大きな可能性を有している。我々は、HIV感染成人における結核発生率に対する抗レトロウイルス療法の影響を分析した研究について系統的レビューを行った。 方法および結果 PubMed、Embase、African Index Medicus、LILACS、および臨床試験登録データベースを系統的に検索した。無作為化対照試験、前向きコホート研究、後ろ向きコホート研究のうち、発展途上国においてHIV感染成人の抗レトロウイルス療法の有無による結核発生率を比較し、中央値で6か月以上追跡した研究を対象とした。メタアナリシスでは、抗レトロウイルス療法開始時のCD4細胞数に基づき4つのカテゴリーに分類した：（1）200細胞/µl未満、（2）200～350細胞/µl、（3）350細胞/µl超、（4）CD4細胞数不問。11の研究が選択基準を満たした。抗レトロウイルス療法は、すべてのベースラインCD4細胞数カテゴリーにおいて結核発生率の大幅な低下と強く関連していた：（1）200細胞/µl未満（ハザード比[HR] 0.16、95％信頼区間[CI] 0.07～0.36）、（2）200～350細胞/µl（HR 0.34、95％CI 0.19～0.60）、（3）350細胞/µl超（HR 0.43、95％CI 0.30～0.63）、（4）CD4細胞数不問（HR 0.35、95％CI 0.28～0.44）。ベースラインCD4細胞数カテゴリーによるハザード比の修飾効果は認められなかった（p = 0.20）。 結論 抗レトロウイルス療法は、すべてのCD4細胞数層において結核発生率の低下と強く関連している。抗レトロウイルス療法の早期開始は、HIV関連結核の重複的流行（syndemic）を制御するための国際的および国家的戦略の重要な要素となる可能性がある。 レビュー登録 国際系統的レビュー登録施設 CRD42011001209 編集者による要約は、記事の後半に掲載されている。 [992 chars] |
| インターフェロン誘導性遺伝子の急速な上昇調節およびより高い基礎的発現は、ウエストナイルウイルスに感染した顆粒細胞ニューロンの生存を低下させる。 [71 chars] | 脳内の神経細胞が微生物感染に対して感受性を示すことは、臨床的転帰を左右する主要な要因であるが、この感受性を制御する分子的因子についてはほとんど分かっていない。本研究では、異なる脳領域に由来する2種類の神経細胞が、いくつかの正鎖RNAウイルスの複製に対して異なる許容性を示すことを明らかにした。小脳の顆粒細胞および大脳皮質の皮質神経細胞は、それぞれ独自の自然免疫プログラムを有しており、これによりウイルス感染に対する感受性が、ex vivoおよびin vivoにおいて異なっていた。顆粒細胞でより高発現している遺伝子を皮質神経細胞に導入することにより、複数の神経向性ウイルスに対して抗ウイルス作用を示す3つのインターフェロン刺激遺伝子（ISG；Ifi27、Irg1およびRsad2（別名Viperin））を同定した。さらに、ISGのエピジェネティックな状態およびmicroRNA（miRNA）による制御が、顆粒細胞での抗ウイルス応答の増強と相関していることが分かった。したがって、進化的に異なる脳領域に由来する神経細胞はそれぞれ独自の自然免疫シグネチャーを有しており、これが感染に対する相対的許容性に寄与していると考えられる。 [512 chars] |

### Public Sources

- [Fact or Fiction: Verifying Scientific Claims](https://arxiv.org/abs/2004.14974).
- [SciFact repository](https://github.com/allenai/scifact).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).
- [hakari-bench/NanoBEIR-ja](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ja).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Fact or Fiction: Verifying Scientific Claims | 2020 | task paper | [https://arxiv.org/abs/2004.14974](https://arxiv.org/abs/2004.14974) |
| SciFact repository |  | project page | [https://github.com/allenai/scifact](https://github.com/allenai/scifact) |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | [https://arxiv.org/abs/2104.08663](https://arxiv.org/abs/2104.08663) |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | [https://arxiv.org/abs/2502.13595](https://arxiv.org/abs/2502.13595) |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | [https://huggingface.co/collections/zeta-alpha-ai/nanobeir](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
