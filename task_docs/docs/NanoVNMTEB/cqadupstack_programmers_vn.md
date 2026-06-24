# NanoVNMTEB / cqadupstack_programmers_vn

## Overview

`cqadupstack_programmers_vn` is the Vietnamese NanoVNMTEB version of the CQADupStack Programmers duplicate-question retrieval task. The original CQADupStack benchmark uses StackExchange questions manually linked as duplicates; this split adapts the software-engineering or Programmers community into Vietnamese through the VN-MTEB data pipeline. Each query is a short translated question title, and each relevant document is a longer archived thread asking the same engineering or programming-practice question.

The Nano split contains 200 queries, 10,000 candidate documents, and 490 positive qrels. Queries average 58.73 characters, while documents average 1,070.5566 characters. The task is not primarily code search. It covers architecture, APIs, frameworks, licensing, project process, internships, career choices, data structures, testing, and everyday programming practice. In the observed retrieval data, dense retrieval is strongest at the top ranks, while `reranking_hybrid` has the best recall@100 by a small margin. This makes the task a useful example of software-engineering duplicate retrieval where semantic intent is stronger than exact token overlap, but lexical evidence still helps recover additional candidates.

## Details

### What the Original Data Measures

CQADupStack measures retrieval of earlier community questions that were marked as duplicates. In the Programmers subset, relevance is about duplicate engineering intent rather than identical code. A query about the difference between a library, framework, runtime, and API should retrieve a document asking the same conceptual distinction. A query about whether using .NET requires payment to Microsoft should retrieve licensing-oriented duplicates, not arbitrary .NET programming questions.

The Vietnamese version keeps this duplicate-search structure while translating software-engineering titles and bodies. Product names, APIs, language names, and framework identifiers often remain in English, while surrounding explanation and decision framing appear in Vietnamese. A good model must combine exact technical anchors with broader semantic understanding of the user decision being asked.

### Observed Data Profile

The task has 490 positive judgments across 200 queries, with an average of 2.45 positives per query. The median number of positives is 1, but 74 queries have multiple positives, giving a multi-positive query rate of 37.0%. The largest positive cluster has 32 documents. This mix creates both precise duplicate searches and broader clusters around recurring software-engineering topics.

Documents are long relative to queries and commonly include background constraints, project context, technology choices, and partial examples. The query title may state only a compact decision, such as choosing a Java client-server approach, understanding assertions, or becoming a technical architect. The relevant thread may answer through a longer discussion with different wording. This length and framing mismatch makes pure keyword matching incomplete.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.3568096031, hit@10 of 0.5500, and recall@100 of 0.5387755102 with a top-500 candidate set. It benefits from distinctive terms such as Selenium, GSoC, Java, .NET, API, framework, algorithm, assertion, and boolean parameter. When a duplicate shares the same tool or named concept, lexical matching can find a relevant document reliably.

The main limitation is that many software-engineering duplicates are expressed as decisions, tradeoffs, or conceptual explanations rather than repeated terminology. Two questions can ask the same thing while using different examples, job contexts, or tool names. Conversely, many hard negatives share visible tokens but ask a different design decision. BM25 is therefore useful as a candidate generator but less reliable as the only top-rank signal.

### Dense Evaluation Profile

Dense retrieval with `harrier-oss-270m` reaches nDCG@10 of 0.4294210014, hit@10 of 0.6400, and recall@100 of 0.6306122449. It is the strongest condition for nDCG@10 and hit@10. This result fits the nature of the task: many duplicates are semantically equivalent engineering questions that do not require exact phrase overlap.

Dense retrieval is especially helpful for career, process, design, and architecture questions where the same intent can be framed in several ways. It can connect a short title about becoming a technical architect with a longer thread about what makes a good architect, or a licensing query with a practical discussion of distributing software. Its main risk is over-generalization: similar engineering topics may be close in embedding space even when the actual decision differs.

### Reranking Hybrid Evaluation Profile

`reranking_hybrid` reaches nDCG@10 of 0.4229354048, hit@10 of 0.6350, and recall@100 of 0.6387755102. The top-100 reranking pool has mean candidate count 100.135, with 27 rows expanded to 101 candidates by qrels safeguards. This condition nearly matches dense retrieval at the top ranks and slightly exceeds it on recall@100.

The pattern suggests that dense retrieval provides the best ordering signal, while hybrid search recovers a few extra relevant documents through lexical anchors. This is a common situation in software-engineering retrieval: embeddings capture intent, but names of frameworks, platforms, libraries, and legal terms still matter. A strong hybrid system should use sparse evidence to preserve candidate coverage without letting same-token hard negatives dominate the final ranking.

### Metric Interpretation for Model Researchers

This task is a good diagnostic for whether a multilingual retrieval model understands software-engineering intent. Dense retrieval leads BM25 by about 0.0726 nDCG@10 and 0.09 hit@10, showing that semantic matching matters. `reranking_hybrid` slightly improves recall@100 over dense, showing that sparse candidate evidence still contributes useful coverage.

The multi-positive rate of 37.0% means recall@100 should not be ignored. A query may have several duplicate threads around the same recurring topic, and a useful retriever should recover more than one. At the same time, the median positive count is 1, so nDCG@10 remains a strict test of whether the most precise duplicate is ranked early.

### Query and Relevance Type Tendencies

Queries often ask practical questions: what a concept means, which development approach to use, whether a license or framework has consequences, how to reason about assertions, whether an internship or open-source program is valuable, or how to keep up with new tools. Relevant documents may include different examples while preserving the same decision.

The task is less about retrieving code snippets than retrieving the same human engineering question. Product and API names are important but not sufficient. A document about Java is not relevant to every Java query; it must ask the same client-server, architecture, or tooling decision. This makes hard negatives naturally frequent.

