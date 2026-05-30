# NanoVNMTEB / cqadupstack_tex_vn

## Overview

`cqadupstack_tex_vn` is the Vietnamese NanoVNMTEB version of the CQADupStack TeX and LaTeX duplicate-question retrieval task. CQADupStack uses manually linked duplicate questions from StackExchange, and this split adapts the TeX community into Vietnamese while retaining commands, package names, warnings, markup, and mathematical notation. A query is a short translated title, and relevant documents are longer threads that solve the same typesetting or TeX-system problem.

The Nano split contains 200 queries, 10,000 candidate documents, and 743 positive qrels. Queries average 47.79 characters, while documents average 1,090.5561 characters. This is a code-and-markup-heavy retrieval task: Vietnamese prose appears alongside LaTeX commands, package names, citation warnings, installation errors, and math expressions. `reranking_hybrid` is strongest overall, but dense and BM25 are close at top ranks. The task tests whether a model can preserve exact TeX evidence while still recognizing duplicate formatting intent.

## Details

### What the Original Data Measures

The original CQADupStack task measures retrieval of earlier questions that community users marked as duplicates. In the TeX subset, relevance is based on whether two posts ask for the same TeX behavior: drawing an arc in TikZ, citing legal documents in BibTeX, fixing a Ruby executable warning during TeXLive use, formatting a table header, handling undefined citations, or choosing a package or symbol.

The Vietnamese version keeps this duplicate relation while translating explanatory text. Commands, package names, warning strings, file names, and mathematical notation often remain unchanged. This creates a mixed-language retrieval problem where exact token preservation is essential, but so is understanding that two different command paths may address the same formatting intent.

### Observed Data Profile

The task has 743 positives across 200 queries, with an average of 3.715 positives per query. The median is 1, but 86 queries have multiple positives, giving a multi-positive rate of 43.0%. The maximum positive count is 100, indicating that some TeX problems are recurring and have many duplicate or near-duplicate threads.

Documents are long and often contain code snippets, package lists, error output, and explanatory context. A short title may refer only to a desired visual or warning, while the relevant document includes a minimal working example, package conflict, or installation environment. This makes both exact matching and long-document comprehension important.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.2843048718, hit@10 of 0.4700, and recall@100 of 0.3997308210 with a top-500 candidate set. Sparse retrieval can exploit distinctive commands, package names, warning messages, and file names. Tokens such as TikZ, BibTeX, Ruby, TeXLive, LyX, `\newcommand`, or citation-warning text are valuable retrieval anchors.

At the same time, BM25 struggles when the same formatting problem is described through different commands or examples. Two documents may share a package name but ask different questions, while two duplicates may use different packages to express the same layout intent. Lexical overlap is therefore important but brittle. For TeX retrieval, exact command matching is a clue, not a complete relevance decision.

### Dense Evaluation Profile

Dense retrieval with `harrier-oss-270m` reaches nDCG@10 of 0.2927496014, hit@10 of 0.5000, and recall@100 of 0.4576043069. It slightly improves top-rank quality over BM25 and provides a larger recall@100 gain. This suggests that embeddings help connect paraphrased formatting goals and installation issues beyond exact command overlap.

Dense retrieval is useful when a query asks for a visual or document-behavior outcome rather than a specific command. It can connect titles about drawing arcs, formatting table rows, or citing legal sources with documents that use different wording. Its risk is that TeX questions with similar visual goals or package names may be close in embedding space even when the actual fix differs. Dense models also need to preserve backslash commands and warning strings rather than treating them as incidental noise.

### Reranking Hybrid Evaluation Profile

`reranking_hybrid` is the strongest condition, with nDCG@10 of 0.3162843275, hit@10 of 0.5000, and recall@100 of 0.4979811575. The reranking pool uses top-100 candidates, with mean candidate count 100.19. There are 38 safeguard-positive rows, producing 38 rows with 101 candidates.

The hybrid result fits the task structure. BM25 contributes exact command and warning evidence; dense retrieval contributes formatting-intent similarity. The combined candidate pool recovers more positives than either single channel, and the top-10 ranking improves over both on nDCG@10. Hit@10 is tied with dense, so the main top-rank benefit is not simply finding any relevant document, but placing better duplicates higher among the first ten results.

### Metric Interpretation for Model Researchers

