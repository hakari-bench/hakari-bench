# NanoVNMTEB / cqadupstack_wordpress_vn

## Overview

`cqadupstack_wordpress_vn` is the Vietnamese NanoVNMTEB version of the CQADupStack WordPress duplicate-question retrieval task. The original CQADupStack benchmark uses manually flagged StackExchange duplicate links; this split adapts WordPress support questions into Vietnamese while preserving PHP identifiers, hook names, theme filenames, plugin names, error messages, and version-specific details. A short translated query must retrieve a longer support thread asking the same WordPress behavior or troubleshooting problem.

The Nano split contains 200 queries, 10,000 candidate documents, and 337 positive qrels. Queries average 52.37 characters, while documents average 1,028.8101 characters. The task mixes natural-language support questions with code-like WordPress evidence: template routing, custom post types, RSS feeds, Walker classes, image thumbnails, plugin metaboxes, and PHP snippets. `reranking_hybrid` is strongest overall, while BM25 is slightly ahead of dense on nDCG@10 and dense is much stronger on recall@100. This makes the task a clear hybrid-search case.

## Details

### What the Original Data Measures

CQADupStack measures duplicate-question retrieval in community Q&A. In the WordPress subset, relevance often depends on matching the same theme, plugin, hook, template, query, feed, or administration behavior. A relevant document may ask the same custom post type routing problem, the same RSS title customization issue, the same image-thumbnail behavior, or the same Walker function error, even when the wording differs.

The Vietnamese version translates explanatory prose but keeps many implementation tokens intact. This creates a mixed retrieval setting: exact PHP and WordPress identifiers matter, but duplicate status depends on the behavior being requested. A document sharing `wp_query`, Yoast SEO, or a template filename is not necessarily relevant unless it asks the same implementation problem.

### Observed Data Profile

The task has 337 positives across 200 queries, averaging 1.685 positives per query. The median is 1, and only 43 queries have multiple positives, for a multi-positive rate of 21.5%. The maximum positive cluster has 62 documents, so most queries are precise single-target searches, but a few common WordPress issues have large duplicate clusters.

Documents are long relative to queries and often include code snippets, function signatures, theme context, plugin configuration, and routing details. The short query may name only a symptom or desired behavior, while the document explains the implementation environment. This makes the task sensitive to both exact identifiers and deeper WordPress intent.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.3214165823, hit@10 of 0.4750, and recall@100 of 0.5103857567 with a top-500 candidate set. It benefits from exact identifiers such as `start_el`, `wp_query`, template filenames, RSS, Yoast SEO, Walker, hook names, and PHP fragments. When the duplicate repeats the same function or plugin name, sparse retrieval is a strong signal.

The limitation is that WordPress problems often involve behavior rather than one exact token. Template routing, custom post type archives, feed title customization, or metabox visibility may be described through different files or hooks. BM25 can also over-rank same-plugin or same-function negatives that do not solve the same issue. Its nDCG edge over dense shows lexical precision matters, but its lower recall shows that exact overlap is not enough.

### Dense Evaluation Profile

Dense retrieval with `harrier-oss-270m` reaches nDCG@10 of 0.3104801121, hit@10 of 0.4800, and recall@100 of 0.6261127596. It is slightly below BM25 on nDCG@10 but higher on hit@10 and much stronger on recall@100. Dense retrieval therefore finds more relevant WordPress duplicates in the candidate pool but does not always order the exact duplicate above lexical near matches at the top.

This pattern fits the domain. Embeddings can connect paraphrased support questions about the same behavior, such as shared users across installations, disabling generated thumbnails, or default customizer images. But dense similarity can blur distinct implementation details, especially when several posts mention the same plugin, template, or hook family.

### Reranking Hybrid Evaluation Profile

`reranking_hybrid` is the strongest condition: nDCG@10 is 0.3671681835, hit@10 is 0.5450, and recall@100 is 0.6528189911. The top-100 reranking pool has mean candidate count 100.21, with 42 safeguard-positive rows and 42 rows containing 101 candidates. The hybrid condition improves both top-rank quality and recall over BM25 and dense.

The result shows why WordPress support retrieval benefits from evidence fusion. BM25 protects exact implementation tokens; dense retrieval broadens recall over paraphrased behavior. Hybrid reranking can keep a same-hook candidate when the function name is crucial while also recovering documents that describe the same behavior with different WordPress terminology. This task is a good example where neither single channel is sufficient.

