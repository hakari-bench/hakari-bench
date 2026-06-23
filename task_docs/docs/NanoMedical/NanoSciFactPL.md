# NanoMedical / NanoSciFactPL

## Overview

`NanoMedical / NanoSciFactPL` is the Polish BEIR-PL adaptation of SciFact. Queries are Polish translations of scientific claims, and documents are Polish translations of biomedical abstracts. The underlying task is the same as English SciFact: retrieve the abstract that contains evidence supporting or refuting a scientific claim. The additional challenge is language transfer into Polish, a morphologically rich language, with translated biomedical terminology, inflected forms, and occasional translation artifacts. This Nano split is useful for evaluating multilingual biomedical retrieval and the robustness of claim-evidence matching outside English.

## Details

### What the Original Data Measures

The original SciFact task measures scientific claim verification over biomedical abstracts. BEIR-PL translates BEIR-style retrieval datasets into Polish to create a zero-shot Polish IR benchmark. This task combines those two settings: it preserves SciFact's evidence relations while presenting the text in Polish.

A relevant document should contain evidence for or against the claim. It is not enough for the abstract to mention the same biomedical topic.

### Observed Data Profile

The Nano split contains 200 queries, 5,183 documents, and 226 positive qrel rows, matching the English SciFact qrel structure. Queries have 1.13 positives on average, with a median of 1 and a maximum of 5. There are 16 multi-positive queries, or 8.0% of the set. Polish queries average 95.52 characters, while documents average 1,554.52 characters.

The examples include claims about metastatic colorectal cancer, CRP and CABG mortality, p150 and EB1 interaction, obesity genetics, and febrile seizures. Documents are translated title-plus-abstract passages, with biomedical names and symbols often retained from English.

### BM25 Evaluation Profile

The BM25 candidate subset uses top-500 candidates and reaches nDCG@10 of 0.5750, hit@10 of 0.7250, and recall@100 of 0.8540. BM25 is substantially weaker than on the English SciFact split, which is consistent with Polish inflection and translation variation reducing exact lexical overlap.

Sparse retrieval can still exploit technical names, acronyms, and biomedical entities. Its failures often occur when relevant abstracts express the same relation with different Polish forms, translated phrasing, or technical wording.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses top-500 candidates and reaches nDCG@10 of 0.6061, hit@10 of 0.7600, and recall@100 of 0.8894. Dense retrieval improves over BM25 across all reported metrics, showing the value of semantic matching for translated Polish scientific claims.

The gain indicates that embeddings help bridge inflection and translation variation. The task remains challenging because the model must still identify exact evidence direction, condition, population, and outcome.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates, with 13 queries carrying a rank-101 safeguard positive. It reaches nDCG@10 of 0.6538, hit@10 of 0.8100, and recall@100 of 0.9292. This is the strongest profile across the candidate types.

Hybrid retrieval works well here because BM25 contributes exact biomedical names and dense retrieval contributes semantic matching across Polish variants. The combined pool is the best starting point for reranking and verification.

### Metric Interpretation for Model Researchers

Most queries have one positive, so nDCG@10 is a direct measure of whether the evidence abstract is ranked early. Recall@100 is important for downstream verification. Comparing this task with English SciFact helps separate language-transfer difficulty from scientific evidence difficulty.

The hybrid advantage suggests that Polish biomedical retrieval benefits from both exact term preservation and multilingual semantic representations.

### Query and Relevance Type Tendencies

Queries are Polish scientific claims, often translated from English and containing biomedical names, interventions, outcomes, or mechanisms. Relevant documents are Polish translated abstracts.

The relevance relation is evidence sufficiency for the claim, not general topic match.

### Representative Failure Modes

Common failures include Polish inflection reducing exact overlap, translation choices altering phrasing, retrieval of same-topic abstracts with different outcomes, and confusion over directionality or negation. Biomedical symbols and English-like names may help exact matching but can also dominate ranking when the evidence relation differs.

### Training Data That May Help

Useful training data includes non-overlapping Polish scientific claim-evidence pairs, Polish biomedical retrieval data, translated SciFact-style supervision outside the evaluation split, and multilingual biomedical retrieval with same-topic hard negatives. BEIR-PL SciFact test examples and translated duplicates of English SciFact evaluation claims or positives should be excluded.

### Model Improvement Notes

