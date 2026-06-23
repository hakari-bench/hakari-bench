# NanoMTEB-Polish / fiqa

## Overview

`fiqa` is the Polish NanoMTEB version of the FiQA financial question-answering retrieval task. FiQA was introduced for financial opinion mining and question answering, where systems rank relevant answer passages for natural-language finance questions. In this Polish split, short personal-finance, investing, tax, loan, brokerage, and household-finance questions retrieve longer answer-style passages. Relevance often depends on explanatory financial reasoning rather than a single factual phrase.

The Nano split contains 200 queries, 10,000 documents, and 534 positive relevance judgments. Queries average about 69 characters, while documents average about 809 characters. Multi-positive relevance is common: 128 queries have more than one positive, the median number of positives is 2, and the average is 2.67. This makes the task different from single-answer fact lookup. A good model should recover several useful answer passages that may explain the same financial issue from different angles.

## Details

### What the Original Data Measures

FiQA 2018 frames the source task as opinion-oriented financial question answering. The retrieval objective is to rank answer passages that are useful for finance questions, including questions where the answer may contain caveats, practical reasoning, or subjective context. The Polish task is a localized retrieval version of that setting, not a separate Polish finance annotation effort.

This task is valuable for retrieval research because finance questions often use everyday language while relevant passages use technical or advisory language. A query may ask about taxes on stocks or ETFs, broker exchange fees, exchange rates for payments, freelancer tax exposure, inflation, contractor incorporation, option assignment, put-call parity, housing affordability, or mortgage-adviser incentives. Models must connect the user-facing concern to explanatory financial content.

### Observed Data Profile

Documents are answer-like passages with reasoning, examples, and caveats. They are longer than the queries and may include legal references, financial instruments, institutional terms, or country-specific context. The Polish translation preserves many finance-domain entities and some quoted or formula-like fragments.

The high multi-positive rate matters. Many queries have several relevant passages, and those passages may not be paraphrases of each other. They can provide complementary explanations. This makes recall and ranking diversity more important than in narrow duplicate-question tasks.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.2353, hit@10 of 0.4550, and recall@100 of 0.4906. It can use exact finance terms such as ETF, broker, tax, exchange rate, mortgage, option, or inflation. When the query contains a distinctive instrument or institution, lexical matching can find relevant documents.

The limitation is that financial answers often reframe the question. A user may ask in plain language, while the answer discusses tax treatment, market mechanics, regulatory rules, or incentives using different terminology. BM25 also struggles when the relevant passage contains reasoning rather than repeated query words. This produces a clear gap between lexical retrieval and semantic retrieval.

### Dense Evaluation Profile

The dense `harrier-oss-270m` run is much stronger at top ranks, with nDCG@10 of 0.3890, hit@10 of 0.6300, and recall@100 of 0.6685. Dense retrieval captures the explanatory relation between a financial question and a relevant answer passage. It can connect a plain-language query about broker costs to an answer about passive and aggressive sides of exchange trades, or a query about inflation to a passage explaining consumer price indexes.

This profile indicates that FiQA is strongly semantic. The relevant passage need not share many surface terms with the question. It must answer the financial concern. Dense retrieval therefore provides the best direct ranking quality among the first-stage profiles.

### Reranking Hybrid Evaluation Profile

`reranking_hybrid` reports nDCG@10 of 0.3574, hit@10 of 0.6450, and recall@100 of 0.6835. Candidate lists contain 100 to 101 items, and 26 rows use the positive safeguard. Hybrid retrieval has the best hit@10 and recall@100, but dense retrieval has higher nDCG@10.

This distinction is useful. The hybrid pool preserves additional positives by combining exact finance terms with dense semantic matches, but the final top ordering is slightly less ideal than dense retrieval. For a reranking pipeline, the hybrid candidate set is attractive because it keeps more answer passages available. For direct search, dense retrieval is the stronger top-rank baseline.

### Metric Interpretation for Model Researchers

This split is dense-favorable for graded top-10 quality and hybrid-favorable for candidate preservation. BM25 is clearly weaker, showing that term frequency alone is not sufficient for financial QA. Dense retrieval captures answer relevance, while hybrid search broadens the pool with exact financial anchors.

Because many queries have multiple positives, recall@100 should be read carefully. A model that returns one good answer but misses other relevant explanations may underperform as a retrieval component for QA systems. Rerankers should be evaluated on whether they can exploit the broader hybrid pool while preserving dense-quality top ordering.

### Query and Relevance Type Tendencies

