# NanoMedical

## Overview

NanoMedical is a multilingual medical, biomedical, and public-health retrieval
group. It covers Chinese medical consultation answer selection,
clinician-facing clinical passage retrieval, consumer medical FAQ retrieval,
nutrition and health literature search, public-health FAQ retrieval in Arabic,
scientific claim evidence retrieval, and COVID-19 literature retrieval in
English and Polish. The group is useful because it treats medical retrieval as
several different evidence-matching problems rather than one domain.

The group contains 1,586 queries, 66,052 task-local documents, and 10,438
positive qrel rows. It should be read as a retrieval benchmark, not as a
clinical decision tool. Some tasks retrieve scientific abstracts, some retrieve
public guidance, and some retrieve online consultation answers. Those settings
have different risks, document styles, and training requirements.

## What This Group Measures

NanoMedical measures whether retrieval systems can connect medical questions,
claims, and information needs to the right evidence surface. `NanoCUREv1`
retrieves biomedical passages for clinician-oriented questions. `NanoNFCorpus`
maps short lay health topics to scientific articles. `NanoSciFact` and
`NanoSciFactPL` retrieve abstracts that support or refute biomedical claims.
`NanoTRECCOVID` and `NanoTRECCOVIDPL` retrieve COVID-19 literature records.
`NanoMedicalQA` and `NanoPublicHealthQA` retrieve trusted-source answers, while
`NanoCmedqa` and `NanoCMedQAv2reranking` retrieve Chinese consultation answers.

The group also measures multilingual robustness. English, Chinese, Arabic, and
Polish are all present, and the translated Polish scientific tasks behave
differently from their English counterparts. A model that handles English
medical abstracts well may still fail on Chinese patient-style questions or
Arabic public-health FAQ wording.

## Task Families

- **Clinical passage retrieval:** `NanoCUREv1` retrieves biomedical passages for
  clinician-oriented questions.
- **Consumer medical QA and FAQ retrieval:** `NanoMedicalQA` and
  `NanoPublicHealthQA` retrieve guidance or public-health answers.
- **Chinese consultation answer retrieval:** `NanoCmedqa` and
  `NanoCMedQAv2reranking` retrieve answer candidates for patient-style Chinese
  questions.
- **Medical and nutrition literature retrieval:** `NanoNFCorpus` retrieves
  biomedical literature for lay health topics.
- **Scientific claim evidence retrieval:** `NanoSciFact` and `NanoSciFactPL`
  retrieve biomedical abstracts for claims.
- **COVID-19 literature retrieval:** `NanoTRECCOVID` and `NanoTRECCOVIDPL`
  retrieve pandemic literature records.

## Dataset Shape

The group has ten task pages. Positive density varies widely. `NanoCUREv1`
averages 25.91 positives per query and `NanoNFCorpus` averages 18.59, so those
tasks evaluate many-relevant-document ranking. `NanoMedicalQA`,
`NanoPublicHealthQA`, and both TREC-COVID Nano splits are single-positive in the
metadata. The Chinese consultation tasks and SciFact variants sit between those
extremes.

Document types are also different. Chinese consultation answers are short.
Public-health and MedicalQA answers are medium-length guidance passages.
NFCorpus, SciFact, and TREC-COVID use scientific or biomedical article records.
CURE uses clinical passages with many positives per query. The group therefore
tests answer selection, evidence retrieval, and literature search at the same
time.

## Retrieval Behavior

### BM25 Profile

BM25 is the best nDCG@10 profile only for `NanoTRECCOVID`, where exact COVID-19
terminology, intervention terms, and biomedical phrases provide useful sparse
anchors. It is also strong on `NanoSciFact`, `NanoSciFactPL`, and
`NanoPublicHealthQA`, where disease names, claim terms, and public-health
phrasing often overlap with the target document.

BM25 is much weaker on Chinese consultation answer selection and broad health
literature retrieval. `NanoCmedqa` and `NanoCMedQAv2reranking` require matching
patient symptoms to useful advice, not only shared Chinese terms. `NanoNFCorpus`
uses short lay topics against technical literature, so many documents share
medical terms but differ in actual relevance. The group-level BM25 nDCG@10 is
0.4288.

