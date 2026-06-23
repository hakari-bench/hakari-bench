# NanoMuPLeR

## Overview

NanoMuPLeR is a language-specific translated/parallel legal retrieval benchmark
for MuPLeR-retrieval. It derives from European Union legal text and covers 14
European languages: Greek, English, Spanish, Finnish, French, Italian,
Lithuanian, Latvian, Dutch, Polish, Portuguese, Slovak, Slovenian, and Swedish.
Each split contains same-language synthetic legal queries and DGT-Acquis-derived
parallel legal passages.

The group contains 2,800 queries, 140,000 task-local documents, and 2,800
positive qrel rows. Every language has exactly 200 queries, 10,000 documents,
and one positive per query. This parallel construction makes NanoMuPLeR useful
for comparing whether a retrieval model preserves legal-search quality across
languages, scripts, morphology, and translation variation.

## What This Group Measures

The group measures focused legal passage retrieval in a controlled multilingual
setup. Queries ask about legal conditions, treaty interpretation, state aid,
procurement, import duties, nuclear policy, pre-accession rules, and EU
institutional procedure. Documents are medium-length legal passages rather than
full acts. The relevance relation is exact: the model must find the one passage
that answers the legal query in the same language.

Because the underlying passages and questions are parallel across languages,
the group is not simply a collection of unrelated monolingual legal tasks. It
tests whether a model can maintain retrieval quality when legal terminology is
expressed through different morphology, word order, scripts, and translation
choices. This is especially useful for diagnosing English-centric models on EU
legal text.

## Task Families

- **Parallel EU legal retrieval:** all fourteen tasks retrieve same-language
  legal passages derived from DGT-Acquis.
- **Single-positive passage ranking:** every query has exactly one relevant
  passage, so nDCG@10 and hit@10 reflect precise ranking of one target.
- **Multilingual legal terminology:** the tasks preserve EU legal references,
  dates, directive numbers, percentages, institutions, and member-state names
  across languages.

## Dataset Shape

The group is highly regular. Each language split has 200 queries, 10,000
candidate passages, and 200 qrel rows. The group-level document count is the sum
of language-local pools; the parallel construction means many passages have
translated counterparts across languages, but evaluation is same-language within
each split.

The queries are medium length and the documents are compact legal passages.
This is not long-document retrieval, but the text is dense. Many wrong
documents share legal vocabulary, EU institutions, and regulatory phrasing. A
model must distinguish the exact actor, condition, threshold, date, article, or
procedure that makes one passage relevant.

## Retrieval Behavior

### BM25 Profile

BM25 is strong but not best for any language in the current Nano data. The
query-weighted BM25 nDCG@10 is 0.7994, and several languages are above 0.83:
Dutch, Swedish, Polish, Latvian, Spanish, Portuguese, and Finnish. This reflects
the lexical nature of EU legal retrieval. Directive numbers, state names,
institution names, percentages, and legal terms often appear in both the query
and the relevant passage.

BM25 is weakest on English and Slovak, with English at 0.6453 nDCG@10 and
Slovak at 0.7041. The English result is a useful warning: even in a legal
dataset with many lexical anchors, synthetic queries can paraphrase the passage
enough that exact term frequency alone is insufficient. BM25 is therefore a
strong legal baseline, but not the best overall retrieval strategy.

### Dense Profile

Dense retrieval with `harrier-oss-270m` is best for English and competitive for
most other languages. English rises from 0.6453 BM25 nDCG@10 to 0.8477 dense
nDCG@10, showing that embedding similarity helps when the legal query and
passage use different wording. Dense is also high for Spanish, Dutch,
Portuguese, Swedish, and French.

Dense is not uniformly better than BM25. It trails BM25 in Finnish, Lithuanian,
Latvian, Dutch, Polish, and Slovenian. This suggests that exact legal wording
and morphology-aware lexical evidence remain valuable, especially in languages
where the dense model's representation does not fully capture the legal
condition. The group-level dense nDCG@10 is 0.8158.

### Reranking Hybrid Profile

The reranking hybrid profile is the strongest group-level profile: 0.8554
nDCG@10, 0.9300 hit@10, and 0.9914 recall@100. It is best for thirteen of the
fourteen languages, with English as the main dense-led exception. Hybrid
retrieval works well here because legal passage search needs both exact legal
anchors and semantic matching of the condition expressed in the query.

This group is one of the clearest examples where hybrid search is the preferred
default. The task is single-positive, so recall@100 close to 1.0 means the
combined candidate set almost always contains the right passage. The remaining
challenge is top-rank ordering among legally similar passages with overlapping
EU vocabulary.

## Task Summary

