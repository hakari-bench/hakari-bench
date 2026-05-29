# MNanoBEIR / NanoBEIR-sr / NanoSciFact

## Overview

SciFact is a scientific claim evidence retrieval task. `NanoBEIR-sr__NanoSciFact`
uses Serbian translated scientific claims to retrieve Serbian translated
abstracts that provide evidence.

## Details

### What the Original Data Measures

[SciFact](https://arxiv.org/abs/2004.14974) evaluates scientific claim
verification using abstracts as evidence. BEIR uses the retrieval portion, and
MMTEB supplies the multilingual context for this Serbian split.

### Observed Data Profile

The sampled task has 50 queries, 2,919 documents, and 56 positive qrels. Most
queries have one positive. Queries average 96.42 characters, and documents
average 1,433.95 characters.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.6468 and hit@10 = 0.8200. The median first-positive
rank is 1.0, so scientific terminology gives BM25 strong anchors, but evidence
ranking still requires distinguishing support from related abstracts.

### Training Data That May Help

Useful data includes non-overlapping scientific claim verification, biomedical
abstract retrieval, Serbian scientific QA, and multilingual evidence retrieval.
Exclude SciFact, BEIR, NanoBEIR, and translated claim-evidence pairs.

### Synthetic Data Guidance

Generate Serbian scientific claims from abstracts and label the abstract that
supports or contradicts each claim. Hard negatives should share entities or
methods without providing the needed evidence.

## Example Data

| Query | Positive document |
| --- | --- |
| Ly49Q usmerava organizaciju migracije neutrofila do mesta zapaljenja regulišući funkcije membranskih splavova. (110 chars) | Neutrofili brzo podležu polarizaciji i usmerenom kretanju kako bi se infiltrirali na mesta infekcije i upale. Ovde pokazujemo da je inhibitorni MHC I receptor, Ly49Q, bio ključan za brzu polarizaciju i infiltraciju tkiva od s ... [truncated 225 chars](989 chars) |
| Antiretrovirusna terapija smanjuje stope oboljevanja od tuberkuloze u širokom rasponu CD4 slojeva. (98 chars) | POZADINA Infekcija virusom humane imunodeficijencije (HIV) predstavlja najznačajniji faktor rizika za razvoj tuberkuloze i podstaknula je njen ponovni porast, posebno u podsaharskoj Africi. Godine 2010. bilo je procenjeno 1,1 ... [truncated 225 chars](2174 chars) |
| Brza regulacija naviše i viši bazalni izražaj interferonom indukovanih gena smanjuju preživljavanje granuliranih neuronskih ćelija zaraženih virusom Zapadnog Nila. (163 chars) | Iako je podložnost neurona u mozgu mikrobnoj infekciji glavni faktor koji određuje klinički ishod, malo se zna o molekularnim faktorima koji upravljaju ovom osetljivošću. Ovde pokazujemo da su dve vrste neurona iz različitih ... [truncated 225 chars](1119 chars) |
| Primarno skrining za rak grlića materice uz detekciju HPV-a ima veću longitudinalnu senzitivnost od konvencionalne citologije u otkrivanju cervikalne neoplazme intraepitelijuma stepena 2. (187 chars) | POZADINA Skrining za rak grlića materice zasnovan na testiranju na humani papiloma virus (HPV) povećava senzitivnost detekcije visokog stepena (stepen 2 ili 3) cervikalne intraepitelne neoplazije, ali je nepoznato da li ovaj ... [truncated 225 chars](2253 chars) |
| Blokiranje interakcije između TDP-43 i proteina respiratornog kompleksa I, ND3 i ND6, dovodí do pojačanog gubitka neurona izazvanog TDP-43. (139 chars) | Genetičke mutacije u TAR DNK-vezujućem proteinu 43 (TARDBP, takođe poznatom kao TDP-43) uzrokuju amiotrofičnu lateralnu sklerozu (ALS), a povećana prisutnost TDP-43 (kodiranog genom TARDBP) u citoplazmi je istaknuta histopato ... [truncated 225 chars](1274 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-sr |
| Task / split | NanoSciFact |
| Hugging Face dataset | [hakari-bench/NanoBEIR-sr](https://huggingface.co/datasets/hakari-bench/NanoBEIR-sr) |
| Language | sr |
| Category | natural_language |
| Queries | 50 |
| Documents | 2,919 |
| Positive qrels | 56 |
| Positives per query avg | 1.12 |
| Positives per query min / median / max | 1 / 1.0 / 4 |
| Multi-positive queries | 4 (8.00%) |
| BM25 nDCG@10 | 0.6468 |
| BM25 hit@10 | 0.8200 |
| BM25 Recall@100 | 0.8750 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.6223 |
| Dense hit@10 | 0.7800 |
| Dense Recall@100 | 0.8750 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.6834 |
| Reranking hybrid hit@10 | 0.8400 |
| Reranking hybrid Recall@100 | 0.9286 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 3 |
| Query length avg chars | 96.42 |
| Document length avg chars | 1,433.95 |

### Public Sources

- [SciFact](https://arxiv.org/abs/2004.14974), [BEIR](https://arxiv.org/abs/2104.08663), [MMTEB](https://arxiv.org/abs/2502.13595), and [NanoBEIR](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-sr](https://huggingface.co/datasets/hakari-bench/NanoBEIR-sr)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| SciFact: Fact or Fiction: Verifying Scientific Claims | 2020 | task paper | https://arxiv.org/abs/2004.14974 |
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
  backing_dataset: NanoBEIR-sr
  dataset_id: hakari-bench/NanoBEIR-sr
  task_name: NanoSciFact
  split_name: NanoSciFact
  language: sr
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-sr__NanoSciFact.md
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
    query_mean: 96.42
    document_mean: 1433.94827
  bm25:
    ndcg_at_10: 0.6467577061432589
    hit_at_10: 0.82
    source: dataset_candidate_subset
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.6467577061
      hit_at_10: 0.82
      recall_at_100: 0.875
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.875
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.6222645445
      hit_at_10: 0.78
      recall_at_100: 0.875
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.875
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.6834341661
      hit_at_10: 0.84
      recall_at_100: 0.9285714286
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.06
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9285714286
      safeguard_positive_rows: 3
      rows_with_101_candidates: 3
```
