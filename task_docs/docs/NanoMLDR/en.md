# NanoMLDR / en

## Overview

`NanoMLDR / en` is the English split of NanoMLDR, a multilingual long-document
retrieval benchmark derived from MLDR. English paragraph-grounded questions
retrieve full English articles, and the answer-bearing paragraph may be a small
part of an extremely long document. The Nano split has 200 queries, 10,000
documents, and 200 positive qrel rows, with exactly one positive document per
query. Current diagnostics show BM25 as the strongest top-rank profile,
`reranking_hybrid` as tied with BM25 on recall@100, and dense retrieval as much
weaker for full-document matching.

## Details

### What the Original Data Measures

MLDR was introduced with the M3-Embedding work as a multilingual long-document
retrieval benchmark. The dataset card describes a construction process in which
long documents are sampled, a paragraph is selected, and a specific question is
generated from that paragraph. The positive is the full article containing the
answer-bearing paragraph.

For English, this creates a long-document retrieval task rather than a passage
retrieval task. A model must retrieve the entire article from a question that
may only correspond to a small local section. The benchmark therefore stresses
long-document indexing, paragraph-to-document matching, and robustness to
documents whose main topic is broader than the query.

### Observed Data Profile

The Nano split contains 200 queries, 10,000 documents, and 200 positive qrel
rows. Every query has exactly one positive document. Queries average 64.06
characters, while documents average 27,991.90 characters. This is one of the
longest NanoMLDR splits and makes full-document representation difficult.

Observed questions cover rare-earth elements, jazz reissue labels, PCR
limitations, UN Security Council Resolution 242, composite bows, protein
engineering, aviation events, aquarium conservation, taxonomy, constitutional
law, and other article-level topics. The question is specific, but the positive
document can contain tens of thousands of characters of surrounding context.

### BM25 Evaluation Profile

The dataset-provided BM25 candidate subset contains 500 candidates per query and
achieves nDCG@10 = 0.7254, hit@10 = 0.8300, and recall@100 = 0.9300. BM25 is the
strongest observed top-rank profile. Long English articles preserve many rare
terms, names, dates, technical phrases, and paragraph-specific expressions from
the generated question.

This is a setting where lexical matching is highly valuable. If the question is
grounded in a paragraph about PCR, a UN resolution, a bow design, or a protein
engineering method, the full article often contains exact anchor terms that
BM25 can use even when the answer paragraph is buried deep in the text.

### Dense Evaluation Profile

The dense `harrier_oss_v1_270m` candidate subset contains 500 candidates per
query and achieves nDCG@10 = 0.4611, hit@10 = 0.5400, and recall@100 = 0.7200.
Dense retrieval is much weaker than BM25. A single dense representation of a
very long article can dilute the paragraph-level evidence needed for retrieval.

Dense similarity may capture broad article themes but miss the precise local
fact that generated the question. This is especially problematic when several
long articles share the same high-level domain, such as biology, law, military
history, or music history, but only one contains the answer-bearing paragraph.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset contains mostly 100 candidates per
query, with 14 queries using a rank-101 safeguard row. It achieves nDCG@10 =
0.5916, hit@10 = 0.7250, and recall@100 = 0.9300. Hybrid retrieval matches BM25
on recall@100 but remains below BM25 on top-rank metrics.

This profile suggests that dense candidates add some useful coverage but do not
improve the observed top ranking over BM25. For English MLDR, hybrid search is
most useful as a candidate pool for reranking, while BM25 remains the strongest
base ranker in the current diagnostics.

### Metric Interpretation for Model Researchers

This task is single-positive: each query has exactly one relevant long
document. Hit@10 measures whether that document appears near the top. nDCG@10
is sensitive to the exact rank of the positive document, and recall@100 measures
whether it survives for reranking.

The English MLDR pattern is a direct test of long-document retrieval. Strong
performance requires preserving paragraph-specific evidence inside long
documents. Single-vector dense retrieval is not enough here; systems should
consider chunked indexing, late interaction, multi-vector representations, or
paragraph-aware document aggregation.

### Query and Relevance Type Tendencies

Queries are English paragraph-grounded fact questions about people, methods,
limitations, legal or diplomatic statements, technical steps, historical
records, and scientific properties. They are often specific but not necessarily
aligned with the article title.

Relevant documents are very long English articles containing the answer-bearing
paragraph. The task rewards exact rare-term matching, entity preservation,
paragraph-to-document linking, and robust ranking among topically adjacent long
articles.

### Representative Failure Modes

Dense retrieval can return a thematically related article while missing the one
paragraph that actually contains the answer. Long documents about similar
scientific, legal, historical, or cultural subjects can collapse into nearby
embedding space. BM25 can fail when the question paraphrases the paragraph or
when many articles share the same rare entity or technical term.

Hybrid retrieval can include the positive but still rank another broad article
higher. Rerankers should inspect chunks or paragraphs rather than scoring only
the full article text as one unit.

### Training Data That May Help

Useful training data includes English long-document QA retrieval pairs, English
Wikipedia article retrieval, NarrativeQA-style long-document evidence retrieval,
and entity-sharing article hard negatives. Training should include cases where a
small paragraph determines the relevance of a long article.

Synthetic data can help when it samples paragraphs from long English
encyclopedic articles, generates grounded fact questions, and uses the full
article as the positive. Hard negatives should be topically adjacent full
articles that share names, dates, methods, or scientific terms but do not
contain the answer-bearing paragraph.

