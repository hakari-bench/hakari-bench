# NanoVNMTEB / cqadupstack_mathematica_vn

## Overview

`cqadupstack_mathematica_vn` is the Vietnamese NanoVNMTEB version of the CQADupStack Mathematica duplicate-question retrieval task. The original CQADupStack benchmark was built from StackExchange duplicate links and is widely used through BEIR-style retrieval evaluations; this variant translates the task into Vietnamese for VN-MTEB coverage while retaining the duplicate-question structure. Each query is a short forum-style title, and the corpus contains longer Mathematica or Wolfram Language discussion threads. A strong model must retrieve posts that ask the same computational or symbolic-programming problem even when the title, code fragment, and explanatory wording differ.

The Nano split contains 200 queries, 10,000 candidate documents, and 424 positive relevance judgments. Queries are short, with a mean length of 49.345 characters, while documents average 1,045.7923 characters. This creates a large mismatch between terse problem statements and long threads that often mix Vietnamese prose, translated technical vocabulary, code identifiers, function names, and error messages. The task is useful for testing whether a retrieval model can preserve exact symbolic evidence while still matching broader programming intent. In the observed Nano data, `reranking_hybrid` is the strongest condition overall, but the absolute scores remain low, showing that Mathematica duplicate detection is difficult for both lexical and dense retrieval.

## Details

### What the Original Data Measures

CQADupStack measures duplicate-question retrieval in community question-answering forums. For this Mathematica subset, the target relation is not broad topical relatedness; it is whether two posts are effectively asking the same Mathematica problem. The relevant document may discuss the same Wolfram Language function, the same plotting or integration behavior, the same symbolic-expression transformation, or the same interface between Mathematica and an external tool.

The Vietnamese version keeps the same retrieval shape but adds translation effects. Query titles may translate ordinary explanation words while leaving code tokens unchanged. A query about `NIntegrate::slwcon`, `ListPlot`, `ListVectorPlot[]`, `Manipulate`, or passing a function as an argument is still anchored by exact technical tokens, but surrounding language can vary substantially. The benchmark therefore measures a mixed skill: exact matching over code-like terms, semantic matching over Vietnamese paraphrases, and duplicate-level reasoning over programming intent.

### Observed Data Profile

This Nano task has 424 positives across 200 queries, with an average of 2.12 positives per query. The median is 1, but 71 queries have more than one positive, giving a multi-positive query rate of 35.5%. The maximum number of positives for a single query is 56, so a small number of common Mathematica issues have many duplicate or near-duplicate threads. Researchers should expect both single-answer needle searches and broader clusters around recurring technical problems.

Documents are long relative to queries. A short title may need to retrieve a thread that contains code examples, partial failed attempts, accepted-answer explanations, and terminology introduced only in the body. This favors systems that can use both title-level intent and body-level evidence. The data also includes language mixing: Vietnamese translation, English function names, mathematical notation, and Wolfram syntax appear together. Tokenization and normalization choices can therefore have unusually visible effects.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.2156751582, hit@10 of 0.3750, and recall@100 of 0.3891509434 when evaluated with a top-500 candidate set. These scores show that lexical matching is necessary but not sufficient. BM25 benefits when query titles contain exact Mathematica symbols, warning names, or function identifiers that also appear in relevant threads. Queries mentioning `NIntegrate`, `ListPlot`, `Python`, curve intersections, or arrows along a parametric curve can expose useful sparse signals.

The same mechanism also creates brittle behavior. A duplicate may describe the same operation using a different function name, a different example expression, or a translated explanation without repeating the title terms. BM25 can rank documents with the same visible code token highly even when they address a different programming issue. In this task, lexical frequency and rare-token overlap are strong signals, but many hard cases require knowing that two pieces of Mathematica code express the same task or failure mode.

### Dense Evaluation Profile

The dense `harrier-oss-270m` condition reaches nDCG@10 of 0.1974986624, hit@10 of 0.3450, and recall@100 of 0.3867924528 with top-500 retrieval. It is slightly behind BM25 at the top ranks and nearly tied on recall@100. This pattern suggests that embedding similarity captures some paraphrased intent but struggles to exploit the exact code and symbolic evidence that often identifies the duplicate.

Dense retrieval can help when a title and relevant thread use different surface forms for the same conceptual operation, such as passing a formula to a function, preparing data for a plot, or avoiding a numerical integration warning. However, the task is code-heavy enough that semantic smoothing can blur distinctions that are critical in Mathematica. Similar-looking discussions about plotting, symbolic evaluation, or numerical integration may be close in embedding space while requiring different fixes. For model researchers, this is a useful stress test for multilingual embeddings that must preserve programming-language tokens as first-class retrieval evidence.

### Reranking Hybrid Evaluation Profile

`reranking_hybrid` is the best reported condition for this task: nDCG@10 is 0.2366666289, hit@10 is 0.4100, and recall@100 is 0.4504716981. The reranking candidate set uses top-100 retrieval, with mean candidate count 100.325; 65 rows include 101 candidates because qrels safeguards add positives into the candidate pool. This condition emulates a hybrid search pipeline that can draw from both sparse lexical evidence and dense semantic similarity before final ranking.

