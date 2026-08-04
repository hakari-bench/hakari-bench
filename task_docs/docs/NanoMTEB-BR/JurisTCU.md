# NanoMTEB-BR / JurisTCU

## Overview

JurisTCU is a Brazilian Portuguese legal information-retrieval task based on
jurisprudence from the Tribunal de Contas da União, Brazil's federal audit
court. The source collection pairs search needs with judged court material and
contains real and synthetic query styles, including keyword-like requests and
natural-language questions. Relevant documents may be lengthy, formal, and
densely populated with public-law terminology. NanoMTEB-BR evaluates a compact
set of queries against a 10,000-document pool containing hard negatives from
the same legal domain. This setup tests more than topical recognition: a model
must distinguish decisions that discuss similar agencies, procurement rules,
benefits, or procedures but resolve a different legal issue. Multiple passages
can be relevant to one query, so coverage and ordering both matter. The task is
especially useful for exposing weaknesses in long legal text representation
and Brazilian institutional vocabulary.

## Details

### What the Task Measures

The task measures query-to-case-law retrieval under domain-homogeneous hard
negatives. Strong retrievers preserve legal entities, procedural posture, and
the relationship among a request, governing rule, and court conclusion instead
of relying only on shared terms.

### Metric Interpretation

`nDCG@10` rewards ranking the set of judged relevant documents early and is
important for multi-positive queries. `Hit@10` only checks whether the first ten
contain at least one relevant item. A gap between them can signal incomplete
coverage of the relevant jurisprudence.

### Training and Leakage Notes

Suitable supervision includes non-overlapping Portuguese case-law retrieval
and legal query-document pairs with same-domain hard negatives. Exclude Nano
queries, qrels, positives, and upstream JurisTCU evaluation records. Court text
often repeats quotations and boilerplate, so passage- and document-level
near-duplicate checks are necessary.

## Public Sources

- [JurisTCU paper](https://doi.org/10.1007/s10579-025-09881-w).
- [JurisTCU preprint](https://arxiv.org/abs/2503.08379).
- [JurisTCU source dataset](https://huggingface.co/datasets/LeandroRibeiro/JurisTCU).
- [NanoMTEB-BR dataset](https://huggingface.co/datasets/hakari-bench/NanoMTEB-BR).