### Model Improvement Notes

Dense retrievers should move beyond single-vector full-article encoding.
Chunked retrieval, paragraph-aware pooling, late interaction, or multi-vector
document representations are better matched to English MLDR. Sparse systems
should preserve rare lexical anchors while reducing over-ranking from repeated
boilerplate or broad topic terms.

For hybrid systems, `NanoMLDR / en` suggests starting from BM25 as a strong
candidate generator and adding dense signals carefully. The current hybrid
profile preserves recall but does not beat BM25 top-rank quality, so reranking
must be evaluated against the sparse baseline.

## Example Data

| Query | Positive document |
| --- | --- |
| Who was the last person mentioned in the text? [46 chars] | Chronological Classics was a French compact disc reissue label. Gilles Pétard, the original owner, intended to release the complete master takes of all jazz and swing recordings that were issued on 78 rpm. By the time the label suspended operations in July 2008, its scope had extended to LPs. Pétard also started the label R&B Classics to reissue postwar rhythm & blues recordings. An unaffiliated label, Neatworks, released alternate takes and misidentified master takes of jazz artists previously issued on Chronological Classics. In 1999, Chronological Classics issued a CD set that included tracks previously unavailable in the regular series and a bonus CD with corrected tracks from previous releases. The jazz series started with number 500 and includes the following albums: 500 – 599 24 Complementary Track (3 CDs) 99 The Classics Collection (The Classics Sampler) [VA 20 Tracks] 500 Ella Fitzgerald 1935–37 501 Jimmie Lunceford 1930–34 502 Chick Webb 1929–34 503 Count Basie 1936–38 504 Co... [1,000 / 31,958 chars] |
| What is one major limitation of PCR? [36 chars] | Polymerase chain reaction (PCR) is a method widely used to rapidly make millions to billions of copies (complete copies or partial copies) of a specific DNA sample, allowing scientists to take a very small sample of DNA and amplify it (or a part of it) to a large enough amount to study in detail. PCR was invented in 1983 by the American biochemist Kary Mullis at Cetus Corporation; Mullis and biochemist Michael Smith, who had developed other essential ways of manipulating DNA, were jointly awarded the Nobel Prize in Chemistry in 1993. PCR is fundamental to many of the procedures used in genetic testing and research, including analysis of ancient samples of DNA and identification of infectious agents. Using PCR, copies of very small amounts of DNA sequences are exponentially amplified in a series of cycles of temperature changes. PCR is now a common and often indispensable technique used in medical laboratory research for a broad variety of applications including biomedical research and... [1,000 / 49,157 chars] |
| What did Ambassador Goldberg say about the US view of Jordan? [61 chars] | United Nations Security Council Resolution 242 (S/RES/242) was adopted unanimously by the UN Security Council on November 22, 1967, in the aftermath of the Six-Day War. It was adopted under Chapter VI of the UN Charter. The resolution was sponsored by British ambassador Lord Caradon and was one of five drafts under consideration. The preamble refers to the "inadmissibility of the acquisition of territory by war and the need to work for a just and lasting peace in the Middle East in which every State in the area can live in security". Operative Paragraph One "Affirms that the fulfillment of Charter principles requires the establishment of a just and lasting peace in the Middle East which should include the application of both the following principles: (i) Withdrawal of Israeli armed forces from territories occupied in the recent conflict; (ii) Termination of all claims or states of belligerency and respect for and acknowledgment of the sovereignty, territorial integrity and political in... [1,000 / 44,540 chars] |

### Public Sources

- [M3-Embedding: Multi-Linguality, Multi-Functionality, Multi-Granularity Text Embeddings Through Self-Knowledge Distillation](https://arxiv.org/abs/2402.03216),
  2024.
- [M3-Embedding ACL Anthology version](https://aclanthology.org/2024.findings-acl.137/),
  2024.
- [Shitao/MLDR dataset card](https://huggingface.co/datasets/Shitao/MLDR).
- [hakari-bench/NanoMLDR](https://huggingface.co/datasets/hakari-bench/NanoMLDR),
  Nano benchmark dataset.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| M3-Embedding: Multi-Linguality, Multi-Functionality, Multi-Granularity Text Embeddings Through Self-Knowledge Distillation | 2024 | benchmark paper | [https://arxiv.org/abs/2402.03216](https://arxiv.org/abs/2402.03216) |
| M3-Embedding ACL Anthology version | 2024 | paper | [https://aclanthology.org/2024.findings-acl.137/](https://aclanthology.org/2024.findings-acl.137/) |
| MLDR: Multilingual Long-Document Retrieval dataset | 2024 | dataset card | [https://huggingface.co/datasets/Shitao/MLDR](https://huggingface.co/datasets/Shitao/MLDR) |

### Representative Snippets

| Query pattern | Positive document pattern |
| --- | --- |
| A question asking who the last person mentioned in a text was. | A long article about a jazz reissue label and associated people. |
| A question asking for one major limitation of PCR. | A long article about polymerase chain reaction. |
| A question asking what an ambassador said about Jordan. | A long article about UN Security Council Resolution 242. |
| A question asking the period of Roman stiffeners. | A long article about composite bows. |
| A question asking the first step in a DNA recombination method. | A long article about protein engineering. |
