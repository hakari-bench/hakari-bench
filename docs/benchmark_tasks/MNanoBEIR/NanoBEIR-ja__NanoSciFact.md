# MNanoBEIR / NanoBEIR-ja / NanoSciFact

## Overview

SciFact is a scientific claim verification dataset. `NanoBEIR-ja__NanoSciFact`
uses Japanese translated scientific claims to retrieve Japanese translated
abstracts that support or refute them.

## Details

### What the Original Data Measures

[Fact or Fiction: Verifying Scientific Claims](https://arxiv.org/abs/2004.14974)
introduced SciFact as expert-written scientific claims with evidence abstracts,
support/refute labels, and rationales. BEIR includes SciFact as fact-checking
retrieval, and MMTEB supplies the multilingual context.

### Observed Data Profile

The sampled task has 50 queries, 2,919 documents, and 56 positive qrels. Most
queries have one positive, while 4 queries have multiple positives. Queries
average 40.58 characters and documents average 633.08 characters.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.7023 and hit@10 = 0.8600. Technical terms often repeat
between claim and abstract, but evidence retrieval still needs to handle
abbreviations, biomedical phrasing, and experimental context.

### Training Data That May Help

Useful data includes non-overlapping scientific fact verification,
claim-evidence retrieval, biomedical abstract retrieval, and Japanese or
multilingual scientific NLI. Exclude SciFact, BEIR, NanoBEIR, and overlapping
abstracts.

### Synthetic Data Guidance

Generate Japanese atomic scientific claims from non-evaluation abstracts. Pair
them with evidence-bearing abstracts and use hard negatives from the same
discipline that share terminology but not the finding.

## Example Data

| Query | Positive document |
| --- | --- |
| Ly49Qは、膜ラフト機能を制御することにより、好中球の炎症部位への移動の組織化を指示する。 (46 chars) | 好中球は感染部位や炎症部位へ迅速に浸潤するために、急速に偏極化し、方向性のある運動を行う。本研究では、阻害性MHC I受容体であるLy49Qが好中球の迅速な偏極化および組織への浸潤に不可欠であることを示した。恒常状態では、Ly49QはおそらくSrcキナーゼおよびPI3キナーゼの活性を阻害することにより、局在複合体の形成を妨げ、好中球の接着を抑制していた。しかし、炎症刺激が存在する状況では、Ly49QはITIMドメインに依存的に好中球の迅速な偏極化 ... [truncated 225 chars](434 chars) |
| 抗レトロウイルス療法は、広範なCD4層において結核の発生率を低下させる。 (36 chars) | 背景 ヒト免疫不全ウイルス（HIV）感染は結核発症の最も強い危険因子であり、特にサブサハラ以南のアフリカで結核の再燃を助長している。2010年には、世界中でHIVに感染している推定3,400万人のうち、110万人が新たに結核を発症した。抗レトロウイルス療法（ART）はHIV関連結核の予防に大きな可能性を有している。我々は、HIV感染成人における結核発生率に対する抗レトロウイルス療法の影響を分析した研究について系統的レビューを行った。 方法および結 ... [truncated 225 chars](992 chars) |
| インターフェロン誘導性遺伝子の急速な上昇調節およびより高い基礎的発現は、ウエストナイルウイルスに感染した顆粒細胞ニューロンの生存を低下させる。 (71 chars) | 脳内の神経細胞が微生物感染に対して感受性を示すことは、臨床的転帰を左右する主要な要因であるが、この感受性を制御する分子的因子についてはほとんど分かっていない。本研究では、異なる脳領域に由来する2種類の神経細胞が、いくつかの正鎖RNAウイルスの複製に対して異なる許容性を示すことを明らかにした。小脳の顆粒細胞および大脳皮質の皮質神経細胞は、それぞれ独自の自然免疫プログラムを有しており、これによりウイルス感染に対する感受性が、ex vivoおよびin ... [truncated 225 chars](512 chars) |
| HPV検出を用いた子宮頸がんの一次スクリーニングは、子宮頸部上皮内腫瘍2度を検出するための従来の細胞診よりも縦断的感度が高い。 (63 chars) | 背景 人乳頭腫瘍ウイルス（HPV）検査に基づく子宮頸がんスクリーニングは、高度（グレード2または3）の子宮頸部上皮内腫瘍の検出感度を高めるが、この感度の向上が過剰診断を意味するのか、それとも将来の高度子宮頸部上皮内腫瘍または子宮頸がんに対する保護を意味するのかは不明である。 方法 スウェーデンの集団ベースのスクリーニングプログラムにおいて、32〜38歳の女性12,527人を1：1の割合で無作為に割り付け、HPV検査と子宮頸細胞診（Pap検査）の両 ... [truncated 225 chars](951 chars) |
| TDP-43と呼吸鎖複合体Iのタンパク質ND3およびND6との相互作用を阻害すると、TDP-43誘導性の神経細胞死が増加する。 (63 chars) | TAR DNA結合タンパク質43（TARDBP、別名TDP-43）の遺伝的変異は筋萎縮性側索硬化症（ALS）を引き起こし、TDP-43（TARDBPがコードする）の細胞質への存在量の増加は、さまざまな神経変性疾患における変性神経細胞の顕著な組織病理学的特徴である。しかし、TDP-43がALSの病態生理にどのように寄与するかの分子機構は依然として不明である。本研究では、ALSまたは前頭側頭葉変性症（FTD）の患者において、TDP-43が神経細胞のミ ... [truncated 225 chars](593 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-ja |
| Task / split | NanoSciFact |
| Hugging Face dataset | [hakari-bench/NanoBEIR-ja](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ja) |
| Language | ja |
| Category | natural_language |
| Queries | 50 |
| Documents | 2,919 |
| Positive qrels | 56 |
| Avg positives / query | 1.12 |
| Positives per query (min / median / max) | 1 / 1.00 / 4 |
| Queries with multiple positives | 4 (8.0%) |
| BM25 nDCG@10 | 0.7023 |
| BM25 hit@10 | 0.8600 |
| Query length avg chars | 40.58 |
| Document length avg chars | 633.08 |

### Public Sources

- [Fact or Fiction: Verifying Scientific Claims](https://arxiv.org/abs/2004.14974).
- [SciFact repository](https://github.com/allenai/scifact).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-ja](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ja)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Fact or Fiction: Verifying Scientific Claims | 2020 | task paper | https://arxiv.org/abs/2004.14974 |
| SciFact repository |  | project page | https://github.com/allenai/scifact |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | https://arxiv.org/abs/2104.08663 |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | https://arxiv.org/abs/2502.13595 |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | https://huggingface.co/collections/zeta-alpha-ai/nanobeir |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: MNanoBEIR
  backing_dataset: NanoBEIR-ja
  dataset_id: hakari-bench/NanoBEIR-ja
  task_name: NanoSciFact
  split_name: NanoSciFact
  language: ja
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-ja__NanoSciFact.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 50
    documents: 2919
    positive_qrels: 56
  positives_per_query:
    average: 1.12
    min: 1
    median: 1.0
    max: 4
    multi_positive_queries: 4
    multi_positive_query_percent: 8.0
  text_stats_chars:
    query_mean: 40.58
    document_mean: 633.084275
  bm25:
    ndcg_at_10: 0.7022625445
    hit_at_10: 0.86
    source: dataset_bm25_column
```
