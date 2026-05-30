# NanoVNMTEB / fi_qa2018_vn

## Overview

`fi_qa2018_vn` is the Vietnamese NanoVNMTEB version of the FiQA 2018 financial question-answer retrieval task. FiQA was introduced for financial opinion mining and question answering, and BEIR uses it as a domain-specific retrieval benchmark. In this VN-MTEB split, translated investor and personal-finance questions retrieve translated answer posts or financial discussion snippets.

The Nano split contains 200 queries, 10,000 candidate documents, and 549 positive qrels. Queries average 69.43 characters, while documents average 811.0306 characters. The task is finance-domain retrieval rather than generic QA: many questions depend on products, jurisdictions, account types, taxation, transfers, investments, and practical decision context. `reranking_hybrid` is strongest across nDCG@10, hit@10, and recall@100, with dense retrieval second and BM25 third. The task rewards systems that combine semantic financial reasoning with exact product, country, and terminology matching.

## Details

### What the Original Data Measures

The FiQA 2018 challenge includes an opinion-based financial QA task over answer posts. Questions ask about investment decisions, tax treatment, market terminology, personal-finance planning, company roles, transfers, inheritance, and financial instruments. In retrieval form, the goal is to find answer posts that address the same financial decision or interpretation.

The Vietnamese version translates the questions and answers while preserving finance-specific tokens such as product names, currencies, jurisdictions, account types, stock-market terms, and company roles. Relevance depends on matching the same financial situation, not just the same product. A document about bonds is relevant only if it answers the same passive-investment or portfolio question.

### Observed Data Profile

The task has 549 positives across 200 queries. The average is 2.745 positives per query, the median is 2, and 129 queries have multiple positives, giving a multi-positive rate of 64.5%. The maximum positive count is 15. This is a moderately multi-positive task where several answer posts may address the same financial need.

Documents are often long and caveated. They may include assumptions about country, law, tax status, account type, product structure, or risk preference. A query may be short, but the relevant answer may explain conditions under which the advice applies. This makes retrieval sensitive to context and constraints.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.3388107397, hit@10 of 0.6000, and recall@100 of 0.5901639344 with a top-500 candidate set. Lexical retrieval can use strong terms such as ETF, Vanguard, director, China, shareholder return, tax, bid, ask, bond, or inheritance. These anchors help when the same financial product or term appears in the answer.

The limitation is that finance answers frequently use explanatory language rather than repeating the exact question. A relevant answer may discuss the mechanism behind a bid-ask spread, taxation rule, short-sale counterparty risk, or passive investment strategy using different wording. BM25 can also retrieve same-product documents that give advice for a different jurisdiction or decision.

### Dense Evaluation Profile

Dense retrieval with `harrier-oss-270m` reaches nDCG@10 of 0.4056925340, hit@10 of 0.6500, and recall@100 of 0.6612021858. It is clearly stronger than BM25, showing that semantic matching is important for finance QA. Dense retrieval can connect a financial question with an answer that explains the same situation even when the exact wording differs.

Dense retrieval is useful for questions about investment strategy, legal or tax interpretation, transfers, inheritance planning, and market mechanics. Its risk is that finance topics can be semantically close while requiring different advice. Same-product or same-country answers may be wrong if the account type, time horizon, legal status, or risk assumption differs.

### Reranking Hybrid Evaluation Profile

`reranking_hybrid` is strongest: nDCG@10 is 0.4118067935, hit@10 is 0.6700, and recall@100 is 0.7030965392. The top-100 candidate pool has mean candidate count 100.105, with 21 safeguard-positive rows and 21 rows containing 101 candidates. Hybrid retrieval improves modestly over dense at the top ranks and more clearly in recall@100.

The result fits the domain. Dense retrieval captures financial intent, while sparse retrieval preserves product names, countries, currencies, and technical market terms. Hybrid search can recover answers that share a decisive product or jurisdiction token while still benefiting from semantic matching. The small top-rank gain over dense suggests that final reranking quality matters more than candidate expansion alone.

### Metric Interpretation for Model Researchers

