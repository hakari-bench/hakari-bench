# NanoMTEB-v2

> [!NOTE]
> This page was prepared by manual review of source papers, dataset cards,
> repository metadata, and sampled benchmark data. It may contain mistakes;
> please treat it as a reference aid rather than a definitive source.

## Overview

NanoMTEB-v2 is the English retrieval group derived from MTEB v2-style retrieval
tasks. It combines ten compact splits covering argument retrieval, claim
evidence retrieval, StackExchange duplicate-question retrieval, financial QA,
multi-hop Wikipedia QA, scientific paper recommendation, controversial-question
argument retrieval, and biomedical literature search. The group is useful
because it is not a single-domain English benchmark: a model must handle long
debate prose, short fact-checking claims, terse technical forum titles,
financial advice questions, scientific paper titles, and COVID-19 information
needs.

## Details

### What the Original Group Measures

[MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316)
standardized retrieval evaluation across many datasets using BEIR-style corpora,
queries, qrels, and nDCG@10. NanoMTEB-v2 keeps that retrieval framing but uses a
small Nano subset for each split. The underlying sources are heterogeneous:
ArguAna tests counterargument retrieval, CLIMATE-FEVER and FEVER test
Wikipedia evidence retrieval for claims, CQADupStack tests duplicate question
retrieval, FiQA tests financial question-answer retrieval, HotpotQA tests
multi-hop supporting-passage retrieval, SCIDOCS tests scientific paper
relatedness, Touché tests argument retrieval for controversial questions, and
TREC-COVID tests biomedical literature retrieval.

The observed data confirms that the group mixes very different relevance
relations. In `argu_ana`, the positive is not a semantically similar supporting
passage; it is the paired opposing argument. In `hotpot_qa`, each question has
two supporting Wikipedia passages. In `touche2020_v3` and `treccovid`, each
query can have many relevant documents, so ranking quality matters even after a
model retrieves one positive. In `scidocs`, relevance often comes from citation
or research affinity rather than exact lexical overlap between paper titles.

### Subtask Coverage

The ten subtasks cover six retrieval families:

- **Argument retrieval:** `argu_ana` retrieves stance-opposed counterarguments,
  while `touche2020_v3` retrieves argument passages for controversial questions.
- **Claim and evidence retrieval:** `climate_fever` and `fever` retrieve
  Wikipedia evidence for climate or general factual claims.
- **Community duplicate retrieval:** `cqadupstack_gaming` and
  `cqadupstack_unix` retrieve duplicate or near-duplicate StackExchange
  questions from short titles.
- **Question-answer retrieval:** `fi_qa2018` retrieves financial advice or
  answer passages, and `hotpot_qa` retrieves Wikipedia supporting passages for
  multi-hop questions.
- **Scientific retrieval:** `scidocs` retrieves related scientific papers from
  paper-title queries.
- **Biomedical literature retrieval:** `treccovid` retrieves COVID-19 article
  records for TREC-style information needs.

All splits are English-labeled natural-language retrieval tasks, but the text
style changes sharply. ArguAna queries are long debate arguments averaging about
1,200 characters. CQADupStack and Touché queries are short titles or questions.
TREC-COVID and SCIDOCS documents usually include title-plus-abstract records,
while FEVER-style documents are Wikipedia passages.

### Observed Group Profile

Across the ten splits, NanoMTEB-v2 contains 1,698 queries, 10,158 positive
qrels, and 98,626 split-local candidate documents. The document count is a sum
over split-local corpora, not a deduplicated group-wide corpus size. Most splits
have 200 queries; `argu_ana` has 199, `touche2020_v3` has 49, and `treccovid`
has 50.

The group is strongly multi-positive overall, but not uniformly. `argu_ana` is
single-positive. `hotpot_qa`, `scidocs`, `touche2020_v3`, and `treccovid` are
multi-positive for every query. `treccovid` is the most extreme case, with 4,584
positive qrels for only 50 queries and a median of 100 positives per query.
This makes group-level averages sensitive to the retrieval task mix: a model
that is good at finding any biomedical article for a broad TREC-COVID topic may
not be equally good at SCIDOCS scientific relatedness or ArguAna
counterargument matching.

