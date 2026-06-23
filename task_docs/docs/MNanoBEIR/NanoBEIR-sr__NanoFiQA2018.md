# MNanoBEIR / NanoBEIR-sr / NanoFiQA2018

## Overview

NanoBEIR-sr NanoFiQA2018 is a Serbian financial question-answer retrieval task
derived from FiQA. Queries are translated personal-finance and investing
questions, and documents are translated financial answer passages. The task is
useful because it tests answer-aware retrieval in a domain where many passages
share vocabulary such as taxes, returns, volume, freelancing, or credit cards,
but only some passages answer the specific decision problem. It is one of the
harder Serbian NanoBEIR tasks for lexical retrieval and highlights the value of
semantic answer matching.

## Details

### What the Original Data Measures

FiQA was introduced for financial opinion mining and question answering. BEIR
turns it into answer-passage retrieval, where the system must rank financial
forum answers for a user question. The MNanoBEIR Serbian version preserves this
question-to-answer objective after translation. It measures whether a model can
connect a short Serbian finance question to an answer that addresses the same
financial concept, product, tax issue, or decision context.

### Observed Data Profile

This Nano subset contains 50 queries, 4,598 documents, and 123 positive qrels.
More than half of queries have multiple positives. The average is 2.46
positives per query, with a minimum of 1, median of 2.00, and maximum of 15.
There are 28 multi-positive queries, covering 56.0% of the task. Queries
average 63.76 characters, while documents average 914.39 characters. This
short-question to long-answer shape makes the task sensitive to whether the
retrieved passage actually resolves the financial question.

### BM25 Evaluation Profile

BM25 uses the `bm25` top-500 candidate subset. It reaches nDCG@10 0.1904,
hit@10 0.4000, and recall@100 0.4959. This is a difficult lexical profile.
Serbian translated finance questions often use concise phrasing, while the
answers explain the situation with examples, caveats, and procedural details.
BM25 can recover passages when the same product or tax term appears directly,
but it often retrieves same-topic passages that answer a different question.
The low hit@10 and recall show that lexical term frequency alone is a weak
first stage for this task.

### Dense Evaluation Profile

Dense retrieval uses the `harrier_oss_v1_270m` top-500 candidate subset. It
scores nDCG@10 0.3094, hit@10 0.6200, and recall@100 0.6423, substantially
outperforming BM25. Dense retrieval is better at connecting question intent to
answer content when the answer uses different wording or explains the concept
indirectly. It helps with questions about Vanguard returns, freelancing taxes,
trading volume, credit card points, and self-employment. The remaining errors
likely reflect finance-domain ambiguity and jurisdiction-specific answer
conditions that generic embeddings may not model precisely.

### Reranking Hybrid Evaluation Profile

The reranking hybrid subset uses `reranking_hybrid` with top-100 candidates and
an optional rank-101 safeguard. Candidate counts range from 100 to 101, with a
mean of 100.20 and 10 safeguard rows. It reaches nDCG@10 0.3183, hit@10
0.6200, and recall@100 0.6504, making it the strongest profile overall by a
small margin over dense retrieval. The hybrid result indicates that financial
answer retrieval benefits from combining exact financial terms with semantic
question-answer matching. Its advantage is modest, but it provides the best
candidate coverage and early ranking for reranking experiments.

### Metric Interpretation for Model Researchers

Because many queries have multiple acceptable answers, recall@100 reflects
answer coverage, while hit@10 only confirms that at least one relevant answer
appears early. nDCG@10 captures first-page ranking quality. The large gap
between BM25 and dense or hybrid retrieval shows that this task is not solved
by lexical overlap. Researchers should use it to test whether models capture
finance question intent and whether rerankers can distinguish true answers
from same-topic financial advice.

### Query and Relevance Type Tendencies

Queries are practical Serbian finance questions about returns, taxes,
freelancing, trading volume, credit card points, and self-employment. Relevant
documents are forum-style answers that may contain definitions, examples,
country-specific tax assumptions, or procedural advice. A passage is relevant
when it answers the decision being asked about. The task favors models that
represent domain concepts, user intent, and answer utility.

### Representative Failure Modes

BM25 may retrieve passages that share financial terms but answer another
problem. Dense models may retrieve generally related finance advice that does
not apply to the query's condition or jurisdiction. Hybrid retrieval improves
coverage but can still contain distractors from both lexical and semantic
channels. Translation may make financial terminology inconsistent, especially
for tax and accounting concepts.

### Training Data That May Help

Helpful training data includes non-overlapping financial QA, Serbian finance
forum retrieval, personal-finance answer ranking, tax and investing question
pairs, and multilingual finance retrieval. Hard negatives should use the same
financial product or tax terms but answer a different decision problem.
Training should exclude FiQA, BEIR, NanoBEIR, and translated evaluation
answers.

### Model Improvement Notes

NanoFiQA2018-sr is a strong diagnostic for finance-domain answer retrieval.
Dense and hybrid retrieval both substantially improve over BM25, with hybrid
slightly stronger overall. Improvements should focus on finance-domain
adaptation, jurisdiction and condition sensitivity, and rerankers that compare
question intent with answer content. A practical system would use hybrid
candidate generation and an answer-aware reranker trained on financial QA.

## Example Data

| Query | Positive document |
| --- | --- |
| Koje vrste prinosa Vanguard navodi? [35 chars] | "Sa stranice Vanguard - Ovo se činilo najlakšim jer je S&P podatke lako pronaći. Koristim MoneyChimp da dobijem - što potvrđuje da Vanguardova stranica nudi CAGR, a ne aritmetički prosek. Napomena: Va... [200 / 392 chars] |
| Poreske implikacije freelancinga [32 chars] | Ako imate prihode u SAD-u, dugovaćete porez na prihod SAD-u, osim ako postoji sporazum sa vašom zemljom koji kaže drugačije. [124 chars] |
| Šta se smatra visokim ili niskim kada je reč o jačini zvuka? [60 chars] | Dnevni volumen se obično upoređuje sa prosečnim dnevnim volumenom u poslednjih 50 dana za određenu akciju. Visok volumen se obično smatra kada je dva ili više puta veći od prosečnog dnevnog volumena t... [200 / 661 chars] |
| Korišćenje kreditnih kartica poena za plaćanje poreski odbitnih poslovnih troškova [82 chars] | Radi jednostavnosti, počnimo samo od keš bek-a. Generalno, keš bek sa kreditnih kartica za ličnu upotrebu nije oporeziv, ali za poslovnu upotrebu jeste (na neki način, objasniću kasnije). Razlog je št... [200 / 3,696 chars] |
| Kako da prijavim svoje poreze kao preduzetnik? [46 chars] | Za poreske svrhe, biće vam potrebno da se prijavite kao zaposleni (T4 obrasci i automatski zadržani porez), ali i kao preduzetnik. I sam sam imao istu situaciju prošle godine. "Zaposleni i samostalni... [200 / 738 chars] |

### Public Sources

- [FiQA: Financial Opinion Mining and Question Answering](https://doi.org/10.1145/3184558.3192301).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).
- [NanoBEIR-sr dataset](https://huggingface.co/datasets/hakari-bench/NanoBEIR-sr).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| FiQA: Financial Opinion Mining and Question Answering | 2018 | task paper | [https://doi.org/10.1145/3184558.3192301](https://doi.org/10.1145/3184558.3192301) |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | [https://arxiv.org/abs/2104.08663](https://arxiv.org/abs/2104.08663) |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | [https://arxiv.org/abs/2502.13595](https://arxiv.org/abs/2502.13595) |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | [https://huggingface.co/collections/zeta-alpha-ai/nanobeir](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
