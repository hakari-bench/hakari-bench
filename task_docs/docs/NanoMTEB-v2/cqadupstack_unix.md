# NanoMTEB-v2 / cqadupstack_unix

## Overview

`NanoMTEB-v2 / cqadupstack_unix` is the Unix slice of CQADupStack duplicate-question retrieval. Short Unix StackExchange titles are used as queries, and longer technical posts are candidate duplicate documents. The original CQADupStack benchmark was built from StackExchange duplicate links, so the task is to retrieve a question that asks the same operational problem, not a document that answers it directly. This split focuses on Unix and Linux administration, shell usage, boot issues, filesystems, commands, configuration paths, and error scenarios. It is a useful benchmark for retrieval models that must handle technical language, command snippets, and near-duplicate problem descriptions.

## Details

### What the Original Data Measures

CQADupStack measures duplicate-question retrieval for community question-answering. In the Unix subset, positives are posts judged as duplicates or near duplicates of the query question. The model must connect terse problem titles to longer posts that describe the same command-line or system-administration issue.

Unlike general passage retrieval, relevance is question equivalence. A document about the same command, package, or subsystem may still be wrong if it asks a different operational question.

### Observed Data Profile

The Nano split contains 200 queries, 10,000 documents, and 486 positive qrel rows. Queries have 2.43 positives on average, with a median of 1 and a maximum of 22. There are 84 multi-positive queries, or 42.0% of the query set. Queries average 49.21 characters, while documents average 969.12 characters.

Documents often contain command snippets, file paths, error messages, duplicate markers, and explanatory body text. The examples include file-copy workflows, GRUB repair, accidental deletion recovery, `/proc` update behavior, and `.bashrc` location changes.

### BM25 Evaluation Profile

The BM25 candidate subset uses top-500 candidates and reaches nDCG@10 of 0.4001, hit@10 of 0.5550, and recall@100 of 0.4774. BM25 helps when commands, paths, package names, or error strings repeat exactly. Technical text often contains distinctive tokens that sparse retrieval can exploit.

However, duplicate Unix questions frequently describe the same operation using different filenames, flags, distributions, or failure details. BM25 may retrieve a question that mentions `grub`, `sudo`, `sed`, or `.bashrc` while asking a different question about that tool. This keeps sparse recall and top-rank quality moderate.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses top-500 candidates and reaches nDCG@10 of 0.5095, hit@10 of 0.6950, and recall@100 of 0.6687. Dense retrieval is substantially stronger than BM25. It better connects paraphrased problem descriptions and operationally similar questions even when exact commands or paths differ.

This result suggests that technical duplicate retrieval benefits from semantic modeling of intent. Still, dense models must preserve command-level precision: a small difference in option, path, or subsystem can change the problem entirely.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates, with 14 queries carrying a rank-101 safeguard positive. It reaches nDCG@10 of 0.4658, hit@10 of 0.6600, and recall@100 of 0.6687. Hybrid retrieval matches dense recall@100 but does not beat dense top-rank quality.

The hybrid profile indicates that BM25 contributes useful exact-token candidates, while dense retrieval supplies the stronger semantic ordering. A reranker should benefit from both, especially when sparse retrieval finds command-specific candidates that dense retrieval might under-rank.

### Metric Interpretation for Model Researchers

This task has many multi-positive duplicate clusters but a median of one positive, so models must handle both single duplicate links and broader duplicate families. nDCG@10 measures whether a true duplicate is ranked early; recall@100 shows whether candidate generation can cover alternative accepted duplicates.

Dense retrieval is the strongest first-stage baseline. Hybrid retrieval is still valuable for reranking because Unix questions contain exact tokens that can be decisive.

### Query and Relevance Type Tendencies

Queries are short Unix problem titles. Relevant documents are longer StackExchange questions asking the same problem, often with commands, paths, logs, or system context. The relevant post may use a different distribution, directory, or example command while preserving the same underlying operation.

