# NanoMTEB-Scandinavian

> [!NOTE]
> This page was prepared by manual review of source papers, dataset cards,
> repository metadata, and sampled benchmark data. It may contain mistakes;
> please treat it as a reference aid rather than a definitive source.

## Overview

NanoMTEB-Scandinavian is a compact retrieval group for Scandinavian-language
MTEB-style tasks. It covers Danish, Norwegian, and Swedish retrieval with a
mixture of fact verification, extractive QA answer selection, encyclopedia
article lookup, FAQ retrieval, news headline or summary retrieval, and informal
social question answering. The group is small in task count, but it is not
single-domain: it deliberately mixes highly lexical title/evidence retrieval
with short-answer and conversational answer retrieval where lexical overlap is
weak.

## Details

### What the Original Group Measures

The group follows the Scandinavian Embedding Benchmark (SEB), which was created
to evaluate text embeddings for Scandinavian languages across multiple task
families and later integrated with MTEB. The Nano version keeps seven retrieval
splits from that ecosystem: Danish DanFEVER, Norwegian NorQuAD and SNL, Swedish
SweFAQ and SweDN, Danish TV2 Nord news, and Danish #Twitterhjerne social QA.

Several source datasets were not originally designed as retrieval benchmarks.
DanFEVER is a Danish FEVER-style claim verification dataset; NorQuAD is an
extractive reading-comprehension dataset; SNL, SweDN, and TV2 Nord are adapted
from encyclopedia or summarization resources. SEB converts these into retrieval
by using claims, questions, titles, headlines, or summaries as queries and the
corresponding evidence, answer, article, or reply text as the relevant document.

### Subtask Coverage

The seven subtasks cover five retrieval families:

- **Fact verification:** `dan_fever` retrieves Danish evidence snippets for
  Danish factual claims.
- **Question answering and answer selection:** `nor_quad`, `swe_faq`, and
  `twitter_hjerne` retrieve short Norwegian answers, Swedish authority FAQ
  answers, or Danish social-media replies.
- **Encyclopedic title retrieval:** `snl` retrieves Store norske leksikon
  article text from short Norwegian headwords or titles.
- **News retrieval:** `swedn` retrieves Swedish Dagens Nyheter summaries and
  articles from headlines, while `tv2_nordretrieval` retrieves Danish TV2 Nord
  articles from short summaries.
- **Multi-positive retrieval:** `nor_quad`, `swedn`, and especially
  `twitter_hjerne` include more than one relevant document for many queries.

The group is mostly monolingual by split, but the configuration marks the
collection as multilingual because it spans Danish, Norwegian, Swedish, and
some language-detector ambiguity among closely related Scandinavian languages.
This is visible in Norwegian and Danish data where short titles, names, and
shared vocabulary can be detected as Danish, Swedish, English, or German even
when the intended retrieval setting is Scandinavian.

### Observed Group Profile

Across the seven splits, NanoMTEB-Scandinavian contains 1,273 queries, 1,753
positive qrels, and 9,737 split-local candidate documents. The document count
is a sum across subtasks, not a deduplicated group-wide corpus size. The group
average is 1.38 positives per query, with 370 multi-positive queries. The
largest per-query relevance set is in `twitter_hjerne`, where a question tweet
can have up to six relevant answer tweets.

The text shapes differ substantially. `snl` has very short title-like queries
averaging 13.25 characters but long encyclopedia documents averaging 1,982.85
characters. `twitter_hjerne` has the longest queries, averaging 165.01
characters, because the questions are full informal tweets; its answer
documents are much shorter. `nor_quad` has compact Norwegian questions and very
short answer documents, often names, dates, locations, or numbers. News splits
use headline or summary queries against long article documents.

### BM25 Difficulty

The query-weighted BM25 baseline reaches nDCG@10 = 0.6464 and hit@10 = 0.7722.
The easiest split by nDCG@10 is `tv2_nordretrieval` at 0.8957, closely followed
by `dan_fever` and `snl`. These tasks often expose strong lexical anchors:
named entities, dates, article titles, local place names, or encyclopedia
headwords.

The hardest split is `nor_quad` at nDCG@10 = 0.1118. This is expected from the
retrieval adaptation: the positive is often a short answer string that does not
repeat the question wording. `twitter_hjerne` is also difficult for BM25
because useful replies to informal questions can be semantically relevant while
sharing little vocabulary with the question tweet. `swe_faq` sits between these
extremes: public-sector terminology helps lexical retrieval, but many answers
resolve the question without restating it.

### Training Data That May Help

Useful training data should preserve the source retrieval shape rather than
treat every split as generic passage retrieval. Danish and Swedish news
headline-to-article pairs help `swedn` and `tv2_nordretrieval`; Danish
claim/evidence and Wikipedia retrieval pairs help `dan_fever`; Norwegian
extractive QA and answer-selection pairs help `nor_quad`; SNL-style
title/article data helps `snl`; Swedish FAQ and public-sector help-center data
helps `swe_faq`; Danish forum or social QA threads help `twitter_hjerne`.