### Dense Profile

Dense retrieval with `harrier-oss-270m` is best for four tasks:
`NanoCMedQAv2reranking`, `NanoCmedqa`, `NanoMedicalQA`, and
`NanoPublicHealthQA`. These tasks rely on answerability and semantic matching
between a question and an answer passage or consultation reply. The gains on
Chinese medical QA are especially clear: both Chinese tasks roughly double
nDCG@10 compared with BM25.

Dense has the highest group-level nDCG@10 at 0.5138. It also improves MedicalQA
and PublicHealthQA, suggesting that semantic answer retrieval is important for
patient- and public-facing medical questions. Dense is not always best for
scientific literature and claim evidence, where exact biomedical terms and
hybrid candidate coverage remain important.

### Reranking Hybrid Profile

The reranking hybrid profile is best for `NanoCUREv1`, `NanoNFCorpus`,
`NanoSciFact`, `NanoSciFactPL`, and `NanoTRECCOVIDPL`. These are mostly
scientific or literature-style tasks where exact biomedical terms and semantic
relatedness both matter. Hybrid also has the best query-weighted recall@100 at
0.7507, which is important for tasks with many positives per query.

Hybrid is not the best profile for Chinese consultation QA or public-health FAQ
retrieval, where dense semantic matching leads top-10 ranking. It is also below
BM25 on English `NanoTRECCOVID`. The practical reading is that hybrid is strong
for biomedical candidate generation and claim/literature retrieval, while dense
retrieval is more important for question-to-answer medical matching.

## Task Summary

| Task | Family | Language | Queries | Docs | Positives | Positives/query | BM25 nDCG@10 | Dense nDCG@10 | Reranking hybrid nDCG@10 | Best profile |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| [NanoCMedQAv2reranking](NanoCMedQAv2reranking.md) | Chinese medical answer retrieval | `zh` | 200 | 10,000 | 377 | 1.89 | 0.1527 | 0.3209 | 0.2529 | Dense |
| [NanoCUREv1](NanoCUREv1.md) | Clinical passage retrieval | `en` | 200 | 10,000 | 5,181 | 25.91 | 0.4693 | 0.5003 | 0.5262 | Reranking hybrid |
| [NanoCmedqa](NanoCmedqa.md) | Chinese consultation answer retrieval | `zh` | 200 | 10,000 | 324 | 1.62 | 0.1669 | 0.3380 | 0.2591 | Dense |
| [NanoMedicalQA](NanoMedicalQA.md) | Medical FAQ retrieval | `en` | 200 | 2,007 | 200 | 1.00 | 0.5439 | 0.7308 | 0.6510 | Dense |
| [NanoNFCorpus](NanoNFCorpus.md) | Biomedical literature retrieval | `en` | 200 | 3,593 | 3,718 | 18.59 | 0.2921 | 0.3070 | 0.3182 | Reranking hybrid |
| [NanoPublicHealthQA](NanoPublicHealthQA.md) | Public-health FAQ retrieval | `ar` | 86 | 86 | 86 | 1.00 | 0.7379 | 0.8176 | 0.7847 | Dense |
| [NanoSciFact](NanoSciFact.md) | Scientific claim evidence retrieval | `en` | 200 | 5,183 | 226 | 1.13 | 0.7017 | 0.7334 | 0.7506 | Reranking hybrid |
| [NanoSciFactPL](NanoSciFactPL.md) | Scientific claim evidence retrieval | `pl` | 200 | 5,183 | 226 | 1.13 | 0.5750 | 0.6061 | 0.6538 | Reranking hybrid |
| [NanoTRECCOVID](NanoTRECCOVID.md) | COVID-19 literature retrieval | `en` | 50 | 10,000 | 50 | 1.00 | 0.3983 | 0.3875 | 0.3193 | BM25 |
| [NanoTRECCOVIDPL](NanoTRECCOVIDPL.md) | COVID-19 literature retrieval | `pl` | 50 | 10,000 | 50 | 1.00 | 0.3266 | 0.3585 | 0.3864 | Reranking hybrid |

