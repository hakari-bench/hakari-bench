# NanoFaMTEB-v2 / neu_clir2023_fas

## Overview

`neu_clir2023_fas` is a Persian NeuCLIR retrieval task in NanoFaMTEB-v2. The queries are Persian information needs, and the documents are long Persian news or web documents drawn from a hard-negative retrieval pool.

This task is a useful long-document retrieval benchmark. It combines named events, organizations, countries, and policy topics with many relevant documents per query. A model must retrieve multiple articles that satisfy the same information need rather than only identify one short answer passage.

## Details

### What the Original Data Measures

FaMTEB includes NeuCLIR retrieval among its Persian retrieval resources. NeuCLIR is a cross-language and multilingual information retrieval benchmark focused on news-like topics and document collections. In this Nano split, the task is represented as Persian retrieval over Persian documents.

The public source is `mteb/NeuCLIR2023RetrievalHardNegatives`, described as a hard-negative version built from BM25 and multilingual dense retriever pools. This makes the task suitable for comparing lexical retrieval, dense semantic retrieval, and hybrid candidate pools on long Persian documents.

### Observed Data Profile

This Nano split contains 74 queries, 10,000 documents, and 3,669 positive qrels. It is strongly multi-positive: queries have 49.58 positives on average, with a minimum of 1, a median of 38.0, and a maximum of 100. There are 73 multi-positive queries, or 98.65% of the split. Queries average 65.82 characters, and documents average 3,121.94 characters.

Observed examples ask for information about Chinese companies sanctioned by the United States, the Evergreen ship blocked in the Suez Canal, tourism potential between Uzbekistan and Iran, ecological effects of the Sanchi tanker collision, and the opportunities and challenges of 5G internet. Positive documents are long news-style passages or articles.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.4336, hit@10 of 0.9054, and recall@100 of 0.5508 with a top-500 candidate pool. The high hit rate shows that lexical retrieval usually finds at least one relevant article, especially when queries contain names such as organizations, ships, countries, or technologies.

The ranking and coverage limits are visible in nDCG and recall. Long documents contain many overlapping terms, and hard negatives may mention the same event without satisfying the exact information need. BM25 can also over-prioritize articles with repeated keywords while missing broader contextual relevance.

### Dense Evaluation Profile

The dense harrier-oss-270m profile reaches nDCG@10 of 0.5766, hit@10 of 0.9730, and recall@100 of 0.5890. Dense retrieval is the strongest top-ranking profile and improves all three headline metrics over BM25.

This suggests that embedding similarity is important for NeuCLIR-style topics. Queries often describe an information need rather than a single entity lookup, and relevant articles may express the event, consequence, or policy issue using varied wording. Dense retrieval helps connect the query intent to long documents that do not repeat every phrase.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate subset reaches nDCG@10 of 0.5595, hit@10 of 0.9459, and recall@100 of 0.5993. It uses exactly 100 candidates per query and has no safeguard-positive rows.

Hybrid retrieval is strongest on recall@100, which matters in this task because nearly all queries have many positives. Its nDCG@10 is slightly below dense retrieval, indicating that dense-only ranking is a better first-stage top-10 ordering signal, while hybrid retrieval gives rerankers a broader and more complete candidate pool.

### Metric Interpretation for Model Researchers

`neu_clir2023_fas` is best read as a long-document, many-positive retrieval task. Hit@10 is less discriminative because most profiles retrieve at least one positive. nDCG@10 measures how well the first page is ordered, and recall@100 measures whether the model covers the broader relevant article set.

Dense retrieval is the strongest direct ranking signal. reranking_hybrid is attractive for reranking because it improves relevant coverage despite using only 100 candidates. BM25 remains useful as a lexical component, but exact term matching alone is not enough for high-quality ranking.

### Query and Relevance Type Tendencies

Queries are Persian information needs about events, policy issues, international relations, accidents, technologies, and organizations. They are longer than typical keyword queries and often ask to "find information" about a topic.

Relevant documents are long articles or news-style passages. A document may be relevant because it discusses the event background, consequence, stakeholder, or policy angle requested by the query. This creates a broader relevance space than single-answer QA.

### Representative Failure Modes

BM25 may retrieve articles that mention the same entity or event but do not cover the requested angle. Dense retrieval may find thematically similar articles while missing a precise named organization, date, or incident. Hybrid retrieval improves coverage but still leaves the reranker to choose among long documents with overlapping event descriptions.

Another failure mode is under-coverage. With dozens of relevant documents per query, a model can look strong on hit@10 while still missing a large fraction of relevant articles in the top 100.

### Training Data That May Help

Useful training data includes Persian news retrieval, NeuCLIR-style topic-document judgments, long-document retrieval data, multilingual CLIR resources, and hard negatives centered on the same event or organization. Training should include many-positive topics so the model learns coverage rather than only one-answer matching.

Training should exclude this split's topics, documents, and relevance labels.

### Model Improvement Notes

Improving this task requires long-document representations that preserve both entity details and topic-level intent. Models should handle Persian news style, dates, organization names, event descriptions, and consequence-oriented queries.

For reranking, passage or document chunking may matter: a long document can be relevant because of one section, while the rest contains unrelated context. A strong reranker should identify whether the document satisfies the information need, not only whether it discusses the same broad topic.

## Example Data

### Public Sources

This task is documented through the FaMTEB paper, the NeuCLIR benchmark context, and the `mteb/NeuCLIR2023RetrievalHardNegatives` dataset card. MTEB provides the broader retrieval evaluation interface.

### Source Reference Table

| Source | Role |
| --- | --- |
| [FaMTEB: Massive Text Embedding Benchmark in Persian Language](https://arxiv.org/abs/2502.11571) | Persian embedding benchmark paper. |
| [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316) | General embedding benchmark framework. |
| [NeuCLIR project](https://neuclir.github.io/) | Original NeuCLIR benchmark context. |
| [mteb/NeuCLIR2023RetrievalHardNegatives](https://huggingface.co/datasets/mteb/NeuCLIR2023RetrievalHardNegatives) | Public hard-negative source dataset card. |
| [hakari-bench/NanoFaMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoFaMTEB-v2) | Nano benchmark dataset containing this split. |

### Representative Snippets

| Query Pattern | Positive Document Pattern |
| --- | --- |
| A Persian topic asking for information about Chinese companies sanctioned by the United States, excluding Huawei. | A news article listing Chinese companies added to a Pentagon blacklist and giving details about their business context. |
| A topic asking for information about the Evergreen ship stuck in the Suez Canal. | A news passage about attempts to refloat the large cargo ship blocking the canal. |
| A question about tourism potential between Uzbekistan and Iran. | An article discussing Silk Road tourism links and economic or cultural ties between the countries. |
| A topic asking about ecological and environmental effects of the Sanchi tanker collision. | A report about the oil slick, collision details, and environmental consequences near China. |
| A question about the potential and challenges of 5G internet for people and companies. | A technology news article discussing spectrum availability, infrastructure, and 5G deployment constraints. |
