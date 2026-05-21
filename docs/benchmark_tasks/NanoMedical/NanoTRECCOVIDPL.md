# NanoMedical / NanoTRECCOVIDPL

## Overview

`NanoTRECCOVIDPL` is the Polish BEIR-PL adaptation of TREC-COVID. Queries are
Polish translations of COVID-19 information needs, and documents are Polish
translations of CORD-19 scientific article records. The task tests retrieval of
pandemic scientific evidence in Polish, with additional difficulty from machine
translation, Polish morphology, and specialized biomedical terminology.

## Details

### What the Original Data Measures

[Searching for Scientific Evidence in a Pandemic: An Overview of TREC-COVID](https://arxiv.org/abs/2104.09632)
describes TREC-COVID as a five-round COVID-19 information-retrieval challenge
over CORD-19. It used 50 topics, 92 participating teams, 556 submissions, and
69,318 manual judgments. Topics cover biological, clinical, and public-health
questions, and documents come from a rapidly updated scientific corpus that
includes both peer-reviewed papers and preprints.

[BEIR-PL: Zero Shot Information Retrieval Benchmark for the Polish Language](https://arxiv.org/abs/2305.19840)
translates BEIR datasets into Polish with Google Translate and evaluates Polish
retrieval systems. The paper reports that translation quality was checked through
sampled strict and semantic evaluations plus LaBSE similarity, and it notes that
translations were generally adequate for IR but not perfect, especially for named
entities and phrasing. Its dataset table lists TREC-COVID as one of the BEIR-PL
datasets, with 50 test queries and a large COVID-19 corpus.

This Nano task is a compact Polish version of that setting: each translated
COVID-19 question retrieves one positive translated scientific document from a
10,000-document subset.

### Observed Data Profile

The Nano split has 50 queries, 10,000 documents, and exactly one positive qrel
per query. Queries average 69.42 characters, and documents average 1,251.91
characters. The translated queries cover the same pandemic topics as the English
TREC-COVID split, including origin, weather effects, immunity, animal studies,
rapid testing, serology, social distancing, masks, remdesivir, vaccines, and
dexamethasone.

Documents are Polish translations of title-plus-abstract COVID-19 or related
coronavirus literature. Some passages contain translation artifacts in biomedical
phrasing or named entities, but the main information need is generally clear.
The corpus includes direct COVID-19 papers as well as older coronavirus,
influenza, virology, and public-health literature.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.1098
and hit@10 = 0.1600. It ranks only 2 of 50 positives first and 8 positives
inside the top 10. This is substantially harder than the English NanoTRECCOVID
split. The drop matches BEIR-PL's observation that lexical retrieval can be less
effective for Polish because of inflection, named-entity translation, and
phrasing differences.

Observed failures include a mask-prevention query where BM25 retrieves social
network disease-spread and general mask-modeling papers before the relevant
barrier-intervention review; a Canada-impact query where the positive long-term
care living review is ranked far below unrelated virus and preparedness
documents; and a social-distancing query where influenza-pandemic modeling
documents outrank a COVID-19 social-distancing simulation study. A strong model
needs multilingual semantic retrieval and pandemic-specific intent matching, not
only translated keyword overlap.

### Training Data That May Help

Useful training data includes non-overlapping Polish COVID-19 literature
retrieval, translated biomedical ad hoc retrieval, Polish public-health QA,
multilingual CORD-19 retrieval, and hard negatives from related coronavirus or
influenza documents. Models should learn Polish morphology and robust handling
of translated biomedical entities such as `SARS-CoV-2`, `remdesiwir`,
`deksametazon`, and `przeciwciała`.

For clean evaluation, training should exclude BEIR-PL TREC-COVID test examples,
their translated positive documents, and translated duplicates of English
TREC-COVID evaluation topics. Training on TREC-COVID prior-round judgments or
English qrels translated into Polish is a supervised or feedback setting and
should be reported separately.

### Synthetic Data Guidance

For document-to-question generation, use non-evaluation Polish COVID-19 or
coronavirus abstracts and generate Polish natural-language information needs
about treatments, transmission, testing, prevention, vaccines, outcomes, or risk
groups. Preserve scientific names and drug names consistently.

For joint document-and-question generation, create Polish title-plus-abstract
passages and paired pandemic questions, with hard negatives that share
COVID-19-related terms but differ in population, intervention, outcome, or
evidence type. Do not seed synthetic examples with Nano evaluation queries or
positive documents.

## Example Data

| Query | Positive document |
| --- | --- |
| jakie są dowody na to, że deksametazon może być stosowany w leczeniu COVID-19? (78 chars) | Połączenie tocilizumabu i metyloprednizolonu wraz ze wstępną strategią rekrutacji płuc w chorobie koronawirusowej 2019 Pacjenci wymagający wentylacji mechanicznej: seria 21 kolejnych przypadków CEL: Opisanie wyników leczenia ... [truncated 225 chars](1767 chars) |
| jak długo koronawirus pozostaje stabilny na powierzchniach? (59 chars) | Płyny ustrojowe mogą przyczyniać się do przenoszenia z człowieka na człowieka koronawirusa zespołu ostrej ostrej niewydolności oddechowej 2: dowody i doświadczenia praktyczne TŁO: W grudniu 2019 r. w mieście Wuhan w prowincji ... [truncated 225 chars](1201 chars) |
| czy dystans społeczny miał wpływ na spowolnienie rozprzestrzeniania się COVID-19? (81 chars) | Zwiększona wykrywalność w połączeniu z planowaniem dystansu społecznego i zdrowia Zmniejsz obciążenie przypadkami i ofiarami śmiertelnymi związanymi z COVID-19: badanie weryfikujące koncepcję przy użyciu stochastycznego model ... [truncated 225 chars](1773 chars) |
| czy istnieją testy serologiczne wykrywające przeciwciała przeciwko koronawirusowi? (82 chars) | Serodiagnostyka dla koronawirusa-2 związanego z ciężkim ostrym zespołem oddechowym: przegląd narracyjny Dokładne testy serologiczne w celu wykrycia przeciwciał gospodarza przeciwko koronawirusowi-2 związanemu z ciężkim ostrym ... [truncated 225 chars](1507 chars) |
| które biomarkery przewidują ciężki przebieg kliniczny zakażenia 2019-nCOV? (74 chars) | Cechy kliniczne i predyktory dla pacjentów z ciężkim zapaleniem płuc SARS-CoV-2: retrospektywne wieloośrodkowe badanie kohortowe Cele: Badanie to przeprowadzono w celu zbadania cech klinicznych pacjentów z ciężkim zapaleniem ... [truncated 225 chars](1578 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMedical |
| Backing dataset | NanoMedical |
| Task / split | NanoTRECCOVIDPL |
| Hugging Face dataset | [hakari-bench/NanoMedical](https://huggingface.co/datasets/hakari-bench/NanoMedical) |
| Language | pl |
| Category | natural_language |
| Queries | 50 |
| Documents | 10,000 |
| Positive qrels | 50 |
| BM25 nDCG@10 | 0.1098 |
| BM25 hit@10 | 0.1600 |
| Query length avg chars | 69.42 |
| Document length avg chars | 1,251.91 |

### Public Sources

- [BEIR-PL: Zero Shot Information Retrieval Benchmark for the Polish Language](https://arxiv.org/abs/2305.19840); 2024; Konrad Wojtasik, Kacper Wołowiec, Vadim Shishkin, Arkadiusz Janz, and Maciej Piasecki.
- [ACL Anthology record for BEIR-PL](https://aclanthology.org/2024.lrec-main.194/).
- [Searching for Scientific Evidence in a Pandemic: An Overview of TREC-COVID](https://arxiv.org/abs/2104.09632); 2021; Kirk Roberts, Tasmeer Alam, Steven Bedrick, Dina Demner-Fushman, Kyle Lo, Ian Soboroff, Ellen Voorhees, Lucy Lu Wang, and William R. Hersh.
- [TREC-COVID data archive](https://ir.nist.gov/trec-covid/).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMedical](https://huggingface.co/datasets/hakari-bench/NanoMedical)
- BEIR-PL publisher/models: [clarin-knext](https://huggingface.co/clarin-knext)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| BEIR-PL: Zero Shot Information Retrieval Benchmark for the Polish Language | 2024 | arXiv paper | https://arxiv.org/abs/2305.19840 |
| BEIR-PL: Zero Shot Information Retrieval Benchmark for the Polish Language | 2024 | ACL Anthology paper | https://aclanthology.org/2024.lrec-main.194/ |
| Searching for Scientific Evidence in a Pandemic: An Overview of TREC-COVID | 2021 | arXiv paper | https://arxiv.org/abs/2104.09632 |
| TREC-COVID data archive | 2020 | benchmark archive | https://ir.nist.gov/trec-covid/ |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMedical
  backing_dataset: NanoMedical
  dataset_id: hakari-bench/NanoMedical
  task_name: NanoTRECCOVIDPL
  split_name: NanoTRECCOVIDPL
  language: pl
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMedical/NanoTRECCOVIDPL.md
  source_research:
    primary_source_type: benchmark_paper_and_translation_benchmark_paper
    paper_pdf_or_html_checked: true
    paper_url: https://arxiv.org/abs/2305.19840
    additional_source_urls:
      - https://aclanthology.org/2024.lrec-main.194/
      - https://arxiv.org/abs/2104.09632
      - https://ir.nist.gov/trec-covid/
      - https://huggingface.co/clarin-knext
  counts:
    queries: 50
    documents: 10000
    positive_qrels: 50
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 69.42
    document_mean: 1251.911
  bm25:
    ndcg_at_10: 0.109759642
    hit_at_10: 0.16
    source: dataset_bm25_column
  learning:
    original_train_split: available_in_BEIR_PL_and_TREC_COVID_feedback_settings
    evaluation_split_origin: BEIR-PL translated TREC-COVID retrieval split sampled into NanoMedical
    train_eval_overlap_audit: not_audited
    leakage_note: exclude BEIR-PL TREC-COVID test examples, translated positives, and translated duplicates of English TREC-COVID evaluation topics
    useful_training_data:
      - non-overlapping Polish COVID-19 literature retrieval data
      - translated biomedical ad hoc retrieval data
      - Polish public-health QA and medical retrieval data
      - multilingual CORD-19 retrieval with hard negatives
    synthetic_data:
      document_generation: Polish COVID-19 and coronavirus title-plus-abstract passages
      question_generation: Polish clinical, biological, or public-health pandemic information needs
      hard_negatives: translated documents sharing COVID-19 vocabulary but differing in population, intervention, outcome, or evidence type
      answerability: the document should contain evidence responsive to the Polish information need
    multi_positive_training: single_positive_question_document_focus_in_this_nano_split
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMedical
    source_urls:
      - label: BEIR-PL arXiv
        url: https://arxiv.org/abs/2305.19840
      - label: BEIR-PL ACL Anthology
        url: https://aclanthology.org/2024.lrec-main.194/
      - label: TREC-COVID arXiv
        url: https://arxiv.org/abs/2104.09632
      - label: TREC-COVID archive
        url: https://ir.nist.gov/trec-covid/
      - label: clarin-knext Hugging Face
        url: https://huggingface.co/clarin-knext
```