### BM25 Difficulty

Query-weighted BM25 nDCG@10 is 0.4852 and query-weighted hit@10 is 0.7167. The
unweighted task means are higher for nDCG@10 at 0.5409 and hit@10 at 0.7578,
because the smaller TREC-COVID and Touché splits are easier for BM25 and receive
less weight in the query-weighted average.

The task-level spread is large. `treccovid` is the easiest by nDCG@10 at 0.9039,
and `fever` and `hotpot_qa` are also very high. These splits often contain
strong entity or biomedical term overlap between query and relevant passage.
`scidocs` and `climate_fever` are the hardest by nDCG@10 at about 0.193. For
SCIDOCS, the positive paper can be related through research topic or citation
context even when the query title shares few exact words. For Climate-FEVER,
short claims may require evidence under broader Wikipedia topics rather than a
document whose title repeats the claim.

BM25 is therefore a useful diagnostic for this group: high lexical overlap
solves some FEVER, HotpotQA, and TREC-COVID cases, but lexical matching is much
less reliable for scientific relatedness, climate evidence, finance answers,
argument matching, and duplicate technical questions with paraphrased titles.

### Training Data That May Help

Useful training data should be selected by retrieval family. Claim-evidence
training can use non-overlapping FEVER, climate fact-checking, and
Wikipedia-evidence pairs. Community QA training can use StackExchange
duplicate-question pairs and answer retrieval data outside the evaluation
examples. Scientific and biomedical retrieval can use citation-linked papers,
paper recommendation data, PubMed-style title-abstract search data, and
TREC-COVID-like topics. Argument retrieval benefits from debate corpora,
counterargument pairs, stance-labeled arguments, and controversial-question
argument collections.

Training should exclude NanoMTEB-v2 queries, qrels, and positive documents.
Because these splits are derived from well-known public datasets, upstream test
sets and benchmark packages should be treated as potential leakage sources
unless an explicit overlap audit is performed. This is especially important for
FEVER, HotpotQA, TREC-COVID, ArguAna, CQADupStack, and SCIDOCS, which are common
in retrieval and embedding training mixtures.

### Synthetic Data Guidance

Synthetic data for NanoMTEB-v2 should preserve the retrieval relation for each
family instead of producing generic paraphrase pairs. For ArguAna, positives
should counter the query while discussing the same aspect. For FEVER-style
tasks, positives should contain evidence for or against the claim, and hard
negatives should share entities but not the required fact. For CQADupStack,
synthetic pairs should use different surface wording for the same technical or
gaming problem. For HotpotQA, the query should require two supporting passages.
For SCIDOCS, positives should be scientifically related papers, not only papers
with matching title tokens. For TREC-COVID, positives should address the
information need by population, intervention, outcome, mechanism, or evidence
type.

Generated negatives should be close in vocabulary but wrong in relevance. Do
not seed synthetic generation with NanoMTEB-v2 evaluation queries or positive
documents.

## Task Summary