| Task | Family | Language | Queries | Docs | Positives | Positives/query | BM25 nDCG@10 | Dense nDCG@10 | Reranking hybrid nDCG@10 | Best profile |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| [el](el.md) | EU legal retrieval | `el` | 200 | 10,000 | 200 | 1.00 | 0.7749 | 0.7834 | 0.8390 | Reranking hybrid |
| [en](en.md) | EU legal retrieval | `en` | 200 | 10,000 | 200 | 1.00 | 0.6453 | 0.8477 | 0.7986 | Dense |
| [es](es.md) | EU legal retrieval | `es` | 200 | 10,000 | 200 | 1.00 | 0.8302 | 0.8803 | 0.8862 | Reranking hybrid |
| [fi](fi.md) | EU legal retrieval | `fi` | 200 | 10,000 | 200 | 1.00 | 0.8230 | 0.7955 | 0.8682 | Reranking hybrid |
| [fr](fr.md) | EU legal retrieval | `fr` | 200 | 10,000 | 200 | 1.00 | 0.8179 | 0.8329 | 0.8628 | Reranking hybrid |
| [it](it.md) | EU legal retrieval | `it` | 200 | 10,000 | 200 | 1.00 | 0.7920 | 0.8257 | 0.8422 | Reranking hybrid |
| [lt](lt.md) | EU legal retrieval | `lt` | 200 | 10,000 | 200 | 1.00 | 0.8115 | 0.7495 | 0.8442 | Reranking hybrid |
| [lv](lv.md) | EU legal retrieval | `lv` | 200 | 10,000 | 200 | 1.00 | 0.8376 | 0.7910 | 0.8672 | Reranking hybrid |
| [nl](nl.md) | EU legal retrieval | `nl` | 200 | 10,000 | 200 | 1.00 | 0.8909 | 0.8580 | 0.9072 | Reranking hybrid |
| [pl](pl.md) | EU legal retrieval | `pl` | 200 | 10,000 | 200 | 1.00 | 0.8400 | 0.8299 | 0.8909 | Reranking hybrid |
| [pt](pt.md) | EU legal retrieval | `pt` | 200 | 10,000 | 200 | 1.00 | 0.8222 | 0.8552 | 0.8895 | Reranking hybrid |
| [sk](sk.md) | EU legal retrieval | `sk` | 200 | 10,000 | 200 | 1.00 | 0.7041 | 0.7714 | 0.7872 | Reranking hybrid |
| [sl](sl.md) | EU legal retrieval | `sl` | 200 | 10,000 | 200 | 1.00 | 0.7455 | 0.7428 | 0.7983 | Reranking hybrid |
| [sv](sv.md) | EU legal retrieval | `sv` | 200 | 10,000 | 200 | 1.00 | 0.8563 | 0.8576 | 0.8946 | Reranking hybrid |

## Interpretation Notes for Model Researchers

NanoMuPLeR is a controlled test of multilingual legal retrieval. Because every
language has the same query count, document count, and positive density, score
differences are easier to interpret than in mixed-domain groups. Strong
performance indicates that a model can match precise legal conditions across EU
languages, not merely retrieve topical legal documents.

The retrieval-profile pattern is also clear. BM25 is a strong legal baseline,
dense retrieval helps especially when the query paraphrases the passage, and
hybrid retrieval is usually best because it combines exact legal anchors with
semantic condition matching. English is the exception in this Nano slice, where
dense retrieval is strongest.

## Training and Leakage Notes

Useful training data includes non-overlapping EUR-Lex and DGT-Acquis passage
retrieval, multilingual legal QA, legal passage reranking data, and parallel EU
legal bitext with hard negatives from nearby provisions. Synthetic legal queries
can help if they preserve the exact legal condition and do not turn the task
into vague topical retrieval.

Leakage control should account for parallel documents. Training should exclude
MuPLeR evaluation queries, positives, and translated equivalents across
languages. Hard negatives should share institutions, dates, directives, and
legal topics while differing in the actual condition, actor, threshold, or
procedural rule.

## Public Sources

- [mteb/MuPLeR-retrieval](https://huggingface.co/datasets/mteb/MuPLeR-retrieval).
- [DGT-Acquis](https://joint-research-centre.ec.europa.eu/language-technology-resources/dgt-acquis_en).
- [An overview of the European Union's highly multilingual parallel corpora](https://link.springer.com/article/10.1007/s10579-014-9277-0), 2014.
- [Massive Text Embedding Benchmark](https://github.com/embeddings-benchmark/mteb).

### Source Reference Table

| Source | Year | Type | URL |
| --- | ---: | --- | --- |
| mteb/MuPLeR-retrieval |  | dataset card | [https://huggingface.co/datasets/mteb/MuPLeR-retrieval](https://huggingface.co/datasets/mteb/MuPLeR-retrieval) |
| DGT-Acquis |  | source corpus page | [https://joint-research-centre.ec.europa.eu/language-technology-resources/dgt-acquis_en](https://joint-research-centre.ec.europa.eu/language-technology-resources/dgt-acquis_en) |
| An overview of the European Union's highly multilingual parallel corpora | 2014 | source reference paper | [https://link.springer.com/article/10.1007/s10579-014-9277-0](https://link.springer.com/article/10.1007/s10579-014-9277-0) |
| Massive Text Embedding Benchmark |  | benchmark repository | [https://github.com/embeddings-benchmark/mteb](https://github.com/embeddings-benchmark/mteb) |
