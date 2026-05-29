# NanoMIRACL / es

## Overview

The MIRACL paper positions Spanish as same-language ad hoc retrieval over
Spanish Wikipedia, with native relevance assessment rather than translated
English labels. This Nano split compresses that task to short Spanish questions
and single positive passages. The visible questions use natural interrogative
forms such as `¿Qué`, `¿Cuál`, `¿Cómo`, `¿Por`, and `¿Quién`, so retrieval
depends on resolving the requested historical, geographic, religious, political,
scientific, or definitional fact in Spanish passage text.

## Details

### What the Original Data Measures

[Making a MIRACL: Multilingual Information Retrieval Across a Continuum of
Languages](https://arxiv.org/abs/2210.09984) describes MIRACL as monolingual
ad hoc retrieval over Wikipedia passages. The query and corpus language are the
same, so Spanish queries search Spanish Wikipedia passages. The paper states
that the dataset was built for standard retrieval evaluation with nDCG and
recall-style metrics, using native-speaker relevance assessments rather than
synthetic labels.

Spanish belongs to MIRACL's "new known languages" group. The paper says Hindi,
Spanish, French, Farsi, and Chinese were added beyond Mr. TyDi/TyDi QA and that,
for those languages, all data was generated from scratch. This matters because
the Spanish split is not a denser relabeling of an older Mr. TyDi split; it is a
MIRACL-created Spanish question and passage retrieval task over Spanish
Wikipedia.

The construction process also affects interpretation. MIRACL annotators first
generated well-formed questions from Wikipedia prompts and then judged candidate
passages retrieved by an ensemble of BM25, mDPR, and mColBERT. The relevant
item is therefore an evidence-bearing passage, not a short answer string. For
Spanish, the original paper reports development-set BM25 nDCG@10 of 0.319 and
hybrid BM25+mDPR nDCG@10 of 0.641, indicating substantial headroom beyond
lexical matching on the full task.

### Observed Data Profile

The sampled Nano task has 200 queries, 1,312 documents, and 200 positive qrel
rows. Every query has exactly one positive passage. Queries average 48.21
characters. The most common openings are `¿Qué`, `¿Cuál`, `¿Cómo`, `¿Por`,
`¿Cuáles`, `¿Quién`, and `¿Cuándo`, so the sample is dominated by natural
Spanish questions rather than keyword strings.

Documents average 612.47 characters and are Spanish Wikipedia passages, usually
beginning with the article title. The examples include early representations of
Jesus, Cyrillic letters, Paraguayan popular music, Brazilian wine regions, and
Greek mythology. Other inspected queries cover Greenland Vikings, jihadist
groups, Malaysian skyscrapers, Chilean television, parliaments, the Iberian
Peninsula, the Pentateuch, tree age, the Amazon region, synthetic oils, Lutheran
offices, and anthropogony.

The task rewards exact relation matching within a broad encyclopedia setting.
Many queries contain a clear entity or topic, but relevance depends on the
requested attribute: painter or representation, pronunciation of a letter,
highest buildings, why a peninsula has a name, or where a belief about human
origin comes from. A candidate can be topically close and still fail if it does
not express the requested evidence.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.5110
and hit@10 = 0.7600 on this Nano split. BM25 places 55 of 200 positives at rank
1 and 152 of 200 positives in the top 10. Lexical matching works when the query
has distinctive names or terms, such as `alfabeto cirílico`, `Olimpo`, or
`Food Network`, but it misses nearly one quarter of the labeled positives from
the top 10.

The inspected misses are mostly relation and intent failures. For "¿Cuáles son
los 10 rascacielos más altos de Malasia?", BM25 ranks unrelated pages containing
`10` and skyscraper vocabulary above the Merdeka PNB118 passage. For "¿Por qué
se llama así la Península Ibérica?", it finds other peninsula and Iberian pages
before the passage that explains the name. For "¿Cómo llaman los judíos al
Pentateuco?", pages about Jewish history and the Samaritan Pentateuch outrank
the passage that states the Torah relation. For "¿Todavía hay vikingos en
Groenlandia?", BM25 ranks neighboring Viking-Greenland passages but the positive
passage with the relevant historical continuation evidence is just outside the
top 10.

Because every query has one positive qrel, hit@10 directly measures whether the
labeled evidence passage is retrieved at all. nDCG@10 captures the additional
problem of ranking the correct passage ahead of related but non-answering
material. A strong model should combine Spanish lexical matching with better
recognition of the requested relation, especially for `qué`, `cuál`, `cómo`,
`por qué`, and `quién` questions.

### Training Data That May Help

The first existing data to inspect is non-overlapping Spanish MIRACL training
data. Since this task is MIRACL-derived, upstream development or test queries,
qrels, and positive passages likely to overlap with NanoMIRACL should preferably
be excluded from training. Other useful sources include Spanish Wikipedia
question-to-passage retrieval pairs, Spanish open-domain QA evidence datasets,
and Spanish entity-attribute supervision for history, geography, media,
religion, organizations, and definitions.

Training should prioritize evidence retrieval. The model needs to learn that a
question such as "what is X called", "why is Y named that", or "which entities
belong to Z" should retrieve a passage containing the exact supporting
statement, not merely a page with overlapping entities.

### Synthetic Data Guidance

For document-to-question generation, use non-evaluation Spanish Wikipedia-style
passages and generate Spanish questions whose answer is explicitly grounded in
one selected passage. Useful question forms include `¿Qué`, `¿Cuál`,
`¿Cuáles`, `¿Cómo`, `¿Por qué`, `¿Quién`, `¿Cuándo`, `¿Dónde`, and `¿Cuántos`,
covering definitions, names, causes, locations, counts, dates, and entity
membership.

For joint document-and-question generation, create Spanish encyclopedia-style
passages with titles, aliases, dates, places, lists, institutional roles, and
definition sentences, then generate answerable Spanish questions. Do not seed
generation with Nano evaluation queries or positive passages. Synthetic
examples should include related-topic distractors so that models learn that
topic overlap alone is not sufficient relevance.

## Example Data

| Query | Positive document |
| --- | --- |
| ¿Cuál fue la primera universidad para mujeres en Japón? (55 chars) | Universidad Femenina de Japón Fundada el 20 de abril de 1901 por Jinzō Naruse, fue la primera institución de educación superior para mujeres establecida en Japón. Su fundador, Naruse, hizo hincapié en la necesidad de brindar ... [truncated 225 chars](1010 chars) |
| ¿Cómo llaman los judíos al Pentateuco? (38 chars) | Pentateuco Se corresponde con los que en la tradición hebrea forman la "Torá" —La Ley—, núcleo de la religión judía. Los cinco libros que lo componen son:Está contenido a su vez en el "Tanaj", el cual es considerado sagrado p ... [truncated 225 chars](678 chars) |
| ¿Cómo se pronuncia Massachusetts? (33 chars) | Massachusetts Massachusetts (/mæsəˈtʃusɪts/ en inglés), oficialmente Mancomunidad de Massachusetts (en inglés "Commonwealth of Massachusetts"), es uno de los cincuenta estados que, junto con Washington D. C., forman los Estad ... [truncated 225 chars](289 chars) |
| ¿Cuáles son las ciudades más turísticas de Grecia? (50 chars) | Turismo en Grecia El Turismo en Grecia ha sido un elemento clave de la actividad económica en el país, y es uno de los sectores más importantes del país. Grecia ha sido un destino turístico importante y atractivo en Europa de ... [truncated 225 chars](829 chars) |
| ¿De qué falleció Bertram Fletcher Robinson? (43 chars) | Bertram Fletcher Robinson En 2011, el escritor, Paul Spiring, encontró documentos que demostraban un pago de Doyle a Robinson de más de quinientas libras por la idea. Previamente, Doyle ya le habría pagado a Robinson cincuent ... [truncated 225 chars](525 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMIRACL |
| Backing dataset | NanoMIRACL |
| Task / split | es |
| Hugging Face dataset | [hakari-bench/NanoMIRACL](https://huggingface.co/datasets/hakari-bench/NanoMIRACL) |
| Language | es |
| Category | natural_language |
| Queries | 200 |
| Documents | 1,312 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.6861 |
| BM25 hit@10 | 0.9900 |
| BM25 Recall@100 | 0.9807 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.7793 |
| Dense hit@10 | 0.9350 |
| Dense Recall@100 | 0.9133 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.7478 |
| Reranking hybrid hit@10 | 0.9900 |
| Reranking hybrid Recall@100 | 1.0000 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100 |
| Reranking hybrid safeguard rows | 0 |
| Query length avg chars | 48.21 |
| Document length avg chars | 612.47 |

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
  task_name: es
  split_name: es
  language: es
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMIRACL/es.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 200
    documents: 1312
    positive_qrels: 200
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 48.21
    document_mean: 612.473323
  bm25:
    ndcg_at_10: 0.6860703911912536
    hit_at_10: 0.99
    source: dataset_candidate_subset
  learning:
    original_train_split: available
    evaluation_split_origin: unknown
    train_eval_overlap_audit: not_audited
    leakage_note: prefer excluding upstream development/test data or other MIRACL-derived
      data likely to overlap with the NanoMIRACL evaluation questions and passages
    useful_training_data:
    - non-overlapping MIRACL Spanish train split data
    - Spanish Wikipedia question-to-passage retrieval pairs
    - Spanish open-domain QA evidence retrieval datasets
    synthetic_data:
      document_generation: Spanish Wikipedia-style passages with titles, aliases,
        dates, locations, lists, definitions, and factual evidence
      question_generation: natural Spanish fact questions using varied qué, cuál,
        cómo, por qué, quién, cuándo, dónde, and cuántos forms
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
      ndcg_at_10: 0.6860703912
      hit_at_10: 0.99
      recall_at_100: 0.9807280514
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9807280514
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.7793227222
      hit_at_10: 0.935
      recall_at_100: 0.9132762313
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9132762313
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.7478415097
      hit_at_10: 0.99
      recall_at_100: 1.0
      candidate_count_min: 100
      candidate_count_max: 100
      candidate_count_mean: 100.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 1.0
      safeguard_positive_rows: 0
      rows_with_101_candidates: 0
```
