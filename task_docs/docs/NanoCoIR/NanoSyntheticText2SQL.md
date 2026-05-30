# NanoCoIR / NanoSyntheticText2SQL

## Overview

NanoSyntheticText2SQL is an English text-to-code retrieval task in NanoCoIR. It is adapted by CoIR from Gretel's synthetic Text-to-SQL dataset. The query is a natural-language analytics or database-management request, and the target document is the SQL statement that answers it.

The task evaluates whether a model can align business-style prompts with SQL semantics. The relevant SQL may contain joins, aggregations, filters, window functions, grouping, inserts, deletes, or updates. Matching table words alone is not enough: the model must recognize which SQL operation answers the requested question.

## Details

### What the Original Data Measures

CoIR adapts Gretel's synthetic Text-to-SQL data into retrieval by using the natural-language prompt as the query and the SQL query as the document. The source dataset includes domains, schema context, SQL complexity labels, prompts, SQL, and explanations.

The original task measures natural-language-to-SQL alignment. In retrieval form, the positive SQL must answer the prompt, not merely mention a related table or column. This makes the benchmark sensitive to schema linking, operation selection, and analytical intent.

### Observed Data Profile

This Nano split contains 200 queries, 10,000 documents, and 200 positive qrels. Each query has exactly one positive SQL document. Queries average 102.94 characters, and documents average 130.60 characters. Both sides are relatively short, but they express different representations of the same database task.

Observed prompts ask about permit costs, government aid totals, tree-species differences, female mayor tenure, and product ingredients with safety violations. SQL documents include joins, grouping, aggregate functions, filters, window operations, and nested subqueries.

### BM25 Evaluation Profile

BM25 performs poorly relative to dense retrieval. It reaches nDCG@10 of 0.2240, hit@10 of 0.3100, and recall@100 of 0.6900 with a top-500 candidate pool. Lexical matching helps when prompt words resemble table or column names, but many SQL statements use compact identifiers, aliases, and schema-specific terms that do not directly match the natural-language phrasing.

This task exposes the limits of term frequency for text-to-SQL retrieval. A prompt may ask for "the difference in average permit cost" while the SQL uses `AVG`, `LAG`, `PARTITION BY`, aliases, and table-specific column names. BM25 can retrieve statements from the same domain but miss the exact analytical operation.

### Dense Evaluation Profile

The dense harrier-oss-270m profile is extremely strong, with nDCG@10 of 0.9567, hit@10 of 0.9800, and recall@100 of 0.9800. Dense retrieval clearly captures the semantic relation between prompt intent and SQL structure better than lexical retrieval.

Dense similarity can connect natural-language requests for totals, averages, longest periods, differences, and filtered entities to SQL constructs such as `SUM`, `AVG`, `GROUP BY`, `HAVING`, joins, and subqueries. The few remaining errors likely involve prompts from the same domain with similar table names or SQL statements that answer closely related but different questions.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate subset reaches nDCG@10 of 0.5577, hit@10 of 0.7350, and recall@100 of 0.9850. It uses top-100 candidates with optional rank-101 safeguards; three rows contain 101 candidates and three safeguard-positive rows are recorded. Hybrid retrieval has slightly higher recall@100 than dense but much lower nDCG@10.

This pattern shows that lexical evidence can broaden coverage, but it can also harm top ranking by introducing SQL statements from the same domain or schema that do not answer the prompt. Dense retrieval is the preferred top-rank candidate source, while hybrid candidates may be useful when a downstream reranker can reason about SQL semantics.

### Metric Interpretation for Model Researchers

NanoSyntheticText2SQL is a dense-dominant text-to-SQL retrieval task. The very large gap between dense and BM25 indicates that the important signal is semantic operation matching, not simple word overlap. Reranking_hybrid recovers slightly more positives by rank 100, but dense retrieval places positives much better in the top 10.

For researchers, this split is a good diagnostic for schema-aware semantic retrieval. A model should map "which cities have had a female mayor for the longest continuous period" to the SQL pattern involving mayor tenure, gender filtering, grouping, and maximum duration. Exact table words help, but operation-level understanding is decisive.

### Query and Relevance Type Tendencies

Queries are natural-language analytics or database prompts. They often mention entities, conditions, time windows, comparisons, totals, averages, or superlatives. Documents are SQL statements with table names, column names, joins, aggregates, filters, and sometimes nested logic.

Relevance requires query-answer equivalence. A SQL statement is positive only if it answers the prompt. Statements from the same domain or schema are non-relevant if they compute a different aggregate, filter, time range, or entity relationship.

### Representative Failure Modes

BM25 often retrieves SQL that shares table names or domain terms but performs a different operation. Dense retrieval can fail when multiple prompts share the same schema and differ only by aggregation target, comparison direction, or time condition.

Hybrid retrieval may include the correct SQL in the candidate pool but rank a schema-similar distractor higher. This is especially likely when many SQL statements reuse the same table and column identifiers.

### Training Data That May Help

Useful training data includes text-to-SQL prompt and query pairs, schema-linking retrieval data, and domain-sharing SQL hard negatives. Synthetic examples should include varied domains, SQL task types, and complexity levels, with hard negatives that use the same tables but answer a different analytical question.

Leakage filtering is required. The Nano split is derived from CoIR Synthetic Text-to-SQL test-side data. Training should exclude NanoSyntheticText2SQL prompt-SQL pairs and should not train on Gretel or CoIR Text-to-SQL test-derived rows. Filters should cover normalized prompt text, SQL text, schema context, and token fingerprints.

### Model Improvement Notes

Improving this task requires semantic parsing-like retrieval behavior. Models should represent SQL operations, aggregation intent, join structure, filters, and schema links in a way that aligns with natural-language requests.

For reranking, the most useful capability is to compare whether a SQL statement actually answers the prompt. This requires more than domain similarity: the ranker should inspect operation type, grouping keys, conditions, and selected outputs.

## Example Data

### Public Sources

NanoSyntheticText2SQL is documented through CoIR and the Gretel synthetic Text-to-SQL dataset card. The source dataset card is the public reference for the synthetic prompt-SQL data.

### Source Reference Table

| Source | Role |
| --- | --- |
| [CoIR: A Comprehensive Benchmark for Code Information Retrieval Models](https://arxiv.org/abs/2407.02883) | Benchmark paper defining the retrieval adaptation. |
| [gretelai/synthetic_text_to_sql](https://huggingface.co/datasets/gretelai/synthetic_text_to_sql) | Public source dataset card for synthetic Text-to-SQL data. |
| [hakari-bench/NanoCoIR](https://huggingface.co/datasets/hakari-bench/NanoCoIR) | Nano benchmark dataset containing this split. |

### Representative Snippets

| Query Pattern | Positive Document Pattern |
| --- | --- |
| Asks for the difference in average permit cost between high-rise and low-rise buildings in a province and year. | SQL computes an average-cost comparison with filters on province, year, and building type. |
| Asks for government aid totals and average project durations for community development. | SQL joins project and government tables, sums aid, and averages date differences. |
| Asks for the difference between tree species with highest and lowest carbon sequestration rates. | SQL compares maximum and minimum species-level sequestration values. |
| Asks which cities had a female mayor for the longest continuous period. | SQL filters mayor records by gender, groups by city, and ranks or compares tenure duration. |
| Asks which ingredients appear in unsafe products that are not cruelty-free certified. | SQL joins ingredient, product, and safety records with violation and certification filters. |
