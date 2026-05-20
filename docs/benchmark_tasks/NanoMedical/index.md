# NanoMedical

> [!NOTE]
> This page was prepared by manual review of source papers, dataset cards,
> repository metadata, and sampled benchmark data. It may contain mistakes;
> please treat it as a reference aid rather than a definitive source.

## Overview

NanoMedical is a multilingual medical, biomedical, and public-health retrieval
group. It covers Chinese medical consultation answer selection, clinician-facing
clinical passage retrieval, consumer medical FAQ retrieval, nutrition and health
literature search, public-health FAQ retrieval in Arabic, scientific claim
evidence retrieval, and COVID-19 literature retrieval in English and Polish.
The group is useful because it combines several distinct medical retrieval
surfaces rather than treating "medical retrieval" as one task type.

NanoMedical should be read as a benchmark for retrieval and evidence matching,
not as a clinical decision tool. Some tasks retrieve scientific abstracts, some
retrieve public-facing advice, and some retrieve online-consultation answers;
their risks and training requirements differ.

## Details

### What the Original Group Measures

NanoMedical is assembled from several established medical or scientific
retrieval resources. CURE measures point-of-care clinical retrieval with
expert-written questions and biomedical article passages. NFCorpus measures the
gap between lay health or nutrition topics and technical biomedical literature.
TREC-COVID measures pandemic scientific literature retrieval over CORD-19, while
SciFact measures retrieval of biomedical abstracts that support or refute
scientific claims. BEIR-PL contributes Polish translations of SciFact and
TREC-COVID, adding multilingual and translation robustness requirements.

The group also includes medical QA and answer-selection settings. MedicalQA is
based on trusted-source medical question answering in the question-entailment
tradition. PublicHealthQA retrieves official-style public-health answers in
Arabic from CDC/WHO-derived FAQ material. `NanoCmedqa` and
`NanoCMedQAv2reranking` evaluate Chinese online medical consultation answer
retrieval, where short patient questions must be matched to medically useful
answer replies.

### Subtask Coverage

The ten subtasks cover six retrieval families:

- **Clinical passage retrieval:** `NanoCUREv1` retrieves biomedical passages for
  clinician-oriented questions across multiple medical specialties.
- **Consumer medical QA and FAQ retrieval:** `NanoMedicalQA` retrieves
  answer-bearing medical guidance passages, and `NanoPublicHealthQA` retrieves
  Arabic public-health FAQ answers.
- **Chinese consultation answer retrieval:** `NanoCmedqa` and
  `NanoCMedQAv2reranking` retrieve short Chinese medical-advice answers for
  patient-style questions.
- **Medical and nutrition literature retrieval:** `NanoNFCorpus` maps very short
  layperson health topics to scientific medical articles.
- **Scientific claim evidence retrieval:** `NanoSciFact` and `NanoSciFactPL`
  retrieve abstracts that support or refute biomedical claims in English and
  Polish.
- **COVID-19 literature retrieval:** `NanoTRECCOVID` and `NanoTRECCOVIDPL`
  retrieve COVID-19 or coronavirus scientific literature in English and Polish.

The group is multilingual: English, Chinese, Arabic, and Polish are all present.
It also mixes single-positive and heavily multi-positive tasks. `NanoCUREv1` and
`NanoNFCorpus` have many positives per query, while MedicalQA, PublicHealthQA,
and both TREC-COVID variants are single-positive in the Nano splits.

### Observed Group Profile

Across the ten splits, NanoMedical contains 1,586 queries, 10,438 positive
qrels, and 66,052 split-local candidate documents. The document count is a sum
across subtasks, not a deduplicated group-wide corpus size. The group average is
6.58 positives per query, but this is dominated by `NanoCUREv1` and
`NanoNFCorpus`; most other tasks have one or two positives per query.

Queries are usually short. The query-weighted mean length is 63.55 characters.
`NanoNFCorpus` has the shortest queries, averaging only 17.15 characters, and
often uses terse health topics or acronyms. Chinese medical QA queries average
about 50 characters, while SciFact claims and PublicHealthQA questions are still
compact. Documents are longer and more varied: short Chinese consultation
answers average near 100 to 158 characters, while scientific abstracts and
COVID-19 records average around 1,200 to 1,590 characters.

### BM25 Difficulty

The query-weighted BM25 baseline reaches nDCG@10 = 0.3670 and hit@10 = 0.5731.
The easiest split for BM25 is `NanoPublicHealthQA` with nDCG@10 = 0.6722 and
hit@10 = 0.8372, helped by close question-answer wording and distinctive Arabic
public-health terms. The hardest split is `NanoTRECCOVIDPL` with nDCG@10 =
0.1098 and hit@10 = 0.1600, where translated Polish biomedical text, COVID-19
terminology, and broad pandemic information needs reduce lexical matching.

