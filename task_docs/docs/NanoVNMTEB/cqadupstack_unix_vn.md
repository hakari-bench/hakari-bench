# NanoVNMTEB / cqadupstack_unix_vn

## Overview

`cqadupstack_unix_vn` is the Vietnamese NanoVNMTEB version of the CQADupStack Unix duplicate-question retrieval task. The original CQADupStack benchmark uses StackExchange duplicate links to test whether a system can retrieve an earlier question that resolves the same user problem. In this split, short Vietnamese Unix or Linux question titles must retrieve longer system-administration and command-line threads.

The Nano split contains 200 queries, 10,000 candidate documents, and 434 positive qrels. Queries average 52.795 characters, while documents average 875.765 characters. The content mixes Vietnamese prose with commands, paths, flags, terminal output, signals, mount options, package names, and error messages. Dense retrieval is strongest on nDCG@10, while `reranking_hybrid` has the best hit@10 and recall@100. This makes the task a useful test of technical intent matching: the model must preserve exact Unix tokens but also understand when different symptoms point to the same underlying system behavior.

## Details

### What the Original Data Measures

CQADupStack measures duplicate-question retrieval in community Q&A. For the Unix subset, duplicates can involve command syntax, filesystem behavior, shell configuration, package management, networking, process handling, permissions, mounting, or terminal behavior. Relevance is stricter than broad topical similarity: a document is relevant only if it asks the same operational problem.

The Vietnamese version keeps the same retrieval structure while translating the explanatory text. Technical tokens often remain unchanged. A strong model must handle exact command evidence such as paths, flags, signals, and error strings, while also recognizing equivalent descriptions of one Unix behavior. A question about making a host accessible by name on a LAN may be phrased through hostname resolution, local DNS, or simple addressing; those are semantically connected even when the surface words differ.

### Observed Data Profile

The task has 434 positives across 200 queries, for an average of 2.17 positives per query. The median is 1, but 80 queries have multiple positives, giving a multi-positive query rate of 40.0%. The largest positive cluster has 16 documents. This means many queries have a single precise duplicate, but a substantial share belong to small clusters around recurring Unix problems.

Documents are compact compared with some CQADupStack subsets, but they often contain dense technical evidence. A relevant thread may include commands, configuration files, terminal output, and explanation of the environment. The query title may mention only a symptom. This forces retrieval systems to match both the visible command tokens and the hidden system concept behind the symptom.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.3821778840, hit@10 of 0.5750, and recall@100 of 0.5230414747 with a top-500 candidate set. These are relatively strong lexical scores because Unix tasks often contain distinctive command names, paths, filenames, and error text. Exact tokens such as `fstab`, `TERM`, hostnames, mount options, or file suffixes can be highly diagnostic.

BM25 still misses many duplicates because same-command overlap is not always equivalent to same problem. A command may be used in different contexts, and the same issue may be described by an error, a desired workflow, or the underlying system behavior. BM25 can also over-rank documents that share a command name but differ in cause, environment, or configuration.

### Dense Evaluation Profile

Dense retrieval with `harrier-oss-270m` reaches nDCG@10 of 0.4486157817, hit@10 of 0.6300, and recall@100 of 0.6981566820. It is strongest on nDCG@10 and much stronger than BM25 on recall@100. This indicates that many Unix duplicates are connected by operational intent rather than exact term overlap alone.

Dense retrieval helps when a title describes a symptom and the relevant document describes the underlying behavior. It can connect questions about launching applications from a terminal, read-only mounts, terminal color support, file-change reactions, or LAN hostname resolution even when the wording shifts. Its main risk is grouping related administration topics too broadly, especially when system terms are semantically close but technically distinct.

### Reranking Hybrid Evaluation Profile

`reranking_hybrid` reaches nDCG@10 of 0.4455146829, hit@10 of 0.6750, and recall@100 of 0.7027649770. The top-100 reranking pool has mean candidate count 100.095, with 19 safeguard-positive rows and 19 rows containing 101 candidates. It nearly matches dense on nDCG@10, exceeds dense on hit@10, and provides the best recall@100.

This pattern shows complementary evidence. Dense retrieval supplies the best semantic ordering, while sparse retrieval adds command-level coverage. The hybrid pipeline is useful when exact command strings or error messages rescue relevant documents that dense retrieval ranks lower. The slight nDCG gap versus dense suggests that lexical evidence can also introduce same-command distractors, so reranking must distinguish shared tokens from shared system behavior.

### Metric Interpretation for Model Researchers

The Unix split is a strong example of technical duplicate retrieval where dense semantic matching is valuable even though exact tokens matter. BM25 is not weak, but dense retrieval substantially improves recall. `reranking_hybrid` is best for hit@10 and recall@100, showing that a hybrid candidate pool is useful, while dense remains marginally better for top-order nDCG.

The multi-positive rate of 40.0% means recall@100 is informative. Many Unix problems have several duplicate formulations, and a model should recover a cluster rather than one thread. The median positive count of 1 still makes top-rank precision important. Good systems should be evaluated for whether they retrieve the same cause, not only the same command.

### Query and Relevance Type Tendencies

