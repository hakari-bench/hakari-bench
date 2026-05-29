# MNanoBEIR / NanoBEIR-de / NanoSciFact

## Overview

SciFact is a scientific claim verification dataset. `NanoBEIR-de__NanoSciFact`
is the German MNanoBEIR version: German translated scientific claims must
retrieve German translated abstracts that support or refute the claim. The task
tests evidence retrieval in research literature with domain-specific scientific
terminology.

## Details

### What the Original Data Measures

[Fact or Fiction: Verifying Scientific Claims](https://arxiv.org/abs/2004.14974)
introduces SciFact as a dataset of expert-written scientific claims paired with
evidence-containing abstracts annotated with support or refute labels and
rationales. The paper derives claims from citation sentences, making the claims
natural assertions about scientific findings rather than generic factoid
questions.

[BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information
Retrieval Models](https://arxiv.org/abs/2104.08663) includes SciFact as a
fact-checking retrieval task. [MMTEB: Massive Multilingual Text Embedding
Benchmark](https://arxiv.org/abs/2502.13595) provides the multilingual
benchmark context for this German Nano split.

### Observed Data Profile

The sampled German Nano task has 50 queries, 2,919 documents, and 56 positive
qrel rows. Most queries have one positive abstract, while 4 queries have
multiple positives. The average query length is 110.56 characters, and the
average document length is 1,647.88 characters.

The inspected claims involve breast cancer risk, brown adipose tissue, T-cell
receptor diversity, disease models, and G-quadruplex biology. Positive documents
are translated scientific abstracts with methods, context, and results.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.5936 and hit@10 = 0.7600. BM25 ranks a positive first for 23 queries, and the
median first-positive rank is 2.

Lexical matching is often useful because scientific claims repeat technical
terms from the abstract. The harder cases require recognizing evidence that
supports or contradicts the claim despite different phrasing, abbreviations, or
experimental context. Retrieval quality should be interpreted separately from
the later support/refute classification problem.

### Training Data That May Help

Useful training data includes non-overlapping SciFact-style claim-evidence
pairs, scientific fact verification data, biomedical abstract retrieval pairs,
CORD-19 style claim retrieval, and German or multilingual scientific NLI or
evidence selection data.

Training should exclude SciFact, BEIR, NanoBEIR, or translated abstracts and
claims likely to overlap with these evaluation records.

### Synthetic Data Guidance

For document-to-query generation, start from non-evaluation scientific abstracts
and generate German claims that are supported or refuted by the abstract. Claims
should be atomic and should contain enough scientific terminology to be
verifiable.

For joint generation, create abstracts with clear findings and generate paired
claims plus hard negatives from related abstracts that mention the same disease,
gene, or intervention but do not provide the needed evidence.

## Example Data

| Query | Positive document |
| --- | --- |
| Ly49Q steuert die Organisation der Migration von Neutrophilen zu Entzündungsherden, indem es die Funktionen von Membran-Rafts reguliert. (136 chars) | Neutrophile durchlaufen eine schnelle Polarisation und gerichtete Bewegung, um Infektions- und Entzündungsherde zu infiltrieren. Wir zeigen, dass ein inhibitorischer MHC-I-Rezeptor, Ly49Q, für die schnelle Polarisation und Ge ... [truncated 225 chars](1116 chars) |
| Antiretrovirale Therapie verringert die Häufigkeit von Tuberkulose bei verschiedenen CD4-Werten. (96 chars) | HINTERGRUND Die Infektion mit dem humanen Immundefizienz-Virus (HIV) ist der stärkste Risikofaktor für die Entwicklung von Tuberkulose und hat deren Wiederauftreten, insbesondere in Subsahara-Afrika, begünstigt. Im Jahr 2010 ... [truncated 225 chars](2378 chars) |
| Eine schnelle Hochregulierung und eine höhere basale Expression von Interferon-induzierten Genen verringern die Überlebensfähigkeit von Granulazellneuronen, die mit dem West-Nil-Virus infiziert sind. (199 chars) | Obwohl die Anfälligkeit von Neuronen im Gehirn für mikrobiologische Infektionen ein entscheidender Faktor für den klinischen Verlauf ist, ist wenig über die molekularen Faktoren bekannt, die diese Anfälligkeit steuern. Hier z ... [truncated 225 chars](1264 chars) |
| Primäre Zervixkarzinom-Screening mit HPV-Nachweis weist eine höhere longitudinale Sensitivität auf als die konventionelle Zytologie zur Erkennung von Zervixintraepithelialen Neoplasien Grad 2. (192 chars) | HINTERGRUND Das Screening auf Gebärmutterhalskrebs durch HPV-Tests erhöht die Sensitivität bei der Erkennung von hochgradigen (Grad 2 oder 3) zervikalen intraepithelialen Neoplasien, aber ob dieser Gewinn Überdiagnosen darste ... [truncated 225 chars](2622 chars) |
| Die Hemmung der Interaktion zwischen TDP-43 und den Proteinen ND3 und ND6 des Atmungskomplexes I führt zu erhöhten TDP-43-induzierten neuronalen Zellschäden. (157 chars) | Genetische Mutationen im TAR-DNA-bindenden Protein 43 (TARDBP, auch bekannt als TDP-43) verursachen amyotrophe Lateralsklerose (ALS), und eine erhöhte Präsenz von TDP-43 (kodiert durch TARDBP) im Zytoplasma ist ein prominente ... [truncated 225 chars](1463 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-de |
| Task / split | NanoSciFact |
| Hugging Face dataset | [hakari-bench/NanoBEIR-de](https://huggingface.co/datasets/hakari-bench/NanoBEIR-de) |
| Language | de |
| Category | natural_language |
| Queries | 50 |
| Documents | 2,919 |
| Positive qrels | 56 |
| Avg positives / query | 1.12 |
| Positives per query (min / median / max) | 1 / 1.00 / 4 |
| Queries with multiple positives | 4 (8.0%) |
| BM25 nDCG@10 | 0.6212 |
| BM25 hit@10 | 0.7600 |
| BM25 Recall@100 | 0.8393 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.7017 |
| Dense hit@10 | 0.8400 |
| Dense Recall@100 | 0.8929 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.6577 |
| Reranking hybrid hit@10 | 0.8200 |
| Reranking hybrid Recall@100 | 0.9464 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 3 |
| Query length avg chars | 110.56 |
| Document length avg chars | 1,647.88 |

### Public Sources

- [Fact or Fiction: Verifying Scientific Claims](https://arxiv.org/abs/2004.14974); 2020; David Wadden, Shanchuan Lin, Kyle Lo, Lucy Lu Wang, Madeleine van Zuylen, Arman Cohan, Hannaneh Hajishirzi; DOI: `10.18653/v1/2020.emnlp-main.609`.
- [SciFact repository](https://github.com/allenai/scifact).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663); 2021; Nandan Thakur, Nils Reimers, Andreas Rueckle, Abhishek Srivastava, Iryna Gurevych; DOI: `10.48550/arXiv.2104.08663`.
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595); 2025; Kenneth Enevoldsen, Isaac Chung, Imene Kerboua, Marton Kardos, Ashwin Mathur, and others; DOI: `10.48550/arXiv.2502.13595`.
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-de](https://huggingface.co/datasets/hakari-bench/NanoBEIR-de)
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
  backing_dataset: NanoBEIR-de
  dataset_id: hakari-bench/NanoBEIR-de
  task_name: NanoSciFact
  split_name: NanoSciFact
  language: de
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-de__NanoSciFact.md
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
    query_mean: 110.56
    document_mean: 1647.877355
  bm25:
    ndcg_at_10: 0.621243841517917
    hit_at_10: 0.76
    source: dataset_candidate_subset
  learning:
    original_train_split: available
    evaluation_split_origin: MNanoBEIR German NanoBEIR task split from hakari-bench/NanoBEIR-de
    train_eval_overlap_audit: not_audited
    leakage_note: prefer excluding SciFact, BEIR, or NanoBEIR records likely to overlap
      with these evaluation claims or abstracts
    useful_training_data:
    - non-overlapping SciFact-style claim-evidence pairs
    - scientific fact verification data
    - biomedical abstract retrieval pairs
    - German or multilingual scientific NLI and evidence selection data
    synthetic_data:
      document_generation: German scientific abstracts with explicit findings outside
        the evaluation set
      question_generation: atomic German scientific claims supported or refuted by
        the abstract
      answerability: positives should provide evidence for or against the claim, not
        only share scientific terminology
    multi_positive_training: useful_but_not_central
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoBEIR-de
    source_urls:
    - label: SciFact paper
      url: https://arxiv.org/abs/2004.14974
    - label: SciFact repository
      url: https://github.com/allenai/scifact
    - label: BEIR paper
      url: https://arxiv.org/abs/2104.08663
    - label: MMTEB paper
      url: https://arxiv.org/abs/2502.13595
    - label: Zeta Alpha NanoBEIR collection
      url: https://huggingface.co/collections/zeta-alpha-ai/nanobeir
    source_notes:
    - German task is a multilingual NanoBEIR adaptation of the original English BEIR
      task
  references:
  - title: 'Fact or Fiction: Verifying Scientific Claims'
    url: https://arxiv.org/abs/2004.14974
    year: 2020
    doi: 10.18653/v1/2020.emnlp-main.609
    is_paper: true
    source_confidence: definitive_paper_link
  - title: SciFact repository
    url: https://github.com/allenai/scifact
    year: null
    doi: null
    is_paper: false
    source_confidence: definitive_project_page
  - title: 'BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information
      Retrieval Models'
    url: https://arxiv.org/abs/2104.08663
    year: 2021
    doi: 10.48550/arXiv.2104.08663
    is_paper: true
    source_confidence: benchmark_context_paper
  - title: 'MMTEB: Massive Multilingual Text Embedding Benchmark'
    url: https://arxiv.org/abs/2502.13595
    year: 2025
    doi: 10.48550/arXiv.2502.13595
    is_paper: true
    source_confidence: benchmark_context_paper
  - title: 'NanoBEIR: Smaller BEIR dataset subsets'
    url: https://huggingface.co/collections/zeta-alpha-ai/nanobeir
    year: 2024
    doi: null
    is_paper: false
    source_confidence: dataset_collection
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.6212438415
      hit_at_10: 0.76
      recall_at_100: 0.8392857143
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.8392857143
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.7016869793
      hit_at_10: 0.84
      recall_at_100: 0.8928571429
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.8928571429
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.6576943632
      hit_at_10: 0.82
      recall_at_100: 0.9464285714
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.06
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9464285714
      safeguard_positive_rows: 3
      rows_with_101_candidates: 3
```