The relevance relation is duplicate problem equivalence, not topical relatedness.

### Representative Failure Modes

Common failures include retrieving a question about the same command but a different operation, confusing bootloader repair with partition installation, matching a file path token without matching the workflow, and missing paraphrases of error recovery or shell configuration problems. Dense systems may under-weight exact command syntax; sparse systems may over-weight it.

### Training Data That May Help

Useful training data includes StackExchange duplicate-question pairs, Unix and shell support questions, command-error paraphrase pairs, and hard negatives from the same command or subsystem. Multi-positive training is recommended because duplicate clusters can contain many variants.

### Model Improvement Notes

Models should preserve both semantic intent and exact technical constraints. Effective training should include same-command hard negatives and paraphrased duplicates with different filenames, flags, or distributions. Rerankers should inspect the full body text because the title alone often omits critical operational details.

## Example Data

| Query | Positive document |
| --- | --- |
| copy sas file from prior version directory to new version directory [67 chars] | How to copy datasets from prior version directory to latest version directory I've go a number of directories named like: /data/db/OX/8_10 /data/db/OX/9_1 /data/db/OX/9_2 And need to copy some files (all the `pt.*` files) from the second latest one (above `9_1`) to the latest one (above `9_2`). I have tried directly like this. cp -p /data/db/OX/9_1/pt.* /data/db/OX/9_2 However, Instead of typing /data/db/OX/9_1/ & /data/db/OX/9_2. I'd like to be able to write: cp -p /data/db/OS/"$prior_version"/pt.* /data/db/OS/"$latest_version"/ And derive `$prior_version` and `$latest_version` from the list of directories in `/data/db/OX/` in a shell script. [718 chars] |
| Linux Mint Booting Installed Partition [38 chars] | How can I fix/install/reinstall grub? So I started out with a 250GB HDD, the stock drive from an EeePC 1015pem that I am trying to turn into a MintBook. The drive is physically operable, but all data has been nuked, including the old OS. Given this, I attached the HDD to my desktop and installed Linux Mint 16 Xfce from a live USB created through Unetbootin-585. Set aside 10GB for swap and 240GB for Ext4 and /. The drive now refuses to boot for either the desktop or netbook. Both motherboards are sounding the correct sequence of beeps, so they seem healthy, and I can successfully access the BIOS on both systems. However, the only thing that comes up after starting the computer is a nonresponsive command- line. There is no error message, no grub or grub-rescue, nothing. Is there anything I can try besides reformatting and starting over? How would I go about installing a boot loader that can boot my OS? [914 chars] |
| Yanked USB Key During Move [26 chars] | Recovering accidentally deleted files I accidentally deleted a file from my laptop. I'm using Fedora. Is it possible to recover the file? [138 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| CQADupStack: A Benchmark Data Set for Community Question-Answering Research | 2015 | source task paper | [https://eltimster.github.io/www/pubs/adcs2015.pdf](https://eltimster.github.io/www/pubs/adcs2015.pdf) |
| MTEB: Massive Text Embedding Benchmark | 2023 | benchmark paper | [https://arxiv.org/abs/2210.07316](https://arxiv.org/abs/2210.07316) |
| mteb/cqadupstack-unix |  | dataset card | [https://huggingface.co/datasets/mteb/cqadupstack-unix](https://huggingface.co/datasets/mteb/cqadupstack-unix) |

### Representative Snippets

| Query | Relevant document excerpt |
| --- | --- |
| copy sas file from prior version directory to new version directory | A Unix post about copying datasets from prior version directories to the latest version directory under `/data/db/OX/`. |
| Linux Mint Booting Installed Partition | A post about fixing, installing, or reinstalling GRUB after drive and partition problems. |
| Yanked USB Key During Move | A post about recovering accidentally deleted files on Fedora. |
| How proc gets updated about the devices | A question asking how frequently the Linux `proc` filesystem is updated. |
| bashrc in custom folder | A post asking whether `.bashrc` can be moved from the home directory to another location. |
