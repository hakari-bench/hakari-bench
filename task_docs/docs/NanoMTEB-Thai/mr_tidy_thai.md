# NanoMTEB-Thai / mr_tidy_thai

## Overview

`NanoMTEB-Thai / mr_tidy_thai` is the Thai split of Mr. TyDi retrieval. It evaluates monolingual Thai passage retrieval: Thai factual questions must retrieve Thai Wikipedia-style evidence passages. The original Mr. TyDi benchmark was derived from TyDi QA and designed to evaluate dense retrieval across multiple non-English languages without requiring cross-lingual matching. This Nano task preserves that same-language evidence-retrieval setting in a 200-query, 10,000-document slice. It is a useful benchmark for Thai retrieval because the passages are long enough to contain real context, while the queries often include names, dates, and answer types that expose the different strengths of BM25, dense retrieval, and hybrid candidate generation.

## Details

### What the Original Data Measures

Mr. TyDi measures retrieval over language-specific corpora built from TyDi QA. The task is not to translate the query or retrieve English evidence; it is to match a Thai question with a Thai passage that contains the relevant answer context. This makes it a direct test of Thai lexical processing, Thai semantic representation, and passage-level ranking.

The data is especially valuable because many queries are ordinary factual questions rather than synthetic keyword searches. A retrieval model must understand what the question asks and select a passage that actually supports the answer.

### Observed Data Profile

The Nano split contains 200 queries, 10,000 documents, and 234 positive qrel rows. Each query has 1.17 positives on average, with a median of 1 and a maximum of 3. There are 32 multi-positive queries, or 16.0% of the query set. Queries average 41.59 characters, while documents average 416.31 characters.

The examples include Thai politics, sports coaching, artist biographies, medical definitions, and British monarchy questions. Most documents are compact Thai passages with an entity title followed by explanatory text. Compared with long-document or answer-label tasks, this split has a clean passage-retrieval shape.

### BM25 Evaluation Profile

The BM25 candidate subset uses top-500 candidates and reaches nDCG@10 of 0.8502, hit@10 of 0.9250, and recall@100 of 0.9658. This is one of the stronger BM25 profiles in the Thai set. Query terms frequently overlap with entity titles, person names, country names, and distinctive Thai phrases in the relevant passages.

BM25 is therefore a serious baseline, not a weak lexical floor. It is likely to perform well when the query names the target entity or contains a rare phrase. Its main weakness is fine-grained evidence selection: it may retrieve a related country, organization, person, or event page when the surface vocabulary looks similar but the passage does not answer the exact question.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses top-500 candidates and reaches nDCG@10 of 0.9147, hit@10 of 0.9350, and recall@100 of 0.9530. Dense retrieval produces the best nDCG@10, showing that semantic matching improves top-rank ordering even when BM25 is already very strong.

This result suggests that Thai embedding quality matters most for ranking the correct evidence above plausible lexical neighbors. Dense retrieval may lose a small amount of recall@100 relative to BM25, but it more often places the right passage near the very top. For model researchers, this split is a good test of whether dense representations add value beyond exact Thai term overlap.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates, with two queries carrying a rank-101 safeguard positive. It reaches nDCG@10 of 0.8914, hit@10 of 0.9650, and recall@100 of 0.9915. The hybrid pool has the strongest hit@10 and recall@100, while dense retrieval remains strongest on nDCG@10.

This is a classic hybrid-search profile: sparse and dense retrieval each contribute useful candidates, and their combination gives a reranker a broader and more reliable candidate window. A strong reranker should be able to improve on this pool by preserving the hybrid coverage while learning the passage-level evidence distinction that dense retrieval already captures well.

### Metric Interpretation for Model Researchers

Because all three systems score well, small metric differences matter. Dense retrieval's nDCG@10 advantage points to better rank ordering; hybrid recall shows better candidate coverage; BM25 shows that Thai lexical matching remains highly competitive. Reporting only one metric would hide this structure.

The relatively low multi-positive rate also means that top-rank precision is important. Most queries have only one judged positive, so retrieving a merely related passage is not enough.

### Query and Relevance Type Tendencies

Queries are short factual Thai questions. They often ask about people, events, organizations, capitals, deaths, definitions, or roles. Relevant documents are Thai passages that contain answer-bearing context, frequently beginning with a title-like entity mention.

The task is monolingual and evidence-based. It rewards the ability to retrieve the specific passage that answers the question, not just the most popular page about the topic.

### Representative Failure Modes

Likely failures include confusing similar politicians, countries, institutions, or historical events; retrieving a broad page that shares a named entity but lacks the answer; and over-weighting repeated terms in the document title. Dense systems may also blur fine distinctions between related entities when the question requires an exact role, date, or location.

### Training Data That May Help

Useful training data includes Thai Mr. TyDi examples, Thai Wikipedia QA retrieval, Thai MIRACL, and hard negatives from same-category pages. Entity-rich negatives are especially important: other politicians for political questions, other countries for capital questions, and other biographies for person questions.

### Model Improvement Notes

The best systems for this task should combine Thai-aware lexical recall with dense semantic ranking. Thai segmentation and normalization can improve BM25-style systems, while dense systems need training that emphasizes exact evidence selection and entity disambiguation. Hybrid retrieval is especially attractive because it nearly saturates recall@100 and creates a strong candidate set for reranking experiments.

## Example Data

### Public Sources

- [Mr. TyDi: A Multi-lingual Benchmark for Dense Retrieval](https://arxiv.org/abs/2108.08787), 2021.
- [castorini/mr-tydi](https://huggingface.co/datasets/castorini/mr-tydi), source dataset card.
- [mteb/mrtidy](https://huggingface.co/datasets/mteb/mrtidy), MTEB dataset card.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Mr. TyDi: A Multi-lingual Benchmark for Dense Retrieval | 2021 | paper | https://arxiv.org/abs/2108.08787 |
| castorini/mr-tydi |  | dataset card | https://huggingface.co/datasets/castorini/mr-tydi |
| mteb/mrtidy |  | dataset card | https://huggingface.co/datasets/mteb/mrtidy |

### Representative Snippets

| Query | Relevant document excerpt |
| --- | --- |
| พรรคแผ่นดินไทยมีใครป็นหัวหน้าพรรค? | A Thai passage about the Puea Pandin political party and its first party leader. |
| โค้ชเชคยเป็นโค้ชให้กับเทควันโดทีมชาติใดก่อนที่จะโค้ชให้ทีมไทย? | A Thai passage about Choi Young-seok and his earlier role coaching Bahrain's national taekwondo team. |
| ดร. ถวัลย์ ดัชนี เสียชีวิตเมื่อไหร่? | A Thai biographical passage giving Thawan Duchanee's birth and death dates. |
| เยื่อหุ้มสมองชั้นใน หมายถึงอะไร? | A Thai medical passage defining the pia mater as the delicate innermost meningeal layer. |
| ใครคือพระราชินีของอังกฤษในปี พ.ศ. 2550 ? | A Thai passage about Queen Elizabeth II and her role as monarch. |