### Representative Failure Modes

BM25 can over-rank documents that share a platform or language name but ask a different question. A `.NET` licensing query may be confused with ordinary `.NET` development, and an API/framework distinction may be confused with unrelated framework usage. Dense retrieval can over-rank broadly similar software-process questions that differ in the actual recommendation being sought.

Another failure mode is losing constraints. The relevant duplicate may depend on whether the user asks about payment, architecture responsibility, server-client design, assertions versus exceptions, or a behavior-changing boolean parameter. Models that summarize the query too broadly may retrieve plausible but non-duplicate discussions.

### Training Data That May Help

Useful training data includes non-overlapping Software Engineering or Programmers StackExchange duplicate pairs, Vietnamese developer Q&A, translated CQADupStack training splits with overlap removed, and hard negatives from the same technology but different intent. Multi-positive training should be preserved because many queries have more than one duplicate.

Synthetic data can help when it creates clusters of short Vietnamese software-engineering titles and longer forum-style posts around the same decision. Hard negatives should share tools or keywords but change the intent: same framework but different licensing question, same language but different architecture choice, or same career context but different recommendation.

### Model Improvement Notes

The best improvement target is dense semantic ranking with controlled lexical support. Dense retrieval already gives the best top-10 behavior, so sparse evidence should mainly improve coverage and disambiguate exact product names. A reranker trained on software-engineering duplicate pairs could learn to compare decision intent, constraints, and tool context more precisely.

Researchers should audit errors by topic type. Career and process questions may need broad semantic paraphrase training; API, framework, and licensing questions may need exact terminology and hard negatives. Because `reranking_hybrid` already has the best recall@100, better final reranking is likely more valuable than simply expanding the candidate pool.

## Example Data

| Query | Positive document |
| --- | --- |
| Thư viện so với khung so với API? [33 chars] | Sự khác biệt giữa API, thư viện, runtime và khung làm việc là gì? > **Có thể trùng lặp:** > Thư viện so với framework so với API? Tôi đang gặp khó khăn trong việc hiểu những khái niệm này thực sự có nghĩa là gì. "Stack phần mềm" này rất nhầm lẫn. Bạn có thể giúp tôi với câu hỏi này, hoặc nếu bạn có thể giới thiệu cho tôi một số bài viết/sách mà tôi có thể học chi tiết về stack phần mềm này và cách chúng tương tác cùng nhau không. Tôi đã thử Wikipedia nhưng không có đủ lời giải thích ở đó và sự nhầm lẫn vẫn tồn tại. [523 chars] |
| Điều kiện tiên quyết để trở thành kiến trúc sư kỹ thuật [55 chars] | Những điều cần thiết để trở thành kiến trúc sư kỹ thuật tốt là gì? Tôi chỉ tò mò muốn biết làm thế nào để trở thành một kiến trúc sư kỹ thuật tốt. Hoặc những điều gì tạo nên một nhà phát triển kiến trúc tốt. Hãy chia sẻ ý kiến và bài viết của bạn. [248 chars] |
| Java phát triển giải pháp server-client [39 chars] | Tôi nên tiếp cận phát triển ứng dụng client-server dựa trên Java như thế nào? Tôi đã được yêu cầu phát triển một ứng dụng khách hàng-máy chủ (yêu cầu cơ sở dữ liệu) cho một công ty. Tôi rất thành thạo Java và muốn sử dụng nó. Tôi có thể tự do phát triển ứng dụng theo cách tôi muốn. Nó có thể là một ứng dụng web JSP hoặc ứng dụng dựa trên giao diện đồ họa Swing Java. Tôi có những câu hỏi/lỗi sau đây. Vì vậy, nếu tôi tiếp tục phát triển một ứng dụng web, tôi phải dạy nhân viên công ty: 1. Làm thế nào để cài đặt Tomcat 2. Làm thế nào để tải ứng dụng web Tomcat 3. Làm thế nào để bắt đầu máy chủ để bắt đầu ứng dụng. Nếu tôi tiếp tục phát triển một ứng dụng dựa trên giao diện đồ họa Swing Java, 1. Nó nên bắt đầu khi máy tính khởi động. nghĩa là nó nên được thêm tự động vào dịch vụ khởi động của hệ điều hành khi cài đặt 2. Có phím tắt ứng dụng trong thanh khởi chạy nhanh, thanh tác vụ trên khi cài đặt. Về phần Cơ sở dữ liệu: Tôi muốn có một cơ sở dữ liệu giống như MS-Access nhưng miễn phí. Đi... [1,000 / 1,358 chars] |

### Source Reference Table

| Source | Role |
|---|---|
| CQADupStack | Original duplicate-question retrieval benchmark |
| BEIR | Common retrieval-evaluation framing for CQADupStack |
| VN-MTEB | Vietnamese benchmark collection using translated retrieval tasks |
| GreenNode dataset card | Public dataset entry for this Vietnamese Programmers subset |

### Representative Snippets

- Query: `Thư viện so với khung so với API?`
  Relevant documents ask the same distinction among APIs, libraries, runtimes, and frameworks.
- Query: `Điều kiện tiên quyết để trở thành kiến trúc sư kỹ thuật`
  Relevant documents discuss what makes a strong technical or software architect.
- Query: `Java phát triển giải pháp server-client`
  Relevant documents concern how to approach a Java client-server application with database requirements.
- Query: `Nếu tôi sử dụng .NET Framework cho ứng dụng của mình, tôi có phải trả tiền cho Microsoft không?`
  Relevant documents discuss licensing or payment implications of distributing a .NET application.
- Query: `Về cách sử dụng của các khẳng định`
  Relevant documents compare using assertions with throwing exceptions for precondition handling.