The metrics show a difficult hybrid-retrieval case. BM25 and dense are close in nDCG@10, dense has better hit@10 and recall@100, and `reranking_hybrid` is best overall. A model that ignores sparse evidence will miss command-anchored duplicates; a model that overweights sparse evidence will retrieve same-package false positives. The right behavior is evidence fusion.

The high multi-positive rate and maximum cluster size of 100 make recall@100 especially important. Some TeX issues are common enough to have many valid duplicates. However, the median positive count remains 1, so top-rank precision still matters. Researchers should inspect both whether a model retrieves the cluster and whether it ranks the closest duplicate before related-but-different TeX troubleshooting threads.

### Query and Relevance Type Tendencies

Queries often ask for concrete TeX outcomes: draw a TikZ arc when the center is known, cite legal documents properly, use ERT in LyX, fix a Ruby-related TeXLive problem, or format the first row of a table differently. Relevant documents may contain minimal examples, warnings, package conflicts, and partial solutions.

The relevance relation is behavior-level duplicate matching. Two posts about TikZ are not automatically relevant; they must ask for the same drawing behavior. Two BibTeX posts are relevant only when they address the same citation problem. This makes the task valuable for testing retrieval over mixed prose, code, and markup.

### Representative Failure Modes

BM25 can over-rank documents sharing a command or package name but solving a different issue. Dense retrieval can over-rank visually or conceptually similar formatting tasks with different TeX mechanics. Both approaches can fail if they normalize away backslashes, citation labels, executable names, or warning text.

Another failure mode is confusing the desired output with the implementation path. A document may contain similar table or drawing code but ask about spacing, alignment, compilation, or package conflicts in a different way. Strong models need to compare the user's intended behavior, not only the visible code.

### Training Data That May Help

Useful training data includes non-overlapping TeX StackExchange duplicate pairs, Vietnamese technical-writing Q&A, LaTeX documentation retrieval pairs, and translated CQADupStack training splits after overlap removal. Training should preserve commands, package names, mathematical notation, and warning strings exactly.

Synthetic data can generate Vietnamese titles for long TeX troubleshooting threads, but it must keep code tokens intact. Hard negatives should share a package, command, or warning while changing the task, such as same TikZ package but different drawing geometry, or same BibTeX context but different citation requirement.

### Model Improvement Notes

The task rewards code-aware hybrid retrieval. Sparse retrieval should retain exact TeX commands and warnings; dense retrieval should represent the formatting or installation intent. Rerankers should compare short titles with long documents that include code blocks and should learn that commands are evidence, not noise.

Error analysis should group failures by problem type: drawing and layout, bibliography and citations, package conflicts, installation, LyX integration, and custom macros. If a model misses exact warning strings, improve tokenization and sparse features. If it retrieves the wrong same-package question, improve behavior-level duplicate supervision.

## Example Data

### Public Sources

- [CQADupStack paper](https://doi.org/10.1145/2838931.2838934)
- [VN-MTEB paper](https://aclanthology.org/2026.findings-eacl.86/)
- [BEIR paper](https://arxiv.org/abs/2104.08663)
- [GreenNode/cqadupstack-tex-vn](https://huggingface.co/datasets/GreenNode/cqadupstack-tex-vn)

### Source Reference Table

| Source | Role |
|---|---|
| CQADupStack | Original duplicate-question retrieval benchmark |
| BEIR | Common retrieval-evaluation framing for CQADupStack |
| VN-MTEB | Vietnamese benchmark collection using translated retrieval tasks |
| GreenNode dataset card | Public dataset entry for this Vietnamese TeX subset |

### Representative Snippets

- Query: `Vẽ cung tròn trong Tikz khi trung tâm của đường tròn được chỉ định`
  Relevant documents discuss drawing an arc in TikZ when the circle center is known.
- Query: `Cách trích dẫn tài liệu pháp lý đúng cách là gì?`
  Relevant documents ask how to cite legal cases or legal documents in BibTeX.
- Query: `Sử dụng ERT trong LyX`
  Relevant documents discuss LyX and embedded TeX content when table or document output changes unexpectedly.
- Query: `Làm thế nào để sửa lỗi "ruby.exe seems not to be installed" trong Windows 7 khi cả Miktex 2.9 và Ruby đều đã được cài đặt?`
  Relevant documents concern TeXLive or MiKTeX Ruby executable detection problems.
- Query: `Định dạng hàng đầu tiên của bảng khác nhau`
  Relevant documents ask how to format a first table row or macro-generated header differently.