| Task | Retrieval shape | Queries | Docs | Positives | BM25 nDCG@10 | BM25 hit@10 | Query avg chars | Doc avg chars | Source status |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| [argu_ana](argu_ana.md) | debate argument to counterargument | 199 | 8,626 | 199 | 0.3326 | 0.7085 | 1,199.80 | 1,029.60 | ArguAna + MTEB papers |
| [climate_fever](climate_fever.md) | climate claim to Wikipedia evidence | 200 | 10,000 | 621 | 0.1934 | 0.4750 | 114.97 | 1,115.93 | CLIMATE-FEVER + MTEB papers |
| [cqadupstack_gaming](cqadupstack_gaming.md) | gaming question title to duplicate question | 200 | 10,000 | 415 | 0.4888 | 0.6850 | 47.62 | 481.08 | CQADupStack + MTEB papers |
| [cqadupstack_unix](cqadupstack_unix.md) | Unix question title to duplicate question | 200 | 10,000 | 486 | 0.3666 | 0.5350 | 49.21 | 969.12 | CQADupStack + MTEB papers |
| [fever](fever.md) | factual claim to Wikipedia evidence | 200 | 10,000 | 229 | 0.8951 | 0.9950 | 50.56 | 565.98 | FEVER + MTEB papers |
| [fi_qa2018](fi_qa2018.md) | finance question to answer passage | 200 | 10,000 | 534 | 0.3385 | 0.5950 | 61.70 | 780.39 | FiQA + MTEB papers |
| [hotpot_qa](hotpot_qa.md) | multi-hop question to supporting passages | 200 | 10,000 | 400 | 0.8891 | 1.0000 | 95.83 | 421.20 | HotpotQA + MTEB papers |
| [scidocs](scidocs.md) | paper title to related paper | 200 | 10,000 | 986 | 0.1933 | 0.6050 | 69.79 | 1,202.68 | SCIDOCS/SPECTER + MTEB papers |
| [touche2020_v3](touche2020_v3.md) | controversial question to argument passage | 49 | 10,000 | 1,704 | 0.8083 | 0.9796 | 43.43 | 2,386.21 | Touché 2020 + MTEB papers |
| [treccovid](treccovid.md) | COVID-19 information need to article record | 50 | 10,000 | 4,584 | 0.9039 | 1.0000 | 69.24 | 1,326.60 | TREC-COVID + MTEB papers |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMTEB-v2 |
| Backing dataset | NanoMTEB-v2 |
| Hugging Face dataset | [hakari-bench/NanoMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoMTEB-v2) |
| Language | en |
| Category | natural_language |
| Subtasks | 10 |
| Total queries | 1,698 |
| Split-local documents | 98,626 |
| Positive qrels | 10,158 |
| Positives per query | avg 5.98, min 1, median varies by split, max 100 |
| Multi-positive subtasks | 9 of 10 |
| Multi-positive queries | 982 |
| Query-weighted BM25 nDCG@10 | 0.4852 |
| Query-weighted BM25 hit@10 | 0.7167 |
| Mean query length | 201.58 chars, weighted by query count |
| Mean document length | 1,027.86 chars, weighted by split-local document count |

### Public Sources

