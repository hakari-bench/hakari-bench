# MNanoBEIR / NanoBEIR-vi / NanoFiQA2018

## Overview

NanoFiQA2018 in the Vietnamese NanoBEIR slice is a financial question-answer retrieval task derived from FiQA. The queries are Vietnamese translated finance questions, and the corpus contains Vietnamese translated answer passages. The retrieval goal is to find passages that answer practical finance questions about returns, taxes, trading volume, credit card rewards, and contractor filing. This makes the task a compact diagnostic for domain-specific Vietnamese answer retrieval.

## Details

### What the Original Data Measures

FiQA was introduced for financial opinion mining and question answering. In retrieval form, it tests whether a model can connect a finance question to an answer passage that resolves the user's need. The relevant passage may explain a rule, define a metric, discuss a tax treatment, or give practical financial advice.

The Vietnamese translated version adds multilingual and domain-specific challenges. Financial names, acronyms, and tax forms may remain in English, while the rest of the question and answer are Vietnamese. A strong model must bridge short question wording to longer answer passages that may use technical terminology or examples.

### Observed Data Profile

The task contains 50 queries, 4,598 documents, and 123 relevance judgments. The average number of positives is 2.46 per query, with a minimum of 1, a median of 2.0, and a maximum of 15. There are 28 multi-positive queries, or 56.0% of the query set. The task therefore mixes single-answer retrieval with broader answer-set ranking.

Queries average 66.50 characters, while documents average 936.13 characters. The questions are short but domain-specific, and the answer passages are often explanatory. The model must identify answer usefulness, not merely financial topicality.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.3300, hit@10 of 0.5800, and recall@100 of 0.6260 using the top-500 BM25 candidate subset. This is a useful but incomplete lexical profile. Finance terms such as Vanguard, tax, volume, and credit card provide anchors, but many answers use different wording from the question.

BM25 can retrieve passages that share visible financial terminology, yet it may miss passages that answer the need through explanation or technical synonyms. It can also over-rank passages about the same financial topic that answer a different decision problem. The result shows that lexical matching alone is not enough for robust Vietnamese finance QA retrieval.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.3306, hit@10 of 0.6000, and recall@100 of 0.6911. Dense retrieval is slightly stronger than BM25, especially for candidate coverage. This indicates that embedding similarity helps connect finance questions to explanatory passages beyond exact word overlap.

The small top-rank gain suggests that finance-domain specificity remains hard. A general dense model may retrieve semantically related financial passages that do not answer the exact question. Domain terms, jurisdictional details, and assumptions can determine relevance, and those details may require more specialized training.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.3693, hit@10 of 0.6600, and recall@100 of 0.7317. It uses a top-100 candidate range with an optional rank-101 safeguard; the observed candidate count ranges from 100 to 101, with 4 safeguard rows and a mean of 100.08 candidates. This is the strongest profile across the main metrics.

The hybrid result shows that Vietnamese FiQA benefits from combining lexical finance anchors with dense semantic answer matching. BM25 contributes exact domain terms, while dense retrieval adds paraphrase and answer-intent coverage. The combined pool improves both first-page ranking and recall, making it the best first-stage option among these profiles.

### Metric Interpretation for Model Researchers

nDCG@10 is the most practical metric because finance QA systems need answer passages near the top. hit@10 measures whether at least one answer is visible, and recall@100 measures whether downstream reranking can access the answer set. Since more than half the queries have multiple positives, recall also reflects answer diversity.

The comparison shows that BM25 and dense retrieval are close at the top, but hybrid search is clearly better. This task is useful for evaluating whether a retrieval system can combine financial terminology with semantic answer intent rather than relying on either signal alone.

### Query and Relevance Type Tendencies

Queries ask practical finance questions such as what type of yield Vanguard reports, tax effects of freelancing in the United States, what counts as high or low trading volume, using credit-card points for deductible business expenses, and how to file taxes as a contractor. Relevant passages are explanatory answers with assumptions, examples, and caveats.

The task rewards domain-sensitive answer matching. A passage can discuss taxes or investments but still answer a different question. The model must track the decision problem and the answer type expected by the query.

### Representative Failure Modes

Likely failures include retrieving same-term finance passages that answer a different issue, missing answers expressed with technical synonyms, over-ranking generic investment or tax advice, and confusing personal and business contexts. BM25 is too literal in some cases, while dense retrieval can be too broad.

### Training Data That May Help

