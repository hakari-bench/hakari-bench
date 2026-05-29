# NanoLaw

## Overview

NanoLaw is a compact legal retrieval benchmark group spanning English, German,
and Chinese legal data. It includes Indian precedent and statute retrieval,
German legal passage and QA retrieval, Chinese criminal-case retrieval,
LegalBench-derived consumer-contract and corporate-lobbying retrieval, and
plain-English contract-summary retrieval.

The group is useful because it does not test only one legal search pattern.
Several tasks require mapping facts to applicable law or analogous cases, while
others require matching policy descriptions, consumer questions, or simplified
contract summaries to exact clauses and summaries. A model can be topically
close and still be wrong if it misses jurisdiction, statutory role, contract
obligation, procedural posture, or legal analogy.

## Details

### What the Original Group Measures

NanoLaw draws from several legal NLP resources rather than from one benchmark
paper. The AILA tasks measure retrieval for legal assistance in Indian law:
finding relevant precedent cases and statutory provisions for long factual
scenarios. GerDaLIR and LegalQuAD cover German legal information access, with
passage-to-judgment and question-to-judgment retrieval over long legal
documents. LeCaRDv2 evaluates Chinese legal case retrieval where relevance
depends on legal characterization, penalty, procedure, and factual similarity.

The remaining English splits turn legal reasoning or summarization resources
into retrieval tasks. LegalBench contributes consumer-contract QA and corporate
lobbying tasks, where the retriever must find contract clauses or bill summaries
that support a legal judgment. LegalSummarization reverses contract
simplification into summary-to-clause retrieval. At group level, NanoLaw
therefore measures legal semantic matching across jurisdiction, language,
document length, and reasoning style.

### Subtask Coverage

The eight subtasks cover five legal retrieval families:

- **Factual scenario to law:** `NanoAILACasedocs` retrieves Indian precedent
  judgments, while `NanoAILAStatutes` retrieves applicable statutory provisions
  for the same long fact patterns.
- **Long legal document retrieval:** `NanoGerDaLIRSmall`, `NanoLeCaRDv2`, and
  `NanoLegalQuAD` retrieve full or near-full legal decisions from German or
  Chinese legal text.
- **Contract and terms-of-service retrieval:**
  `NanoLegalBenchConsumerContractsQA` and `NanoLegalSummarization` retrieve
  clauses or snippets that answer consumer-contract questions or match
  plain-English summaries.
- **Legislative and policy retrieval:** `NanoLegalBenchCorporateLobbying`
  retrieves bill titles and summaries from short policy descriptions.
- **Multilingual legal search:** English, German, and Chinese subtasks are all
  present, and they differ sharply in tokenization, citation style, and document
  structure.

Three splits are heavily multi-positive: AILA statutes, AILA case documents,
and LeCaRDv2. Four splits are exactly single-positive, and LegalSummarization is
moderately multi-positive. This mixture matters for training and evaluation
because some tasks reward finding one exact clause, while others reward ranking
several legally related authorities.

### Observed Group Profile

Across the eight splits, NanoLaw contains 1,259 queries, 5,488 positive qrels,
and 15,142 split-local candidate documents. The document count is a sum across
subtasks, not a deduplicated cross-task corpus size. The group average is 4.36
positives per query, driven mainly by `NanoLeCaRDv2`, where every query has many
positive related cases.

The observed text profile is unusually broad. The AILA queries are long English
case narratives averaging 3,038.42 characters. `NanoLeCaRDv2` queries are even
longer Chinese criminal judgments or fact sections averaging 4,259.44
characters. In contrast, `NanoLegalQuAD` uses short German legal questions
averaging 71.94 characters, and LegalBench contract questions average 97.22
characters. Documents range from short contract snippets and bill summaries to
German judgments averaging more than 19K characters and AILA case documents
averaging nearly 27K characters.

### BM25 Difficulty

The query-weighted BM25 baseline is relatively strong overall, with nDCG@10 =
0.6275 and hit@10 = 0.8133, but the spread by task is large. BM25 is strongest
on `NanoLegalBenchCorporateLobbying` with nDCG@10 = 0.8757, where bill phrasing
and policy terms often overlap directly between query and document. It is
weakest on `NanoAILAStatutes` with nDCG@10 = 0.1900, where long factual
scenarios imply statutory provisions without necessarily repeating statute
titles or exact statutory language.

