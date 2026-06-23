# NanoRTEB / NanoWikiSQL

## Overview

`NanoWikiSQL` is an English text-to-SQL retrieval task from NanoRTEB. The query contains a natural-language question plus Wikipedia table metadata and rows, and the relevant document is the corresponding SQL `SELECT` statement. Each query has one positive SQL document among 2,022 candidates. Dense retrieval is extremely strong for top-rank quality, `reranking_hybrid` reaches full recall@100, and BM25 is competitive but much weaker because many SQL candidates share column and predicate tokens.

## Details

### What the Original Data Measures

WikiSQL was introduced with Seq2SQL as a large natural-language-to-SQL benchmark over Wikipedia tables. The original task maps a question and table schema to an executable SQL query.

RTEB converts this into retrieval. The model receives the question plus table context and must retrieve the correct SQL statement from a candidate corpus. This tests schema-aware semantic matching rather than SQL generation.

### Observed Data Profile

The Nano split contains 200 queries, 2,022 documents, and 200 positive qrel rows. Every query has exactly one positive. Queries average 1,551.46 characters because they include headers, table metadata, and row content. SQL documents are short, averaging 62.34 characters.

Example questions ask for an election result for Lindsey Graham, a total win-loss value for a tennis player, a race date for Misano, a week 7 record, and an original air date for an episode title.

### BM25 Evaluation Profile

The BM25 candidate subset uses top-500 candidates and reaches nDCG@10 of 0.4898, hit@10 of 0.7300, and recall@100 of 0.9450. BM25 benefits from exact column names, entity values, and SQL tokens that overlap with the table context.

The limitation is ambiguity. Many candidate SQL strings share common clauses such as `SELECT`, `FROM table`, column names, or similar predicate values. Long table context can also dilute the few terms that identify the exact query.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses top-500 candidates and reaches nDCG@10 of 0.9507, hit@10 of 0.9750, and recall@100 of 0.9750. Dense retrieval is the strongest top-rank profile by a large margin.

This indicates that embedding similarity can connect the natural-language question, table schema, and intended SQL structure. It is especially effective for selecting the right column and predicate relation from the context.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates and does not need the rank-101 safeguard. It reaches nDCG@10 of 0.7763, hit@10 of 0.9400, and recall@100 of 1.0000. Hybrid retrieval has perfect recall@100 but lower early rank quality than dense retrieval.

The pattern is useful for reranking. Dense retrieval is better as a direct ranker, while hybrid retrieval provides a complete high-recall candidate pool where exact schema tokens and semantic matching are combined.

### Metric Interpretation for Model Researchers

With one positive per query, nDCG@10 measures how early the exact SQL statement appears, hit@10 measures whether it appears in the first ten candidates, and recall@100 measures reranker availability.

For `NanoWikiSQL`, dense nDCG@10 is the main first-stage quality signal. Hybrid recall@100 is valuable when a second-stage model can inspect SQL structure and table grounding.

### Query and Relevance Type Tendencies

Queries combine a natural-language question with table headers, page metadata, types, and rows. Relevant documents are short SQL `SELECT` statements with a selected column and a condition.

Relevance is exact SQL correspondence. A candidate with the right table but wrong selected column, predicate value, or aggregation is not relevant.

### Representative Failure Modes

Common failures include selecting the wrong column, confusing similar cell values, retrieving a SQL query for another row in the same table, and overmatching common SQL syntax. BM25 is vulnerable to shared schema tokens; dense retrieval can still confuse close table entities.

### Training Data That May Help

Useful training data includes text-to-SQL pairs, schema-aware query retrieval, table QA retrieval, and hard negatives from the same table with different columns or predicates. Evaluation questions, SQL statements, and qrels should be excluded.

### Model Improvement Notes

Models should encode the relation between question wording, schema columns, row values, and SQL structure. Hard negatives should use the same table and near-identical SQL with one changed selected column or condition. Dense retrieval is the best direct ranker, while hybrid retrieval is useful for recall-oriented reranking.

## Example Data

| Query | Positive document |
| --- | --- |
| tell the final for lindsey graham {'header': ['State (linked to summaries below)', 'Senator', 'Party', 'Electoral history', 'Result', 'Candidates Winning candidate in bold'], 'page_title': '', 'page_id': '', 'types': ['text', 'text', 'text', 'text', 'text', 'text'], 'id': '1-1133844-4', 'section_title': '', 'caption': '', 'rows': [['Arkansas', 'Mark Pryor', 'Democratic', '2002', 'Incumbent re-elected', 'Mark Pryor (D) 79.5% Rebekah Kennedy (G) 20.5%'], ['Delaware', 'Joe Biden', 'Democratic', '19... [500 / 2,038 chars] | SELECT Result FROM table WHERE Senator = Lindsey Graham [55 chars] |
| what's the total w–l where player is boro jovanović category:articles with hcards {'header': ['Player', 'Total W–L', 'Singles W–L', 'Doubles W–L', 'Ties played', 'Debut', 'Years played'], 'page_title': 'Yugoslavia Davis Cup team', 'page_id': '', 'types': ['text', 'text', 'text', 'text', 'real', 'real', 'real'], 'id': '1-10294071-1', 'section_title': 'Players', 'caption': 'Players', 'rows': [['Željko Franulović Category:Articles with hCards', '32–27', '23–15', '9–12', '22', '1967', '12'], ['Boro... [500 / 1,190 chars] | SELECT Total W–L FROM table WHERE Player = Boro Jovanović Category:Articles with hCards [87 chars] |
| What was the date of the race in Misano? {'header': ['No', 'Date', 'Round', 'Circuit', 'Pole Position', 'Fastest Lap', 'Race winner', 'Report'], 'page_title': '2007 Supersport World Championship season', 'page_id': '', 'types': ['real', 'text', 'text', 'text', 'text', 'text', 'text', 'text'], 'id': '1-10083598-1', 'section_title': 'Season calendar', 'caption': 'Season calendar', 'rows': [['1', '24 February', 'Qatar', 'Losail', 'Kevin Curtain', 'Sébastien Charpentier', 'Kenan Sofuoğlu', 'Report']... [500 / 1,742 chars] | SELECT Date FROM table WHERE Circuit = Misano [45 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Seq2SQL: Generating Structured Queries from Natural Language using Reinforcement Learning | 2017 | task paper | [https://arxiv.org/abs/1709.00103](https://arxiv.org/abs/1709.00103) |
| Salesforce/wikisql |  | dataset card | [https://huggingface.co/datasets/Salesforce/wikisql](https://huggingface.co/datasets/Salesforce/wikisql) |
| Introducing RTEB: A New Standard for Retrieval Evaluation | 2025 | benchmark article | [https://huggingface.co/blog/rteb](https://huggingface.co/blog/rteb) |

### Representative Snippets

| Query | Relevant document excerpt |
| --- | --- |
| Tell the final result for Lindsey Graham in an election-results table. | `SELECT Result FROM table WHERE Senator = Lindsey Graham` |
| What is the total win-loss record where the player is Boro Jovanovic? | `SELECT Total W-L FROM table WHERE Player = Boro Jovanovic` |
| What was the date of the race in Misano? | `SELECT Date FROM table WHERE Circuit = Misano` |
| What was the record at week 7? | `SELECT Record FROM table WHERE Week = 7` |
| What is the original air date for the title "Hell"? | `SELECT Original air date FROM table WHERE Title = "Hell"` |