Models should handle Polish morphology while preserving biomedical names and evidence direction. Hard negatives should share the same disease, gene, intervention, or method while differing in population, organism, condition, or outcome. Cross-lingual training can help, but split hygiene matters because this task is translated from a known English benchmark.

## Example Data

| Query | Positive document |
| --- | --- |
| Rak jelita grubego z przerzutami leczony pojedynczym lekiem fluoropirymidynami skutkował zmniejszoną... [100 / 223 chars] | Opcje chemioterapii u starszych i słabych pacjentów z przerzutowym rakiem jelita grubego (MRC FOCUS2): otwarte, randomizowane badanie czynnikowe TŁO Pacjenci w podeszłym wieku i słabi z rakiem, chocia... [200 / 3,343 chars] |
| CRP nie pozwala przewidzieć śmiertelności pooperacyjnej po operacji pomostowania aortalno-wieńcowego... [100 / 108 chars] | Ocena opłacalności stosowania prognostycznych biomarkerów z modelami decyzyjnymi: studium przypadku w ustalaniu priorytetów pacjentów oczekujących na operację tętnicy wieńcowej CEL Określenie skuteczn... [200 / 3,169 chars] |
| Arginina 90 w p150n jest ważna dla interakcji z EB1. [52 chars] | Strukturalne podstawy do aktywacji składania mikrotubul przez kompleks EB1 i p150Glued. Białka śledzące plus, takie jak EB1 i kompleks dyneina/dynaktyna, regulują dynamikę mikrotubul. Uważa się, że bi... [200 / 1,210 chars] |
| O otyłości decydują wyłącznie czynniki środowiskowe. [52 chars] | Genetyka otyłości u dorosłych adopcyjnych i ich biologicznego rodzeństwa. Przeprowadzono badanie adopcyjne wpływu genetycznego na otyłość w wieku dorosłym, w którym osoby adoptowane oddzielone od swoi... [200 / 1,465 chars] |
| Napady gorączkowe zwiększają próg rozwoju padaczki. [51 chars] | Napady gorączkowe w rozwijającym się mózgu powodują uporczywą modyfikację pobudliwości neuronalnej w obwodach limbicznych Napady gorączkowe (wywołane gorączką) dotykają 3–5% niemowląt i małych dzieci.... [200 / 812 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| BEIR-PL: Zero Shot Information Retrieval Benchmark for the Polish Language | 2024 | arXiv paper | [https://arxiv.org/abs/2305.19840](https://arxiv.org/abs/2305.19840) |
| BEIR-PL: Zero Shot Information Retrieval Benchmark for the Polish Language | 2024 | ACL Anthology paper | [https://aclanthology.org/2024.lrec-main.194/](https://aclanthology.org/2024.lrec-main.194/) |
| Fact or Fiction: Verifying Scientific Claims | 2020 | arXiv paper | [https://arxiv.org/abs/2004.14974](https://arxiv.org/abs/2004.14974) |
| Fact or Fiction: Verifying Scientific Claims | 2020 | ACL Anthology paper | [https://aclanthology.org/2020.emnlp-main.609/](https://aclanthology.org/2020.emnlp-main.609/) |
| clarin-knext |  | Hugging Face publisher | [https://huggingface.co/clarin-knext](https://huggingface.co/clarin-knext) |

### Representative Snippets

| Query | Relevant document excerpt |
| --- | --- |
| Rak jelita grubego z przerzutami leczony pojedynczym lekiem fluoropirymidynami skutkował zmniejszoną skutecznością i niższą jakością życia w porównaniu z chemioterapią opartą na oksaliplatynie u pacjentów w podeszłym wieku. | A Polish translated abstract about chemotherapy options for elderly and frail patients with metastatic colorectal cancer. |
| CRP nie pozwala przewidzieć śmiertelności pooperacyjnej po operacji pomostowania aortalno-wieńcowego (CABG). | A Polish translated abstract about prognostic biomarkers and prioritizing patients waiting for coronary artery surgery. |
| Arginina 90 w p150n jest ważna dla interakcji z EB1. | A translated abstract about EB1, p150Glued, and activation of microtubule assembly. |
| O otyłości decydują wyłącznie czynniki środowiskowe. | A translated abstract about genetic effects on obesity in adoptees and their biological siblings. |
| Napady gorączkowe zwiększają próg rozwoju padaczki. | A translated abstract about febrile seizures and persistent neuronal excitability changes in limbic circuits. |
