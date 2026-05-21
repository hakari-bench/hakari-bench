# NanoMMTEB-v2 / twitter_hjerne

## Overview

`twitter_hjerne` is a Danish social-media answer retrieval task. Queries are
#Twitterhjerne help-seeking tweets, and documents are human reply tweets. The
retriever must find useful replies, often among several valid answers.

## Details

### What the Original Data Measures

The [sorenmulli/da-hashtag-twitterhjerne](https://huggingface.co/datasets/sorenmulli/da-hashtag-twitterhjerne)
dataset card describes Danish questions asked on Twitter/X with the
`#Twitterhjerne` hashtag and their answers. The [Scandinavian Embedding Benchmarks](https://arxiv.org/abs/2406.02396)
paper includes this as a Danish retrieval task where social-media questions are
matched to relevant replies.

### Observed Data Profile

The split has 77 queries, 262 documents, and 262 positive qrels. Queries average
165.75 characters and documents average 128.77 characters. The task is strongly
multi-positive: positives average 3.40 per query, with up to six valid replies.
Text is informal Danish with URLs, hashtags, emojis, recommendations, and
troubleshooting advice.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.2395
and hit@10 = 0.6104. Lexical overlap helps for product names and places, but
useful replies often introduce new terms rather than repeating the question.

### Training Data That May Help

Useful data includes Danish forum QA, social-media question-reply pairs,
community-support threads, and multi-positive answer retrieval. Training should
retain multiple valid replies instead of forcing one canonical answer.

### Synthetic Data Guidance

Generate informal Danish questions asking for recommendations, troubleshooting,
shopping advice, travel tips, or household help. Generate several plausible
reply tweets per question. Negatives should be plausible replies to adjacent
topics but not useful for the specific query.

## Example Data

| Query | Positive document |
| --- | --- |
| Hej #Twitterhjerne & twitterfolkens (- eller X'ere, whatever 😊) Er der nogen der kan fortælle mig hvor jeg kan købe IKKE-danske kartofler? Hverken Rema1000, Netto, Kvickly ell SuperBrugsen sælger andet end danske. (Jeg ønsker ... [truncated 225 chars](278 chars) | Økologiske er vel ok? (21 chars) |
| Hvis I betaler for medieovervågning på arbejdet - hvem bruger I så, og er I tilfredse? #dkmedier #dkbiz #twitterhjerne (118 chars) | Infomedia - og mnjah (20 chars) |
| Er der andre der døjer med samme problem som mig, min controller til ps5 lader maks 1 streg om natten. Hver gang jeg sidder og spiller disconneter den hele tiden, jeg har ikke gjort noget ved den. Den havde det allerede 1 uge ... [truncated 225 chars](250 chars) | Du skal bare indlevere den, hvor du har købt, så får du en ny (61 chars) |
| Hej Twitter Ofte når jeg ser madvideoer på engelsk så bruger de noget de kalder heavy cream. Svarer det til vores piskefløde? #twitterhjerne #madtwitter (152 chars) | Er heavy cream ikke mere 48-50% fløde (37 chars) |
| Teknisk sommerspørgsmål: Hvordan deler i fotos med familien? Krav: ikke Google Photo eller iCloud. Meget gerne løsning, der er let at bruge for alle familiemedlemmer. Har kigget på Jottacloud og overvejet Nextcloud (opsætning ... [truncated 225 chars](259 chars) | OneDrive. Vi har også Jottacloud til backup, men deling af billeder med andre i OneDrive fungerer fint, oplever jeg. (116 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMMTEB-v2 |
| Backing dataset | NanoMMTEB-v2 |
| Task / split | twitter_hjerne |
| Hugging Face dataset | [hakari-bench/NanoMMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoMMTEB-v2) |
| Source dataset | [mteb/TwitterHjerneRetrieval](https://huggingface.co/datasets/mteb/TwitterHjerneRetrieval) |
| Language | da |
| Category | natural_language |
| Queries | 77 |
| Documents | 262 |
| Positive qrels | 262 |
| Avg positives / query | 3.40 |
| Positives per query (min / median / max) | 1 / 3 / 6 |
| Queries with multiple positives | 75 (97.40%) |
| BM25 nDCG@10 | 0.2395 |
| BM25 hit@10 | 0.6104 |
| Query length avg chars | 165.75 |
| Document length avg chars | 128.77 |

### Public Sources

- [The Scandinavian Embedding Benchmarks](https://arxiv.org/abs/2406.02396).
- [sorenmulli/da-hashtag-twitterhjerne](https://huggingface.co/datasets/sorenmulli/da-hashtag-twitterhjerne).
- [mteb/TwitterHjerneRetrieval](https://huggingface.co/datasets/mteb/TwitterHjerneRetrieval).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoMMTEB-v2)
- Source dataset: [mteb/TwitterHjerneRetrieval](https://huggingface.co/datasets/mteb/TwitterHjerneRetrieval)
- Upstream dataset: [sorenmulli/da-hashtag-twitterhjerne](https://huggingface.co/datasets/sorenmulli/da-hashtag-twitterhjerne)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| The Scandinavian Embedding Benchmarks | 2024 | benchmark paper | https://arxiv.org/abs/2406.02396 |
| sorenmulli/da-hashtag-twitterhjerne | 2024 | dataset card | https://huggingface.co/datasets/sorenmulli/da-hashtag-twitterhjerne |
| mteb/TwitterHjerneRetrieval | 2024 | dataset card | https://huggingface.co/datasets/mteb/TwitterHjerneRetrieval |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMMTEB-v2
  backing_dataset: NanoMMTEB-v2
  dataset_id: hakari-bench/NanoMMTEB-v2
  task_name: twitter_hjerne
  split_name: twitter_hjerne
  language: da
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMMTEB-v2/twitter_hjerne.md
  source_research:
    primary_source_type: dataset_card
    paper_pdf_or_html_checked: true
    no_paper_note: "No standalone TwitterHjerne retrieval paper was confirmed; source dataset card and Scandinavian benchmark paper were checked."
  counts:
    queries: 77
    documents: 262
    positive_qrels: 262
  positives_per_query:
    average: 3.4025974025974026
    min: 1
    median: 3
    max: 6
    multi_positive_queries: 75
    multi_positive_query_percent: 97.40259740259741
  text_stats_chars:
    query_mean: 165.75324675324674
    document_mean: 128.7709923664122
  bm25:
    ndcg_at_10: 0.23947764988878614
    hit_at_10: 0.6103896103896104
    source: dataset_bm25_column
  learning:
    original_train_split: available
    evaluation_split_origin: train
    train_eval_overlap_audit: not_audited
    leakage_note: do not train on this Nano split's question tweets, reply tweets, or qrels
    useful_training_data:
      - Danish social-media QA pairs
      - Danish forum question-reply data
      - community-support and recommendation threads
      - multi-positive answer retrieval data
    synthetic_data:
      document_generation: informal Danish reply tweets with advice, recommendations, and troubleshooting tips
      question_generation: Danish #Twitterhjerne-style help-seeking tweets
      answerability: several replies may be valid if they address the same user need
    multi_positive_training: multi_positive_objective
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMMTEB-v2
    source_urls:
      - label: Scandinavian Embedding Benchmarks
        url: https://arxiv.org/abs/2406.02396
      - label: sorenmulli/da-hashtag-twitterhjerne
        url: https://huggingface.co/datasets/sorenmulli/da-hashtag-twitterhjerne
      - label: mteb/TwitterHjerneRetrieval
        url: https://huggingface.co/datasets/mteb/TwitterHjerneRetrieval
    source_notes: []
  references:
    - title: "The Scandinavian Embedding Benchmarks"
      url: https://arxiv.org/abs/2406.02396
      year: 2024
      is_paper: true
      source_confidence: benchmark_paper_link
```
