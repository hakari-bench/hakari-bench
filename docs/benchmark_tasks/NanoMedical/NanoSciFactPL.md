# NanoMedical / NanoSciFactPL

## Overview

`NanoSciFactPL` is the Polish BEIR-PL adaptation of SciFact. Queries are Polish
translations of scientific claims, and documents are Polish translations of
biomedical abstracts. Like English SciFact, the retrieval target is an evidence
abstract that supports or refutes the claim. The additional challenge is that the
data is machine-translated into a morphologically rich language, so lexical
matching must handle Polish inflection and translated biomedical terminology.

## Details

### What the Original Data Measures

[Fact or Fiction: Verifying Scientific Claims](https://arxiv.org/abs/2004.14974)
defines the original SciFact task as retrieving scientific abstracts that support
or refute expert-written claims, with rationale annotations. SciFact contains
1,409 claims and 5,183 abstracts from a biomedical scientific corpus.

[BEIR-PL: Zero Shot Information Retrieval Benchmark for the Polish Language](https://arxiv.org/abs/2305.19840)
translates accessible BEIR datasets into Polish to create a large Polish
information-retrieval benchmark. The paper states that BEIR-PL was built with
Google Translate and that translation quality was checked by sampled manual
assessment in semantic and strict settings, plus LaBSE similarity checks. The
authors note that translated texts were usually adequate for IR but not perfect,
with errors especially around named entities and phrasing.

This task therefore measures Polish evidence retrieval under translated
scientific-claim conditions. The underlying evidence relations are SciFact's, but
retrieval quality can be affected by Polish inflection, translation choices for
technical terms, and translated abstract style.

### Observed Data Profile

The Nano split has 200 queries, 5,183 documents, and 226 positive qrel rows, the
same qrel structure as the English NanoSciFact split. The average query has 1.13
positives, and 16 queries have more than one positive. Polish queries average
95.52 characters, and documents average 1,554.52 characters, slightly longer
than the English version.

Observed claims include translated biomedical statements about AIRE expression
in skin tumors, combined smoking-cessation therapy, Ly6C monocytes, monoclonal
antibodies against N-cadherin, asymptomatic vision screening, H. pylori urease,
breast-cancer risk, memory T cells, and Arabidopsis PIN1. Documents are long
translated article-title plus abstract passages. The Polish text is generally
readable, but some biomedical names, symbols, and phrasing remain close to the
English source.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.5121
and hit@10 = 0.6600. It ranks 80 of 226 positives first and 137 positives inside
the top 10. This is lower than English NanoSciFact, consistent with the BEIR-PL
paper's broader observation that BM25 tends to perform worse in Polish than in
English because Polish has many word forms and translation can alter lexical
overlap.

The failures show both scientific and translation-side difficulty. For the H.
pylori urease claim, BM25 retrieves other H. pylori infection and urease-related
documents before the positive channel-structure abstract. For a breast-cancer
claim about genetic determinism, it retrieves mammographic or hormone-risk
abstracts before the gene-environment interaction abstract. For memory T cells,
it retrieves other T-cell subset and tissue-resident T-cell papers before the
positive developmental tissue-compartmentalization abstract. A good model needs
both Polish retrieval robustness and SciFact-style evidence relation matching.

### Training Data That May Help

Useful training data includes non-overlapping Polish scientific claim-evidence
pairs, Polish biomedical retrieval data, translated SciFact-style supervision,
and multilingual biomedical retrieval with hard negatives. Training should expose
models to Polish inflection, translated gene/protein names, and claims whose
truth relation depends on direction, condition, or population.

For clean evaluation, training should exclude the BEIR-PL SciFact test examples
and any translated duplicates of the English SciFact evaluation claims or
positive abstracts. If English SciFact training data is translated for training,
the split boundaries and duplicate claims should be audited carefully.

### Synthetic Data Guidance

For document-to-question generation, start from non-evaluation Polish biomedical
abstracts or high-quality translations and generate Polish atomic scientific
claims. Preserve biomedical names and symbols carefully, and vary inflection and
word order naturally.

For joint document-and-question generation, create Polish scientific abstracts
and paired claims with same-topic hard negatives. Include cases where a negative
shares the same disease, gene, or intervention but differs in direction,
population, organism, or outcome. Avoid seeding synthetic data with Nano
evaluation text or direct translations of its claims.

## Example Data

| Query | Positive document |
| --- | --- |
| Rak jelita grubego z przerzutami leczony pojedynczym lekiem fluoropirymidynami skutkował zmniejszoną skutecznością i niższą jakością życia w porównaniu z chemioterapią opartą na oksaliplatynie u pacjentów w podeszłym wieku. (223 chars) | Opcje chemioterapii u starszych i słabych pacjentów z przerzutowym rakiem jelita grubego (MRC FOCUS2): otwarte, randomizowane badanie czynnikowe TŁO Pacjenci w podeszłym wieku i słabi z rakiem, chociaż często leczeni chemiote ... [truncated 225 chars](3343 chars) |
| CRP nie pozwala przewidzieć śmiertelności pooperacyjnej po operacji pomostowania aortalno-wieńcowego (CABG). (108 chars) | Ocena opłacalności stosowania prognostycznych biomarkerów z modelami decyzyjnymi: studium przypadku w ustalaniu priorytetów pacjentów oczekujących na operację tętnicy wieńcowej CEL Określenie skuteczności i opłacalności wykor ... [truncated 225 chars](3169 chars) |
| Arginina 90 w p150n jest ważna dla interakcji z EB1. (52 chars) | Strukturalne podstawy do aktywacji składania mikrotubul przez kompleks EB1 i p150Glued. Białka śledzące plus, takie jak EB1 i kompleks dyneina/dynaktyna, regulują dynamikę mikrotubul. Uważa się, że białka te stabilizują mikro ... [truncated 225 chars](1210 chars) |
| O otyłości decydują wyłącznie czynniki środowiskowe. (52 chars) | Genetyka otyłości u dorosłych adopcyjnych i ich biologicznego rodzeństwa. Przeprowadzono badanie adopcyjne wpływu genetycznego na otyłość w wieku dorosłym, w którym osoby adoptowane oddzielone od swoich naturalnych rodziców n ... [truncated 225 chars](1465 chars) |
| Napady gorączkowe zwiększają próg rozwoju padaczki. (51 chars) | Napady gorączkowe w rozwijającym się mózgu powodują uporczywą modyfikację pobudliwości neuronalnej w obwodach limbicznych Napady gorączkowe (wywołane gorączką) dotykają 3–5% niemowląt i małych dzieci. Pomimo dużej częstości w ... [truncated 225 chars](812 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMedical |
| Backing dataset | NanoMedical |
| Task / split | NanoSciFactPL |
| Hugging Face dataset | [hakari-bench/NanoMedical](https://huggingface.co/datasets/hakari-bench/NanoMedical) |
| Language | pl |
| Category | natural_language |
| Queries | 200 |
| Documents | 5,183 |
| Positive qrels | 226 |
| Positives per query | avg 1.13; min 1; median 1; max 5 |
| Multi-positive queries | 16 / 200 (8.00%) |
| BM25 nDCG@10 | 0.5750 |
| BM25 hit@10 | 0.7250 |
| BM25 Recall@100 | 0.8540 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.6061 |
| Dense hit@10 | 0.7600 |
| Dense Recall@100 | 0.8894 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.6538 |
| Reranking hybrid hit@10 | 0.8100 |
| Reranking hybrid Recall@100 | 0.9292 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 13 |
| Query length avg chars | 95.52 |
| Document length avg chars | 1,554.52 |

### Public Sources

- [BEIR-PL: Zero Shot Information Retrieval Benchmark for the Polish Language](https://arxiv.org/abs/2305.19840); 2024; Konrad Wojtasik, Kacper Wołowiec, Vadim Shishkin, Arkadiusz Janz, and Maciej Piasecki.
- [ACL Anthology record for BEIR-PL](https://aclanthology.org/2024.lrec-main.194/).
- [Fact or Fiction: Verifying Scientific Claims](https://arxiv.org/abs/2004.14974); 2020; David Wadden, Shanchuan Lin, Kyle Lo, Lucy Lu Wang, Madeleine van Zuylen, Arman Cohan, and Hannaneh Hajishirzi.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMedical](https://huggingface.co/datasets/hakari-bench/NanoMedical)
- BEIR-PL publisher/models: [clarin-knext](https://huggingface.co/clarin-knext)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| BEIR-PL: Zero Shot Information Retrieval Benchmark for the Polish Language | 2024 | arXiv paper | https://arxiv.org/abs/2305.19840 |
| BEIR-PL: Zero Shot Information Retrieval Benchmark for the Polish Language | 2024 | ACL Anthology paper | https://aclanthology.org/2024.lrec-main.194/ |
| Fact or Fiction: Verifying Scientific Claims | 2020 | arXiv paper | https://arxiv.org/abs/2004.14974 |
| Fact or Fiction: Verifying Scientific Claims | 2020 | ACL Anthology paper | https://aclanthology.org/2020.emnlp-main.609/ |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMedical
  backing_dataset: NanoMedical
  dataset_id: hakari-bench/NanoMedical
  task_name: NanoSciFactPL
  split_name: NanoSciFactPL
  language: pl
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMedical/NanoSciFactPL.md
  source_research:
    primary_source_type: benchmark_paper_and_task_paper
    paper_pdf_or_html_checked: true
    paper_url: https://arxiv.org/abs/2305.19840
    additional_source_urls:
    - https://aclanthology.org/2024.lrec-main.194/
    - https://arxiv.org/abs/2004.14974
    - https://aclanthology.org/2020.emnlp-main.609/
    - https://huggingface.co/clarin-knext
  counts:
    queries: 200
    documents: 5183
    positive_qrels: 226
  positives_per_query:
    average: 1.13
    min: 1
    median: 1.0
    max: 5
    multi_positive_queries: 16
    multi_positive_query_percent: 8.0
  text_stats_chars:
    query_mean: 95.52
    document_mean: 1554.517847
  bm25:
    ndcg_at_10: 0.5749962931973077
    hit_at_10: 0.725
    source: dataset_candidate_subset
  learning:
    original_train_split: available_in_BEIR_PL_and_SciFact_sources
    evaluation_split_origin: BEIR-PL translated SciFact retrieval split sampled into
      NanoMedical
    train_eval_overlap_audit: not_audited
    leakage_note: exclude BEIR-PL SciFact test examples and translated duplicates
      of English SciFact evaluation claims or positive abstracts
    useful_training_data:
    - non-overlapping Polish scientific claim-evidence pairs
    - Polish biomedical retrieval data
    - translated SciFact-style supervision outside the evaluation split
    - multilingual biomedical retrieval with same-topic hard negatives
    synthetic_data:
      document_generation: Polish biomedical abstracts or high-quality translations
        preserving technical names
      question_generation: Polish atomic scientific claims with natural inflection
        and careful biomedical terminology
      hard_negatives: same-topic abstracts differing in direction, condition, population,
        organism, or outcome
      answerability: the abstract should contain evidence sufficient to support or
        refute the Polish claim
    multi_positive_training: mostly single-positive with limited multi-positive support
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMedical
    source_urls:
    - label: BEIR-PL arXiv
      url: https://arxiv.org/abs/2305.19840
    - label: BEIR-PL ACL Anthology
      url: https://aclanthology.org/2024.lrec-main.194/
    - label: SciFact arXiv
      url: https://arxiv.org/abs/2004.14974
    - label: SciFact ACL Anthology
      url: https://aclanthology.org/2020.emnlp-main.609/
    - label: clarin-knext Hugging Face
      url: https://huggingface.co/clarin-knext
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.5749962932
      hit_at_10: 0.725
      recall_at_100: 0.8539823009
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.8539823009
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.6060723997
      hit_at_10: 0.76
      recall_at_100: 0.889380531
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.889380531
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.6538049109
      hit_at_10: 0.81
      recall_at_100: 0.9292035398
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.065
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9292035398
      safeguard_positive_rows: 13
      rows_with_101_candidates: 13
```
