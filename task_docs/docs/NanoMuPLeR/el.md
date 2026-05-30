# NanoMuPLeR / el

## Overview

`NanoMuPLeR / el` is the Greek split of MuPLeR-retrieval, a multilingual legal retrieval benchmark built from European Union legal passages. Queries are synthetic Greek legal questions, and documents are Greek passages aligned with DGT-Acquis material. Each query has one relevant passage. The task is useful for evaluating same-language Greek legal retrieval where formal EU terminology, institutional names, numeric thresholds, article references, and legal conditions must be matched precisely. It also supports comparison with other MuPLeR language splits because the underlying legal material and query design are parallel across languages.

## Details

### What the Original Data Measures

MuPLeR-retrieval measures multilingual parallel legal retrieval over DGT-Acquis passages. The source dataset card describes 10,000 human-translated EU legal passages and 200 synthetic parallel queries per language. The DGT-Acquis source belongs to the European Union's multilingual legal corpus resources.

For this Greek split, both query and document text are Greek. The retrieval target is the passage that grounds the legal condition, institution, threshold, date, or procedural rule asked about in the query.

### Observed Data Profile

The Nano split contains 200 queries, 10,000 documents, and 200 positive qrel rows. Each query has exactly one positive. Queries average 141.28 characters, while documents average 744.82 characters.

The examples include questions about social clauses, state aid, EU budget control, data retention for maintenance claims, and research-program funding measures. Documents are formal legal or administrative passages with dense institutional wording.

### BM25 Evaluation Profile

The BM25 candidate subset uses top-500 candidates and reaches nDCG@10 of 0.7749, hit@10 of 0.8600, and recall@100 of 0.9500. BM25 is strong because synthetic legal questions often preserve exact legal terms, institutions, dates, percentages, and named bodies from the positive passage.

Its weaknesses are legal paraphrase and condition matching. A wrong passage can share the same institution or policy area but not answer the exact legal condition in the query.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses top-500 candidates and reaches nDCG@10 of 0.7834, hit@10 of 0.8650, and recall@100 of 0.9450. Dense retrieval is slightly stronger than BM25 in top-rank quality, while BM25 is slightly stronger in recall@100.

This indicates that Greek semantic matching adds value over exact term matching, but sparse legal anchors remain important. The task rewards models that can preserve formal Greek legal meaning while still recognizing exact references.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates, with one query carrying a rank-101 safeguard positive. It reaches nDCG@10 of 0.8390, hit@10 of 0.9150, and recall@100 of 0.9950. This is the strongest profile across the candidate types.

Hybrid retrieval is therefore the best candidate-generation strategy for this split. It combines BM25's exact legal terminology with dense retrieval's ability to match paraphrased legal conditions.

### Metric Interpretation for Model Researchers

This is a single-positive task, so nDCG@10 and hit@10 directly reflect whether the exact grounding passage is ranked early. Recall@100 measures whether the correct legal passage is available to a reranker.

The strong hybrid result suggests that Greek legal retrieval should be evaluated with both sparse and dense signals, especially when queries contain exact legal anchors but also synthetic paraphrase.

### Query and Relevance Type Tendencies

Queries are formal Greek legal questions. Relevant documents are Greek EU legal passages. The questions often ask which institution, provision, committee, period, or rule satisfies a specific condition.

The relevance relation is exact legal grounding. A passage about the same EU topic is not enough unless it answers the specific condition.

### Representative Failure Modes

Common failures include retrieving a nearby EU provision, matching an institution name without the required action, confusing similar policy programs, and over-weighting repeated legal formulae. Dense systems may blur legal distinctions; sparse systems may miss paraphrased conditions.

### Training Data That May Help

Useful training data includes non-overlapping Greek EU legal retrieval pairs, DGT-Acquis or EUR-Lex passages, multilingual legal QA, and hard negatives from adjacent EU acts. MuPLeR evaluation queries and exact positive passages should be excluded.

### Model Improvement Notes

Models should preserve Greek morphology, legal terminology, article references, and institutional names. Hard negatives should share the same legal domain but fail the query's exact condition. Hybrid retrieval and reranking are especially appropriate because the task benefits from both exact and semantic signals.

## Example Data

### Public Sources

- [mteb/MuPLeR-retrieval](https://huggingface.co/datasets/mteb/MuPLeR-retrieval), source dataset card.
- [An overview of the European Union's highly multilingual parallel corpora](https://link.springer.com/article/10.1007/s10579-014-9277-0), DGT-Acquis source reference.
- [DGT-Acquis](https://joint-research-centre.ec.europa.eu/language-technology-resources/dgt-acquis_en), European Commission source-corpus page.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| MuPLeR: Multilingual Parallel Legal Retrieval |  | dataset card | https://huggingface.co/datasets/mteb/MuPLeR-retrieval |
| An overview of the European Union's highly multilingual parallel corpora | 2014 | source paper | https://link.springer.com/article/10.1007/s10579-014-9277-0 |
| DGT-Acquis |  | source corpus | https://joint-research-centre.ec.europa.eu/language-technology-resources/dgt-acquis_en |

### Representative Snippets

| Query | Relevant document excerpt |
| --- | --- |
| Ποια διάταξη της Ένωσης απαιτεί τη συνεκτίμηση απασχόλησης, κοινωνικής προστασίας, καταπολέμησης αποκλεισμού και εκπαίδευσης, κατάρτισης και προστασίας υγείας; | A Greek EU-law passage describing a social-clause provision requiring the Union to take social requirements into account in policy definition and implementation. |
| Ποια εταιρεία προμηθεύει 25% της ηπειρωτικής ζήτησης κινητήρων οικιακών συσκευών και στοχεύει 10% μερίδιο μηχανισμών καθίσματος έως 2006; | A Greek state-aid passage discussing Commission doubts about market distortions and minimum necessary aid. |
| Ποιο όργανο πρότεινε να αναπτυχθεί πλαίσιο εσωτερικού κοινοτικού ελέγχου για τον αποτελεσματικό έλεγχο του κοινοτικού προϋπολογισμού; | A Greek passage about the Court's opinion on effective control of the Community budget. |
| Ποιος Ευρωπαίος επόπτης προστασίας δεδομένων προτίμησε ευέλικτη αναλογική αποθήκευση αντί ετήσιου ορίου για είσπραξη αξιώσεων διατροφής; | A Greek passage about the EDPS preferring a flexible but proportional retention period. |
| Ποια συμβουλευτική επιτροπή επικρότησε κατάργηση μέτρων του 7ου προγράμματος-πλαισίου και αύξηση συγχρηματοδότησης πιλοτικών για άνθρακα και χάλυβα; | A Greek passage about the EESC welcoming simplified administrative procedures and increased co-financing. |
