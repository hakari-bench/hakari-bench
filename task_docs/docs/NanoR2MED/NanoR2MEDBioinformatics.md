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
| Compare alignment quality of multiple sequencing runs aligned against the same reference genome/nI have run Oxford Nanopore Technologies' MinION sequencing on the same DNA sample using three flowcells, each aligned against the same reference genome (E.coli K12 MG1655) using both BWA MEM and GraphMap and stored as BAM files. How can I quantitatively and efficiently analyse the quality of alignment (percentage identity, insertion rate, deletion rate) of each of these files? [476 chars] | Qualimap Evaluating next generation sequencing alignment data What is it? Qualimap 2 is a platform-independent application written in Java and R that provides both a Graphical User Inteface (GUI) and a command-line interface to facilitate the quality control of alignment sequencing data and its derivatives like feature counts. Supported types of experiments include: Whole-genome sequencing Whole-exome sequencing RNA-seq (speical mode available) ChIP-seq How does it work? Qualimap examines sequencing alignment data in SAM/BAM files according to the features of the mapped reads and provides an overall view of the data that helps to the detect biases in the sequencing and/or mapping of the data and eases decision-making for further analysis. Starting from version 2.0 Qualimap provides multi-sample comparison of alignment and counts data. Features [871 chars] |
| Can I index a compressed FASTA file using STAR?/nI am using STAR to align RNA-seq reads to a reference genome. Before the alignment, I need to generate an index of the reference genome. I use the following code to generate the index successfully: STAR --runThreadN 8 --runMode genomeGenerate --genomeDir output/index/star --genomeFastaFiles ref.fa --sjdbGTFfile ref.gtf --sjdbOverhang 100 This works fine. However, I would like to keep my reference genome compressed to save disk space. So I am tryin... [500 / 1,258 chars] | 3.5.6 Process Substitution Process substitution allows a process’s input or output to be referred to using a filename. It takes the form of <(list) or >(list) The process list is run asynchronously, and its input or output appears as a filename. This filename is passed as an argument to the current command as the result of the expansion. If the >(list) form is used, writing to the file will provide input for list. If the <(list) form is used, the file passed as an argument should be read to obtain the output of list. Note that no space may appear between the < or > and the left parenthesis, otherwise the construct would be interpreted as a redirection. [669 chars] |
| How to manipulate a reference FASTA or bam to include variants from a VCF?/nI have some software which takes fastas as the input. I need to include SNVs and InDels from a VCF into the reference hg38 and then use this. The problem is, I don't know of an algorithmically sound way to do this. Are there any existing software packages which could do this efficiently? Is it easier to output a FASTA, or a bam (and then convert to a FASTA)? What about if I wanted to do the same with a bedpe of germline... [500 / 520 chars] | 6.3.3.11. vcf2bed The vcf2bed script converts 1-based, closed [start, end] Variant Call Format v4.2 (VCF) to sorted, 0-based, half-open [start-1, start) extended BED data. Note Note that this script converts from [start, end] to [start-1, start). Unless the --snvs, --insertions or --deletions options are added, we perform the equivalent of a single-base insertion to make BED output that is guaranteed to work with BEDOPS, regardless of what the actual variant may be, to allow operations to be performed. The converted output contains additional columns which allow reconstruction of the original VCF data and associated variant parameters. For convenience, we also offer vcf2starch, which performs the extra step of creating a Starch-formatted archive. 6.3.3.11.1. Dependencies The vcf2bed script requires convert2bed. The vcf2starch script requires starch. [870 chars] |

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