Training data should exclude evaluation queries, qrels, positives, and near
duplicates from the Nano splits. For `swedn`, the two-positive structure should
be preserved because both summary and article documents can be relevant. For
`twitter_hjerne`, multi-answer relevance is central to the task and should not
be collapsed into one canonical answer.

### Synthetic Data Guidance

Synthetic data should mirror each source family. For fact verification, generate
Danish claims and evidence snippets with controlled entity, date, and relation
changes. For answer selection, generate Norwegian questions with concise answer
strings and Swedish FAQ questions with policy-style answers. For encyclopedia
retrieval, generate Norwegian headwords, aliases, and article-style bodies. For
news retrieval, generate Danish or Swedish headlines, summaries, and full
articles with hard negatives from the same location, section, or event type.
For social QA, generate informal Danish help-seeking tweets with multiple
plausible replies and near-negative replies from adjacent topics.

Synthetic examples should not use NanoMTEB-Scandinavian evaluation queries,
positive documents, tweet threads, or article pairs as seeds.

## Task Summary

| Task | Retrieval shape | Lang | Queries | Docs | Positive qrels | BM25 nDCG@10 | BM25 hit@10 | Query avg chars | Doc avg chars | Source status |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| [dan_fever](dan_fever.md) | Danish claim to evidence snippet | da | 200 | 2,522 | 200 | 0.8856 | 0.9900 | 59.48 | 312.00 | DanFEVER paper / SEB |
| [nor_quad](nor_quad.md) | Norwegian question to short answer | no | 196 | 1,048 | 291 | 0.1118 | 0.2143 | 48.61 | 214.39 | NorQuAD paper / SEB |
| [snl](snl.md) | Norwegian headword to lexicon article | no | 200 | 1,300 | 200 | 0.8781 | 0.9000 | 13.25 | 1,982.85 | SNL dataset card / SEB |
| [swe_faq](swe_faq.md) | Swedish FAQ question to authority answer | sv | 200 | 511 | 200 | 0.5449 | 0.7500 | 73.33 | 319.78 | SuperLim / SweFAQ |
| [swedn](swedn.md) | Swedish headline to summary and article | sv | 200 | 2,046 | 400 | 0.7081 | 0.8950 | 45.26 | 2,895.97 | SweDN / SuperLim |
| [tv2_nordretrieval](tv2_nordretrieval.md) | Danish local-news summary to article | da | 200 | 2,048 | 200 | 0.8957 | 0.9350 | 127.97 | 1,440.57 | TV2 Nord dataset card / SEB |
| [twitter_hjerne](twitter_hjerne.md) | Danish question tweet to answer tweets | da | 77 | 262 | 262 | 0.2395 | 0.6104 | 165.01 | 128.49 | #Twitterhjerne dataset card / SEB |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMTEB-Scandinavian |
| Backing dataset | NanoMTEB-Scandinavian |
| Hugging Face dataset | [hakari-bench/NanoMTEB-Scandinavian](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Scandinavian) |
| Languages | da, no, sv, multilingual |
| Category | natural_language |
| Subtasks | 7 |
| Total queries | 1,273 |
| Split-local documents | 9,737 |
| Positive qrels | 1,753 |
| Positives per query | 1.38 average |
| Multi-positive queries | 370 |
| Query-weighted BM25 nDCG@10 | 0.6464 |
| Query-weighted BM25 hit@10 | 0.7722 |
| Mean query length | 67.63 chars, weighted by query count |
| Mean document length | 1,300.38 chars, weighted by split-local document count |

### Public Sources

