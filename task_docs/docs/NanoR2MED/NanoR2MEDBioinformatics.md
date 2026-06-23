# NanoR2MED / NanoR2MEDBioinformatics

## Overview

`NanoR2MEDBioinformatics` is an English reasoning-driven medical retrieval task from R2MED. Queries are Bioinformatics StackExchange posts about sequencing, alignment, file formats, variant handling, structural biology, and command-line analysis tools. Documents are 10,000 technical or biomedical passages, and each query may have multiple relevant passages. The task tests whether a retriever can bridge from a practical bioinformatics problem to supporting documentation or biomedical explanation. Dense retrieval is much stronger than BM25, while the hybrid pool improves recall but does not match dense top-rank quality.

## Details

### What the Original Data Measures

R2MED is introduced in the paper `R2MED: A Benchmark for Reasoning-Driven Medical Retrieval`. The benchmark focuses on retrieval where relevance depends on answer-supporting reasoning, not only surface overlap between query and document. The project includes Q&A reference retrieval, clinical evidence retrieval, and clinical case retrieval.

Bioinformatics belongs to the Q&A reference retrieval group. The source task uses StackExchange-style questions as queries and external answer-supporting resources as positives. The R2MED pipeline mines candidates from query, answer, and reasoning-path views, then applies automated relevance assessment and expert review.

### Observed Data Profile

The Nano split contains 77 queries, 10,000 documents, and 226 positive qrel rows. Queries average 890.32 characters, reflecting long posts with command snippets, experimental context, sequence-processing details, and error descriptions. Documents average 666.84 characters.

Each query has 2.94 positives on average, with a median of 2 and a maximum of 8. A majority of queries have multiple positives: 49 of 77 queries, or 63.64%. Examples include Oxford Nanopore alignment quality, compressed FASTA indexing with STAR, VCF-to-BED conversion, PDB remark fields, and counting BAM reads per BED interval with bedtools.

### BM25 Evaluation Profile

The BM25 candidate subset uses top-500 candidates and reaches nDCG@10 of 0.2189, hit@10 of 0.4805, and recall@100 of 0.5664. BM25 is useful when the question names a tool, file format, command option, or biological entity that also appears in the relevant passage.

The low score shows the core difficulty of the task. Many queries ask a troubleshooting or explanation question whose answer depends on recognizing the right documentation concept. Term overlap can retrieve pages about the same tool or data type while missing the passage that explains the specific operation, convention, or biological mechanism.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses top-500 candidates and reaches nDCG@10 of 0.3425, hit@10 of 0.6234, and recall@100 of 0.7389. Dense retrieval clearly outperforms BM25 across all reported metrics. Embedding similarity helps connect long user questions to explanatory passages even when wording differs from the document.

This is the strongest standalone profile for Bioinformatics. It suggests that semantic retrieval is essential for mapping from practical StackExchange posts to answer-supporting documentation, especially when queries include noisy context and the relevant passage states a general rule.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates, with six rows receiving the optional rank-101 safeguard. It reaches nDCG@10 of 0.2623, hit@10 of 0.5844, and recall@100 of 0.7478. The hybrid pool has slightly better recall@100 than dense retrieval but lower top-rank quality.

This profile separates candidate coverage from ranking quality. Hybrid retrieval is useful for giving a reranker access to more positives, but the dense ranking itself is better at placing relevant bioinformatics passages near the top. A reranker should be evaluated on whether it can exploit the extra hybrid coverage without inheriting the weaker early ordering.

### Metric Interpretation for Model Researchers

Unlike single-positive tasks, this split has multiple positives for many queries. nDCG@10 rewards ranking several supporting passages early, hit@10 measures whether at least one positive appears in the first ten results, and recall@100 measures how much of the multi-positive evidence set is available to a reranker.

For this split, dense retrieval is the top-rank baseline to beat, while hybrid retrieval is the broader candidate-coverage baseline. Strong models should handle long, noisy technical queries and identify the specific documentation or biological concept needed to solve the problem.

### Query and Relevance Type Tendencies

Queries are long bioinformatics troubleshooting or explanation posts. They often include command lines, file-format assumptions, sequencing technologies, or analysis goals. Relevant documents are tool documentation, format specifications, biomedical explanations, or technical reference passages.

Relevance is answer-supporting. A document does not need to repeat the whole query; it must explain the command behavior, file coordinate convention, analysis method, or biological mechanism required by the answer.

