# NanoVNMTEB / cqadupstack_webmasters_vn

## Overview

`cqadupstack_webmasters_vn` is the Vietnamese NanoVNMTEB version of the CQADupStack Webmasters duplicate-question retrieval task. The original CQADupStack benchmark evaluates retrieval of manually flagged duplicate StackExchange questions; this split adapts website administration, SEO, hosting, analytics, advertising, and CMS-related questions into Vietnamese. A query is a short translated webmaster title, and relevant documents are longer archived threads asking the same site-operation need.

The Nano split contains 200 queries, 10,000 candidate documents, and 825 positive qrels. Queries average 58.005 characters, while documents average 731.448 characters. The task has large duplicate clusters, with some queries reaching 100 positives. Dense retrieval is strongest on all three reported metrics, while `reranking_hybrid` is between BM25 and dense. This is an important contrast with other CQADupStack subsets: broad semantic intent around website administration appears more useful than lexical matching over common platform and SEO terms.

## Details

### What the Original Data Measures

CQADupStack measures whether a system can retrieve earlier questions that answer the same community Q&A need. For Webmasters, duplicates often involve search-engine behavior, Google snippets and sitelinks, URL structure, hidden text, analytics, localization, advertising alternatives, CMS selection, hosting, redirects, and domain configuration.

The Vietnamese version translates the prose while retaining product names, domains, HTML terms, SEO vocabulary, CMS names, and advertising brands. Relevance is duplicate-level rather than topic-level. A document about Google is not automatically relevant to a Google query; it must address the same search-result, analytics, indexing, or site-configuration problem.

### Observed Data Profile

There are 825 positive qrels across 200 queries, averaging 4.125 positives per query. The median is 1, but 73 queries have multiple positives, for a 36.5% multi-positive rate. The maximum positive count is 100, showing that some webmaster problems recur in many near-duplicate forms.

Documents are shorter on average than many other CQADupStack Vietnamese subsets, but the relevance clusters can be large. A short query may represent a common SEO or administration issue with many previous discussions. The challenge is not simply finding a related page; it is selecting threads that match the same operational goal or policy question.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.2516535279, hit@10 of 0.4300, and recall@100 of 0.3769696970 with a top-500 candidate set. These are relatively low scores for the Vietnamese CQADupStack group. The weakness is understandable: terms such as Google, SEO, CMS, AdSense, analytics, forum, keywords, URL, and domain occur across many related but non-duplicate webmaster questions.

BM25 can still help when exact brands, HTML terms, or URL patterns are decisive. However, generic web vocabulary creates many false positives. A query about hidden text for SEO, Google Sitelinks, AdSense alternatives, or localized search crawling often needs policy or intent matching rather than just shared terms.

### Dense Evaluation Profile

Dense retrieval with `harrier-oss-270m` is strongest: nDCG@10 is 0.3498185758, hit@10 is 0.5450, and recall@100 is 0.5224242424. The gain over BM25 is large, especially at top ranks. This indicates that embeddings capture webmaster intent more effectively than raw term overlap.

Dense retrieval helps because the same site-operation need can be expressed with different wording. A question about helping Google build SiteLinks may match a document about encouraging Sitelinks. A query about localized crawler views may match a broader multilingual SEO discussion. Dense similarity is better suited to these paraphrased administrative intents. The remaining risk is over-grouping broadly related SEO or hosting topics that do not solve the same problem.

### Reranking Hybrid Evaluation Profile

`reranking_hybrid` reaches nDCG@10 of 0.3235792203, hit@10 of 0.5150, and recall@100 of 0.5030303030. The top-100 reranking pool has mean candidate count 100.2, with 40 safeguard-positive rows and 40 rows containing 101 candidates. Hybrid retrieval is clearly better than BM25 but below dense on all three metrics.

This pattern shows that hybrid search is not always the best final condition. Sparse signals add some useful brand and vocabulary evidence, but they also bring in many same-brand or same-topic distractors. In this task, the dense ranking better preserves the administrative intent. Hybrid candidate generation remains useful, but the fusion or reranking strategy needs to avoid overweighting generic webmaster terms.

### Metric Interpretation for Model Researchers

The metric ordering is simple and useful: dense retrieval is best, `reranking_hybrid` is second, and BM25 is weakest. This suggests a domain where exact token overlap is less reliable because important terms are reused across many distinct webmaster problems. A model optimized for this task should prioritize semantic intent while using lexical evidence only for precise identifiers such as domains, products, HTML tags, or ad platforms.