Representative queries ask about taxes on stocks or ETFs, exchange-rate conversion for payments, broker fees paid to exchanges, state tax on freelancer income while living abroad, and the meaning or measurement of inflation. These questions typically seek explanation, policy interpretation, or practical guidance rather than a single named entity.

Relevant passages may include caveats, jurisdiction-specific constraints, or financial mechanisms. A model should identify the question's financial intent and retrieve passages that answer it, even when the answer uses different vocabulary.

### Representative Failure Modes

BM25 may retrieve passages that mention the same instrument but do not answer the question. Dense retrieval may retrieve financially related advice that is plausible but not directly relevant. Hybrid retrieval can include both kinds of candidates, so rerankers must decide whether the passage actually addresses the user's concern.

Another failure mode is ignoring jurisdiction or context. Tax, mortgage, and brokerage questions often depend on country, account type, or market structure. A passage that is topically similar can be wrong if it applies to a different financial setting.

### Training Data That May Help

Useful training data includes FiQA training data outside the evaluation split, financial QA pairs, personal-finance forum answers, Polish finance-domain retrieval pairs, and hard negatives that share instruments but answer different questions. Pairwise or listwise supervision is valuable because the task is multi-positive and explanation-oriented.

Hard negatives should include near-topic answers about the same asset, tax term, or loan product that do not answer the query. This helps models distinguish financial topicality from answer relevance.

### Model Improvement Notes

Dense models can improve by representing financial reasoning, practical constraints, and answer usefulness across Polish questions and longer passages. Sparse systems can improve through finance-specific tokenization and entity handling, but they remain limited by vocabulary mismatch. Hybrid systems are useful for candidate generation, especially when followed by a reranker that can evaluate whether the answer passage addresses the question.

For evaluation, nDCG@10 reflects answer ranking quality, while recall@100 reflects whether enough relevant answers remain available for reranking or answer synthesis. This split makes both dimensions important.

## Example Data

| Query | Positive document |
| --- | --- |
| Podatek od akcji lub ETF [24 chars] | „Jeśli sprzedajesz akcje bez wypłat, Twój zysk podlega opodatkowaniu zgodnie z § 1001. Ale nie wszystkie zrealizowane zyski zostaną uznane za podlegające opodatkowaniu. A niektóre zyski, które prawdop... [200 / 2,122 chars] |
| Jaki kurs wymiany stosuje El Al przy przeliczaniu kwoty płatności końcowej na szekle? [85 chars] | „Stawka za „czeki i przelewy” jest ustalana przez każdy bank wielokrotnie w ciągu dnia w oparciu o rynek. Jest to przeciwieństwo stawki za „gotówkę/banknoty”, również ustalaną przez każdy bank, a „„st... [200 / 691 chars] |
| Ile brokerzy płacą za wymianę za transakcję? [44 chars] | Nie ma jednej odpowiedzi na to pytanie, ale są pewne ogólniki. Większość giełd rozróżnia pasywną i agresywną stronę handlu. Uczestnik pasywny to zlecenie, które znajdowało się na rynku w momencie tran... [200 / 1,211 chars] |
| Czy dochód freelancera uzyskany przez obywatela USA mieszkającego za granicą podlega stanowemu podat... [100 / 117 chars] | Brak podatków stanowych, ale Włochy mają również korzystny traktat z rządem federalnym Stanów Zjednoczonych. Zastanów się nad obniżeniem podatków federalnych do 5% ;) to gruba lektura, http://www.irs.... [200 / 629 chars] |
| Ile wynosi inflacja? [20 chars] | Istnieje coś takiego jak indeks cen konsumpcyjnych (CPI). Istnieje koszyk towarów, po który ludzie, którzy prowadzą indeks, w zasadzie robią zakupy. Jest o wiele bardziej szczegółowy ze względu na dok... [200 / 614 chars] |

### Source Reference Table

| Source | What it contributes |
| --- | --- |
| FiQA challenge site | Official task framing for financial question answering. |
| WWW18 Open Challenge record | Challenge paper context for financial opinion mining and QA. |
| MTEB task card | Polish retrieval task packaging. |

### Representative Snippets

- A query asks about taxes on stocks or ETFs; relevant passages discuss taxable gains and treatment of realized profits.
- A query asks what exchange rate El Al uses for final payment conversion; relevant documents discuss bank-set rates and representative rates.
- A query asks how much brokers pay exchanges per trade; relevant answers explain passive and aggressive sides of trades.
- A query asks whether freelancer income earned abroad by a U.S. citizen is subject to state income tax; relevant passages discuss state and federal treatment.
- A query asks how much inflation is; relevant documents explain consumer price indexes and baskets of goods.
