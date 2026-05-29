# NanoLongEmbed / NanoSummScreenFD

## Overview

`NanoSummScreenFD` is the ForeverDreaming subset of SummScreen as used in
LongEmbed. Queries are human-written TV episode recaps, and documents are long
screenplay-style transcripts. The retriever must find the episode transcript
whose dialogue and scene actions correspond to the recap.

## Details

### What the Original Data Measures

[SummScreen: A Dataset for Abstractive Screenplay Summarization](https://arxiv.org/abs/2104.07091)
introduces a dataset of TV transcripts paired with episode recaps. The paper
states that plot details are often communicated indirectly through character
dialogue, that many transcript lines are not central to the plot, and that
parallel subplots can be separated by scene breaks.

[LongEmbed: Extending Embedding Models for Long Context Retrieval](https://arxiv.org/abs/2404.12096)
turns SummScreenFD into retrieval by using the recap as the query and the input
transcripts as candidates. The task rewards matching a concise plot summary to
a noisy long dialogue transcript.

### Observed Data Profile

The Nano split has 200 English recap queries, 336 transcript documents, and 200
positive qrels. Every query has one positive. Queries average 600.67
characters, while documents average 30,854.33 characters. Sampled positives
come from `Doctor Who`, `High Maintenance`, `One Tree Hill`, `Friday Night
Lights`, and `Charmed`.

Documents are dialogue-heavy and often begin in the middle of action or
conversation. Speaker names, scene breaks, and recurring character names are
strong signals, but the recap often paraphrases the transcript rather than
copying a contiguous span.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.9746 and hit@10 = 0.9950. It ranks 189 positives first and 199 positives in
the top 10, so lexical overlap is very strong in this Nano subset.

The high score says that the recaps contain many names, episode-specific
events, and show-specific terms that identify the transcript. Remaining
difficulty is mostly in distinguishing episodes from the same show when
character names and recurring settings overlap.

### Training Data That May Help

Useful data includes non-overlapping SummScreen train examples, TV episode
recap-to-transcript pairs, dialogue summarization data, and retrieval pairs
that match long conversations to concise plot summaries. Training should avoid
the same SummScreenFD evaluation examples, Nano queries, qrels, and positive
transcripts.

### Synthetic Data Guidance

For document-to-question generation, use non-evaluation episode transcripts and
generate recap-like queries that mention the central conflict, characters, and
outcome. For joint generation, create long dialogue transcripts with speaker
labels, scene breaks, parallel subplots, and a short recap grounded in events
distributed across the transcript. Do not use Nano evaluation recaps or
transcripts as seeds.

## Example Data

| Query | Positive document |
| --- | --- |
| Angel decides to do the right thing and break up with Buffy. Meanwhile, Buffy has to save the prom from Hellhounds with a fetish for formal wear. Angel shows up for the last dance. (180 chars) | Buffy is napping in Angel's bed. Angel is watching her sleep. He smiles at her as she wakes. Buffy: (smiles) What? Do I have funny bed hair or something? Angel: Or something? Buffy: I guess we got a little carried away with t ... [truncated 225 chars](31147 chars) |
| Whilst Haley cares for their new daughter, Lydia, Nathan confronts Professor Kellerman (guest star Peter Riegert) about the accident. Meanwhile Quinn organizes a concert at Tric and Brooke gets an offer to return to Clothes O ... [truncated 225 chars](476 chars) | [PREVIOUSLY_ON] IAN: What the hell? I knew you guys couldn't be complete dorks. CLAY: Complete dorks and officially your agents. NATHAN: You got a bathroom in this place? IAN: There's one in the back of the house passed the k ... [truncated 225 chars](26247 chars) |
| Led by Prue, the Charmed Ones help a young man named Brendan ( Michael Weatherly ) who wants to become a priest in order to avoid fulfilling his predicted destiny as a warlock along with his brothers. They begin attacking peo ... [truncated 225 chars](447 chars) | [Scene: Church. Brendan and a priest are there.] Brendan: I wake up at night, my heart pounding, a voice whispering in my head your a fraud, you can't fool God. Priest: These are not new fears, Brendan. I've watched you grow, ... [truncated 225 chars](31115 chars) |
| Frasier has a recurring erotic dream in which he wakes up in bed, hears the shower running and is shocked when the person who emerges is KACL's food critic, Gil Chesterton. He struggles to work out the meaning of the dream, e ... [truncated 225 chars](557 chars) | Act One Scene One - A Seedy Motel Room. Frasier is lying in bed, asleep, in the motel room. He awakens and finds that he has a tattoo on his arm that reads "Chesty." There is a half-empty bottle of tequila on a table across f ... [truncated 225 chars](23983 chars) |
| The Skins make all the humans in Roswell, New Mexico disappear, turning it into a ghost town. Maria and Liz manage to slip through the cracks and don't disappear with the rest of the humans because they were out of town at th ... [truncated 225 chars](694 chars) | "Wipe Out" 29th Episode of Roswell Production Code: 2ADA07 [SCENE_BREAK] (Episode begins with a tour bus heading towards Roswell) (At the Evans household, Diane Evans is trying out her cooking skills) Diane: It's a frijoles f ... [truncated 225 chars](26102 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoLongEmbed |
| Backing dataset | NanoLongEmbed |
| Task / split | NanoSummScreenFD |
| Hugging Face dataset | [hakari-bench/NanoLongEmbed](https://huggingface.co/datasets/hakari-bench/NanoLongEmbed) |
| Language | en |
| Category | natural_language |
| Queries | 200 |
| Documents | 336 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.9813 |
| BM25 hit@10 | 1.0000 |
| BM25 Recall@100 | 1.0000 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.9198 |
| Dense hit@10 | 0.9600 |
| Dense Recall@100 | 0.9700 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.9443 |
| Reranking hybrid hit@10 | 0.9700 |
| Reranking hybrid Recall@100 | 1.0000 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100 |
| Reranking hybrid safeguard rows | 0 |
| Query length avg chars | 600.67 |
| Document length avg chars | 30854.33 |

### Public Sources

- [SummScreen: A Dataset for Abstractive Screenplay Summarization](https://arxiv.org/abs/2104.07091); 2022; Mingda Chen et al.; DOI: `10.18653/v1/2022.acl-long.589`.
- [LongEmbed: Extending Embedding Models for Long Context Retrieval](https://arxiv.org/abs/2404.12096); 2024; Dawei Zhu et al.; DOI: `10.18653/v1/2024.emnlp-main.47`.
- [dwzhu/LongEmbed dataset card](https://huggingface.co/datasets/dwzhu/LongEmbed).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoLongEmbed](https://huggingface.co/datasets/hakari-bench/NanoLongEmbed)
- Source dataset: [dwzhu/LongEmbed](https://huggingface.co/datasets/dwzhu/LongEmbed)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| SummScreen: A Dataset for Abstractive Screenplay Summarization | 2022 | arXiv paper | https://arxiv.org/abs/2104.07091 |
| LongEmbed: Extending Embedding Models for Long Context Retrieval | 2024 | arXiv paper | https://arxiv.org/abs/2404.12096 |
| dwzhu/LongEmbed | 2024 | dataset card | https://huggingface.co/datasets/dwzhu/LongEmbed |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoLongEmbed
  backing_dataset: NanoLongEmbed
  dataset_id: hakari-bench/NanoLongEmbed
  task_name: NanoSummScreenFD
  split_name: NanoSummScreenFD
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoLongEmbed/NanoSummScreenFD.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 200
    documents: 336
    positive_qrels: 200
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 600.665
    document_mean: 30854.32738095238
  bm25:
    ndcg_at_10: 0.9813493022457247
    hit_at_10: 1.0
    source: dataset_candidate_subset
  learning:
    original_train_split: available
    evaluation_split_origin: unknown
    train_eval_overlap_audit: not_audited
    leakage_note: exclude SummScreenFD evaluation examples, Nano queries, qrels, and
      positive transcripts likely to overlap with this task
    useful_training_data:
    - non-overlapping SummScreen train examples
    - TV recap-to-transcript retrieval pairs
    - long dialogue summarization pairs
    - adjacent-episode hard negatives from the same show
    synthetic_data:
      document_generation: long TV transcript-style dialogue with speaker labels,
        scene breaks, multiple characters, and parallel subplots
      question_generation: recap-like English summaries naming characters, conflicts,
        outcomes, and key episode events
      answerability: the recap should be grounded in events distributed across the
        transcript
    multi_positive_training: single_positive_question_document_focus
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoLongEmbed
    source_urls:
    - label: SummScreen arXiv
      url: https://arxiv.org/abs/2104.07091
    - label: LongEmbed arXiv
      url: https://arxiv.org/abs/2404.12096
    - label: dwzhu/LongEmbed
      url: https://huggingface.co/datasets/dwzhu/LongEmbed
    source_notes: []
  references:
  - title: 'SummScreen: A Dataset for Abstractive Screenplay Summarization'
    url: https://arxiv.org/abs/2104.07091
    year: 2022
    doi: 10.18653/v1/2022.acl-long.589
    is_paper: true
    source_confidence: definitive_paper_link
  - title: 'LongEmbed: Extending Embedding Models for Long Context Retrieval'
    url: https://arxiv.org/abs/2404.12096
    year: 2024
    doi: 10.18653/v1/2024.emnlp-main.47
    is_paper: true
    source_confidence: definitive_paper_link
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.9813493022
      hit_at_10: 1.0
      recall_at_100: 1.0
      candidate_count_min: 336
      candidate_count_max: 336
      candidate_count_mean: 336.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 1.0
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.9198303494
      hit_at_10: 0.96
      recall_at_100: 0.97
      candidate_count_min: 336
      candidate_count_max: 336
      candidate_count_mean: 336.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.97
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.944324837
      hit_at_10: 0.97
      recall_at_100: 1.0
      candidate_count_min: 100
      candidate_count_max: 100
      candidate_count_mean: 100.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 1.0
      safeguard_positive_rows: 0
      rows_with_101_candidates: 0
```