The metric ordering shows a domain where semantic similarity is stronger than lexical overlap, but lexical constraints still improve coverage. BM25 alone is not enough; dense retrieval gives a large nDCG@10 gain. `reranking_hybrid` is best, especially on recall@100, indicating that exact finance tokens remain important.

The median of 2 positives and multi-positive rate of 64.5% make multi-positive training useful. Many questions have multiple acceptable answers, but those answers may differ in caveats or assumptions. A strong model should retrieve several answer posts while ranking those that match the query's decision context highest.

### Query and Relevance Type Tendencies

Queries include market terminology, tax filing, short-selling consequences, passive-investment allocation, inheritance, international transfers, company directors invoicing their own company, real-estate investment, and shareholder-return headlines. Relevant documents often explain mechanisms or conditions rather than giving a short fact.

Relevance is context-sensitive. A financial answer can be wrong for the query if it assumes a different country, account structure, tax rule, or investment objective. The task therefore tests domain-aware retrieval with constraints, not just broad finance-topic similarity.

### Representative Failure Modes

BM25 can retrieve same-term answers that do not match the jurisdiction or decision. Dense retrieval can retrieve advice-like answers from the same financial neighborhood but with incompatible assumptions. Hybrid retrieval can improve recall but still needs reranking to prefer answers with the right legal, product, and timing context.

Another failure mode is treating financial terms as generic semantics. Terms such as bid, ask, short seller, bond, ETF, and tax deduction have specific meanings. Models should preserve these meanings and avoid overly broad paraphrase.

### Training Data That May Help

Useful training data includes official FiQA training pairs with overlap removed, Vietnamese personal-finance and investment QA, financial forum answer ranking data, and translated finance retrieval data. Data should include product names, currencies, countries, account types, and caveats.

Synthetic data can generate Vietnamese finance questions from answer posts, but it should include hard negatives sharing the same product or country with different advice. It should also avoid turning benchmark content into training data because finance questions can be highly specific.

### Model Improvement Notes

The main improvement direction is domain-aware hybrid retrieval. Dense retrieval should model the financial decision; sparse retrieval should preserve exact financial terms and jurisdictional clues. Rerankers should compare assumptions, caveats, and product context between query and answer.

Error analysis should separate failures by product mismatch, jurisdiction mismatch, missing caveats, and generic topic confusion. Because financial content can be stale or jurisdiction-specific, benchmark use should remain separate from real advice generation.

## Example Data

### Public Sources

- [FiQA 2018 paper](https://doi.org/10.1145/3184558.3192301)
- [FiQA project page](https://sites.google.com/view/fiqa/)
- [VN-MTEB paper](https://aclanthology.org/2026.findings-eacl.86/)
- [BEIR paper](https://arxiv.org/abs/2104.08663)
- [GreenNode/fiqa-vn](https://huggingface.co/datasets/GreenNode/fiqa-vn)

### Source Reference Table

| Source | Role |
|---|---|
| FiQA 2018 | Original financial opinion mining and QA challenge |
| FiQA project page | Challenge and dataset context |
| BEIR | Retrieval benchmark framing |
| VN-MTEB | Vietnamese benchmark collection using translated retrieval tasks |
| GreenNode dataset card | Public dataset entry for this Vietnamese split |

### Representative Snippets

- Query: `"Sell on ask", "sell on bid" trong chứng khoán là gì?`
  Relevant documents explain bid and ask prices and how buy or sell orders relate to them.
- Query: `Giải thích chi phí sinh viên - Để khai thuế cho năm tiếp theo`
  Relevant documents discuss education expenses and tax deduction treatment.
- Query: `Điều gì xảy ra với "người mua dài" của một cổ phiếu khi người bán ngắn khác thất bại`
  Relevant documents explain short selling, ownership, and counterparty consequences.
- Query: `Tôi có nên thay thế trái phiếu trong một chiến lược đầu tư thụ động không?`
  Relevant documents discuss bonds in passive investment portfolios.
- Query: `28 tuổi vừa thừa kế một số tiền lớn và bất động sản - không biết làm gì với nó`
  Relevant documents address starting investment after an inheritance with practical caveats.