- [The Scandinavian Embedding Benchmarks](https://arxiv.org/abs/2406.02396); 2024; group benchmark source.
- [DanFEVER: claim verification dataset for Danish](https://aclanthology.org/2021.nodalida-main.47/); 2021; Danish FEVER-style claim verification source.
- [NorQuAD: Norwegian Question Answering Dataset](https://aclanthology.org/2023.nodalida-1.17/); 2023; Norwegian extractive QA source.
- [Superlim: A Swedish Language Understanding Evaluation Benchmark](https://aclanthology.org/2023.emnlp-main.506/); 2023; Swedish benchmark source for SweFAQ and SweDN context.
- [SweDN resource page](https://spraakbanken.gu.se/en/resources/swedn); Swedish Dagens Nyheter summarization corpus source.
- [Nordjylland News datasheet](https://www.foundationmodels.dk/data/nordjyllandnews/nordjyllandnews.html); Danish TV2 Nord summarization source.
- [#Twitterhjerne dataset card](https://huggingface.co/datasets/sorenmulli/da-hashtag-twitterhjerne); Danish question-tweet and answer-tweet source.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMTEB-Scandinavian](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Scandinavian)
- Source examples:
  [strombergnlp/danfever](https://huggingface.co/datasets/strombergnlp/danfever),
  [mteb/norquad_retrieval](https://huggingface.co/datasets/mteb/norquad_retrieval),
  [adrlau/navjordj-SNL_summarization_copy](https://huggingface.co/datasets/adrlau/navjordj-SNL_summarization_copy),
  [mteb/SweFaqRetrieval](https://huggingface.co/datasets/mteb/SweFaqRetrieval),
  [mteb/SwednRetrieval](https://huggingface.co/datasets/mteb/SwednRetrieval),
  [alexandrainst/nordjylland-news-summarization](https://huggingface.co/datasets/alexandrainst/nordjylland-news-summarization),
  [sorenmulli/da-hashtag-twitterhjerne](https://huggingface.co/datasets/sorenmulli/da-hashtag-twitterhjerne).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| The Scandinavian Embedding Benchmarks | 2024 | benchmark paper | https://arxiv.org/abs/2406.02396 |
| DanFEVER: claim verification dataset for Danish | 2021 | source task paper | https://aclanthology.org/2021.nodalida-main.47/ |
| NorQuAD: Norwegian Question Answering Dataset | 2023 | source task paper | https://aclanthology.org/2023.nodalida-1.17/ |
| Superlim: A Swedish Language Understanding Evaluation Benchmark | 2023 | benchmark paper | https://aclanthology.org/2023.emnlp-main.506/ |
| SweDN 1.0 | 2022 | dataset card | https://spraakbanken.gu.se/en/resources/swedn |
| Nordjylland News | 2024 | dataset card | https://www.foundationmodels.dk/data/nordjyllandnews/nordjyllandnews.html |
| da-hashtag-twitterhjerne | 2024 | dataset card | https://huggingface.co/datasets/sorenmulli/da-hashtag-twitterhjerne |

## Machine-Readable Metadata

<!-- benchmark-task-group-metadata:v1 -->

```yaml
benchmark_task_group_metadata:
  schema_version: 1
  document_status: reviewed_manual
  nano_set: NanoMTEB-Scandinavian
  backing_dataset: NanoMTEB-Scandinavian
  dataset_id: hakari-bench/NanoMTEB-Scandinavian
  language: multilingual
  languages:
    - da
    - no
    - sv
    - multilingual
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMTEB-Scandinavian/index.md
  source_research:
    primary_source_type: benchmark_paper_and_dataset_cards
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    tasks: 7
    queries: 1273
    split_local_documents: 9737
    positive_qrels: 1753
  positives_per_query:
    average: 1.3770620581304007
    min: 1
    median_task_median: 1.0
    max: 6
    multi_positive_tasks: 3
    multi_positive_queries: 370
  text_stats_chars:
    query_mean_weighted_by_queries: 67.6268656716418
    document_mean_weighted_by_documents: 1300.3762966005957
  bm25:
    ndcg_at_10_query_weighted: 0.6463871836210713
    hit_at_10_query_weighted: 0.772191673212883
    ndcg_at_10_unweighted_task_mean: 0.6091099737576102
    hit_at_10_unweighted_task_mean: 0.7563821892393321
    source: dataset_bm25_column
    easiest_task_by_ndcg_at_10: tv2_nordretrieval
    hardest_task_by_ndcg_at_10: nor_quad
  tasks:
    - name: dan_fever
      path: docs/benchmark_tasks/NanoMTEB-Scandinavian/dan_fever.md
      retrieval_shape: danish_claim_to_evidence_snippet
      language: da
      queries: 200
      documents: 2522
      positive_qrels: 200
      bm25_ndcg_at_10: 0.8856498970178633
      bm25_hit_at_10: 0.99
    - name: nor_quad
      path: docs/benchmark_tasks/NanoMTEB-Scandinavian/nor_quad.md
      retrieval_shape: norwegian_question_to_short_answer
      language: no
      queries: 196
      documents: 1048
      positive_qrels: 291
      bm25_ndcg_at_10: 0.11183189367748354
      bm25_hit_at_10: 0.21428571428571427
    - name: snl
      path: docs/benchmark_tasks/NanoMTEB-Scandinavian/snl.md
      retrieval_shape: norwegian_headword_to_lexicon_article
      language: no
      queries: 200
      documents: 1300
      positive_qrels: 200
      bm25_ndcg_at_10: 0.8780559736224016
      bm25_hit_at_10: 0.9
    - name: swe_faq
      path: docs/benchmark_tasks/NanoMTEB-Scandinavian/swe_faq.md
      retrieval_shape: swedish_faq_question_to_authority_answer
      language: sv
      queries: 200
      documents: 511
      positive_qrels: 200
      bm25_ndcg_at_10: 0.5449484654219235
      bm25_hit_at_10: 0.75
    - name: swedn
      path: docs/benchmark_tasks/NanoMTEB-Scandinavian/swedn.md
      retrieval_shape: swedish_headline_to_summary_and_article
      language: sv
      queries: 200
      documents: 2046
      positive_qrels: 400
      bm25_ndcg_at_10: 0.7081125173979356
      bm25_hit_at_10: 0.895
    - name: tv2_nordretrieval
      path: docs/benchmark_tasks/NanoMTEB-Scandinavian/tv2_nordretrieval.md
      retrieval_shape: danish_local_news_summary_to_article
      language: da
      queries: 200
      documents: 2048
      positive_qrels: 200
      bm25_ndcg_at_10: 0.8956934192768778
      bm25_hit_at_10: 0.935
    - name: twitter_hjerne
      path: docs/benchmark_tasks/NanoMTEB-Scandinavian/twitter_hjerne.md
      retrieval_shape: danish_question_tweet_to_answer_tweets
      language: da
      queries: 77
      documents: 262
      positive_qrels: 262
      bm25_ndcg_at_10: 0.23947764988878614
      bm25_hit_at_10: 0.6103896103896104
  learning:
    leakage_note: exclude NanoMTEB-Scandinavian evaluation queries, qrels, positive documents, tweet threads, answer strings, and source article pairs from training
    useful_training_data:
      - Danish claim/evidence and Wikipedia retrieval pairs
      - Norwegian extractive QA and short-answer selection pairs
      - Norwegian lexicon title-to-article pairs
      - Swedish public-sector FAQ question-answer pairs
      - Danish and Swedish headline, summary, and article retrieval pairs
      - Danish social QA and forum answer-retrieval threads
      - hard negatives from the same entity, answer type, authority topic, news section, local place, or social question topic
    synthetic_data:
      document_generation: Scandinavian evidence snippets, short answers, encyclopedia entries, FAQ answers, news articles, summaries, and social replies in source-like style
      question_generation: Danish claims, Norwegian questions and headwords, Swedish FAQ questions and headlines, Danish local-news summaries, and informal Danish question tweets grounded in generated documents
      answerability: positives must preserve evidence support, exact answer validity, title/article identity, FAQ resolution, headline/article pairing, or useful reply relevance rather than broad topical similarity
    multi_positive_training: preserve_nor_quad_swedn_and_twitter_hjerne_multi_positive_qrels
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMTEB-Scandinavian
    source_urls:
      - label: Scandinavian Embedding Benchmarks
        url: https://arxiv.org/abs/2406.02396
      - label: DanFEVER paper
        url: https://aclanthology.org/2021.nodalida-main.47/
      - label: NorQuAD paper
        url: https://aclanthology.org/2023.nodalida-1.17/
      - label: Superlim paper
        url: https://aclanthology.org/2023.emnlp-main.506/
      - label: SweDN resource page
        url: https://spraakbanken.gu.se/en/resources/swedn
      - label: Nordjylland News datasheet
        url: https://www.foundationmodels.dk/data/nordjyllandnews/nordjyllandnews.html
      - label: da-hashtag-twitterhjerne dataset card
        url: https://huggingface.co/datasets/sorenmulli/da-hashtag-twitterhjerne
    source_notes: []
  references:
    - title: The Scandinavian Embedding Benchmarks
      url: https://arxiv.org/abs/2406.02396
      year: 2024
      is_paper: true
      source_confidence: definitive_paper_link
    - title: "DanFEVER: claim verification dataset for Danish"
      url: https://aclanthology.org/2021.nodalida-main.47/
      year: 2021
      is_paper: true
      source_confidence: definitive_paper_link
    - title: "NorQuAD: Norwegian Question Answering Dataset"
      url: https://aclanthology.org/2023.nodalida-1.17/
      year: 2023
      is_paper: true
      source_confidence: definitive_paper_link
    - title: "Superlim: A Swedish Language Understanding Evaluation Benchmark"
      url: https://aclanthology.org/2023.emnlp-main.506/
      year: 2023
      is_paper: true
      source_confidence: definitive_paper_link
    - title: SweDN 1.0
      url: https://spraakbanken.gu.se/en/resources/swedn
      year: 2022
      is_paper: false
      source_confidence: definitive_dataset_card
    - title: Nordjylland News
      url: https://www.foundationmodels.dk/data/nordjyllandnews/nordjyllandnews.html
      year: 2024
      is_paper: false
      source_confidence: definitive_dataset_card
    - title: da-hashtag-twitterhjerne
      url: https://huggingface.co/datasets/sorenmulli/da-hashtag-twitterhjerne
      year: 2024
      is_paper: false
      source_confidence: definitive_dataset_card
```
