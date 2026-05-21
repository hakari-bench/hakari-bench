# NanoMIRACL / sw

## Overview

MIRACL's Swahili split is intended as same-language retrieval over Swahili
Wikipedia passages, with native-language question and relevance data. The Nano
task keeps that framing but the inspected corpus shows some multilingual noise,
which makes exact language handling part of the practical retrieval problem.
Queries are short factual questions with starts such as `Je,`, `Mji`, `Rais`,
`Nchi`, `Jina`, and `Nani`; the model must still recover the passage about the
right person, country, political fact, science topic, geography item, medical
term, sport, music topic, or definition.

## Details

### What the Original Data Measures

[Making a MIRACL: Multilingual Information Retrieval Across a Continuum of
Languages](https://arxiv.org/abs/2210.09984) describes MIRACL as a monolingual
ad hoc retrieval benchmark over Wikipedia passages. Swahili queries retrieve
Swahili Wikipedia passages, so the task measures same-language retrieval rather
than cross-lingual search. The paper states that MIRACL uses well-formed
questions and native-speaker relevance judgments over passage-level corpora.

Swahili is one of the MIRACL languages inherited from Mr. TyDi and TyDi QA. The
paper explains that, for these languages, MIRACL aligns with the Mr. TyDi split
structure while adding denser passage-level annotations and fixing corpus
segmentation issues. This makes the task a retrieval benchmark over Swahili
Wikipedia passages, not answer extraction from a single selected article.

MIRACL annotators generated questions from Wikipedia prompts and judged
candidate passages returned by an ensemble of BM25, mDPR, and mColBERT. For
Swahili, the MIRACL overview reports development-set BM25 nDCG@10 of 0.383 and
hybrid BM25+mDPR nDCG@10 of 0.446. That gap is useful context for this split:
lexical retrieval is often strong enough to find the right topic, but hybrid
ranking can still help when the answer is expressed through paraphrase,
inflection, or a relation inside a longer passage.

### Observed Data Profile

The sampled Nano task has 200 queries, 1,600 documents, and 200 positive qrel
rows. Every query has exactly one positive passage. Queries average 38.33
characters. The most common starts are `Je,`, `Mji`, `Je`, `Rais`, `Nchi`,
`Jina`, and `Nani`, with many variants where punctuation is attached directly
to the next word, such as `Je,mwanamziki` or `Je,rais`.

Documents average 532.75 characters and usually begin with a Wikipedia article
title. The observed positives cover thermometers, Beyonce, railway gauge,
footballers, physiology, Mozambique borders, FIFA, KANU and Kenyan politics,
giraffe pregnancy, the Atlantic Ocean, Kenya, HIV/AIDS, beans, Saint Peter, and
other short encyclopedia facts. The repository metadata labels the split as
`multilingual` and lists both `sw` and `en`; the sampled data is primarily
Swahili, but English names, loanwords, and some non-Swahili passages or detector
confusions are visible.

The task is dominated by short fact questions. Many positives contain the exact
entity name and a compact answer sentence, but several queries ask for a
relation that is easy to miss: inventor, birth date, capital, scientific name,
office holder, border count, or duration. A strong model should rank the
answer-bearing passage above related pages that share the entity, country, or
topic but do not answer the requested relation.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.5782
and hit@10 = 0.8150 on this Nano split. BM25 places 69 of 200 positives at rank
1 and 163 of 200 positives in the top 10. It works well for distinctive names
and terms such as `Beyonce`, `Samir Nasri`, `FIFA`, and `Kipima joto`, but it
misses 37 positives from the top 10.

The failures show near-topic lexical traps. For "Nchi ya Msumbiji imepakana na
nchi ngapi?", BM25 ranks district and Tanzania geography passages before the
Mozambique passage that lists the bordering countries. For "Je,rais wa kwanza
wa Marekani aliitwa nani?", pages about current or other national leaders can
outrank the U.S. presidents list. For "Je,twiga hubeba uja uzito kwa miezi
ngapi?", pregnancy and weight-related vocabulary pulls unrelated passages above
the giraffe passage. For "Jina la kisayansi la maharagwe ni nini?", a related
bean page can outrank the passage that names `Phaseolus vulgaris`.

Because this Nano split is single-positive, hit@10 measures whether the labeled
evidence passage appears at all. nDCG@10 is still important because many
queries have plausible near matches that mention the same entity or category
but answer the wrong attribute.

### Training Data That May Help

Non-overlapping Swahili MIRACL training data is the first source to inspect.
Because this task is MIRACL-derived, upstream development or test queries,
qrels, and positive passages likely to overlap with NanoMIRACL should
preferably be excluded from training. Other useful data includes Swahili
Wikipedia question-to-passage retrieval pairs, Swahili open-domain QA evidence
retrieval data, and multilingual African-language QA pairs with explicit
Swahili evidence passages.

Training should focus on evidence passage retrieval. The model needs to map
short Swahili fact questions to the passage that contains the requested
attribute, while distinguishing related country, person, organization, or
definition passages that share high lexical overlap.

### Synthetic Data Guidance

For document-to-question generation, use non-evaluation Swahili
Wikipedia-style passages and generate Swahili questions grounded in one
selected passage. Useful forms include `Je`, `Nani`, `Mji`, `Nchi`, `Jina`,
`Rais`, `Ni nini`, `lini`, and `ngapi`, with realistic punctuation and spacing
variants because the observed queries often attach commas directly to words.

For joint document-and-question generation, create Swahili encyclopedia-style
passages with article titles, aliases, dates, locations, offices, borders,
scientific names, definitions, and short biographical facts, then generate
answerable questions. Do not seed generation with Nano evaluation queries or
positive passages. Include related but non-answering distractors around the
same country, person, institution, animal, disease, or scientific term.

## Example Data

| Query | Positive document |
| --- | --- |
| Chelsea F.C. ilizinduliwa lini? (31 chars) | Chelsea F.C. Chelsea Football Club ni klabu ya mpira wa miguu ya nchini Uingereza iliyo na maskani yake Fulham, London. Klabu hii ilianzishwa mwaka 1905, na kwa miaka mingi sana imekuwa ikishiriki ligi kuu ya Uingereza. Uwanj ... [truncated 225 chars](358 chars) |
| Rais wa kwanza wa Gabon aliitwa nani? (37 chars) | Omar Bongo Kiongozi huyo amevunja rekodi ya kuwa Rais aliyekaa muda mrefu marakani kuliko Rais yeyote barani Afrika. Rais huyo amefariki dunia akiwa na umri wa miaka 73, ambapo ameiongoza Gabon kwa miaka 42. Bongo alijiunga n ... [truncated 225 chars](1262 chars) |
| Je,nani mwanzilishi wa mziki wa hIhop nchini Tanzania? (54 chars) | Machozi Jasho na Damu Halkadhalika ame-enzi kazi ya mwanzilishi halisi wa rap ya Kiswahili nchini Tanzania bwana Edward Mtui (maarufu kama Fresh XE) kwa kuchukua kiitikio chake cha "Piga Makofi" ambacho kilimpelekea ashinde t ... [truncated 225 chars](411 chars) |
| Nigeria ilipata huru mwaka gani? (32 chars) | Ahmadu Bello Katika uchaguzi wa kwanza uliofanyika Kaskazini mwa Nigeria mwaka 1952, Bwana Ahmadu Bello alishinda [[kiti[[ cha bunge cha Kaskazini, na kuwa mwanachama wa [[baraza tendaji]] kikanda kama [[waziri wa kazi]]. Bel ... [truncated 225 chars](1288 chars) |
| Nani alikuwa rais wa kwanza Urusi? (34 chars) | Boris Yeltsin Boris Nikolayevich Yeltsin () (kwa herufi za Kirusi huita:Бори́с Никола́евич Е́льцин) (1 Februari 1931 - 23 Aprili 2007) alikuwa rais wa kwanza wa Urusi baada ya mwisho wa ukomunisti. Alitumikia taifa la Urusi k ... [truncated 225 chars](453 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMIRACL |
| Backing dataset | NanoMIRACL |
| Task / split | sw |
| Hugging Face dataset | [hakari-bench/NanoMIRACL](https://huggingface.co/datasets/hakari-bench/NanoMIRACL) |
| Language | multilingual (primarily sw; config also lists en) |
| Category | natural_language |
| Queries | 200 |
| Documents | 1,600 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.5782 |
| BM25 hit@10 | 0.8150 |
| Query length avg chars | 38.33 |
| Document length avg chars | 532.75 |

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
  task_name: sw
  split_name: sw
  language: multilingual
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMIRACL/sw.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 200
    documents: 1600
    positive_qrels: 200
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 38.33
    document_mean: 532.750625
  bm25:
    ndcg_at_10: 0.5781778774
    hit_at_10: 0.815
    source: dataset_bm25_column
  learning:
    original_train_split: available
    evaluation_split_origin: unknown
    train_eval_overlap_audit: not_audited
    leakage_note: prefer excluding upstream development/test data or other MIRACL-derived data likely to overlap with the NanoMIRACL evaluation questions and passages
    useful_training_data:
      - non-overlapping MIRACL Swahili train split data
      - Swahili Wikipedia question-to-passage retrieval pairs
      - Swahili open-domain QA evidence retrieval datasets
      - multilingual African-language QA pairs with explicit Swahili evidence passages
    synthetic_data:
      document_generation: Swahili Wikipedia-style passages with titles, aliases, dates, locations, offices, borders, scientific names, definitions, and factual evidence
      question_generation: Swahili fact questions using Je, Nani, Mji, Nchi, Jina, Rais, Ni nini, lini, and ngapi forms with realistic punctuation and spacing variants
      answerability: questions should be grounded in explicit facts or relations in the generated or selected passage
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
    source_notes:
      - repository metadata labels this split as multilingual and lists sw and en, although observed queries and positives are primarily Swahili
  references:
    - title: 'Making a MIRACL: Multilingual Information Retrieval Across a Continuum of Languages'
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
    - title: MIRACL GitHub repository
      url: https://github.com/project-miracl/miracl
      year: null
      doi: null
      is_paper: false
      source_confidence: official_project_repository
    - title: MIRACL corpus dataset
      url: https://huggingface.co/datasets/miracl/miracl-corpus
      year: null
      doi: null
      is_paper: false
      source_confidence: official_dataset_card
    - title: MIRACL source queries and qrels
      url: https://huggingface.co/datasets/miracl/miracl
      year: null
      doi: null
      is_paper: false
      source_confidence: official_dataset_card
```
