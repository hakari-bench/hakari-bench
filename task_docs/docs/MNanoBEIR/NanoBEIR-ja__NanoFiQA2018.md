# MNanoBEIR / NanoBEIR-ja / NanoFiQA2018

## Overview

`NanoBEIR-ja__NanoFiQA2018` is the Japanese NanoBEIR version of FiQA 2018, a
financial question-answer retrieval benchmark. The task uses Japanese
translated personal-finance questions as queries and asks a retriever to rank
Japanese translated answer passages. The Nano split contains 50 queries, 4,598
documents, and 123 positive qrels. More than half of the queries have multiple
positives, with 2.46 positives per query on average. The task is useful for
testing whether retrieval models can match practical finance questions to
answers involving taxes, investing, credit cards, loans, volume, contracts, and
jurisdiction-specific advice.

## Details

### What the Original Data Measures

[FiQA 2018](https://doi.org/10.1145/3184558.3192301) was created around
financial opinion and question answering data. BEIR uses its retrieval version
as a finance-domain benchmark in which the system must retrieve answer passages
for financial questions. In this Japanese NanoBEIR version, translated user
questions are matched against translated forum-style answers. The task measures
domain-specific semantic retrieval: the relevant answer may share financial
terms with the query, but it must also address the same decision, rule, or
interpretation.

### Observed Data Profile

The task has 50 queries and 4,598 documents. It contains 123 positive qrels,
with positives per query ranging from 1 to 15 and a median of 2.00. Queries
average 28.48 characters, while documents average 427.96 characters. The
examples include questions about Vanguard returns, freelance tax implications,
stock volume, business expenses paid with credit card points, and contractor
tax filing. The queries are short and practical; the documents are longer
answers that often include qualifications, assumptions, and jurisdictional
details.

### BM25 Evaluation Profile

The BM25 top-500 subset reaches nDCG@10 = 0.3288, hit@10 = 0.6200, and
Recall@100 = 0.6585. BM25 benefits from repeated finance terms such as tax,
volume, credit card, business expense, or contractor. However, exact term
matching is limited because many finance answers use explanatory wording rather
than the same phrasing as the question. A passage can share the term "tax" while
answering a different filing status, jurisdiction, or accounting treatment.
This makes lexical retrieval useful but insufficient.

### Dense Evaluation Profile

The dense `harrier-oss-270m` top-500 subset reaches nDCG@10 = 0.3762, hit@10 =
0.6800, and Recall@100 = 0.7398. Dense retrieval improves over BM25 on every
reported metric. This indicates that embedding similarity helps connect short
financial questions with answer passages that explain the same concept using
different wording. The gain is especially relevant for practical finance
queries, where the important match may be between a user situation and an
answer's reasoning rather than between identical keywords.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses 100 to 101 candidates per query and reaches
nDCG@10 = 0.4041, hit@10 = 0.7000, and Recall@100 = 0.7480. Seven queries use
the rank-101 safeguard. Hybrid retrieval is the strongest profile across the
main metrics. The pattern suggests that lexical signals still matter for
financial terminology and named products, while dense retrieval adds semantic
matches for advice, rules, and decision context. The hybrid pool is therefore a
good approximation of practical search behavior for this domain.

### Metric Interpretation for Model Researchers

This task shows a clean progression from BM25 to dense to hybrid. BM25 captures
obvious term overlap, dense retrieval improves semantic answer matching, and
`reranking_hybrid` combines both into the best top-10 quality and best top-100
coverage. Researchers should interpret gains on this task as evidence that a
model handles domain-specific paraphrase and answer relevance, not merely
general topic similarity. Since many queries have multiple positives, coverage
also matters: a good system should retrieve several valid answers when the
question admits multiple explanations or related advice.

### Query and Relevance Type Tendencies

Queries are concise personal-finance questions. Relevant documents are
forum-style answers that may include caveats such as country, tax treatment,
business versus personal use, or comparison with historical averages. The
relevance relationship is often situational: the passage must answer the user's
financial decision, not just mention the same instrument or accounting term.
This makes hard negatives easy to construct from documents that share terms but
answer a different financial scenario.

### Representative Failure Modes

BM25 can retrieve passages that repeat finance keywords while answering the
wrong issue. Dense retrieval can retrieve broad finance advice that is
semantically close but lacks the specific rule or assumption needed by the
query. Hybrid retrieval improves both ranking and coverage, but it can still
over-rank documents from the same broad topic, such as tax filing, when the
jurisdiction or status differs. Multi-positive queries also expose whether the
model retrieves only one answer style or covers multiple valid explanations.

### Training Data That May Help

Useful training data includes non-overlapping financial QA, finance forum
retrieval, tax and investing question-answer pairs, and multilingual finance
retrieval data. Hard negatives should share financial vocabulary but answer a
different decision, account type, jurisdiction, or business context. Training
should exclude FiQA, BEIR, NanoBEIR, and translated answer passages likely to
overlap with this benchmark.

### Model Improvement Notes

Strong systems should preserve financial terminology while modeling the user's
actual situation. Good retrieval requires distinguishing similar questions about
tax, investing, credit, or contracting that have different answers because of
context. Hybrid candidate generation is a natural fit, and reranking should
focus on answer-bearing specificity rather than broad finance-topic similarity.

## Example Data

| Query | Positive document |
| --- | --- |
| ヴァンガードが提示しているリターンの種類は何ですか？ [26 chars] | ヴァンガードのページから - S&Pのデータが見つけやすいため、これが最も簡単な方法に思えた。私はMoneyChimpを使用して確認したが、そこではヴァンガードのページが算術平均ではなくCAGR（複利成長率）を提示していることを裏付けている。注：ヴァンガードは「米国株式市場のリターンについては、1926年から1957年3月3日まではS&P 90を使用している」と述べているが、Chimpはノーベル賞... [200 / 230 chars] |
| フリーランスの税務上の影響 [13 chars] | 米国で所得がある場合、あなたの国と米国との間に別段の規定を定める条約がない限り、米国所得税が課税されます。 [53 chars] |
| 「ボリューム」について話す際に、高いまたは低いとは何を指すのでしょうか？ [36 chars] | 1日の出来高は、通常、その銘柄の過去50日間の平均1日出来高と比較されます。高い出来高とは、その銘柄の過去50日間の平均1日出来高の2倍以上を指すことが一般的ですが、あるトレーダーは特定のパターンや出来事の確認のために、3倍または4倍の平均1日出来高を基準とすることもあります。出来高はその銘柄自身の平均1日出来高（ADV）と比較されるため、他の銘柄の出来高と比較することはしません。これは、異なる企... [200 / 294 chars] |
| クレジットカードのポイントを、税務上の経費として計上可能なビジネス支出の支払いに使用する [44 chars] | 単純化するために、まずキャッシュバックについてのみ考えましょう。一般的に、個人利用のクレジットカードからのキャッシュバックは課税対象ではありませんが、事業利用の場合は課税対象になります（ただし、後で説明しますが、完全にそうというわけではありません）。その理由は、個人での購入のほとんどが税後所得で行われるためです。通常、個人的な購入品の費用を個人の所得から控除することはないため、100ドルの商品を購... [200 / 1,624 chars] |
| 請負業として税金を申告するにはどうすればよいですか？ [26 chars] | 税務上の目的で、従業員として（T4スリップで自動的に税金が控除される）申告するだけでなく、起業家としても申告する必要があります。昨年、私も同じ状況でした。「Employee and self-employed」はカナダ税務局（Revenue Canada）が発行している資料で、参考になります。事業活動明細書のフォームを記入し、控除可能なすべての経費について詳細な記録を残す必要があります。コピーを取... [200 / 317 chars] |

### Public Sources

- [FiQA 2018](https://doi.org/10.1145/3184558.3192301).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).
- [hakari-bench/NanoBEIR-ja](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ja).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| FiQA 2018 | 2018 | task paper | [https://doi.org/10.1145/3184558.3192301](https://doi.org/10.1145/3184558.3192301) |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | [https://arxiv.org/abs/2104.08663](https://arxiv.org/abs/2104.08663) |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | [https://arxiv.org/abs/2502.13595](https://arxiv.org/abs/2502.13595) |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | [https://huggingface.co/collections/zeta-alpha-ai/nanobeir](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
