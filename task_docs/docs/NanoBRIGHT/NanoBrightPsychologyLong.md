# NanoBRIGHT / NanoBrightPsychologyLong

## Overview

NanoBrightPsychologyLong is the long-document Psychology StackExchange slice of NanoBRIGHT. Queries are detailed user posts about cognition, behavior, emotion, perception, or research terminology, while candidate documents are full cited pages or long source documents. The task measures whether a retriever can identify the source page that contains the psychological construct or evidence needed to answer the query, even when that evidence is only one section of a long article.

## Details

### What the Original Data Measures

BRIGHT's long-document StackExchange variants use complete source pages rather than short passages. For Psychology, that means a relevant document may be a long encyclopedia entry, popular psychology article, research-oriented page, or publisher page whose useful evidence is embedded among navigation text, examples, references, and adjacent concepts.

The task retains the core Psychology difficulty: users often describe an experience in everyday language, while the relevant source uses formal terms. The long-document version adds another layer because the correct source must be scored as relevant even if most of the page is not directly about the query.

### Observed Data Profile

The task contains 101 queries, 509 documents, and 116 relevance judgments. It is mostly single-positive: there are 1.15 positives per query on average, a minimum of 1, a median of 1.0, a maximum of 5, and 11 multi-positive queries, or 10.89% of the set.

Queries average 693.16 characters, matching the passage-level Psychology slice. Documents average 40,097.47 characters, so each candidate may contain multiple sections and substantial surrounding material. The small document count should not be mistaken for an easy task; document length creates heavy topical dilution.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.3010, hit@10 of 0.4554, and recall@100 of 0.7845 using the top-500 BM25 candidate subset. Lexical retrieval has good recall because long pages contain many terms, including formal construct names and related psychological vocabulary.

The top-rank quality remains limited. A long page can include many broadly relevant words without making the specific construct central. BM25 can find source pages that mention the right terms, but it often struggles to rank the exact supporting page high enough when the query uses lay phrasing or when the page contains broad psychology coverage.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.5069, hit@10 of 0.7426, and recall@100 of 0.8879. Dense retrieval is the strongest top-ranking profile in this task. It substantially improves over BM25 for nDCG@10 and hit@10.

This suggests that semantic matching is especially valuable for long psychology sources. The model can connect a user's scenario to a source page whose central topic or explanatory content aligns with the intended construct, even when exact wording differs. Dense retrieval is better at selecting the right page near the top.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.4149, hit@10 of 0.6337, and recall@100 of 0.9310. It uses a top-100 candidate range with an optional rank-101 safeguard; this task has 6 safeguard rows, candidate counts from 100 to 101, and a mean of 100.06 candidates.

The hybrid profile has the best recall@100 but does not beat dense retrieval at the top of the ranking. This means the combined sparse and dense pool is valuable for downstream reranking, while dense retrieval alone gives the strongest first-page ordering. The pattern separates candidate coverage from ranking quality.

### Metric Interpretation for Model Researchers

This task is a dense-favorable long-document benchmark with a hybrid recall advantage. BM25 retrieves many positives somewhere in the top 100 because long source pages contain useful terms. Dense retrieval ranks positives much better in the top 10. Reranking_hybrid gives the broadest positive coverage for reranker input.

Researchers should evaluate whether their models represent the specific psychological construct rather than only the page's broad topic. Long documents can obscure the small evidence-bearing span, so models that combine semantic document retrieval with section-level reranking may be especially effective.

### Query and Relevance Type Tendencies

Queries ask about phenomena such as normalization of extreme claims, flow, mental blocks, attention-seeking behavior, empathy gaps, perception, cognition, and social behavior. Relevant long documents may be encyclopedia pages, psychology articles, popular explanatory pages, or research-oriented resources.

The relevance relation is usually source-level support. A positive document contains the construct, example, or explanation needed for the answer, though the specific evidence may occupy only a small part of the page.

### Representative Failure Modes

Likely failures include ranking a long psychology page because it mentions related terms without supporting the specific phenomenon, missing the formal construct when the query is phrased as a personal scenario, over-weighting navigation or boilerplate, and confusing adjacent constructs such as flow, motivation, attention, and emotional state.

BM25 is exposed to long-page term dilution. Dense retrieval can still retrieve broadly similar but insufficient pages. Hybrid retrieval improves coverage but needs a reranker to recover dense-like top-rank precision.

### Training Data That May Help

Useful training data includes document-level psychology reference retrieval, cited-source retrieval from psychology forums, long-article QA with evidence grounding, and section-to-document supervision that maps answer-bearing spans back to full source pages.

Synthetic data should generate long psychology source pages with sections, definitions, examples, and research context, then write user-style questions about behavior, cognition, or measurement. Hard negatives should be long pages about adjacent constructs that are plausible but not the right explanation.

### Model Improvement Notes

Strong models should combine lay-language understanding with formal psychology terminology. Dense retrieval is the best observed first-stage ranker, so model training should emphasize scenario-to-construct mapping. Reranking_hybrid is useful when recall@100 matters, but the final ranking should inspect whether the relevant section actually supports the query.

Long-document systems may benefit from section-aware pooling, passage aggregation, or reranking over extracted evidence spans. The task is especially useful for testing whether full-page retrieval hides or preserves the evidence signal.

## Example Data

### Public Sources

The original task is based on BRIGHT's reasoning-intensive retrieval benchmark, with NanoBRIGHT providing the compact dataset packaging and long-document split.

### Source Reference Table

| Item | Reference |
| --- | --- |
| Original benchmark paper | [BRIGHT](https://arxiv.org/abs/2407.12883) |
| Project page | [BRIGHT project page](https://brightbenchmark.github.io/) |
| Source dataset | [xlangai/BRIGHT](https://huggingface.co/datasets/xlangai/BRIGHT) |
| NanoBRIGHT dataset | [hakari-bench/NanoBRIGHT](https://huggingface.co/datasets/hakari-bench/NanoBRIGHT) |

Representative query and positive source snippets:

| Query | Positive document snippet |
| --- | --- |
| What is it called when extreme claims make extreme views seem normal? | A long article discusses how repeated extreme statements can alter perceived normality. |
| What term describes work that seems to do itself despite effort? | A long reference page contains a section on flow and challenges to maintaining it. |
| What is the term for knowing what you mean but being unable to explain it? | A long mental-block page discusses difficulty expressing or accessing thought. |
| Why would someone say shocking things to enjoy others' reactions? | A psychology article discusses excessive attention-seeking behavior. |
| What term describes being unable to see beyond one's current emotional state? | A long reference page explains the hot-cold empathy gap. |
