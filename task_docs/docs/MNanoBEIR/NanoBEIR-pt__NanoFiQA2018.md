# MNanoBEIR / NanoBEIR-pt / NanoFiQA2018

## Overview

NanoBEIR-pt NanoFiQA2018 is a Portuguese financial question-answer retrieval
task derived from FiQA. Queries are translated personal-finance and investing
questions, and documents are translated answer passages from financial forum
data. The task is useful for evaluating answer-aware retrieval in a domain
where terms such as tax, return, volume, credit card, or freelancer can appear
in many passages while only some passages answer the specific decision problem.
It is a compact multilingual benchmark for finance-domain semantics and
question-to-answer matching.

## Details

### What the Original Data Measures

FiQA was introduced for financial opinion mining and question answering. In
BEIR, the retrieval version asks systems to rank answer-bearing financial
forum passages for a user question. The MNanoBEIR Portuguese version keeps
that structure after translation. It measures whether a retriever can connect
a concise Portuguese finance question to the passage that addresses the same
financial concept, action, product, or tax situation, rather than merely
sharing general finance vocabulary.

### Observed Data Profile

This Nano subset contains 50 queries, 4,598 documents, and 123 positive qrels.
More than half of the queries have multiple positives. The average is 2.46
positives per query, with a minimum of 1, median of 2.00, and maximum of 15.
There are 28 multi-positive queries, covering 56.0% of the task. Queries
average 71.92 characters, while documents average 972.51 characters. This
short-question to longer-answer structure makes the task sensitive to answer
utility and domain-specific interpretation.

### BM25 Evaluation Profile

BM25 uses the `bm25` top-500 candidate subset. It reaches nDCG@10 0.2621,
hit@10 0.4600, and recall@100 0.5528. Lexical matching finds some relevant
answers when the same product, tax term, or financial phrase appears in both
query and document. However, many relevant answers explain the issue using
different wording or include jurisdictional and procedural context that is not
present in the short question. BM25 also over-ranks same-topic passages that
mention the right financial terms while answering a different decision
problem. It is therefore useful but limited as a first-stage retriever.

### Dense Evaluation Profile

Dense retrieval uses the `harrier_oss_v1_270m` top-500 candidate subset. It
scores nDCG@10 0.3853, hit@10 0.6000, and recall@100 0.7073, substantially
outperforming BM25. This shows that embedding similarity is better at mapping
Portuguese finance questions to answer passages that resolve the underlying
intent. Dense retrieval helps when a question asks about tax implications,
investment returns, or trading volume and the answer explains the concept
rather than repeating the query. The remaining gap reflects financial
ambiguity, jurisdictional differences, and same-domain advice that is related
but not truly responsive.

### Reranking Hybrid Evaluation Profile

The reranking hybrid subset uses `reranking_hybrid` with top-100 candidates and
an optional rank-101 safeguard. Candidate counts range from 100 to 101, with a
mean of 100.14 and 7 safeguard rows. It reaches nDCG@10 0.3478, hit@10 0.6000,
and recall@100 0.7561. The hybrid profile has the best recall@100 and matches
dense hit@10, while dense has better top-10 ordering. This means hybrid search
is valuable for collecting more potentially relevant answers, especially when
rare financial terms matter, but the initial hybrid order needs a stronger
answer-aware reranker to beat dense early ranking.

### Metric Interpretation for Model Researchers

Because many queries have more than one acceptable answer, recall@100 is an
answer-coverage signal, while hit@10 only confirms that at least one answer
appears early. nDCG@10 is the key indicator of first-page quality. The results
show a clear pattern: BM25 is weak for finance QA, dense retrieval is the best
single ranking profile, and reranking hybrid gives the broadest candidate
coverage. Researchers should use this task to test whether a model can match
financial question intent rather than simply retrieve passages with shared
domain terms.

### Query and Relevance Type Tendencies

Queries ask practical questions about returns, taxes, trading volume, credit
card points, and self-employment. Relevant documents are forum-style answers
that may contain definitions, examples, caveats, or procedural guidance. A
passage is relevant when it answers the decision problem, not just when it
mentions the same financial product. The task favors models that can represent
intent, conditions, and answer utility in finance language.

### Representative Failure Modes

BM25 may retrieve passages that share terms such as "imposto", "volume", or
"cartão de crédito" but address another situation. Dense models may retrieve
general finance advice that is semantically nearby but not specific enough for
the query. Hybrid retrieval improves coverage but can mix exact-term and
semantic distractors. Translation can also make financial terminology less
consistent across questions and answers, especially for tax or accounting
concepts.

### Training Data That May Help

Helpful training data includes non-overlapping financial QA, personal-finance
forum retrieval, Portuguese finance questions, investing and tax answer
ranking, and multilingual domain-specific retrieval. Hard negatives should use
the same financial product or tax vocabulary while answering a different
decision problem. Training should exclude FiQA, BEIR, NanoBEIR, and translated
evaluation answers.

### Model Improvement Notes

NanoFiQA2018-pt is a useful test of domain-specific answer retrieval. Dense
retrieval is strongest for ranking, but reranking hybrid provides better
coverage and should be a strong reranker input. Improvements should focus on
finance-domain embedding quality, jurisdiction and condition sensitivity, and
rerankers that compare a question with the actual answer content. A practical
system would use hybrid candidates for recall and an answer-aware model for
final ranking.

## Example Data

| Query | Positive document |
| --- | --- |
| Que tipos de rentabilidade a Vanguard está oferecendo? | Da página da Vanguard - Esta pareceu a mais fácil, pois os dados da S&P são simples de encontrar... |
| Quais são as implicações fiscais do trabalho freelancer? | Se você tiver rendimentos nos EUA, terá de pagar imposto de renda dos EUA sobre eles, a menos que haja um tratado... |
| O que é considerado alto ou baixo quando se fala de volume? | O volume diário é geralmente comparado ao volume médio diário dos últimos 50 dias para uma ação... |
| Como utilizar os pontos do cartão de crédito para pagar despesas empresariais que podem ser deduzidas no imposto de renda? | Para simplificar, vamos começar considerando apenas o cashback. Em geral, o cashback de cartões de crédito para uso pessoal não é tributável... |
| Como devo declarar meus impostos como autônomo? | Para fins fiscais, você precisará declarar como empregado e também como empreendedor... |

### Public Sources

- [FiQA: Financial Opinion Mining and Question Answering](https://doi.org/10.1145/3184558.3192301).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).
- [NanoBEIR-pt dataset](https://huggingface.co/datasets/hakari-bench/NanoBEIR-pt).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| FiQA: Financial Opinion Mining and Question Answering | 2018 | task paper | https://doi.org/10.1145/3184558.3192301 |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | https://arxiv.org/abs/2104.08663 |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | https://arxiv.org/abs/2502.13595 |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | https://huggingface.co/collections/zeta-alpha-ai/nanobeir |
