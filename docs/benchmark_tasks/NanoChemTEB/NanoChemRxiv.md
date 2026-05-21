# NanoChemTEB / NanoChemRxiv

## Overview

`NanoChemRxiv` is a chemical-literature retrieval task from the ChEmbed /
ChemRxiv Retrieval benchmark. Queries are English chemistry questions generated
for held-out ChemRxiv paragraphs, and documents are paragraphs extracted from
ChemRxiv preprints. The task measures whether a retriever can match mechanistic,
experimental, computational, and synthesis-oriented information needs to the
specific scientific paragraph that answers them.

## Details

### What the Original Data Measures

[ChEmbed: Enhancing Chemical Literature Search Through Domain-Specific Text
Embeddings](https://arxiv.org/abs/2508.01643) introduces ChemRxiv Retrieval as a
literature-driven chemistry benchmark. The paper reports that the authors
processed approximately 30 thousand ChemRxiv manuscripts with GROBID, segmented
texts into paragraphs, filtered low-quality or short paragraphs, and built a
retrieval benchmark with 69,457 chemical literature paragraphs and 5,000
synthetic queries generated from held-out paragraphs using a different LLM from
the training-generation models.

The BASF dataset card describes the task as a domain-specific retrieval dataset
for ChemRxiv papers published up to March 2025, with scientific paragraphs as
the corpus, LLM-synthesized questions or statements as queries, and 1:1 qrels
between each query and its source paragraph. The ChEmbed paper also highlights
why this matters: chemistry retrieval includes specialized nomenclature,
chemical formulas, reaction conditions, measurements, and long scientific
contexts that general retrieval benchmarks underrepresent.

### Observed Data Profile

The Nano split has 200 queries, 10,000 documents, and 200 positive qrel rows.
Every query has one positive. Queries average 111.70 characters and are usually
well-formed scientific questions about methods, thresholds, reaction conditions,
ligand effects, genome alignment, molecular dynamics, catalysts, or spectroscopy
instruments. Documents average 1,079.07 characters and are scientific paragraphs
with equations, concentrations, temperatures, catalysts, instruments, ligands,
and literature-style citations.

This is the most domain-specific NanoChemTEB split. Unlike ChemHotpotQA and
ChemNQ, which are chemistry-filtered Wikipedia tasks, ChemRxiv uses actual
chemical-literature paragraphs. The sampled positives often require matching a
technical question to a later clause in a long paragraph rather than finding a
short answer sentence.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.8718
and hit@10 = 0.9400. BM25 ranks 160 positives first and places 188 of 200
positives in the top 10. The high score reflects substantial lexical alignment:
queries often contain the same catalysts, ligands, instruments, genome variants,
or method names that appear in the source paragraph.

The remaining hard cases are still meaningful. BM25 can be distracted by
generic phrases such as "domain adaptation", "density functional theory", or
"binding free energy" when the correct paragraph depends on a specific
limitation, protocol, or compound. Some failures retrieve a topically related
chemistry paragraph but miss the exact experimental condition or structural
feature requested by the query.

### Training Data That May Help

Useful training data includes ChEmbed-style non-overlapping synthetic
query-passage pairs, ChemRxiv paragraphs outside the evaluation set, PubChem and
Semantic Scholar chemistry passages, chemistry QA over papers, and scientific
literature retrieval with hard negatives from the same article or subfield.
Training should exclude the ChemRxiv Retrieval evaluation queries, qrels, and
source paragraphs used by NanoChemRxiv.

Because this benchmark is based on LLM-generated queries for held-out
paragraphs, training should avoid reusing the same held-out paragraphs as seeds.
The most useful supervision is asymmetric: a natural chemistry information need
should retrieve the answer-bearing paragraph, not just another paragraph from
the same preprint.

### Synthetic Data Guidance

For document-to-question generation, use non-evaluation ChemRxiv or chemistry
literature paragraphs and generate one clear question that can be answered from
the paragraph. Preserve chemical specificity: reaction conditions, catalysts,
ligands, assay thresholds, instruments, spectroscopic methods, molecular
dynamics settings, concentrations, and numerical results should remain grounded.

For joint generation, create realistic chemical-literature paragraphs with
methods, results, and measured quantities, then generate concise technical
questions over them. Hard negatives should come from the same article, method
family, compound class, or subfield but omit the requested detail. Do not seed
synthetic data with Nano evaluation queries or positive paragraphs.

## Example Data

| Query | Positive document |
| --- | --- |
| How are the equilibrium densities from molecular dynamics simulations utilized to determine the solvation free energy in binary mixtures? (137 chars) | Vapor-Liquid Equilibrium Simulations. Vapor-liquid equilibrium simulations were performed by setting up systems of dimensions 9 × 9 × Z nm 3 where Z ranges from ≈20 to ≈30 nm depending on the mixture; at least 7 nm of the Z d ... [truncated 225 chars](1111 chars) |
| What percentage threshold of unknown letters was used to exclude viral genome sequences during the alignment process? (117 chars) | Genome sequences of Variants of Concern (VOCs) were aligned with the Wuhan-Hu-1 sequence using MAFFT 7 . During alignment, sequences containing over 5% unknown letters were excluded. This resulted in a dataset comprising 9,73 ... [truncated 225 chars](564 chars) |
| How does increasing the steric bulk of substituents on the ligands affect the enantioselectivity in the cross-coupling synthesis of 1,1-diarylethanes? (150 chars) | We commenced our study by investigating the cross-coupling of 2-chloronaphthalene (1a) and benzylic zinc reagent (2a, 1.5 equiv) for the synthesis of 1,1-diarylethanes (3a) (Table ). Firstly, we examined several privileged ch ... [truncated 225 chars](1519 chars) |
| How does water content in the ionic liquid electrolyte affect methanol formation rate and Faradaic efficiency when using LaCo0.5Fe0.5O3 catalyst? (145 chars) | Were responsible for the excellent performance of NiO-V2O5/Rh. Another study reported a methanol production rate of 752.9 μmol g -1 h -1 with 77% product selectivity using CuO/CeO2 mixed oxides as anodic catalysts and carbona ... [truncated 225 chars](835 chars) |
| What structural features of Ligand 4 caused it to require longer simulation times for accurate binding free energy calculations? (128 chars) | Average protein-ligand complex ΔG, solvated ligand ΔG, and overall ∆∆𝐺 𝐴→𝐵 𝑏𝑖𝑛𝑑 of the shortrun simulations and long-run simulations with all three equilibration methods are tabulated in Table . ∆∆𝐺 𝐴→𝐵 𝑏𝑖𝑛𝑑 and alchemical st ... [truncated 225 chars](2070 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoChemTEB |
| Backing dataset | NanoChemTEB |
| Task / split | NanoChemRxiv |
| Hugging Face dataset | [hakari-bench/NanoChemTEB](https://huggingface.co/datasets/hakari-bench/NanoChemTEB) |
| Language | en |
| Category | natural_language |
| Queries | 200 |
| Documents | 10,000 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.8718 |
| BM25 hit@10 | 0.9400 |
| Query length avg chars | 111.70 |
| Document length avg chars | 1,079.07 |

### Public Sources

- [ChEmbed: Enhancing Chemical Literature Search Through Domain-Specific Text Embeddings](https://arxiv.org/abs/2508.01643); 2025; Ali Shiraee Kasmaee, Mohammad Khodadad, Mehdi Astaraki, Mohammad Arshi Saloot, Nicholas Sherck, Hamidreza Mahyar, and Soheila Samiee; DOI: `10.48550/arXiv.2508.01643`.
- [ChemTEB: Chemical Text Embedding Benchmark, an Overview of Embedding Models Performance & Efficiency on a Specific Domain](https://arxiv.org/abs/2412.00532); 2024; Ali Shiraee Kasmaee et al.; DOI: `10.48550/arXiv.2412.00532`.
- [BASF-AI/ChemRxivRetrieval dataset card](https://huggingface.co/datasets/BASF-AI/ChemRxivRetrieval).
- [BASF-AI ChEmbed training data collection](https://huggingface.co/collections/BASF-AI/chembed-training-data).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoChemTEB](https://huggingface.co/datasets/hakari-bench/NanoChemTEB)
- Source dataset: [BASF-AI/ChemRxivRetrieval](https://huggingface.co/datasets/BASF-AI/ChemRxivRetrieval)
- Source papers table: [BASF-AI/ChemRxiv-Papers](https://huggingface.co/datasets/BASF-AI/ChemRxiv-Papers)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| ChEmbed: Enhancing Chemical Literature Search Through Domain-Specific Text Embeddings | 2025 | arXiv paper | https://arxiv.org/abs/2508.01643 |
| ChemTEB: Chemical Text Embedding Benchmark, an Overview of Embedding Models Performance & Efficiency on a Specific Domain | 2024 | arXiv paper | https://arxiv.org/abs/2412.00532 |
| BASF-AI/ChemRxivRetrieval | 2025 | dataset card | https://huggingface.co/datasets/BASF-AI/ChemRxivRetrieval |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoChemTEB
  backing_dataset: NanoChemTEB
  dataset_id: hakari-bench/NanoChemTEB
  task_name: NanoChemRxiv
  split_name: NanoChemRxiv
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoChemTEB/NanoChemRxiv.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    paper_url: https://arxiv.org/abs/2508.01643
    additional_source_urls:
      - https://arxiv.org/abs/2412.00532
      - https://huggingface.co/datasets/BASF-AI/ChemRxivRetrieval
      - https://huggingface.co/collections/BASF-AI/chembed-training-data
  counts:
    queries: 200
    documents: 10000
    positive_qrels: 200
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 111.705
    document_mean: 1079.0728
  bm25:
    ndcg_at_10: 0.8717574389
    hit_at_10: 0.94
    source: dataset_bm25_column
  learning:
    original_train_split: not_found
    evaluation_split_origin: ChemRxivRetrieval held-out test split
    train_eval_overlap_audit: not_audited
    leakage_note: exclude ChemRxiv Retrieval evaluation queries, qrels, and held-out source paragraphs
    useful_training_data:
      - non-overlapping ChEmbed synthetic query-passage pairs
      - ChemRxiv paragraphs outside the evaluation set
      - PubChem and Semantic Scholar chemistry passages
      - chemistry literature QA and same-paper hard negatives
    synthetic_data:
      document_generation: non-evaluation ChemRxiv-style scientific paragraphs with methods, measurements, compounds, catalysts, and results
      question_generation: clear technical chemistry questions answerable from one paragraph and grounded in exact experimental or computational details
      answerability: the source paragraph should contain the requested condition, method, threshold, compound effect, or numerical result
    multi_positive_training: single_positive_question_document_focus
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoChemTEB
    source_urls:
      - label: ChEmbed arXiv
        url: https://arxiv.org/abs/2508.01643
      - label: ChemTEB arXiv
        url: https://arxiv.org/abs/2412.00532
      - label: BASF-AI/ChemRxivRetrieval
        url: https://huggingface.co/datasets/BASF-AI/ChemRxivRetrieval
      - label: ChEmbed training data collection
        url: https://huggingface.co/collections/BASF-AI/chembed-training-data
    source_notes: []
  references:
    - title: "ChEmbed: Enhancing Chemical Literature Search Through Domain-Specific Text Embeddings"
      url: https://arxiv.org/abs/2508.01643
      year: 2025
      doi: 10.48550/arXiv.2508.01643
      is_paper: true
      source_confidence: definitive_paper_link
    - title: "ChemTEB: Chemical Text Embedding Benchmark, an Overview of Embedding Models Performance & Efficiency on a Specific Domain"
      url: https://arxiv.org/abs/2412.00532
      year: 2024
      doi: 10.48550/arXiv.2412.00532
      is_paper: true
      source_confidence: definitive_paper_link
```