Useful training data includes Vietnamese financial QA, multilingual finance retrieval, personal-finance forums, tax and investment answer ranking, and hard negatives that share financial terminology but answer a different need. For rerankers, near-topic wrong answers are particularly valuable.

### Model Improvement Notes

A model targeting this task should improve domain-specific answer matching. Sparse systems need query expansion and normalization for finance terminology. Dense systems need finance-specific positives and hard negatives. Hybrid systems are promising here because the task benefits from both exact terminology and semantic answer intent.

## Example Data

| Query | Positive document |
| --- | --- |
| Loại lợi suất nào mà Vanguard đang báo giá? [43 chars] | "Từ trang Vanguard - Đây có vẻ là cái dễ nhất vì dữ liệu S&P dễ tìm. Tôi sử dụng MoneyChimp để lấy - điều này xác nhận rằng trang của Vanguard đang cung cấp CAGR, không phải Trung bình số học. Lưu ý: Vanguard tuyên bố ""Đối với lợi nhuận thị trường chứng khoán Mỹ, chúng tôi sử dụng Standard & Poor's 90 từ năm 1926 đến ngày 3 tháng 3 năm 1957,"" trong khi Chimp sử dụng dữ liệu từ trang của người đoạt giải Nobel, Robert Shiller." [431 chars] |
| Các tác động thuế của việc làm tự do ở Hoa Kỳ [45 chars] | Nếu bạn có thu nhập ở Mỹ, bạn sẽ phải nộp thuế thu nhập Mỹ trên số thu nhập đó, trừ khi có hiệp định với quốc gia của bạn quy định khác. [136 chars] |
| Cái gì được coi là cao hoặc thấp khi nói về âm lượng? [53 chars] | Khối lượng giao dịch hàng ngày thường được so sánh với khối lượng giao dịch trung bình hàng ngày trong 50 ngày qua của một cổ phiếu. Khối lượng cao thường được coi là gấp 2 lần hoặc hơn khối lượng giao dịch trung bình hàng ngày trong 50 ngày qua của cổ phiếu đó, tuy nhiên một số nhà giao dịch có thể đặt tiêu chí là gấp 3 hoặc 4 lần khối lượng giao dịch trung bình để xác nhận một mẫu hình hoặc sự kiện cụ thể. Khối lượng được so sánh với khối lượng giao dịch trung bình của chính cổ phiếu đó, vì việc so sánh với khối lượng của các cổ phiếu khác sẽ giống như so sánh táo với cam, vì các công ty khác nhau sẽ có số lượng cổ phiếu tổng cộng khác nhau, các mức độ thanh khoản khác nhau và các mức độ biến động khác nhau, tất cả đều có thể góp phần vào khối lượng giao dịch hàng ngày. [782 chars] |

### Source Reference Table

| Item | Reference |
| --- | --- |
| Original dataset | [FiQA](https://doi.org/10.1145/3184558.3192301) |
| Retrieval benchmark framing | [BEIR](https://arxiv.org/abs/2104.08663) |
| Multilingual benchmark context | [MMTEB](https://arxiv.org/abs/2502.13595) |
| NanoBEIR collection | [NanoBEIR on Hugging Face](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
| NanoBEIR-vi dataset | [hakari-bench/NanoBEIR-vi](https://huggingface.co/datasets/hakari-bench/NanoBEIR-vi) |

Representative query and positive answer snippets:

| Query | Positive document snippet |
| --- | --- |
| Loại lợi suất nào mà Vanguard đang báo giá? | Từ trang Vanguard - Đây có vẻ là cái dễ nhất vì dữ liệu S&P dễ tìm... |
| Các tác động thuế của việc làm tự do ở Hoa Kỳ | Nếu bạn có thu nhập ở Mỹ, bạn sẽ phải nộp thuế thu nhập Mỹ... |
| Cái gì được coi là cao hoặc thấp khi nói về âm lượng? | Khối lượng giao dịch hàng ngày thường được so sánh với khối lượng giao dịch trung bình hàng ngày... |
| Sử dụng điểm thẻ tín dụng để thanh toán cho chi phí kinh doanh có thể khấu trừ thuế | Để đơn giản, hãy bắt đầu bằng cách chỉ xem xét tiền hoàn lại... |
| Tôi nên nộp thuế của mình như thế nào với tư cách là một nhà thầu? | Về mục đích thuế, bạn sẽ cần nộp hồ sơ như một nhân viên... |