- [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316); 2023; Niklas Muennighoff et al.
- [Retrieval of the Best Counterargument without Prior Topic Knowledge](https://aclanthology.org/P18-1023/); 2018; ArguAna source paper.
- [CLIMATE-FEVER: A Dataset for Verification of Real-World Climate Claims](https://arxiv.org/abs/2012.00614); 2020.
- [CQADupStack: A Benchmark Data Set for Community Question-Answering Research](https://eltimster.github.io/www/pubs/adcs2015.pdf); 2015.
- [FEVER: a Large-scale Dataset for Fact Extraction and VERification](https://arxiv.org/abs/1803.05355); 2018.
- [Financial Opinion Mining and Question Answering](https://doi.org/10.1145/3184558.3192301); 2018.
- [HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering](https://arxiv.org/abs/1809.09600); 2018.
- [SPECTER: Document-level Representation Learning using Citation-informed Transformers](https://arxiv.org/abs/2004.07180); 2020; source for SCIDOCS context.
- [Overview of Touché 2020: Argument Retrieval](https://downloads.webis.de/touche/publications/papers/bondarenko_2020d.pdf); 2020.
- [TREC-COVID: Constructing a Pandemic Information Retrieval Test Collection](https://arxiv.org/abs/2005.04474); 2020.
- [NIST TREC-COVID challenge page](https://ir.nist.gov/covidSubmit/index.html).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoMTEB-v2)
- Source datasets:
  [mteb/arguana](https://huggingface.co/datasets/mteb/arguana),
  [mteb/ClimateFEVER_test_top_250_only_w_correct-v2](https://huggingface.co/datasets/mteb/ClimateFEVER_test_top_250_only_w_correct-v2),
  [mteb/cqadupstack-gaming](https://huggingface.co/datasets/mteb/cqadupstack-gaming),
  [mteb/cqadupstack-unix](https://huggingface.co/datasets/mteb/cqadupstack-unix),
  [mteb/FEVER_test_top_250_only_w_correct-v2](https://huggingface.co/datasets/mteb/FEVER_test_top_250_only_w_correct-v2),
  [mteb/fiqa](https://huggingface.co/datasets/mteb/fiqa),
  [mteb/HotpotQA_test_top_250_only_w_correct-v2](https://huggingface.co/datasets/mteb/HotpotQA_test_top_250_only_w_correct-v2),
  [mteb/scidocs](https://huggingface.co/datasets/mteb/scidocs),
  [mteb/webis-touche2020-v3](https://huggingface.co/datasets/mteb/webis-touche2020-v3),
  [mteb/trec-covid](https://huggingface.co/datasets/mteb/trec-covid).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| MTEB: Massive Text Embedding Benchmark | 2023 | benchmark paper | https://arxiv.org/abs/2210.07316 |
| Retrieval of the Best Counterargument without Prior Topic Knowledge | 2018 | source task paper | https://aclanthology.org/P18-1023/ |
| CLIMATE-FEVER: A Dataset for Verification of Real-World Climate Claims | 2020 | source task paper | https://arxiv.org/abs/2012.00614 |
| CQADupStack: A Benchmark Data Set for Community Question-Answering Research | 2015 | source task paper | https://eltimster.github.io/www/pubs/adcs2015.pdf |
| FEVER: a Large-scale Dataset for Fact Extraction and VERification | 2018 | source task paper | https://arxiv.org/abs/1803.05355 |
| Financial Opinion Mining and Question Answering | 2018 | source task paper | https://doi.org/10.1145/3184558.3192301 |
| HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering | 2018 | source task paper | https://arxiv.org/abs/1809.09600 |
| SPECTER: Document-level Representation Learning using Citation-informed Transformers | 2020 | source task paper | https://arxiv.org/abs/2004.07180 |
| Overview of Touché 2020: Argument Retrieval | 2020 | source task paper | https://downloads.webis.de/touche/publications/papers/bondarenko_2020d.pdf |
| TREC-COVID: Constructing a Pandemic Information Retrieval Test Collection | 2020 | source task paper | https://arxiv.org/abs/2005.04474 |
| NIST TREC-COVID challenge page | 2020 | source data page | https://ir.nist.gov/covidSubmit/index.html |

## Machine-Readable Metadata

<!-- benchmark-task-group-metadata:v1 -->

```yaml
benchmark_task_group_metadata:
  schema_version: 1
  document_status: reviewed_manual
  nano_set: NanoMTEB-v2
  backing_dataset: NanoMTEB-v2
  dataset_id: hakari-bench/NanoMTEB-v2
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMTEB-v2/index.md
  source_research:
    primary_source_type: task_papers_and_benchmark_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    tasks: 10
    queries: 1698
    split_local_documents: 98626
    positive_qrels: 10158
  positives_per_query:
    average: 5.982332155477032
    min: 1
    median: null
    max: 100
    multi_positive_tasks: 9
    multi_positive_queries: 982
  text_stats_chars:
    query_mean_weighted_by_queries: 201.58127208480568
    document_mean_weighted_by_documents: 1027.856386754
  bm25:
    ndcg_at_10_query_weighted: 0.48523283029423026
    hit_at_10_query_weighted: 0.7167255594817432
    ndcg_at_10_unweighted_task_mean: 0.5409424516462953
    hit_at_10_unweighted_task_mean: 0.7578134550302533
    source: dataset_bm25_column
    easiest_task_by_ndcg_at_10: treccovid
    hardest_task_by_ndcg_at_10: scidocs
  tasks:
    - name: argu_ana
      path: docs/benchmark_tasks/NanoMTEB-v2/argu_ana.md
      retrieval_shape: debate_argument_to_counterargument
      queries: 199
      documents: 8626
      positive_qrels: 199
      bm25_ndcg_at_10: 0.3325660140573749
      bm25_hit_at_10: 0.7085427135678392
    - name: climate_fever
      path: docs/benchmark_tasks/NanoMTEB-v2/climate_fever.md
      retrieval_shape: climate_claim_to_wikipedia_evidence
      queries: 200
      documents: 10000
      positive_qrels: 621
      bm25_ndcg_at_10: 0.19336752051783465
      bm25_hit_at_10: 0.475
    - name: cqadupstack_gaming
      path: docs/benchmark_tasks/NanoMTEB-v2/cqadupstack_gaming.md
      retrieval_shape: gaming_question_title_to_duplicate_question
      queries: 200
      documents: 10000
      positive_qrels: 415
      bm25_ndcg_at_10: 0.4888328019086286
      bm25_hit_at_10: 0.685
    - name: cqadupstack_unix
      path: docs/benchmark_tasks/NanoMTEB-v2/cqadupstack_unix.md
      retrieval_shape: unix_question_title_to_duplicate_question
      queries: 200
      documents: 10000
      positive_qrels: 486
      bm25_ndcg_at_10: 0.36656783742488813
      bm25_hit_at_10: 0.535
    - name: fever
      path: docs/benchmark_tasks/NanoMTEB-v2/fever.md
      retrieval_shape: factual_claim_to_wikipedia_evidence
      queries: 200
      documents: 10000
      positive_qrels: 229
      bm25_ndcg_at_10: 0.8951263986829078
      bm25_hit_at_10: 0.995
    - name: fi_qa2018
      path: docs/benchmark_tasks/NanoMTEB-v2/fi_qa2018.md
      retrieval_shape: finance_question_to_answer_passage
      queries: 200
      documents: 10000
      positive_qrels: 534
      bm25_ndcg_at_10: 0.33847946359419095
      bm25_hit_at_10: 0.595
    - name: hotpot_qa
      path: docs/benchmark_tasks/NanoMTEB-v2/hotpot_qa.md
      retrieval_shape: multi_hop_question_to_supporting_passages
      queries: 200
      documents: 10000
      positive_qrels: 400
      bm25_ndcg_at_10: 0.889065539981155
      bm25_hit_at_10: 1.0
    - name: scidocs
      path: docs/benchmark_tasks/NanoMTEB-v2/scidocs.md
      retrieval_shape: paper_title_to_related_paper
      queries: 200
      documents: 10000
      positive_qrels: 986
      bm25_ndcg_at_10: 0.19329407857667313
      bm25_hit_at_10: 0.605
    - name: touche2020_v3
      path: docs/benchmark_tasks/NanoMTEB-v2/touche2020_v3.md
      retrieval_shape: controversial_question_to_argument_passage
      queries: 49
      documents: 10000
      positive_qrels: 1704
      bm25_ndcg_at_10: 0.8082621810352335
      bm25_hit_at_10: 0.9795918367346939
    - name: treccovid
      path: docs/benchmark_tasks/NanoMTEB-v2/treccovid.md
      retrieval_shape: covid_information_need_to_article_record
      queries: 50
      documents: 10000
      positive_qrels: 4584
      bm25_ndcg_at_10: 0.9038626806840664
      bm25_hit_at_10: 1.0
  source_links:
    - label: MTEB paper
      url: https://arxiv.org/abs/2210.07316
    - label: ArguAna paper
      url: https://aclanthology.org/P18-1023/
    - label: CLIMATE-FEVER paper
      url: https://arxiv.org/abs/2012.00614
    - label: CQADupStack paper
      url: https://eltimster.github.io/www/pubs/adcs2015.pdf
    - label: FEVER paper
      url: https://arxiv.org/abs/1803.05355
    - label: FiQA paper
      url: https://doi.org/10.1145/3184558.3192301
    - label: HotpotQA paper
      url: https://arxiv.org/abs/1809.09600
    - label: SCIDOCS/SPECTER paper
      url: https://arxiv.org/abs/2004.07180
    - label: Touché 2020 overview
      url: https://downloads.webis.de/touche/publications/papers/bondarenko_2020d.pdf
    - label: TREC-COVID paper
      url: https://arxiv.org/abs/2005.04474
    - label: NIST TREC-COVID
      url: https://ir.nist.gov/covidSubmit/index.html
```