The task-level spread is important. BM25 performs relatively well on SciFact and
MedicalQA because disease names, gene symbols, and answer-type cues often appear
in both query and document. It is weaker on Chinese medical answer selection,
NFCorpus, and TREC-COVID-style literature search, where many documents share the
same symptoms, disease names, or pandemic terms but differ in the specific
answer or evidence relation. CURE also shows a multi-positive effect: BM25 often
finds at least one relevant passage, but many relevant passages remain far down
the candidate list.

### Training Data That May Help

Useful training data should be separated by task family. For clinical and
biomedical passage retrieval, CURE-style clinical questions, PubMed or PMC
passage retrieval, CORD-19 judgments, NFCorpus-style health-topic supervision,
and SciFact-style claim-evidence pairs are directly relevant. For medical QA,
use trusted-source FAQ pairs, MedQuAD-style answer passages, public-health FAQ
data, and answer-type supervision that distinguishes symptoms, diagnosis,
prevention, treatment, and definition.

For multilingual and Chinese medical tasks, useful data includes
non-overlapping Chinese medical consultation QA, answer-selection data with hard
negative replies, Polish biomedical retrieval, translated SciFact/TREC-COVID
style supervision, and Arabic public-health QA. Training should exclude
NanoMedical evaluation queries, qrels, positive documents, and near-duplicate
source pages. Public medical datasets often contain repeated FAQ templates or
translated variants, so overlap audits should check more than exact query text.

### Synthetic Data Guidance

Synthetic data for NanoMedical should preserve both medical grounding and the
retrieval shape. For FAQ and guidance tasks, generate questions whose answer
requires the selected passage and whose negatives share the disease name but
answer a different type of question. For scientific claim and literature tasks,
generate claims, questions, and abstracts where the relevance depends on
directionality, experimental context, population, intervention, or evidence
role, not only on shared biomedical entities.

For Chinese consultation data, synthetic questions should keep patient-style
symptom descriptions and answer replies should be concise but medically
specific. For Polish and Arabic data, synthetic examples should preserve the
target language and domain terminology rather than translating only the
keywords. Evaluation queries and positive documents from NanoMedical should not
be used as seeds.

## Task Summary

