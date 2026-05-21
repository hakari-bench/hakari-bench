# NanoMuPLeR / el

## Overview

`NanoMuPLeR / el` is the Greek split of MuPLeR-retrieval, a multilingual legal
retrieval task built from European Union legal passages. Queries are synthetic
Greek legal questions, and documents are Greek passages aligned with the same
underlying DGT-Acquis material. The model must retrieve the single passage that
answers or grounds the question.

## Details

### What the Original Data Measures

The [MuPLeR-retrieval dataset card](https://huggingface.co/datasets/mteb/MuPLeR-retrieval)
describes the task as multilingual parallel legal retrieval with 10,000
human-translated DGT-Acquis passages and 200 synthetic parallel queries per
language. [An overview of the European Union's highly multilingual parallel corpora](https://link.springer.com/article/10.1007/s10579-014-9277-0)
documents the EU parallel-corpus family and notes that DGT-Acquis is among the
resources for which the article serves as a reference publication.

### Observed Data Profile

The split contains 200 Greek queries, 10,000 Greek documents, and 200 positive
qrels. Every query has one positive. Queries average 141.28 characters, and
documents average 744.82 characters. The sampled records are formal EU-law
questions about intra-EU import charges, state aid, procurement criteria,
Euratom research priorities, and pre-accession production rules.

### BM25 Difficulty

BM25 is strong on this split: nDCG@10 = 0.7749 and hit@10 = 0.8600, with 138
positives at rank 1 and 172 in the top 10. The synthetic legal questions often
reuse named institutions, numeric thresholds, dates, and legal concepts from the
positive passage, making exact lexical matching a high baseline.

### Training Data That May Help

Useful data includes non-overlapping EU legal retrieval pairs, DGT-Acquis or
EUR-Lex passages in Greek, multilingual legal QA, and hard negatives from nearby
EU acts. Avoid using the MuPLeR evaluation queries or their exact aligned
positive passages in training.

### Synthetic Data Guidance

Generate Greek questions from non-evaluation EU legal passages, preserving
article references, percentages, institutions, dates, and legal conditions.
Synthetic negatives should be legally adjacent but fail to answer the specific
condition in the query.

## Example Data

| Query | Positive document |
| --- | --- |
| Ποια διάταξη της Ένωσης απαιτεί τη συνεκτίμηση απασχόλησης, κοινωνικής προστασίας, καταπολέμησης αποκλεισμού και εκπαίδευσης, κατάρτισης και προστασίας υγείας; (159 chars) | Τούτο συμβαίνει, παραδείγματος χάρη, στην περίπτωση της κοινωνικής πολιτικής, με την ενσωμάτωση μιας γενικής διάταξης (η οποία καλείται κοινωνική ρήτρα) σύμφωνα με την οποία η Ένωση οφείλει, κατά τον καθορισμό και την εφαρμογ ... [truncated 225 chars](810 chars) |
| Ποια εταιρεία προμηθεύει 25% της ηπειρωτικής ζήτησης κινητήρων οικιακών συσκευών και στοχεύει 10% μερίδιο μηχανισμών καθίσματος έως 2006; (137 chars) | Βάσει των σημερινών πληροφοριών, η Επιτροπή αμφιβάλλει επίσης για το κατά πόσον δεν θα υπάρξουν στρεβλώσεις στον ανταγωνισμό και για το κατά πόσον η ενίσχυση περιορίζεται στο ελάχιστο αναγκαίο. Π.χ., οι κοινοποιηθείσες πληροφ ... [truncated 225 chars](629 chars) |
| Ποιο όργανο πρότεινε να αναπτυχθεί πλαίσιο εσωτερικού κοινοτικού ελέγχου για τον αποτελεσματικό έλεγχο του κοινοτικού προϋπολογισμού; (133 chars) | Στη γνωμοδότησή του αριθ. 2/2004 το Συνέδριο τονίζει την ανάγκη για αποδοτικό και αποτελεσματικό έλεγχο επί του κοινοτικού προϋπολογισμού σε όλα τα επίπεδα διοίκησης. Κρίνει ότι υπάρχει περιθώριο βελτίωσης του σχεδιασμού των ... [truncated 225 chars](768 chars) |
| Ποιος Ευρωπαίος επόπτης προστασίας δεδομένων προτίμησε ευέλικτη αναλογική αποθήκευση αντί ετήσιου ορίου για είσπραξη αξιώσεων διατροφής; (136 chars) | Για τους λόγους αυτούς, ο ΕΕΠΔ προτιμά ευέλικτη αλλά αναλογική περίοδο αποθήκευσης μάλλον παρά αυστηρό a priori περιορισμό της περιόδου αποθήκευσης σε ένα έτος [όπως προτείνεται σήμερα βάσει του άρθρου 46 παράγραφος 3)], η οπ ... [truncated 225 chars](607 chars) |
| Ποια συμβουλευτική επιτροπή επικρότησε κατάργηση μέτρων του 7ου προγράμματος-πλαισίου και αύξηση συγχρηματοδότησης πιλοτικών για άνθρακα και χάλυβα; (148 chars) | Η ΕΟΚΕ επικροτεί το γεγονός ότι η πρόταση απόφασης απλουστεύει τις διοικητικές διαδικασίες, καταργώντας, μεταξύ άλλων, ορισμένα συνοδευτικά μέτρα, δεδομένου ότι ήδη καλύπτονται από το 7ο πρόγραμμα-πλαίσιο έρευνας, αυξάνει τη ... [truncated 225 chars](665 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMuPLeR |
| Backing dataset | NanoMuPLeR |
| Task / split | el |
| Hugging Face dataset | [hakari-bench/NanoMuPLeR](https://huggingface.co/datasets/hakari-bench/NanoMuPLeR) |
| Source dataset | [mteb/MuPLeR-retrieval](https://huggingface.co/datasets/mteb/MuPLeR-retrieval) |
| Language | el |
| Category | natural_language |
| Queries | 200 |
| Documents | 10,000 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.7749 |
| BM25 hit@10 | 0.8600 |
| Query length avg chars | 141.28 |
| Document length avg chars | 744.82 |

### Public Sources

- [mteb/MuPLeR-retrieval](https://huggingface.co/datasets/mteb/MuPLeR-retrieval), source dataset card.
- [An overview of the European Union's highly multilingual parallel corpora](https://link.springer.com/article/10.1007/s10579-014-9277-0), DGT-Acquis source reference paper.
- [DGT-Acquis](https://joint-research-centre.ec.europa.eu/language-technology-resources/dgt-acquis_en), European Commission source-corpus page.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMuPLeR](https://huggingface.co/datasets/hakari-bench/NanoMuPLeR)
- Source task dataset: [mteb/MuPLeR-retrieval](https://huggingface.co/datasets/mteb/MuPLeR-retrieval)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| MuPLeR: Multilingual Parallel Legal Retrieval |  | dataset card | https://huggingface.co/datasets/mteb/MuPLeR-retrieval |
| An overview of the European Union's highly multilingual parallel corpora | 2014 | source paper | https://link.springer.com/article/10.1007/s10579-014-9277-0 |
| DGT-Acquis |  | source corpus | https://joint-research-centre.ec.europa.eu/language-technology-resources/dgt-acquis_en |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMuPLeR
  backing_dataset: NanoMuPLeR
  dataset_id: hakari-bench/NanoMuPLeR
  task_name: el
  split_name: el
  language: el
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMuPLeR/el.md
  source_research:
    primary_source_type: dataset_card
    paper_pdf_or_html_checked: true
    no_paper_note: no standalone MuPLeR technical paper was confirmed
  counts:
    queries: 200
    documents: 10000
    positive_qrels: 200
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 141.28
    document_mean: 744.82
  bm25:
    ndcg_at_10: 0.7749
    hit_at_10: 0.86
    source: dataset_bm25_column
  example_count: 5
```