The group should not be treated as solved by lexical overlap. BM25 performs well
when legal formulas, charge names, bill titles, or clause keywords are shared,
as in corporate lobbying, LegalQuAD, LegalBench consumer contracts, and many
LeCaRDv2 examples. It struggles more when legal relevance is analogical or
normative: facts must be mapped to statutes, a precedent must be legally
analogous rather than merely topically similar, or a plain-English summary must
be matched to paraphrased contract language.

### Training Data That May Help

Useful training data should preserve the jurisdiction and retrieval shape of
each subtask. For the AILA tasks, useful sources include non-overlapping Indian
legal precedent retrieval, fact-to-statute retrieval, citation prediction, and
hard negatives from cases or statutes with shared legal vocabulary but different
governing issues. For German tasks, useful data includes passage-to-case
retrieval, German legal QA, long German court decisions, and hard negatives that
share statutes or court domains. For LeCaRDv2, useful supervision includes
Chinese legal case retrieval, criminal-charge classification with fact
sections, and related-case pairs separated by characterization, penalty, and
procedure.

For the contract and policy splits, useful data includes consumer-contract QA,
contract clause retrieval, terms-of-service entailment, bill-title to
bill-summary retrieval, and legislative search. Training should exclude NanoLaw
evaluation queries, qrels, and positive documents. When using public source
datasets, upstream evaluation splits should be audited carefully because several
NanoLaw tasks are direct Nano samples of known benchmark resources.

### Synthetic Data Guidance

Synthetic data for NanoLaw should remain legally grounded. Scenario-to-case or
scenario-to-statute data should use full factual narratives with procedural
posture, legal issues, and jurisdiction-specific terminology. Positives should
be legally applicable or analogous authorities, while hard negatives should
share charges, statutes, agencies, or contract topics but fail the decisive
legal condition.

For German and Chinese legal tasks, generated examples should preserve the
language, citation style, and long-document structure of the source data. For
consumer-contract and summary retrieval, synthetic queries should paraphrase
rights, obligations, exceptions, and permissions rather than only copying clause
keywords. Synthetic data should not use NanoLaw evaluation documents as seeds.

## Task Summary