The high positive count and maximum cluster size make recall@100 important. Some queries correspond to large sets of duplicate discussions. However, because the median positive count is still 1, top-rank precision remains necessary. Researchers should distinguish between finding any SEO-related thread and ranking the exact duplicate cluster near the top.

### Query and Relevance Type Tendencies

Queries include URL query strings and SEO, hidden text, Google Sitelinks, Google Analytics concurrent-user measurement, localized crawler views, CMS selection, forum software, advertising alternatives, and domain or redirect operations. Relevant documents often contain practical site-management constraints or search-engine policy framing.

The relevance relation is practical-intent matching. A document about Google Analytics is relevant only if it asks the same measurement problem. A document about multilingual sites is relevant only if it addresses the same crawler or localization issue. The task therefore tests whether a model understands website-administration goals rather than only web vocabulary.

### Representative Failure Modes

BM25 can over-rank documents with the same brand or SEO term but a different goal. Dense retrieval can over-rank broadly related site-operation questions, especially when several SEO concepts appear together. Hybrid retrieval can inherit both problems if it gives too much weight to common platform tokens.

Another failure mode is confusing policy questions with implementation questions. Hidden text, sitelinks, AdSense alternatives, redirects, and localized crawling each involve both practical setup and search-engine policy. A model must match the same kind of need, not just the same named service.

### Training Data That May Help

Useful training data includes non-overlapping Webmasters StackExchange duplicate pairs, Vietnamese website-administration Q&A, SEO documentation retrieval, hosting and CMS support threads, and translated CQADupStack training data with overlap removed. Hard negatives should share brands or platforms while changing the administrative goal.

Synthetic data can create Vietnamese titles from longer webmaster support threads. It should preserve product names, domains, HTML tags, CMS names, analytics vocabulary, and search-engine policy terms. Strong synthetic hard negatives would reuse Google, CMS, AdSense, or SEO terms while asking different site-management questions.

### Model Improvement Notes

The main improvement direction is dense semantic retrieval with careful hard-negative training. The model should learn webmaster intent categories: indexing, snippets, analytics, advertising, hosting, redirects, localization, and CMS selection. Sparse signals should be used as disambiguating evidence, not as dominant ranking features.

Error analysis should check whether false positives are same-brand, same-policy, or same-operation errors. If the model retrieves many same-brand non-duplicates, add hard negatives by brand and product. If it misses paraphrased administrative needs, add multilingual webmaster paraphrase and duplicate-pair data.

## Example Data

### Public Sources

- [CQADupStack paper](https://doi.org/10.1145/2838931.2838934)
- [VN-MTEB paper](https://aclanthology.org/2026.findings-eacl.86/)
- [BEIR paper](https://arxiv.org/abs/2104.08663)
- [GreenNode/cqadupstack-webmasters-vn](https://huggingface.co/datasets/GreenNode/cqadupstack-webmasters-vn)

### Source Reference Table

| Source | Role |
|---|---|
| CQADupStack | Original duplicate-question retrieval benchmark |
| BEIR | Common retrieval-evaluation framing for CQADupStack |
| VN-MTEB | Vietnamese benchmark collection using translated retrieval tasks |
| GreenNode dataset card | Public dataset entry for this Vietnamese Webmasters subset |

### Representative Snippets

- Query: `find-new/posts&recent=1 làm trang chủ: còn SEO thì sao?`
  Relevant documents discuss whether URL query strings are better or worse for SEO than cleaner URLs.
- Query: `Đặt các từ khóa liên quan trong một phần tử div ẩn có phải là một thói quen tốt để thực hiện SEO không?`
  Relevant documents discuss hidden text and search-engine ranking behavior.
- Query: `Tôi có thể giúp Google xây dựng SiteLinks như thế nào?`
  Relevant documents ask what actions encourage Google Sitelinks.
- Query: `google analytics - tính toán người dùng đồng thời cao nhất cho một giờ nhất định`
  Relevant documents ask how to measure peak simultaneous visitors using Google Analytics.
- Query: `Làm thế nào để tôi có thể khiến các công cụ tìm kiếm thu thập dữ liệu trên trang web của tôi và xem một bản địa hóa quan điểm của dữ liệu của tôi?`
  Relevant documents discuss multilingual or localized site crawling by search engines.
