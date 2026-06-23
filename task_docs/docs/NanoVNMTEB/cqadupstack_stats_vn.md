# NanoVNMTEB / cqadupstack_stats_vn

## Overview

`cqadupstack_stats_vn` is the Vietnamese NanoVNMTEB version of the CQADupStack Cross Validated duplicate-question retrieval task. CQADupStack uses StackExchange questions that were manually linked as duplicates, and this split adapts the statistics forum portion into Vietnamese through the VN-MTEB translation and filtering pipeline. A query is a short translated title, and relevant documents are longer statistics Q&A threads that ask the same statistical question or interpretation problem.

The Nano split contains 200 queries, 10,000 candidate documents, and 310 positive qrels. Queries average 52.76 characters, while documents average 998.8628 characters. The content mixes natural-language statistical questions with formulas, distribution names, software references, variable names, and occasional code. In the observed data, `reranking_hybrid` is strongest on nDCG@10, hit@10, and recall@100, while dense retrieval is clearly ahead of BM25. This makes the task a compact diagnostic for retrieval systems that must match statistical intent rather than only shared terms such as Poisson, Gaussian, R, Matlab, or probability.

## Details

### What the Original Data Measures

The original CQADupStack task measures duplicate-question retrieval in community Q&A. For the statistics subset, the relevant relation is usually a shared statistical operation or interpretation: understanding a test result, comparing effect-size measures, calculating expected values for a chi-square goodness-of-fit test, handling infinite values in a statistical function, or detecting unusual events in time series.

The Vietnamese version preserves this duplicate relation while translating the surrounding prose. Mathematical notation, distribution names, software names, and short code fragments often remain in their original form. A model therefore needs to handle both Vietnamese paraphrase and exact technical evidence. The task is not simply topic retrieval over statistics; a document about Gaussian densities is relevant only if it asks the same kind of density, probability, or interpretation question.

### Observed Data Profile

There are 310 positives across 200 queries, for an average of 1.55 positives per query. The median is 1, and 49 queries have multiple positives, giving a multi-positive query rate of 24.5%. The largest positive cluster has 18 documents. Compared with some other CQADupStack subsets, this is a relatively sparse duplicate structure: many queries have one main target, while a smaller set of recurring statistical issues has several duplicates.

The query-document length mismatch is substantial. Short titles often omit assumptions that appear in the full document body, including sample structure, variables, equations, modeling goals, or software output. This makes evidence extraction difficult: the relevant thread may use a different example while asking the same statistical question. Retrieval quality depends on recognizing the operation behind the example.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.3204898593, hit@10 of 0.4700, and recall@100 of 0.5677419355 with a top-500 candidate set. It benefits from exact tokens such as distribution names, formulas, software packages, and statistical-test labels. Queries mentioning `R2WinBUGS`, chi-square notation, Cohen's d, Hedges' g, Poisson models, or infinite values can expose strong lexical anchors.

The weakness is that exact term overlap does not determine duplicate status. Two threads may use the same distribution name but ask different questions about estimation, interpretation, simulation, or diagnostics. Conversely, two duplicates may describe the same statistical issue using different examples. BM25 is useful for candidate recall, but its top ranks can be pulled toward same-formula or same-software negatives.

### Dense Evaluation Profile

Dense retrieval with `harrier-oss-270m` reaches nDCG@10 of 0.3694504463, hit@10 of 0.5150, and recall@100 of 0.6258064516. It outperforms BM25 across the reported metrics, indicating that embedding similarity captures many paraphrased statistical questions that lexical matching misses.

This is expected for Cross Validated-style data. A query about interpreting a unit-root test, comparing effect-size statistics, or detecting online anomalies may be phrased in multiple ways while preserving the same analytical intent. Dense retrieval helps connect these alternative phrasings. Its main risk is over-smoothing: statistically adjacent topics can be semantically close but require different answers, especially when they share common words such as model, distribution, probability, or inference.

### Reranking Hybrid Evaluation Profile

`reranking_hybrid` is the strongest condition: nDCG@10 is 0.3796189081, hit@10 is 0.5400, and recall@100 is 0.6677419355. The reranking pool uses top-100 candidates, with mean candidate count 100.225. There are 45 safeguard-positive rows, producing 45 rows with 101 candidates.

The hybrid result shows that statistical retrieval benefits from combining exact formula or software evidence with semantic paraphrase. Dense retrieval supplies the stronger intent signal, while BM25 contributes rare tokens that should not be lost. The gain is clearest in recall@100, where hybrid retrieval finds more of the relevant duplicate cluster than either single channel. For top-10 quality, the improvement over dense is smaller but still positive, suggesting that reranking can use both evidence types without overwhelming semantic matching.

### Metric Interpretation for Model Researchers

The ranking relationship is instructive: BM25 is clearly behind dense, and `reranking_hybrid` improves on dense. This task is therefore not purely lexical and not purely semantic. Exact mathematical strings matter, but they are not enough to decide duplicate status. A strong model should preserve formulas, software names, and distribution labels while comparing the statistical operation being requested.

The relatively low multi-positive rate also matters. With a median of 1 positive, nDCG@10 is a strict measure of whether the main duplicate is ranked early. The recall@100 gap between BM25 and hybrid shows that candidate generation still matters, but top-rank errors often reflect subtle confusion among related statistical questions. Researchers should inspect failures by operation type, such as inference interpretation, probability calculation, model fitting, or software-output reading.