| Task | Retrieval shape | Lang | Queries | Docs | Positive qrels | BM25 nDCG@10 | BM25 hit@10 | Query avg chars | Doc avg chars | Source status |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| [NanoAILACasedocs](NanoAILACasedocs.md) | long legal scenario to precedent case | en | 50 | 186 | 195 | 0.2921 | 0.6000 | 3,038.42 | 26,947.34 | AILA paper + MTEB card |
| [NanoAILAStatutes](NanoAILAStatutes.md) | long legal scenario to statute provision | en | 50 | 82 | 217 | 0.1900 | 0.6600 | 3,038.42 | 1,972.63 | AILA paper + MTEB card |
| [NanoGerDaLIRSmall](NanoGerDaLIRSmall.md) | German legal passage to judgment | de | 200 | 9,969 | 235 | 0.5848 | 0.7200 | 889.88 | 19,706.82 | GerDaLIR paper |
| [NanoLeCaRDv2](NanoLeCaRDv2.md) | Chinese criminal case to related cases | zh | 159 | 3,795 | 3,896 | 0.6379 | 0.9371 | 4,259.44 | 7,231.82 | LeCaRDv2 paper |
| [NanoLegalBenchConsumerContractsQA](NanoLegalBenchConsumerContractsQA.md) | contract question to clause | en | 200 | 153 | 200 | 0.6453 | 0.8400 | 97.22 | 2,743.33 | LegalBench + source article |
| [NanoLegalBenchCorporateLobbying](NanoLegalBenchCorporateLobbying.md) | bill description to bill summary | en | 200 | 319 | 200 | 0.8757 | 0.9700 | 179.67 | 1,157.21 | LegalBench |
| [NanoLegalQuAD](NanoLegalQuAD.md) | German legal question to judgment | de | 200 | 200 | 200 | 0.6765 | 0.7950 | 71.94 | 19,481.02 | paper DOI + MTEB card |
| [NanoLegalSummarization](NanoLegalSummarization.md) | plain-English summary to contract snippet | en | 200 | 438 | 345 | 0.5400 | 0.7350 | 103.06 | 606.16 | contract summarization paper |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoLaw |
| Backing dataset | NanoLaw |
| Hugging Face dataset | [hakari-bench/NanoLaw](https://huggingface.co/datasets/hakari-bench/NanoLaw) |
| Languages | en, de, zh |
| Category | natural_language |
| Subtasks | 8 |
| Total queries | 1,259 |
| Split-local documents | 15,142 |
| Positive qrels | 5,488 |
| Positives per query | 4.36 average |
| Multi-positive queries | 334 |
| Query-weighted BM25 nDCG@10 | 0.6661 |
| Query-weighted BM25 hit@10 | 0.8523 |
| Query-weighted BM25 Recall@100 | 0.9135 |
| Query-weighted Dense nDCG@10 | 0.6064 |
| Query-weighted Dense hit@10 | 0.7792 |
| Query-weighted Dense Recall@100 | 0.8830 |
| Query-weighted Reranking hybrid nDCG@10 | 0.6646 |
| Query-weighted Reranking hybrid hit@10 | 0.8435 |
| Query-weighted Reranking hybrid Recall@100 | 0.9430 |
| Mean query length | 992.41 chars, weighted by query count |
| Mean document length | 15,455.46 chars, weighted by split-local document count |

### Public Sources

- [Overview of the FIRE 2019 AILA Track: Artificial Intelligence for Legal Assistance](https://ceur-ws.org/Vol-2517/T1-1.pdf); 2019; Paheli Bhattacharya et al.
- [Plain English Summarization of Contracts](https://aclanthology.org/W19-2201/); 2019; Laura Manor and Junyi Jessy Li.
- [GerDaLIR: A German Dataset for Legal Information Retrieval](https://aclanthology.org/2021.nllp-1.13/); 2021; Marco Wrzalik and Dirk Krechel.
- [LeCaRDv2: A Large-Scale Chinese Legal Case Retrieval Dataset](https://arxiv.org/abs/2310.17609); 2023; Haitao Li et al.
- [LegalBench: A Collaboratively Built Benchmark for Measuring Legal Reasoning in Large Language Models](https://arxiv.org/abs/2308.11462); 2023; Neel Guha et al.
- [Towards Intelligent Legal Advisors for Document Retrieval and Question-Answering in German Legal Documents](https://doi.org/10.1109/AIKE52691.2021.00011); 2021; Christoph Hoppe et al.
- [Predicting Consumer Contracts](https://doi.org/10.15779/Z382B8VC90); 2021; Noam Kolt.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoLaw](https://huggingface.co/datasets/hakari-bench/NanoLaw)
- Source datasets:
  [mteb/AILA_casedocs](https://huggingface.co/datasets/mteb/AILA_casedocs),
  [mteb/AILA_statutes](https://huggingface.co/datasets/mteb/AILA_statutes),
  [mteb/GerDaLIRSmall](https://huggingface.co/datasets/mteb/GerDaLIRSmall),
  [mteb/LeCaRDv2](https://huggingface.co/datasets/mteb/LeCaRDv2),
  [mteb/LegalBenchConsumerContractsQA](https://huggingface.co/datasets/mteb/LegalBenchConsumerContractsQA),
  [mteb/LegalBenchCorporateLobbying](https://huggingface.co/datasets/mteb/LegalBenchCorporateLobbying),
  [mteb/LegalQuAD](https://huggingface.co/datasets/mteb/LegalQuAD),
  [mteb/legal_summarization](https://huggingface.co/datasets/mteb/legal_summarization).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Overview of the FIRE 2019 AILA Track: Artificial Intelligence for Legal Assistance | 2019 | benchmark paper | https://ceur-ws.org/Vol-2517/T1-1.pdf |
| Plain English Summarization of Contracts | 2019 | source task paper | https://aclanthology.org/W19-2201/ |
| GerDaLIR: A German Dataset for Legal Information Retrieval | 2021 | source task paper | https://aclanthology.org/2021.nllp-1.13/ |
| LeCaRDv2: A Large-Scale Chinese Legal Case Retrieval Dataset | 2023 | source task paper | https://arxiv.org/abs/2310.17609 |
| LegalBench: A Collaboratively Built Benchmark for Measuring Legal Reasoning in Large Language Models | 2023 | benchmark paper | https://arxiv.org/abs/2308.11462 |
| Towards Intelligent Legal Advisors for Document Retrieval and Question-Answering in German Legal Documents | 2021 | source task paper | https://doi.org/10.1109/AIKE52691.2021.00011 |
| Predicting Consumer Contracts | 2021 | source article | https://doi.org/10.15779/Z382B8VC90 |

## Machine-Readable Metadata

<!-- benchmark-task-group-metadata:v1 -->

```yaml
benchmark_task_group_metadata:
  schema_version: 1
  document_status: reviewed_manual
  nano_set: NanoLaw
  backing_dataset: NanoLaw
  dataset_id: hakari-bench/NanoLaw
  language: multilingual
  languages:
  - en
  - de
  - zh
  category: natural_language
  document_path: docs/benchmark_tasks/NanoLaw/index.md
  source_research:
    primary_source_type: multiple_task_papers_and_dataset_cards
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    tasks: 8
    queries: 1259
    split_local_documents: 15142
    positive_qrels: 5488
  positives_per_query:
    average: 4.359015091342335
    min: 1
    median_task_median: 1.0
    max: 30
    multi_positive_tasks: 4
    multi_positive_queries: 334
  text_stats_chars:
    query_mean_weighted_by_queries: 992.4130262112787
    document_mean_weighted_by_documents: 15455.464469686964
  bm25:
    ndcg_at_10_query_weighted: 0.6660581196
    hit_at_10_query_weighted: 0.8522637014
    ndcg_at_10_unweighted_task_mean: 0.5552953413500401
    hit_at_10_unweighted_task_mean: 0.7821383647798742
    source: dataset_candidate_subset
    easiest_task_by_ndcg_at_10: NanoLegalBenchCorporateLobbying
    hardest_task_by_ndcg_at_10: NanoAILAStatutes
  tasks:
  - name: NanoAILACasedocs
    path: docs/benchmark_tasks/NanoLaw/NanoAILACasedocs.md
    retrieval_shape: long_legal_scenario_to_precedent_case
    language: en
    queries: 50
    documents: 186
    positive_qrels: 195
    bm25_ndcg_at_10: 0.29210253925435126
    bm25_hit_at_10: 0.6
  - name: NanoAILAStatutes
    path: docs/benchmark_tasks/NanoLaw/NanoAILAStatutes.md
    retrieval_shape: long_legal_scenario_to_statute_provision
    language: en
    queries: 50
    documents: 82
    positive_qrels: 217
    bm25_ndcg_at_10: 0.19002066324353106
    bm25_hit_at_10: 0.66
  - name: NanoGerDaLIRSmall
    path: docs/benchmark_tasks/NanoLaw/NanoGerDaLIRSmall.md
    retrieval_shape: german_legal_passage_to_judgment
    language: de
    queries: 200
    documents: 9969
    positive_qrels: 235
    bm25_ndcg_at_10: 0.5847975886774149
    bm25_hit_at_10: 0.72
  - name: NanoLeCaRDv2
    path: docs/benchmark_tasks/NanoLaw/NanoLeCaRDv2.md
    retrieval_shape: chinese_criminal_case_to_related_cases
    language: zh
    queries: 159
    documents: 3795
    positive_qrels: 3896
    bm25_ndcg_at_10: 0.6379051373412444
    bm25_hit_at_10: 0.9371069182389937
  - name: NanoLegalBenchConsumerContractsQA
    path: docs/benchmark_tasks/NanoLaw/NanoLegalBenchConsumerContractsQA.md
    retrieval_shape: contract_question_to_clause
    language: en
    queries: 200
    documents: 153
    positive_qrels: 200
    bm25_ndcg_at_10: 0.6453269540326203
    bm25_hit_at_10: 0.84
  - name: NanoLegalBenchCorporateLobbying
    path: docs/benchmark_tasks/NanoLaw/NanoLegalBenchCorporateLobbying.md
    retrieval_shape: bill_description_to_bill_summary
    language: en
    queries: 200
    documents: 319
    positive_qrels: 200
    bm25_ndcg_at_10: 0.8756703056285763
    bm25_hit_at_10: 0.97
  - name: NanoLegalQuAD
    path: docs/benchmark_tasks/NanoLaw/NanoLegalQuAD.md
    retrieval_shape: german_legal_question_to_judgment
    language: de
    queries: 200
    documents: 200
    positive_qrels: 200
    bm25_ndcg_at_10: 0.6765084712604355
    bm25_hit_at_10: 0.795
  - name: NanoLegalSummarization
    path: docs/benchmark_tasks/NanoLaw/NanoLegalSummarization.md
    retrieval_shape: plain_english_summary_to_contract_snippet
    language: en
    queries: 200
    documents: 438
    positive_qrels: 345
    bm25_ndcg_at_10: 0.5400310713621468
    bm25_hit_at_10: 0.735
  learning:
    leakage_note: exclude NanoLaw evaluation queries, qrels, and positive documents;
      audit upstream legal benchmark splits before using public source data for training
    useful_training_data:
    - Indian legal precedent retrieval and fact-to-statute retrieval
    - German legal passage retrieval and legal QA over long judgments
    - Chinese legal case retrieval and criminal-charge similarity data
    - consumer-contract QA and terms-of-service clause retrieval
    - legislative bill title and bill summary retrieval
    - hard negatives sharing legal vocabulary but differing in governing issue
    synthetic_data:
      document_generation: jurisdiction-specific cases, statutes, judgments, contract
        clauses, and bill summaries with realistic legal terminology and structure
      question_generation: factual legal scenarios, legal questions, contract questions,
        plain-English clause summaries, and policy descriptions grounded in the generated
        or selected document
      answerability: positives must be legally applicable, analogous, or evidential
        rather than merely sharing legal keywords
    multi_positive_training: preserve_multi_authority_tasks_for_aila_and_lecardv2
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoLaw
    source_urls:
    - label: AILA 2019 paper
      url: https://ceur-ws.org/Vol-2517/T1-1.pdf
    - label: Plain English Summarization of Contracts
      url: https://aclanthology.org/W19-2201/
    - label: GerDaLIR paper
      url: https://aclanthology.org/2021.nllp-1.13/
    - label: LeCaRDv2 arXiv
      url: https://arxiv.org/abs/2310.17609
    - label: LegalBench arXiv
      url: https://arxiv.org/abs/2308.11462
    - label: LegalQuAD paper DOI
      url: https://doi.org/10.1109/AIKE52691.2021.00011
    - label: Predicting Consumer Contracts DOI
      url: https://doi.org/10.15779/Z382B8VC90
    - label: mteb/AILA_casedocs
      url: https://huggingface.co/datasets/mteb/AILA_casedocs
    - label: mteb/AILA_statutes
      url: https://huggingface.co/datasets/mteb/AILA_statutes
    - label: mteb/GerDaLIRSmall
      url: https://huggingface.co/datasets/mteb/GerDaLIRSmall
    - label: mteb/LeCaRDv2
      url: https://huggingface.co/datasets/mteb/LeCaRDv2
    - label: mteb/LegalQuAD
      url: https://huggingface.co/datasets/mteb/LegalQuAD
    - label: mteb/legal_summarization
      url: https://huggingface.co/datasets/mteb/legal_summarization
    source_notes: []
  references:
  - title: 'Overview of the FIRE 2019 AILA Track: Artificial Intelligence for Legal
      Assistance'
    url: https://ceur-ws.org/Vol-2517/T1-1.pdf
    year: 2019
    is_paper: true
    source_confidence: definitive_paper_link
  - title: Plain English Summarization of Contracts
    url: https://aclanthology.org/W19-2201/
    year: 2019
    is_paper: true
    source_confidence: definitive_paper_link
  - title: 'GerDaLIR: A German Dataset for Legal Information Retrieval'
    url: https://aclanthology.org/2021.nllp-1.13/
    year: 2021
    is_paper: true
    source_confidence: definitive_paper_link
  - title: 'LeCaRDv2: A Large-Scale Chinese Legal Case Retrieval Dataset'
    url: https://arxiv.org/abs/2310.17609
    year: 2023
    is_paper: true
    source_confidence: definitive_paper_link
  - title: 'LegalBench: A Collaboratively Built Benchmark for Measuring Legal Reasoning
      in Large Language Models'
    url: https://arxiv.org/abs/2308.11462
    year: 2023
    is_paper: true
    source_confidence: definitive_paper_link
  - title: Towards Intelligent Legal Advisors for Document Retrieval and Question-Answering
      in German Legal Documents
    url: https://doi.org/10.1109/AIKE52691.2021.00011
    year: 2021
    is_paper: true
    source_confidence: definitive_paper_link
  - title: Predicting Consumer Contracts
    url: https://doi.org/10.15779/Z382B8VC90
    year: 2021
    is_paper: true
    source_confidence: definitive_paper_link
  candidate_subsets:
    bm25:
      query_weighted_ndcg_at_10: 0.6660581196
      query_weighted_hit_at_10: 0.8522637014
      query_weighted_recall_at_100: 0.9135046045
      source: dataset_candidate_subset
    dense:
      query_weighted_ndcg_at_10: 0.6064118823
      query_weighted_hit_at_10: 0.7791898332
      query_weighted_recall_at_100: 0.8829563681
      source: dataset_candidate_subset
    reranking_hybrid:
      query_weighted_ndcg_at_10: 0.6646410752
      query_weighted_hit_at_10: 0.8435266084
      query_weighted_recall_at_100: 0.9429821189
      source: dataset_candidate_subset
```