## Interpretation Notes for Model Researchers

NanoMedical should be interpreted by retrieval surface. Dense-led gains on
Chinese consultation, MedicalQA, and Arabic PublicHealthQA indicate better
question-to-answer matching. Hybrid-led gains on CURE, NFCorpus, SciFact, and
Polish TREC-COVID indicate better combination of biomedical term matching and
semantic evidence retrieval. BM25 remains a meaningful baseline where exact
biomedical terminology is central, but it does not explain most of the group.

The high positive density of CURE and NFCorpus also changes what "good" means.
For those tasks, retrieving one relevant passage is not enough; ranking many
relevant biomedical documents early matters. Medical model comparisons should
therefore inspect per-task nDCG@10 and recall@100 instead of relying only on the
aggregate group score.

## Training and Leakage Notes

Useful training data includes clinical question-passage pairs, PubMed and PMC
retrieval, CORD-19 judgments, NFCorpus-style health-topic supervision,
SciFact-style claim-evidence pairs, trusted medical FAQ data, Arabic
public-health QA, Chinese medical consultation QA, and Polish biomedical
retrieval pairs. Multi-positive tasks should preserve all relevant passages or
abstracts when possible.

Leakage control should exclude Nano evaluation queries, qrels, positive
documents, answer strings, consultation replies, source FAQ pages, and
translated variants. Medical datasets often contain repeated guidance templates
or translated near-duplicates, so overlap checks should include semantic and
document-level duplication, not just exact query text.

## Public Sources

- [CURE: A Dataset for Clinical Understanding & Retrieval Evaluation](https://doi.org/10.1145/3711896.3737435), 2025.
- [A Full-Text Learning to Rank Dataset for Medical Information Retrieval](http://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf), 2016.
- [Searching for Scientific Evidence in a Pandemic: An Overview of TREC-COVID](https://arxiv.org/abs/2104.09632), 2021.
- [BEIR-PL: Zero Shot Information Retrieval Benchmark for the Polish Language](https://aclanthology.org/2024.lrec-main.194/), 2024.
- [Fact or Fiction: Verifying Scientific Claims](https://aclanthology.org/2020.emnlp-main.609/), 2020.
- [A Question-Entailment Approach to Question Answering](https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-019-3119-4), 2019.
- [publichealth-qa](https://huggingface.co/datasets/xhluca/publichealth-qa), 2024.
- [DuReader_retrieval](https://aclanthology.org/2022.emnlp-main.357/), 2022.
- [Multi-Scale Attentive Interaction Networks for Chinese Medical Question Answer Selection](https://doi.org/10.1109/ACCESS.2018.2883637), 2018.

### Source Reference Table

| Source | Year | Type | URL |
| --- | ---: | --- | --- |
| CURE: A Dataset for Clinical Understanding & Retrieval Evaluation | 2025 | benchmark paper | https://doi.org/10.1145/3711896.3737435 |
| A Full-Text Learning to Rank Dataset for Medical Information Retrieval | 2016 | source task paper | http://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf |
| Searching for Scientific Evidence in a Pandemic: An Overview of TREC-COVID | 2021 | source task paper | https://arxiv.org/abs/2104.09632 |
| BEIR-PL: Zero Shot Information Retrieval Benchmark for the Polish Language | 2024 | benchmark paper | https://aclanthology.org/2024.lrec-main.194/ |
| Fact or Fiction: Verifying Scientific Claims | 2020 | source task paper | https://aclanthology.org/2020.emnlp-main.609/ |
| A Question-Entailment Approach to Question Answering | 2019 | source task paper | https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-019-3119-4 |
| publichealth-qa | 2024 | dataset card | https://huggingface.co/datasets/xhluca/publichealth-qa |
| DuReader_retrieval | 2022 | source task paper | https://aclanthology.org/2022.emnlp-main.357/ |
| Multi-Scale Attentive Interaction Networks for Chinese Medical Question Answer Selection | 2018 | source task paper | https://doi.org/10.1109/ACCESS.2018.2883637 |