The improvement is meaningful because the two retrieval families make complementary errors. BM25 is better at preserving rare Mathematica identifiers, while dense retrieval is better at recognizing Vietnamese paraphrase and broader task intent. Hybrid reranking can keep a document that shares an important function name while also rescuing semantically equivalent duplicates that use different wording. The result is still far from solved, but the higher hit@10 and recall@100 indicate that many relevant documents are recoverable when both evidence channels are available.

### Metric Interpretation for Model Researchers

The low top-rank scores should not be read as simple noise. The task contains many genuine duplicate-detection challenges: short titles, long documents, code snippets, symbolic syntax, and translated technical vocabulary. Because the median number of positives is 1, nDCG@10 is sensitive to whether the model places the exact duplicate near the top. At the same time, the long tail of multi-positive queries means recall@100 also matters: a model that finds only one phrasing of a common problem may miss much of the duplicate cluster.

The ranking relationship is informative. BM25 is stronger than dense at nDCG@10, but `reranking_hybrid` is stronger than both. This points to a task where lexical evidence is highly valuable, yet not complete. A retrieval system tuned for this data should not discard sparse matching over code identifiers, but it also needs semantic matching over translated natural language and programming intent. Improvements should be evaluated across nDCG@10, hit@10, and recall@100 rather than a single aggregate.

### Query and Relevance Type Tendencies

Common query types include how-to questions, error avoidance, plotting behavior, symbolic-expression manipulation, and interoperability with Python. Relevant documents often contain the same target operation in a longer worked example rather than a compact answer. Titles can be generic, while bodies carry the decisive context.

The relevance relation is duplicate-oriented. Two posts about curve intersections are relevant when they ask the same intersection-finding problem, not merely because both mention curves. Two `NIntegrate` threads are relevant when they concern the same warning behavior or convergence issue, not merely because both include the same error prefix. This makes the task a useful diagnostic for whether a retriever understands code-bearing user intent rather than only topic labels.

### Representative Failure Modes

Lexical systems can over-rank documents that share a distinctive function name but solve a different task. Dense systems can over-rank documents with similar high-level semantics but different Wolfram Language mechanics. Both approaches can fail when the translated Vietnamese title is short and the decisive signal appears only in a code block or answer discussion.

Another common failure mode is confusing examples with intent. A document may contain similar arrays, plots, equations, or parameterized curves but ask about formatting, evaluation order, visualization, or numerical stability in a different way. Good models need to separate the object being manipulated from the operation requested on that object.

### Training Data That May Help

Useful training data would include multilingual programming Q&A duplicates, StackExchange-style title-to-thread retrieval, and code-aware contrastive pairs where the same identifier appears in both positive and hard-negative examples. Data that preserves Wolfram Language syntax, error messages, and mixed-language explanations is especially relevant.

Synthetic data can help if it is built carefully: paraphrase a user question while preserving code tokens, generate hard negatives with the same function names but different intent, and include pairs where the relevant document explains the same error or operation using different Vietnamese wording. Generic semantic-pair data alone is unlikely to cover the symbolic precision required here.

### Model Improvement Notes

The strongest practical direction is hybrid retrieval with code-aware normalization. Sparse retrieval should keep exact matches for identifiers, warning names, and mathematical syntax. Dense retrieval should improve Vietnamese paraphrase handling without collapsing distinct programming operations. Reranking models should be trained to compare short titles against long thread bodies and to attend to code blocks as evidence rather than noise.

Evaluation should inspect failures by function family. If errors cluster around plotting, numerical integration, symbolic evaluation, or external-language integration, the model may need targeted data rather than only more general retrieval training. Because `reranking_hybrid` already improves recall, a strong reranker could likely gain further nDCG@10 by learning which of the hybrid candidates is the true duplicate.

## Example Data

### Public Sources

- [CQADupStack paper](https://doi.org/10.1145/2838931.2838934)
- [VN-MTEB paper](https://aclanthology.org/2026.findings-eacl.86/)
- [BEIR paper](https://arxiv.org/abs/2104.08663)
- [GreenNode/cqadupstack-mathematica-vn](https://huggingface.co/datasets/GreenNode/cqadupstack-mathematica-vn)

### Source Reference Table

| Source | Role |
|---|---|
| CQADupStack | Original duplicate-question retrieval benchmark |
| BEIR | Common retrieval-evaluation framing for CQADupStack |
| VN-MTEB | Vietnamese benchmark collection using translated retrieval tasks |
| GreenNode dataset card | Public dataset entry for this Vietnamese Mathematica subset |

### Representative Snippets

- Query: `nguồn giao nhau giữa hai đường cong trong Mathematica`
  Relevant documents discuss finding intersections of curves in Mathematica, often with polynomial or plotted-curve examples.
- Query: `Mathematica và Python tích hợp?`
  Relevant documents concern calling or integrating Python from Mathematica rather than generic language comparison.
- Query: `Cách tránh lỗi NIntegrate::slwcon`
  Relevant documents discuss the same numerical-integration warning and convergence behavior.
- Query: `Truyền hàm hoặc công thức như là tham số của hàm`
  Relevant documents ask how to pass a function or formula as an argument in Wolfram Language.
- Query: `Có cách nào để thêm các mũi tên dọc theo một đường cong tham số bên trong một hàm thao tác (Mathematica)?`
  Relevant documents focus on adding arrows to parametric curves, especially inside interactive Mathematica visualizations.