### Representative Failure Modes

Common failures include retrieving general pages about a named tool rather than the exact option behavior, matching a file format without the needed coordinate convention, ranking broad sequencing pages over a specific quality-control explanation, and selecting a related biology passage that does not support the troubleshooting answer. BM25 is especially vulnerable to tool-name overlap; dense retrieval can overgeneralize among similar documentation sections.

### Training Data That May Help

Useful training data includes non-overlapping Bioinformatics StackExchange answer-link retrieval, genomics tool documentation retrieval pairs, sequencing and variant-format QA with hard negatives, and BRIGHT-style reasoning-intensive reference retrieval. Evaluation queries, qrels, and linked positive passages should be excluded.

### Model Improvement Notes

Models should learn to connect user problems to documentation concepts rather than only matching tool names. Hard negatives should share tools, file formats, or biological entities but answer a different operation. Multi-positive training objectives are appropriate because many queries have several supporting passages.

## Example Data

| Query | Positive document |
| --- | --- |
| Compare alignment quality of multiple sequencing runs aligned against the same reference genome/nI h... [100 / 476 chars] | Qualimap Evaluating next generation sequencing alignment data What is it? Qualimap 2 is a platform-independent application written in Java and R that provides both a Graphical User Inteface (GUI) and... [200 / 871 chars] |
| Can I index a compressed FASTA file using STAR?/nI am using STAR to align RNA-seq reads to a referen... [100 / 1,258 chars] | 3.5.6 Process Substitution Process substitution allows a process’s input or output to be referred to using a filename. It takes the form of <(list) or >(list) The process list is run asynchronously, a... [200 / 669 chars] |
| How to manipulate a reference FASTA or bam to include variants from a VCF?/nI have some software whi... [100 / 520 chars] | 6.3.3.11. vcf2bed The vcf2bed script converts 1-based, closed [start, end] Variant Call Format v4.2 (VCF) to sorted, 0-based, half-open [start-1, start) extended BED data. Note Note that this script c... [200 / 870 chars] |
| PDB format: remark number for free text/nI would like to add a text to PDB files that I'm processing... [100 / 650 chars] | REMARK 230 REMARK: Remark 240, Electron Diffraction Experiment Details Remark 240 is mandatory if electron diffraction study. Template 1 2 3 4 5 6 7 123456789012345678901234567890123456789012345678901... [200 / 918 chars] |
| How to count reads in bam per bed interval with bedtools/nI recently installed Ubuntu 16.04 (because... [100 / 648 chars] | bedtools version 2.24.0 The coverage tool now takes advantage of pre-sorted intervals via the -sorted option. This allows the coverage tool to be much faster, use far less memory, and report coverage... [200 / 714 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| R2MED: A Benchmark for Reasoning-Driven Medical Retrieval | 2025 | arXiv paper | [https://arxiv.org/abs/2505.14558](https://arxiv.org/abs/2505.14558) |
| R2MED project page | 2025 | project page | [https://r2med.github.io/](https://r2med.github.io/) |
| R2MED GitHub repository | 2025 | source repository | [https://github.com/R2MED/R2MED](https://github.com/R2MED/R2MED) |
| R2MED/Bioinformatics | 2025 | dataset card | [https://huggingface.co/datasets/R2MED/Bioinformatics](https://huggingface.co/datasets/R2MED/Bioinformatics) |

### Representative Snippets

| Query | Relevant document excerpt |
| --- | --- |
| How can multiple Oxford Nanopore sequencing runs aligned to the same reference genome be compared for alignment quality? | A passage describing Qualimap as a tool for evaluating next-generation sequencing alignment data through GUI and command-line modes. |
| Can STAR index a compressed FASTA file before RNA-seq alignment? | A passage explaining shell process substitution and how command input or output can be exposed through a filename-like handle. |
| How can SNVs and indels from a VCF be incorporated or converted for reference manipulation? | A passage describing `vcf2bed` conversion from 1-based closed VCF intervals to 0-based half-open BED intervals. |
| Which PDB remark number should be used for free-text additions in processed PDB files? | A passage listing PDB REMARK templates and the structured use of remark fields. |
| How should BAM reads be counted per BED interval with modern bedtools behavior? | A passage describing bedtools coverage changes, including sorted interval handling for speed, memory use, and interval-order reporting. |
