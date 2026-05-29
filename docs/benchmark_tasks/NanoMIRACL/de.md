# NanoMIRACL / de

## Overview

The MIRACL TACL paper defines German as a monolingual Wikipedia passage
retrieval task: German questions are matched to German passages with
native-speaker relevance labels. This Nano version keeps a compact,
single-positive slice of that setting. The queries look like ordinary German
fact questions, commonly starting with `Wie`, `Wann`, `Welche`, `Was`, `Wo`, or
`Wer`, so the task is about mapping concise German question forms to the exact
passage that states the requested entity, date, place, definition, or
institutional fact.

## Details

### What the Original Data Measures

[MIRACL: A Multilingual Retrieval Dataset Covering 18 Diverse
Languages](https://aclanthology.org/2023.tacl-1.63/) describes MIRACL as a
monolingual ad hoc retrieval benchmark over Wikipedia passages. Queries and
passages are in the same language, so German queries retrieve German Wikipedia
passages rather than translated evidence. The paper reports more than 726k
high-quality relevance judgments for 78k queries, with annotations performed by
native speakers hired by the MIRACL team.

German has a special role in MIRACL. The TACL paper's dataset table lists German
as one of the two WSDM Cup surprise languages, with development and test-B data
but no training split. The paper explains that surprise-language identities were
hidden until shortly before the competition deadline and that no training splits
were provided for them, specifically to evaluate retrieval under limited data and
time conditions. This makes the German task different from MIRACL languages such
as English or Arabic that have explicit MIRACL train data.

The MIRACL construction process still follows the same retrieval-first design:
native speakers generated well-formed questions from Wikipedia prompts, then
judged candidate passages produced by an ensemble baseline retrieval system. The
paper states that the ensemble included BM25, mDPR, and mColBERT, and that the
corpus was built from Wikipedia passages rather than answer snippets. For this
task, the labeled positive is therefore an evidence-bearing German Wikipedia
passage, not a direct answer string or another question.

### Observed Data Profile

The sampled Nano task has 200 queries, 1,748 documents, and 200 positive qrel
rows. Every query has exactly one positive passage. Queries average 45.57
characters and are mostly ordinary German questions. The most common openings in
the sample are `Wie`, `Wann`, `Welche`, `Was`, `Wo`, and `Wer`, with smaller
numbers of `Warum`, `Wozu`, and prepositional openings such as `In` or `Auf`.

Documents average 629.75 characters and are German Wikipedia passages that
typically begin with the article title. The sampled positives cover pop music,
public broadcasters, football clubs, castles, Indigenous peoples, geography,
government institutions, inventions, universities, film, and sports. Many
queries ask for a precise attribute of a known entity: which chart position, what
an acronym stands for, where a headquarters is, who built something, or when an
event occurred.

The data rewards passage-level relation matching. A query may contain a strong
entity name such as `Neuschwanstein`, `FC Liverpool`, `New York State Police`, or
`ZDF`, but the correct passage is the one that states the requested relation.
German morphology and compounds add another layer: lexical overlap can find the
right topic family while missing the sentence that actually answers the question.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.3665
and hit@10 = 0.6000 on this Nano split. BM25 places 33 of 200 positives at rank
1 and only 120 of 200 positives in the top 10. This is substantially harder for
BM25 than the previously inspected Arabic and Bengali NanoMIRACL splits, despite
German being a high-resource language.

The inspected failures show why. For "Wer hat Neuschwanstein gebaut?", BM25 is
distracted by passages from a film titled "Wer hat eigentlich die Liebe
erfunden?" because the query begins with a common `Wer hat` pattern; the
positive passage about Ludwig II is rank 12. The same pattern appears for "Wer
hat das Mikroskop erfunden?" and "Wer hat das Musical erfunden?", where generic
`Wer hat ... erfunden` lexical overlap outranks the evidence passage. For "Wie
viele Provinzen gibt es in der Türkei?", BM25 retrieves a vehicle-registration
passage that mentions 81 Turkish provinces before the list page that directly
answers the province-count question. For "Welche Inseln gibt es in der
Karibik?", top hits include game and Mediterranean-island pages, while the
positive Dutch Caribbean passage is lower.

Because each Nano query has exactly one positive qrel, hit@10 shows that BM25
misses the labeled evidence passage for 80 queries. nDCG@10 is also important
because many positives are present but not highly ranked. A stronger retriever
needs to retain exact entity matching while down-weighting common German question
templates and selecting passages that express the requested relation.

### Training Data That May Help

Unlike many MIRACL languages, the original MIRACL German setup did not provide a
German training split; the TACL paper lists German as a surprise language with
development and test-B data only. Training should therefore use non-overlapping
German retrieval data outside the evaluation split, such as German Wikipedia
question-to-passage pairs, German QA evidence retrieval datasets, and supervised
entity-attribute examples. Any MIRACL German development or test data likely to
overlap with NanoMIRACL should preferably be excluded from training.

Useful supervision should emphasize relation extraction through retrieval:
founder, date, location, definition, acronym expansion, chart position, stadium,
headquarters, and count questions. Generic German paraphrase pairs can help
language understanding, but the central behavior is retrieving an
answer-bearing passage from a broader article corpus.

### Synthetic Data Guidance

For document-to-question generation, use non-evaluation German Wikipedia-style
passages and generate German questions grounded in one selected passage. The
synthetic queries should include `Wer`, `Was`, `Wann`, `Wo`, `Wie viele`,
`Welche`, and `Wozu` forms, with entity names, compounds, abbreviations,
locations, years, and organization names. The positive should remain the passage
that contains explicit evidence.

For joint document-and-question generation, create German encyclopedia-style
passages with titles, aliases, founding dates, chart positions, locations,
institutional roles, and definitional sentences, then create questions
answerable from those passages. Do not use Nano evaluation queries or positive
passages as seeds. Synthetic data should include hard related-entity situations,
such as same-name people, neighboring institutions, or common question templates
that should not define relevance by themselves.

## Example Data

| Query | Positive document |
| --- | --- |
| Welche Mechanismen helfen Computern, menschliche Sprache zu verstehen? (70 chars) | Wissen Ein anderes Anwendungsfeld sind Dialogsysteme, die in der Mensch-Computer-Interaktion eingesetzt werden und die Kommunikation eines Menschen mit einem Computer mittels natürlicher Sprache ermöglichen sollen. So simulie ... [truncated 225 chars](1584 chars) |
| In welchem Jahr wurde TikTok gegründet? (39 chars) | TikTok "Douyin" wurde im September 2016 von Zhang Yiming, dem Gründer von ByteDance, ins Leben gerufen. Im Januar 2017 erhielt das Unternehmen mehrere Millionen Renminbi von der Toutiao-Gruppe, um die Plattform weiter auszuba ... [truncated 225 chars](297 chars) |
| Was macht Südostasien attraktiv für Touristen? (46 chars) | Krabi (Stadt) Krabi ist eines der attraktivsten Reiseziele in Süd-Thailand. Die Andamanensee im Westen, an der zahllose natürliche Attraktionen liegen, ist beeindruckend. Dazu gehören die weißen Sandstrände, steil aufsteigend ... [truncated 225 chars](349 chars) |
| Was ist das kleinste Teilchen im Universum? (43 chars) | Elementarteilchen Elementarteilchen sind unteilbare subatomare Teilchen und die kleinsten bekannten Bausteine der Materie. Aus der Sicht der theoretischen Physik sind sie die geringsten Anregungsstufen bestimmter Felder. Nach ... [truncated 225 chars](730 chars) |
| Warum sind deutsche Produkte von so guter Qualität? (51 chars) | Gartenbau Um dem Kunden eine gute Qualität zu gewährleisten, vergibt der „Bund deutscher Baumschulen“ an seine Mitgliedsfirmen geschützte Qualitätszeichen, um geprüfte Baumschulprodukte zu kennzeichnen. Die Kunden können dann ... [truncated 225 chars](688 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMIRACL |
| Backing dataset | NanoMIRACL |
| Task / split | de |
| Hugging Face dataset | [hakari-bench/NanoMIRACL](https://huggingface.co/datasets/hakari-bench/NanoMIRACL) |
| Language | de |
| Category | natural_language |
| Queries | 200 |
| Documents | 1,748 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.5172 |
| BM25 hit@10 | 0.8550 |
| BM25 Recall@100 | 0.9126 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.7389 |
| Dense hit@10 | 0.9550 |
| Dense Recall@100 | 0.9387 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.6418 |
| Reranking hybrid hit@10 | 0.9350 |
| Reranking hybrid Recall@100 | 0.9796 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 1 |
| Query length avg chars | 45.57 |
| Document length avg chars | 629.75 |

### Public Sources

- [Making a MIRACL: Multilingual Information Retrieval Across a Continuum of Languages](https://arxiv.org/abs/2210.09984); 2022; Xinyu Zhang, Nandan Thakur, Odunayo Ogundepo, Ehsan Kamalloo, David Alfonso-Hermelo, Xiaoguang Li, Qun Liu, Mehdi Rezagholizadeh, Jimmy Lin; DOI: `10.48550/arXiv.2210.09984`.
- [MIRACL: A Multilingual Retrieval Dataset Covering 18 Diverse Languages](https://aclanthology.org/2023.tacl-1.63/); 2023 TACL version; DOI: `10.1162/tacl_a_00595`.
- [MIRACL GitHub repository](https://github.com/project-miracl/miracl).
- [MIRACL corpus dataset card](https://huggingface.co/datasets/miracl/miracl-corpus).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMIRACL](https://huggingface.co/datasets/hakari-bench/NanoMIRACL)
- Source corpus: [miracl/miracl-corpus](https://huggingface.co/datasets/miracl/miracl-corpus)
- Source queries and qrels: [miracl/miracl](https://huggingface.co/datasets/miracl/miracl)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Making a MIRACL: Multilingual Information Retrieval Across a Continuum of Languages | 2022 | paper | https://arxiv.org/abs/2210.09984 |
| MIRACL: A Multilingual Retrieval Dataset Covering 18 Diverse Languages | 2023 | paper | https://aclanthology.org/2023.tacl-1.63/ |
| MIRACL GitHub repository |  | project repository | https://github.com/project-miracl/miracl |
| miracl/miracl-corpus |  | dataset card | https://huggingface.co/datasets/miracl/miracl-corpus |
| miracl/miracl |  | dataset card | https://huggingface.co/datasets/miracl/miracl |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMIRACL
  backing_dataset: NanoMIRACL
  dataset_id: hakari-bench/NanoMIRACL
  task_name: de
  split_name: de
  language: de
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMIRACL/de.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 200
    documents: 1748
    positive_qrels: 200
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 45.57
    document_mean: 629.745423
  bm25:
    ndcg_at_10: 0.5171646804884762
    hit_at_10: 0.855
    source: dataset_candidate_subset
  learning:
    original_train_split: not_found
    evaluation_split_origin: unknown
    train_eval_overlap_audit: not_audited
    leakage_note: prefer excluding MIRACL German development/test data or other MIRACL-derived
      data likely to overlap with the NanoMIRACL evaluation questions and passages
    useful_training_data:
    - non-overlapping German Wikipedia question-to-passage retrieval pairs
    - German QA evidence retrieval datasets
    - German entity-attribute retrieval supervision
    synthetic_data:
      document_generation: German Wikipedia-style passages with titles, aliases, dates,
        locations, counts, abbreviations, organizations, and factual evidence
      question_generation: German fact questions using varied Wer, Was, Wann, Wo,
        Wie viele, Welche, and Wozu forms
      answerability: questions should be grounded in explicit facts or relations in
        the generated or selected passage
    multi_positive_training: single_positive_question_document_focus
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMIRACL
    source_urls:
    - label: MIRACL corpus dataset
      url: https://huggingface.co/datasets/miracl/miracl-corpus
    - label: MIRACL source queries and qrels
      url: https://huggingface.co/datasets/miracl/miracl
    - label: MIRACL GitHub repository
      url: https://github.com/project-miracl/miracl
    source_notes: []
  references:
  - title: 'Making a MIRACL: Multilingual Information Retrieval Across a Continuum
      of Languages'
    url: https://arxiv.org/abs/2210.09984
    year: 2022
    doi: 10.48550/arXiv.2210.09984
    is_paper: true
    source_confidence: definitive_paper_link
  - title: 'MIRACL: A Multilingual Retrieval Dataset Covering 18 Diverse Languages'
    url: https://aclanthology.org/2023.tacl-1.63/
    year: 2023
    doi: 10.1162/tacl_a_00595
    is_paper: true
    source_confidence: definitive_paper_link
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.5171646805
      hit_at_10: 0.855
      recall_at_100: 0.9126394052
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9126394052
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.7389131283
      hit_at_10: 0.955
      recall_at_100: 0.93866171
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.93866171
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.6417542501
      hit_at_10: 0.935
      recall_at_100: 0.9795539033
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.005
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9795539033
      safeguard_positive_rows: 1
      rows_with_101_candidates: 1
```