### Metric Interpretation for Model Researchers

The ranking relationship is nuanced. BM25 has better nDCG@10 than dense, dense has much better recall@100, and `reranking_hybrid` is best across all metrics. A model that uses only embeddings may retrieve the right neighborhood but miss exact WordPress constraints. A model that uses only lexical matching may rank precise-looking but behaviorally different implementation questions.

The low multi-positive rate means nDCG@10 is particularly important. Many queries have one main duplicate, so the model must rank the correct thread early. The large maximum cluster still makes recall relevant for recurring WordPress issues. Researchers should analyze both single-target template problems and large clusters around common plugin or theme behaviors.

### Query and Relevance Type Tendencies

Queries include shared members across WordPress installations, combining `wp_query` arguments, Walker function behavior, disabling generated thumbnails, and default images in the customizer. Relevant documents often contain PHP snippets, database or multisite context, template filenames, hook behavior, plugin settings, or admin UI details.

The relevance relation is implementation-intent matching. A document mentioning WordPress users is relevant only if it asks the same cross-installation sharing problem. A document using `wp_query` is relevant only if it addresses the same query-combination or pagination behavior. This makes the task useful for testing retrieval over framework-specific support knowledge.

### Representative Failure Modes

BM25 can over-rank posts that share a hook, plugin, or template filename but ask a different implementation question. Dense retrieval can over-rank broadly similar WordPress support issues while missing exact constraints such as custom post type routing, archive behavior, or plugin metabox visibility.

Another failure mode is losing version or file-specific detail. In WordPress, the difference between a theme template, plugin hook, admin setting, and generated file can determine relevance. Models that flatten all WordPress terms into one semantic area will retrieve plausible but non-duplicate support threads.

### Training Data That May Help

Useful training data includes non-overlapping WordPress StackExchange duplicate pairs, Vietnamese WordPress support Q&A, WordPress documentation retrieval pairs, and translated CQADupStack training splits with overlap removed. Training data should preserve PHP identifiers, hook names, template filenames, plugin names, and version details exactly.

Synthetic data can create Vietnamese short titles from longer WordPress troubleshooting threads. Hard negatives should share a plugin, hook, template, or feature while changing the behavior, such as same custom post type topic but different routing issue, or same SEO plugin but different admin-screen question.

### Model Improvement Notes

The main improvement direction is hybrid retrieval with a WordPress-aware reranker. Sparse retrieval should preserve implementation tokens, while dense retrieval should connect paraphrased support intent. A reranker should learn WordPress-specific distinctions among hooks, templates, plugins, custom post types, archives, feeds, and admin settings.

Error analysis should group failures by implementation area: template routing, query construction, media handling, hooks and Walker classes, plugin configuration, multisite or shared users, and feeds. Same-token hard negatives are especially important because many false positives share the same WordPress vocabulary without solving the same problem.

## Example Data

### Public Sources

- [CQADupStack paper](https://doi.org/10.1145/2838931.2838934)
- [VN-MTEB paper](https://aclanthology.org/2026.findings-eacl.86/)
- [BEIR paper](https://arxiv.org/abs/2104.08663)
- [GreenNode/cqadupstack-wordpress-vn](https://huggingface.co/datasets/GreenNode/cqadupstack-wordpress-vn)

### Source Reference Table

| Source | Role |
|---|---|
| CQADupStack | Original duplicate-question retrieval benchmark |
| BEIR | Common retrieval-evaluation framing for CQADupStack |
| VN-MTEB | Vietnamese benchmark collection using translated retrieval tasks |
| GreenNode dataset card | Public dataset entry for this Vietnamese WordPress subset |

### Representative Snippets

- Query: `Các thành viên chia sẻ giữa hai cài đặt khác nhau với các cơ sở dữ liệu khác nhau wordpress`
  Relevant documents ask how to share users or database tables across separate WordPress installations.
- Query: `gán 2 $args cho một wp_query`
  Relevant documents discuss combining `wp_query` arguments or merged queries with pagination.
- Query: `Giúp với chức năng Walker trong Wordpress`
  Relevant documents concern Walker classes and detecting child navigation items.
- Query: `Cách vô hiệu hóa WordPress từ tạo ra hình thu nhỏ?`
  Relevant documents ask how to stop WordPress from generating image thumbnails.
- Query: `Hình ảnh mặc định (logo) cho tùy chỉnh`
  Relevant documents discuss default image values in the WordPress customizer.
