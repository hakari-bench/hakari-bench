# NanoBIRCO / NanoBIRCORelic

## Overview

BIRCO includes RELIC as literary evidence retrieval: the query is a scholarly
analysis passage where a quotation has been replaced by a mask, and the target
is the original literary sentence or passage that completes the argument. This
Nano task is single-positive and uses long criticism-style queries against
classic literature passages. A retriever has to infer the missing quotation
from interpretive context about authors such as Lawrence, Orwell, Dreiser,
Dickens, and Austen, not merely match named works.

## Details

### What the Original Data Measures

[BIRCO: A Benchmark of Information Retrieval Tasks with Complex
Objectives](https://arxiv.org/abs/2402.14151) includes RELIC as one of five
complex-objective retrieval tasks. The paper describes RELIC as 100 queries
drawn from scholars analyzing classic English-language literature. Passages are
sentences from novels, and the objective is to recover the masked quotation in a
literary analysis.

The appendix task objective says the query contains literary analysis in which
one or more quotations are replaced by `[masked sentence(s)]`. The retrieved
passage should directly support at least one claim made in the surrounding
analysis, but it should not merely repeat the same thing as the preceding or
subsequent context. This is a non-standard retrieval objective: the model must
infer what textual evidence would make the analysis coherent.

BIRCO reports RELIC as a particularly difficult task for embedding methods. In
the paper's comparison table, RELIC has low lexical overlap and low E5-v2
nDCG@10 despite a small candidate pool. The decontamination section reports that
8% of RELIC queries were removed after checking whether an LLM could generate
the masked sentence from context.

### Observed Data Profile

The sampled Nano task has 100 queries, 5,023 documents, and 100 positive qrel
rows. Every query has exactly one positive passage. Queries average 1,016.31
characters and are paragraph-length excerpts of literary criticism. Documents
average 477.34 characters and are literary passages, often from classic novels.

The observed positives cover discussions of D. H. Lawrence, Orwell, Dreiser,
Dickens, Austen, and other literary works. Queries frequently give a detailed
interpretive setup, then mark the missing quotation with `[masked sentence(s)]`.
The correct passage may be a sentence or short paragraph that captures a mood,
social relation, irony, character perception, or narrative contrast.

The task is difficult because lexical overlap is not the point. The query often
contains critic language, while the positive passage is original literary prose.
The retriever must infer which quotation would support the analysis, not simply
find repeated words.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.0633
and hit@10 = 0.1200 on this Nano split. BM25 places only 2 of 100 positives at
rank 1 and only 12 of 100 positives in the top 10. This is the weakest BM25
profile among the inspected NanoBIRCO tasks.

The failures show why lexical matching breaks down. For a `Sister Carrie`
analysis about desire, sensory gratification, and urban striving, BM25 ranks
other passages about Carrie's profession and social situations before the
positive passage about city offices and carriages. For a `Barnaby Rudge`
analysis about mystery and Lord Gordon, BM25 retrieves adjacent or more literal
passages before the longer positive passage about mystery as a tool of crowd
attraction. For `Sense and Sensibility`, passages mentioning Elinor, Lucy, and
Edward compete closely, but the positive is the one that fits the analyst's
discourse about prominence and social knowledge.

Because this split is single-positive, hit@10 is straightforward: most BM25 top
10 lists do not contain the labeled quotation. A stronger model needs
discourse-level matching between literary criticism and source prose.

### Training Data That May Help

Useful training data should include non-overlapping literary evidence retrieval
pairs, quotation recovery tasks, and literary analysis paired with supporting
source passages. RELIC or BIRCO development data should be inspected for overlap
before use. Hard negatives should include passages from the same work, chapter,
or character cluster that share names but do not support the specific analytic
claim.

Training should avoid turning the task into memorized quotation lookup. The
goal is to learn how critical prose points to evidence in a text, including
tone, irony, character relation, and narrative function.

### Synthetic Data Guidance

For document-to-question generation, start from public-domain literary passages
and generate literary-analysis contexts with a masked quotation. For joint
generation, create a short source passage and a critical paragraph that refers
to its narrative function, character relation, tone, or imagery.

Do not seed generation with Nano evaluation queries or positive passages.
Include same-work distractors with overlapping characters and themes so the
model must identify the passage that actually supports the analysis.

## Example Data

| Query | Positive document |
| --- | --- |
| Euripides' god, in contrast, is conceived agnostically; he is described in the Hercules as "Jove, whoe'er/ That Jove may be". In all, Moby Dick is strikingly similar to Dionysus, the daemon bull-god of Euripides' Bacchae. Thi ... [truncated 225 chars](650 chars) | thou clear spirit of clear fire, whom on these seas I as Persian once did worship, till in the sacramental act so burned by thee, that to this hour I bear the scar; I now know thee, thou clear spirit, and I now know that thy ... [truncated 225 chars](252 chars) |
| Let us look at the way. Lawrence begins The Rainbow, which was originally to have been the first part of a long novel of which Women in Love was Part II. The Rainbow is about the Brangwen family and about three generations of ... [truncated 225 chars](829 chars) | But heaven and earth was teeming around them, and how should this cease? They felt the rush of the sap in spring, they knew the wave which cannot halt, but every year throws forward the seed to begetting, and, falling back, l ... [truncated 225 chars](794 chars) |
| the latter follows the former in the use of means that drug the masses. The "Semi-Demi Finals of the Women's Heavyweight Wrestling Championship" do not differ greatly from the fascist rallies and parades of the 1930s. In both ... [truncated 225 chars](1164 chars) | Round they went, a circular procession of dancers, each with hands on the hips of the dancer preceding, round and round, shouting in unison, stamping to the rhythm of the music with their feet, beating it, beating it out with ... [truncated 225 chars](342 chars) |
| the monster is likewise doomed to an existence of loneliness and homelessness. Sublimity, supposedly transcendent in value, is in fact a destruction of the common values and pleasures of human existence. Mary Shelley signals ... [truncated 225 chars](1122 chars) | Delighted and surprised, I embraced her, but as I imprinted the first kiss on her lips, they became livid with the hue of death; her features appeared to change, and I thought that I held the corpse of my dead mother in my ar ... [truncated 225 chars](323 chars) |
| She can be his inspiration; her intuitive capacity, often superior to man's, can give him timely warning, and her feeling, always directed towards the personal, can show him ways which his own less personally accented feeling ... [truncated 225 chars](1000 chars) | But on other moonlight nights, when the sadness and the silence have touched me in a different way-have affected me with something as like a sorrowful sense of peace, as any emotion that had pain for its foundations could-I h ... [truncated 225 chars](433 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoBIRCO |
| Backing dataset | NanoBIRCO |
| Task / split | NanoBIRCORelic |
| Hugging Face dataset | [hakari-bench/NanoBIRCO](https://huggingface.co/datasets/hakari-bench/NanoBIRCO) |
| Language | en |
| Category | natural_language |
| Queries | 100 |
| Documents | 5,023 |
| Positive qrels | 100 |
| BM25 nDCG@10 | 0.0633 |
| BM25 hit@10 | 0.1200 |
| Query length avg chars | 1016.31 |
| Document length avg chars | 477.34 |

### Public Sources

- [BIRCO: A Benchmark of Information Retrieval Tasks with Complex Objectives](https://arxiv.org/abs/2402.14151); 2024; Xiaoyue Wang, Jianyou Wang, Weili Cao, Kaicheng Wang, Ramamohan Paturi, Leon Bergen; DOI: `10.48550/arXiv.2402.14151`.
- [BIRCO GitHub repository](https://github.com/BIRCO-benchmark/BIRCO).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBIRCO](https://huggingface.co/datasets/hakari-bench/NanoBIRCO)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| BIRCO: A Benchmark of Information Retrieval Tasks with Complex Objectives | 2024 | paper | https://arxiv.org/abs/2402.14151 |
| BIRCO GitHub repository |  | project repository | https://github.com/BIRCO-benchmark/BIRCO |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoBIRCO
  backing_dataset: NanoBIRCO
  dataset_id: hakari-bench/NanoBIRCO
  task_name: NanoBIRCORelic
  split_name: NanoBIRCORelic
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoBIRCO/NanoBIRCORelic.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 100
    documents: 5023
    positive_qrels: 100
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 1016.31
    document_mean: 477.338244
  bm25:
    ndcg_at_10: 0.0633094248
    hit_at_10: 0.12
    source: dataset_bm25_column
  learning:
    original_train_split: available
    evaluation_split_origin: test
    train_eval_overlap_audit: not_audited
    leakage_note: prefer excluding RELIC/BIRCO evaluation queries, masked contexts, source passages, and same-work candidate pools from training data
    useful_training_data:
      - non-overlapping literary evidence retrieval pairs
      - quotation recovery tasks from public-domain literature
      - literary analysis paired with supporting source passages
      - same-work hard negatives that share characters or themes but do not support the claim
    synthetic_data:
      document_generation: public-domain literary passages with character actions, tone, imagery, irony, and narrative context
      question_generation: literary-analysis contexts with one or more masked quotations and surrounding interpretive claims
      answerability: the positive passage should directly support the surrounding analysis without merely repeating adjacent context
    multi_positive_training: single_positive_quotation_recovery_focus
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoBIRCO
    source_urls:
      - label: BIRCO GitHub repository
        url: https://github.com/BIRCO-benchmark/BIRCO
    source_notes: []
  references:
    - title: 'BIRCO: A Benchmark of Information Retrieval Tasks with Complex Objectives'
      url: https://arxiv.org/abs/2402.14151
      year: 2024
      doi: 10.48550/arXiv.2402.14151
      is_paper: true
      source_confidence: definitive_paper_link
    - title: BIRCO GitHub repository
      url: https://github.com/BIRCO-benchmark/BIRCO
      year: null
      doi: null
      is_paper: false
      source_confidence: official_project_repository
```