### Query and Relevance Type Tendencies

Queries tend to be short problem statements or interpretation requests. They may ask what a test result means, how two measures differ, how to compute expected values, how to handle infinities or overflow, or how to detect special events in a time series. Relevant documents often include longer descriptions of data, formulas, and assumptions.

The relevance relation is duplicate-level. A thread using the same distribution is not necessarily relevant; it must ask the same statistical question. A thread mentioning time series is not necessarily relevant; it must concern the same anomaly-detection or event-detection problem. This makes the benchmark useful for testing whether a model can match statistical intent beyond surface terminology.

### Representative Failure Modes

BM25 can retrieve same-token false positives: documents that share distribution names, formulas, or software packages but answer a different question. Dense models can retrieve same-neighborhood false positives: documents that are broadly about inference, regression, or probability but differ in the assumptions or target quantity.

Another failure mode is losing the role of a formula. The same expression may appear in a question about estimation, simulation, goodness of fit, or interpretation. Models need to identify what the user wants to do with the formula, not merely that the formula appears.

### Training Data That May Help

Useful training data includes non-overlapping Cross Validated duplicate pairs, Vietnamese statistics Q&A, translated CQADupStack training data after overlap removal, and hard negatives that share formulas or distribution names but differ in intent. Data that includes software output from R, Matlab, Python, BUGS, or similar tools can help if the supervision links output interpretation to the same question.

Synthetic data should create short Vietnamese titles from longer statistical threads while preserving equations, variable names, package names, and distribution labels. Hard negatives should reuse the same notation but alter the statistical operation, such as changing from fitting to testing, or from probability density to probability mass.

### Model Improvement Notes

The most promising direction is hybrid retrieval with a statistically aware reranker. Dense retrieval should capture paraphrased intent, while sparse retrieval should preserve rare mathematical and software tokens. A reranker should learn to compare assumptions, target quantities, and requested operations across short titles and long documents.

Error analysis should separate formula mismatch from intent mismatch. If a model fails because it ignores notation, improve token preservation and sparse evidence. If it fails because it retrieves the wrong statistical operation, improve hard-negative training and domain-specific semantic supervision. The task rewards models that can do both.

## Example Data

| Query | Positive document |
| --- | --- |
| Thử nghiệm này có ý nghĩa gì? [29 chars] | Tôi giải thích kết quả của bài kiểm tra căn đơn vị như thế nào? Dickey-Fuller kiểm tra đơn vị gốc Số lượng quan sát = 21 ---------- Dickey-Fuller can thiệp Kiểm tra 1% Quan trọng 5% Quan trọng 10% Qua... [200 / 1,506 chars] |
| Sự khác biệt giữa Cohen's d và Hedges' g trong các số liệu thống kê về kích thước tác động [90 chars] | Sự khác biệt giữa Hedges' g và Cohen's d là gì? Tôi đã đọc http://www.polyu.edu.hk/mm/effectsizefaqs/effect_size_equations2.html và sự khác biệt duy nhất tôi có thể tìm thấy giữa hai phương pháp này l... [200 / 672 chars] |
| $\chi^2$ goodness of fit - cách tính giá trị mong đợi khi $\exists$ các tham số không biết [90 chars] | Cách hiểu về bậc tự do là gì? Từ Wikipedia, có ba cách giải thích về bậc tự do của một thống kê: > Trong thống kê, số bậc tự do là số lượng các giá trị trong **tính toán cuối cùng** của một thống kê m... [200 / 1,087 chars] |
| Cách xử lý Infs trong hàm thống kê ra sao? [42 chars] | xử lý hàm mũ trong python - vô cực và tràn Trong một thuật toán học máy mà tôi đang sử dụng, tôi cần lấy các giá trị mũ của một cái gì đó trong một trong những bước. Đây là bước mà tôi đang xử lý ngay... [200 / 747 chars] |
| Phát hiện các sự kiện đặc biệt [30 chars] | Phương pháp đơn giản để phát hiện ngoại lệ trực tuyến của một chuỗi thời gian chung Tôi đang làm việc với một lượng lớn dữ liệu chuỗi thời gian. Những chuỗi thời gian này chủ yếu là các phép đo mạng đ... [200 / 1,188 chars] |

### Source Reference Table

| Source | Role |
|---|---|
| CQADupStack | Original duplicate-question retrieval benchmark |
| BEIR | Common retrieval-evaluation framing for CQADupStack |
| VN-MTEB | Vietnamese benchmark collection using translated retrieval tasks |
| GreenNode dataset card | Public dataset entry for this Vietnamese statistics subset |

### Representative Snippets

- Query: `Thử nghiệm này có ý nghĩa gì?`
  Relevant documents discuss interpreting a statistical test result, such as unit-root test output.
- Query: `Sự khác biệt giữa Cohen's d và Hedges' g trong các số liệu thống kê về kích thước tác động`
  Relevant documents compare the two effect-size measures and their correction behavior.
- Query: `$\chi^2$ goodness of fit - cách tính giá trị mong đợi khi $\exists$ các tham số không biết`
  Relevant documents ask about expected values and degrees of freedom in chi-square goodness-of-fit settings.
- Query: `Cách xử lý Infs trong hàm thống kê ra sao?`
  Relevant documents discuss infinities or overflow in statistical or machine-learning computations.
- Query: `Phát hiện các sự kiện đặc biệt`
  Relevant documents ask about detecting unusual events or outliers in time-series data.
