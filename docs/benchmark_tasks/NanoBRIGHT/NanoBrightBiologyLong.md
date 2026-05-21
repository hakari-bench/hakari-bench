# NanoBRIGHT / NanoBrightBiologyLong

## Overview

`NanoBrightBiologyLong` is the long-document version of the Biology
StackExchange BRIGHT task. The queries are the same detailed biology posts, but
the retrieval corpus contains full or much longer cited web documents instead
of short passages.

## Details

### What the Original Data Measures

[BRIGHT](https://arxiv.org/abs/2407.12883) adds long-context variants to test
reasoning-intensive retrieval when the relevant evidence is embedded in lengthy
documents. The paper notes that these variants use unsplit web pages with far
fewer documents, and reports recall@1 in the original benchmark because top-10
metrics become less stable on small long-document pools. This Nano page still
reports the repository-provided BM25 nDCG@10 and hit@10 for consistency.

### Observed Data Profile

The split has 103 queries, 498 documents, and 134 positive qrels. Query text is
identical in style to the short Biology split, averaging 523.03 characters.
Documents average 36,923.73 characters and include long encyclopedia or web
pages. Positives average 1.30 per query, so this version is less multi-positive
than the passage-split task.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.2540 and hit@10 = 0.4466. It ranks 16 queries with a positive first, and the
median best positive rank is 13. Long documents add lexical noise: the right
page may contain the concept, but many unrelated page sections also contain
overlapping biological terms.

### Training Data That May Help

Useful data includes long biomedical and biology web pages aligned to questions,
StackExchange posts with full cited sources, and passage-to-document
distillation where a model learns to retrieve the full source page from a
shorter evidence passage.

### Synthetic Data Guidance

Generate or select long biology reference pages with multiple sections, then
write questions whose answer requires one specific mechanism in the page. Hard
negatives should be full pages on nearby biological topics that contain shared
terms but not the supporting explanation.

## Example Data

| Query | Positive document |
| --- | --- |
| What is the longest-lasting protein in a human body? Protein life times are, on average, not particularly long, on a human life timescale. I was wondering, how old is the oldest protein in a human body? Just to clarify, I mea ... [truncated 225 chars](1199 chars) | 2006 Function[edit] The ELN gene encodes a protein that is one of the two components of elastic fibers. The encoded protein is rich in hydrophobic amino acids such as glycine and proline, which form mobile hydrophobic regions ... [truncated 225 chars](6263 chars) |
| Is kissing a natural human activity? The word natural here is meant in contrast to it being a sociological construct. Is kissing in all its forms something natural for humans? Is it instinctively erotic? Or is it just a conve ... [truncated 225 chars](435 chars) | A kiss is the touch or pressing of one's lips against another person or an object. Cultural connotations of kissing vary widely. Depending on the culture and context, a kiss can express sentiments of love, passion, romance, s ... [truncated 225 chars](40449 chars) |
| What types of light can't a plant photosynthesize in? I have a plant on my desk, and it got me to wondering: Can my plant use the light from my monitors to photosynthesize? If so, what light (apart from green light, to a degr ... [truncated 225 chars](509 chars) | Chlorophyll is any of several related green pigments found in cyanobacteria and in the chloroplasts of algae and plants. Its name is derived from the Greek words χλωρός, khloros ("pale green") and φύλλον, phyllon ("leaf"). Ch ... [truncated 225 chars](14080 chars) |
| If Tumors have lots of mutations in them how is it the immune system can't detect them? If a cancerous tumor has a lot of mutations in them why can't the immune system detect them? If a person has cancer could this somehow al ... [truncated 225 chars](425 chars) | The major histocompatibility complex (MHC) is a large locus on vertebrate DNA containing a set of closely linked polymorphic genes that code for cell surface proteins essential for the adaptive immune system. These cell surfa ... [truncated 225 chars](48879 chars) |
| Could viruses be used as antibiotics? Could we use viruses that only affect bacteria to act as antibiotics? The more bacteria, the more times the virus divides, so the stronger it gets. Is this practical? (204 chars) | Phage therapy, viral phage therapy, or phagotherapy is the therapeutic use of bacteriophages for the treatment of pathogenic bacterial infections. This therapeutic approach emerged at the beginning of the 20th century but was ... [truncated 225 chars](41348 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoBRIGHT |
| Backing dataset | NanoBRIGHT |
| Task / split | NanoBrightBiologyLong |
| Source task | Biology StackExchange long-document |
| Hugging Face dataset | [hakari-bench/NanoBRIGHT](https://huggingface.co/datasets/hakari-bench/NanoBRIGHT) |
| Source dataset | [xlangai/BRIGHT](https://huggingface.co/datasets/xlangai/BRIGHT) |
| Language | en |
| Category | natural_language |
| Queries | 103 |
| Documents | 498 |
| Positive qrels | 134 |
| Positives per query | avg 1.30, min 1, median 1, max 4 |
| Multi-positive queries | 24 (23.30%) |
| BM25 nDCG@10 | 0.2540 |
| BM25 hit@10 | 0.4466 |
| Query length avg chars | 523.03 |
| Document length avg chars | 36923.73 |

### Public Sources

- [BRIGHT: A Realistic and Challenging Benchmark for Reasoning-Intensive Retrieval](https://arxiv.org/abs/2407.12883).
- [BRIGHT project page](https://brightbenchmark.github.io/).
- [xlangai/BRIGHT](https://huggingface.co/datasets/xlangai/BRIGHT).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBRIGHT](https://huggingface.co/datasets/hakari-bench/NanoBRIGHT)
- Source dataset: [xlangai/BRIGHT](https://huggingface.co/datasets/xlangai/BRIGHT)
- MTEB dataset record: [mteb/BRIGHT](https://huggingface.co/datasets/mteb/BRIGHT)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| BRIGHT: A Realistic and Challenging Benchmark for Reasoning-Intensive Retrieval | 2024 | benchmark paper | https://arxiv.org/abs/2407.12883 |
| BRIGHT project page | 2024 | project page | https://brightbenchmark.github.io/ |
| xlangai/BRIGHT | 2024 | dataset card | https://huggingface.co/datasets/xlangai/BRIGHT |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoBRIGHT
  backing_dataset: NanoBRIGHT
  dataset_id: hakari-bench/NanoBRIGHT
  task_name: NanoBrightBiologyLong
  split_name: NanoBrightBiologyLong
  source_task: Biology StackExchange long-document
  source_dataset_id: xlangai/BRIGHT
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoBRIGHT/NanoBrightBiologyLong.md
  source_research:
    primary_source_type: benchmark_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 103
    documents: 498
    positive_qrels: 134
  positives_per_query:
    average: 1.3009708737864079
    min: 1
    median: 1
    max: 4
    multi_positive_queries: 24
    multi_positive_query_percent: 23.300970873786408
  text_stats_chars:
    query_mean: 523.0291262135922
    document_mean: 36923.73092369478
  bm25:
    ndcg_at_10: 0.2540185992266564
    hit_at_10: 0.44660194174757284
    source: dataset_bm25_column
  learning:
    original_train_split: unknown
    evaluation_split_origin: BRIGHT Biology long-document evaluation split
    train_eval_overlap_audit: not_audited
    leakage_note: exclude NanoBRIGHT BiologyLong queries and full cited source pages
    useful_training_data:
      - long biology reference pages aligned to questions
      - StackExchange posts with full cited sources
      - passage-to-document retrieval distillation
    synthetic_data:
      document_generation: long multi-section biology reference pages
      question_generation: detailed biology questions grounded in a specific section
      answerability: positive full document should contain the supporting biological mechanism
    multi_positive_training: multi_positive_objective
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoBRIGHT
    source_urls:
      - label: BRIGHT arXiv
        url: https://arxiv.org/abs/2407.12883
      - label: BRIGHT project
        url: https://brightbenchmark.github.io/
      - label: xlangai/BRIGHT
        url: https://huggingface.co/datasets/xlangai/BRIGHT
    source_notes: []
  references:
    - title: "BRIGHT: A Realistic and Challenging Benchmark for Reasoning-Intensive Retrieval"
      url: https://arxiv.org/abs/2407.12883
      year: 2024
      doi: 10.48550/arXiv.2407.12883
      is_paper: true
      source_confidence: definitive_paper_link
```