| Task | Retrieval shape | Lang | Queries | Docs | Positive qrels | BM25 nDCG@10 | BM25 hit@10 | Query avg chars | Doc avg chars | Source status |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| [NanoCMedQAv2reranking](NanoCMedQAv2reranking.md) | Chinese medical question to answer candidate | zh | 200 | 10,000 | 377 | 0.1500 | 0.2750 | 50.10 | 100.90 | CMedQAv2 paper + repository |
| [NanoCUREv1](NanoCUREv1.md) | clinical question to biomedical passage | en | 200 | 10,000 | 5,181 | 0.3699 | 0.8050 | 75.89 | 604.21 | CURE paper + dataset card |
| [NanoCmedqa](NanoCmedqa.md) | Chinese consultation question to answer | zh | 200 | 10,000 | 324 | 0.1668 | 0.2750 | 52.00 | 157.57 | DuReader + CMedQAv2 sources |
| [NanoMedicalQA](NanoMedicalQA.md) | medical FAQ question to answer passage | en | 200 | 2,007 | 200 | 0.4736 | 0.7000 | 54.23 | 1,102.43 | medical QA paper |
| [NanoNFCorpus](NanoNFCorpus.md) | health topic to biomedical article | en | 200 | 3,593 | 3,718 | 0.2434 | 0.5650 | 17.15 | 1,589.52 | NFCorpus paper + official page |
| [NanoPublicHealthQA](NanoPublicHealthQA.md) | Arabic public-health question to FAQ answer | ar | 86 | 86 | 86 | 0.6722 | 0.8372 | 79.85 | 828.15 | dataset card |
| [NanoSciFact](NanoSciFact.md) | scientific claim to evidence abstract | en | 200 | 5,183 | 226 | 0.6289 | 0.7850 | 90.06 | 1,499.41 | SciFact paper |
| [NanoSciFactPL](NanoSciFactPL.md) | Polish claim to translated evidence abstract | pl | 200 | 5,183 | 226 | 0.5121 | 0.6600 | 95.52 | 1,554.52 | BEIR-PL + SciFact papers |
| [NanoTRECCOVID](NanoTRECCOVID.md) | COVID-19 question to scientific article | en | 50 | 10,000 | 50 | 0.1966 | 0.3200 | 69.24 | 1,208.78 | TREC-COVID paper |
| [NanoTRECCOVIDPL](NanoTRECCOVIDPL.md) | Polish COVID-19 question to article | pl | 50 | 10,000 | 50 | 0.1098 | 0.1600 | 69.42 | 1,251.91 | BEIR-PL + TREC-COVID papers |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMedical |
| Backing dataset | NanoMedical |
| Hugging Face dataset | [hakari-bench/NanoMedical](https://huggingface.co/datasets/hakari-bench/NanoMedical) |
| Languages | en, zh, ar, pl |
| Category | natural_language |
| Subtasks | 10 |
| Total queries | 1,586 |
| Split-local documents | 66,052 |
| Positive qrels | 10,438 |
| Positives per query | 6.58 average |
| Multi-positive queries | 521 |
| Query-weighted BM25 nDCG@10 | 0.3670 |
| Query-weighted BM25 hit@10 | 0.5731 |
| Mean query length | 63.55 chars, weighted by query count |
| Mean document length | 863.82 chars, weighted by split-local document count |

### Public Sources

- [CURE: A Dataset for Clinical Understanding & Retrieval Evaluation](https://doi.org/10.1145/3711896.3737435); 2025; Nadia Athar Sheikh et al.
- [A Full-Text Learning to Rank Dataset for Medical Information Retrieval](http://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf); 2016; Vera Boteva et al.
- [Searching for Scientific Evidence in a Pandemic: An Overview of TREC-COVID](https://arxiv.org/abs/2104.09632); 2021; Kirk Roberts et al.
- [BEIR-PL: Zero Shot Information Retrieval Benchmark for the Polish Language](https://aclanthology.org/2024.lrec-main.194/); 2024; Konrad Wojtasik et al.
- [Fact or Fiction: Verifying Scientific Claims](https://aclanthology.org/2020.emnlp-main.609/); 2020; David Wadden et al.
- [A Question-Entailment Approach to Question Answering](https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-019-3119-4); 2019; Asma Ben Abacha and Dina Demner-Fushman.
- [publichealth-qa](https://huggingface.co/datasets/xhluca/publichealth-qa); 2024; Xing Han Lu.
- [DuReader_retrieval: A Large-scale Chinese Benchmark for Passage Retrieval from Web Search Engine](https://aclanthology.org/2022.emnlp-main.357/); 2022; Yifu Qiu et al.
- [Multi-Scale Attentive Interaction Networks for Chinese Medical Question Answer Selection](https://doi.org/10.1109/ACCESS.2018.2883637); 2018; Sheng Zhang et al.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMedical](https://huggingface.co/datasets/hakari-bench/NanoMedical)
- Source datasets:
  [clinia/CUREv1](https://huggingface.co/datasets/clinia/CUREv1),
  [mteb/nfcorpus](https://huggingface.co/datasets/mteb/nfcorpus),
  [xhluca/publichealth-qa](https://huggingface.co/datasets/xhluca/publichealth-qa),
  [clarin-knext/scifact-pl](https://huggingface.co/datasets/clarin-knext/scifact-pl),
  [clarin-knext/trec-covid-pl](https://huggingface.co/datasets/clarin-knext/trec-covid-pl).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| CURE: A Dataset for Clinical Understanding & Retrieval Evaluation | 2025 | benchmark paper | https://doi.org/10.1145/3711896.3737435 |
| A Full-Text Learning to Rank Dataset for Medical Information Retrieval | 2016 | source task paper | http://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf |
| Searching for Scientific Evidence in a Pandemic: An Overview of TREC-COVID | 2021 | source task paper | https://arxiv.org/abs/2104.09632 |
| BEIR-PL: Zero Shot Information Retrieval Benchmark for the Polish Language | 2024 | benchmark paper | https://aclanthology.org/2024.lrec-main.194/ |
| Fact or Fiction: Verifying Scientific Claims | 2020 | source task paper | https://aclanthology.org/2020.emnlp-main.609/ |
| A Question-Entailment Approach to Question Answering | 2019 | source task paper | https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-019-3119-4 |
| publichealth-qa | 2024 | dataset card | https://huggingface.co/datasets/xhluca/publichealth-qa |
| DuReader_retrieval: A Large-scale Chinese Benchmark for Passage Retrieval from Web Search Engine | 2022 | source task paper | https://aclanthology.org/2022.emnlp-main.357/ |
| Multi-Scale Attentive Interaction Networks for Chinese Medical Question Answer Selection | 2018 | source task paper | https://doi.org/10.1109/ACCESS.2018.2883637 |

## Machine-Readable Metadata

<!-- benchmark-task-group-metadata:v1 -->

```yaml
benchmark_task_group_metadata:
  schema_version: 1
  document_status: reviewed_manual
  nano_set: NanoMedical
  backing_dataset: NanoMedical
  dataset_id: hakari-bench/NanoMedical
  language: multilingual
  languages:
    - en
    - zh
    - ar
    - pl
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMedical/index.md
  source_research:
    primary_source_type: multiple_task_papers_and_dataset_cards
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    tasks: 10
    queries: 1586
    split_local_documents: 66052
    positive_qrels: 10438
  positives_per_query:
    average: 6.581336696090794
    min: 1
    median_task_median: 1.0
    max: 100
    multi_positive_tasks: 6
    multi_positive_queries: 521
  text_stats_chars:
    query_mean_weighted_by_queries: 63.55044135056746
    document_mean_weighted_by_documents: 863.8210349510234
  bm25:
    ndcg_at_10_query_weighted: 0.3669964444663304
    hit_at_10_query_weighted: 0.5731399747779319
    ndcg_at_10_unweighted_task_mean: 0.35232356405
    hit_at_10_unweighted_task_mean: 0.53822093023
    source: dataset_bm25_column
    easiest_task_by_ndcg_at_10: NanoPublicHealthQA
    hardest_task_by_ndcg_at_10: NanoTRECCOVIDPL
  tasks:
    - name: NanoCMedQAv2reranking
      path: docs/benchmark_tasks/NanoMedical/NanoCMedQAv2reranking.md
      retrieval_shape: chinese_medical_question_to_answer_candidate
      language: zh
      queries: 200
      documents: 10000
      positive_qrels: 377
      bm25_ndcg_at_10: 0.1500390078
      bm25_hit_at_10: 0.275
    - name: NanoCUREv1
      path: docs/benchmark_tasks/NanoMedical/NanoCUREv1.md
      retrieval_shape: clinical_question_to_biomedical_passage
      language: en
      queries: 200
      documents: 10000
      positive_qrels: 5181
      bm25_ndcg_at_10: 0.3698959662
      bm25_hit_at_10: 0.805
    - name: NanoCmedqa
      path: docs/benchmark_tasks/NanoMedical/NanoCmedqa.md
      retrieval_shape: chinese_consultation_question_to_answer
      language: zh
      queries: 200
      documents: 10000
      positive_qrels: 324
      bm25_ndcg_at_10: 0.1667886836
      bm25_hit_at_10: 0.275
    - name: NanoMedicalQA
      path: docs/benchmark_tasks/NanoMedical/NanoMedicalQA.md
      retrieval_shape: medical_faq_question_to_answer_passage
      language: en
      queries: 200
      documents: 2007
      positive_qrels: 200
      bm25_ndcg_at_10: 0.4735533647
      bm25_hit_at_10: 0.7
    - name: NanoNFCorpus
      path: docs/benchmark_tasks/NanoMedical/NanoNFCorpus.md
      retrieval_shape: health_topic_to_biomedical_article
      language: en
      queries: 200
      documents: 3593
      positive_qrels: 3718
      bm25_ndcg_at_10: 0.2434183752
      bm25_hit_at_10: 0.565
    - name: NanoPublicHealthQA
      path: docs/benchmark_tasks/NanoMedical/NanoPublicHealthQA.md
      retrieval_shape: arabic_public_health_question_to_faq_answer
      language: ar
      queries: 86
      documents: 86
      positive_qrels: 86
      bm25_ndcg_at_10: 0.6722409776
      bm25_hit_at_10: 0.8372093023
    - name: NanoSciFact
      path: docs/benchmark_tasks/NanoMedical/NanoSciFact.md
      retrieval_shape: scientific_claim_to_evidence_abstract
      language: en
      queries: 200
      documents: 5183
      positive_qrels: 226
      bm25_ndcg_at_10: 0.6288504435
      bm25_hit_at_10: 0.785
    - name: NanoSciFactPL
      path: docs/benchmark_tasks/NanoMedical/NanoSciFactPL.md
      retrieval_shape: polish_claim_to_translated_evidence_abstract
      language: pl
      queries: 200
      documents: 5183
      positive_qrels: 226
      bm25_ndcg_at_10: 0.5120801837
      bm25_hit_at_10: 0.66
    - name: NanoTRECCOVID
      path: docs/benchmark_tasks/NanoMedical/NanoTRECCOVID.md
      retrieval_shape: covid19_question_to_scientific_article
      language: en
      queries: 50
      documents: 10000
      positive_qrels: 50
      bm25_ndcg_at_10: 0.1966089962
      bm25_hit_at_10: 0.32
    - name: NanoTRECCOVIDPL
      path: docs/benchmark_tasks/NanoMedical/NanoTRECCOVIDPL.md
      retrieval_shape: polish_covid19_question_to_article
      language: pl
      queries: 50
      documents: 10000
      positive_qrels: 50
      bm25_ndcg_at_10: 0.109759642
      bm25_hit_at_10: 0.16
  learning:
    leakage_note: exclude NanoMedical evaluation queries, qrels, positive documents, translated variants, same FAQ pages, and near-duplicate biomedical abstracts when training
    useful_training_data:
      - clinical question to biomedical passage retrieval
      - medical FAQ and trusted-source answer passage retrieval
      - Chinese medical consultation QA and answer selection
      - NFCorpus-style health topic to biomedical literature retrieval
      - SciFact-style claim to evidence abstract retrieval
      - CORD-19 and COVID-19 ad hoc retrieval with hard negatives
      - Polish biomedical retrieval and Arabic public-health QA
    synthetic_data:
      document_generation: medical FAQ answers, consultation replies, biomedical abstracts, public-health guidance, and COVID-19 evidence passages in the target language
      question_generation: consumer medical questions, clinical questions, health topics, scientific claims, public-health FAQ questions, and Chinese consultation questions grounded in the generated or selected document
      answerability: positives should answer the exact medical, public-health, or evidence relation rather than only sharing the disease or biomedical term
    multi_positive_training: preserve_multi_positive_cure_nfcorpus_and_evidence_tasks
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMedical
    source_urls:
      - label: CURE KDD DOI
        url: https://doi.org/10.1145/3711896.3737435
      - label: NFCorpus ECIR paper
        url: http://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf
      - label: TREC-COVID arXiv
        url: https://arxiv.org/abs/2104.09632
      - label: BEIR-PL ACL Anthology
        url: https://aclanthology.org/2024.lrec-main.194/
      - label: SciFact ACL Anthology
        url: https://aclanthology.org/2020.emnlp-main.609/
      - label: BMC Bioinformatics medical QA article
        url: https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-019-3119-4
      - label: publichealth-qa
        url: https://huggingface.co/datasets/xhluca/publichealth-qa
      - label: DuReader-Retrieval ACL Anthology
        url: https://aclanthology.org/2022.emnlp-main.357/
      - label: CMedQAv2 paper DOI
        url: https://doi.org/10.1109/ACCESS.2018.2883637
    source_notes: []
  references:
    - title: "CURE: A Dataset for Clinical Understanding & Retrieval Evaluation"
      url: https://doi.org/10.1145/3711896.3737435
      year: 2025
      is_paper: true
      source_confidence: definitive_paper_link
    - title: A Full-Text Learning to Rank Dataset for Medical Information Retrieval
      url: http://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf
      year: 2016
      is_paper: true
      source_confidence: definitive_paper_link
    - title: "Searching for Scientific Evidence in a Pandemic: An Overview of TREC-COVID"
      url: https://arxiv.org/abs/2104.09632
      year: 2021
      is_paper: true
      source_confidence: definitive_paper_link
    - title: "BEIR-PL: Zero Shot Information Retrieval Benchmark for the Polish Language"
      url: https://aclanthology.org/2024.lrec-main.194/
      year: 2024
      is_paper: true
      source_confidence: definitive_paper_link
    - title: "Fact or Fiction: Verifying Scientific Claims"
      url: https://aclanthology.org/2020.emnlp-main.609/
      year: 2020
      is_paper: true
      source_confidence: definitive_paper_link
    - title: A Question-Entailment Approach to Question Answering
      url: https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-019-3119-4
      year: 2019
      is_paper: true
      source_confidence: definitive_paper_link
    - title: publichealth-qa
      url: https://huggingface.co/datasets/xhluca/publichealth-qa
      year: 2024
      is_paper: false
      source_confidence: probably_correct
    - title: "DuReader_retrieval: A Large-scale Chinese Benchmark for Passage Retrieval from Web Search Engine"
      url: https://aclanthology.org/2022.emnlp-main.357/
      year: 2022
      is_paper: true
      source_confidence: definitive_paper_link
    - title: Multi-Scale Attentive Interaction Networks for Chinese Medical Question Answer Selection
      url: https://doi.org/10.1109/ACCESS.2018.2883637
      year: 2018
      is_paper: true
      source_confidence: definitive_paper_link
```