Queries often ask about file access, editing as root, terminal colors, LAN hostnames, file-change triggers, special files, or comparing file lists. Relevant documents may provide a command recipe, explain a system behavior, or include a configuration snippet. The same problem may be phrased as a shell question, filesystem question, or administration workflow.

Relevance depends on operational equivalence. Two questions mentioning `fstab` are not necessarily duplicates; two questions about hostnames are not necessarily duplicates. The system must match the user goal, cause, and environment together.

### Representative Failure Modes

BM25 can over-rank same-command false positives, such as documents that mention the same file, flag, or configuration path but address a different cause. Dense retrieval can over-rank broad system-administration neighbors, such as related terminal or filesystem questions that require different actions.

Another failure mode is losing literal command evidence. If tokenization strips paths, flags, or punctuation, the model may miss the decisive clue. Strong retrieval needs both exact token preservation and semantic understanding of Unix behavior.

### Training Data That May Help

Useful training data includes non-overlapping Unix StackExchange duplicate pairs, Vietnamese Linux administration Q&A, man-page and documentation retrieval pairs, and translated CQADupStack training data with overlap removed. Command-line troubleshooting data is especially useful when it includes hard negatives that share commands but differ in cause.

Synthetic data should preserve commands, paths, flags, signals, filenames, and error messages. Generated queries should ask the same command-line or administration problem in different wording, while hard negatives should reuse the same technical token with a different operational intent.

### Model Improvement Notes

The strongest practical direction is a hybrid retriever with a technical reranker. Sparse retrieval should retain literal command evidence. Dense retrieval should connect symptoms to system concepts. The reranker should compare cause, environment, and intended operation across short titles and longer troubleshooting threads.

Error analysis should group failures by shell syntax, permissions, filesystem behavior, process handling, networking, and terminal configuration. If false positives share only commands, add same-command hard negatives. If false negatives use different symptom wording, add paraphrase and troubleshooting-pair supervision.

## Example Data

| Query | Positive document |
| --- | --- |
| Tập tin đặc biệt gây ra lỗi I/O [31 chars] | Tạo ra lỗi đọc lặp đi lặp lại để thử nghiệm? Tôi đang cố gắng thử nghiệm xử lý lỗi trong một số phần mềm, đặc biệt là những gì xảy ra khi có lỗi xảy ra khi đọc từ một tập tin hoặc đường ống. Có cách n... [200 / 457 chars] |
| Xác định gen từ một danh sách các gen [37 chars] | So sánh hai tập tin để tìm các dòng trùng khớp và lưu kết quả dương tính Tôi có 2 file. ### File 1: A0001 C001 B0003 C896 A0024 C234 . B1542 C231 . tới 28412 dòng như thế này ### File 2: A0001 A0024 B... [200 / 568 chars] |
| Làm thế nào để tôi chỉnh sửa một tập tin như là root? [53 chars] | Cách để chỉnh sửa fstab ở Debian Tôi muốn thay đổi tập tin fstab để có thể giải quyết "lỗi đính kèm" (tôi đã thử xóa dòng cuối của tập tin fstab) # /etc/fstab: thông tin hệ thống tập tin tĩnh. # # Sử... [200 / 1,069 chars] |
| Làm thế nào để có được hỗ trợ 256 màu trong một TTY đăng nhập? [62 chars] | 256 màu trong thực tế console Tôi có trong .bashrc của tôi xuất ra biến môi trường TERM = xterm-256color, nhưng điều này gây ra nhấp nháy tất cả các văn bản màu sắc (ls -- màu sắc, trong vim, v.v.) tr... [200 / 636 chars] |
| Cách làm cho một máy tính có thể truy cập được từ LAN sử dụng tên máy chủ [73 chars] | định địa chỉ đơn giản trên LAN Tôi đọc câu hỏi này Làm thế nào để tạo một máy tính có thể truy cập từ mạng cục bộ sử dụng tên máy chủ. Cách đơn giản nhất để cho phép các máy chủ Linux trên LAN xác địn... [200 / 449 chars] |

### Source Reference Table

| Source | Role |
|---|---|
| CQADupStack | Original duplicate-question retrieval benchmark |
| BEIR | Common retrieval-evaluation framing for CQADupStack |
| VN-MTEB | Vietnamese benchmark collection using translated retrieval tasks |
| GreenNode dataset card | Public dataset entry for this Vietnamese Unix subset |

### Representative Snippets

- Query: `Tập tin đặc biệt gây ra lỗi I/O`
  Relevant documents ask how to create repeated read errors or special files for testing error handling.
- Query: `Xác định gen từ một danh sách các gen`
  Relevant documents discuss comparing files and saving matching lines.
- Query: `Làm thế nào để tôi chỉnh sửa một tập tin như là root?`
  Relevant documents ask how to edit protected configuration files such as `fstab`.
- Query: `Làm thế nào để có được hỗ trợ 256 màu trong một TTY đăng nhập?`
  Relevant documents concern terminal color support and `TERM` behavior on a real console.
- Query: `Cách làm cho một máy tính có thể truy cập được từ LAN sử dụng tên máy chủ`
  Relevant documents discuss simple hostname resolution for Linux machines on a local network.
