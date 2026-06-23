# NanoJMTEB-v2 / mintaka_ja

## Overview

`NanoJMTEB-v2 / mintaka_ja` is the Japanese Nano split derived from Mintaka, a
complex multilingual question answering dataset. In this retrieval version, a
Japanese question must retrieve the short answer entity label from a compact
document set. The task is therefore closer to entity-answer retrieval than to
passage retrieval: documents are names such as people, places, films, albums,
or songs, not evidence passages. The Nano split has 200 queries, 1,592
documents, and exactly one positive answer per query. Current diagnostics show
a strongly semantic profile: dense retrieval is best, the `reranking_hybrid`
candidate set improves over BM25, and BM25 is limited because the answer label
often does not appear in the question.

## Details

### What the Original Data Measures

Mintaka was introduced as a complex, natural, multilingual dataset for end-to-
end question answering. The paper describes English questions collected from
crowd workers, annotated with Wikidata entities, and translated into additional
languages including Japanese. It emphasizes complex question types such as
comparative, superlative, ordinal, count, intersection, difference, multi-hop,
and yes/no questions.

The JMTEB and MTEB retrieval setup keeps the Japanese question side and uses
entity-type answers as retrieval targets, excluding answers that are only
numbers or booleans. In this Nano task, the documents are short answer labels.
The benchmark therefore tests whether a retrieval model can map a complex
Japanese question to the correct entity name, often without surface overlap
between the query and the target label.

### Observed Data Profile

The Nano split contains 200 queries, 1,592 documents, and 200 positive qrel
rows. Each query has one positive label, with no multi-positive queries.
Queries average 35.19 characters. Documents average only 9.17 characters,
reflecting the fact that the corpus is made of compact entity labels rather
than passages.

Representative examples ask for the second film in a franchise, a film linked
to U2's soundtrack work, an album in relation to the Beatles, the longest film
in the Twilight series, or the first wife of the director of Jaws. The positive
documents are short labels such as a film title, album title, or person name.
The task is compact but demanding because most of the evidence needed to select
the label is world knowledge or relation reasoning, not wording shared with the
document.

### BM25 Evaluation Profile

The dataset-provided BM25 candidate subset contains 500 candidates per query and
achieves nDCG@10 = 0.2561, hit@10 = 0.3800, and recall@100 = 0.4600. These
scores are much lower than on many lexical retrieval tasks. The reason is
structural: a short answer label often has little or no overlap with the
question. If the query asks for the first film in a franchise, the correct film
title may not occur in the question at all.

BM25 can still help when the answer label is partially named in the question or
when a title contains shared franchise terms. But for many Mintaka-style
questions, lexical frequency is the wrong primary signal. The query expresses a
relationship or constraint, while the document is only the final entity label.
This makes `mintaka_ja` a useful negative example for systems that depend too
heavily on sparse matching.

### Dense Evaluation Profile

The dense `harrier_oss_v1_270m` candidate subset contains 500 candidates per
query and achieves nDCG@10 = 0.3687, hit@10 = 0.4650, and recall@100 = 0.5900.
Dense retrieval is the strongest observed profile. Its advantage over BM25 fits
the task: embedding similarity can connect questions and answer labels through
semantic association, entity knowledge, and multilingual QA patterns rather
than exact word overlap.

The absolute scores remain moderate. This is expected because the documents are
very short labels, which provide little context for embedding models. A dense
retriever must place the correct label above many plausible entities without
seeing an evidence passage. The task therefore tests not just semantic
similarity, but whether entity labels have learned representations that are
useful for relation-style questions.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset contains 100 or 101 candidates per
query, with 86 safeguard positive rows and a mean of 100.43 candidates. It
achieves nDCG@10 = 0.3354, hit@10 = 0.4400, and recall@100 = 0.5700. This is
better than BM25 but below dense retrieval across the main metrics.

The hybrid pattern shows that lexical evidence is not useless, but it is not
the leading signal. Combining BM25 and dense retrieval recovers some positives
that sparse retrieval alone misses, yet the dense candidate set remains the
best direct profile. The large number of safeguard rows also indicates that
candidate construction often needs help to keep positives available in a
top-100 reranking pool. For reranking experiments, `mintaka_ja` is a stress test
of answer-label candidate generation.

### Metric Interpretation for Model Researchers

With one positive label per query, hit@10 asks whether the correct answer label
appears among the first ten results, while nDCG@10 rewards ranking it closer to
the top. Recall@100 is especially important because a reranker cannot recover a
label that candidate generation fails to include.

The metric pattern is instructive: dense is best, BM25 is weakest, and hybrid
lands between them. This means `mintaka_ja` is a good diagnostic for models
that claim to support semantic entity retrieval or complex QA retrieval. It is
less a test of passage understanding and more a test of mapping a question's
constraints to a compact entity label.

### Query and Relevance Type Tendencies

Queries are translated Japanese complex QA questions. They ask about ordered
items, comparisons, relation chains, franchise membership, creators, spouses,
film or album metadata, and other entity-centric facts. The relevance target is
the answer label itself, not a document that explains why the answer is correct.

This setup rewards models with strong entity representations, relation
awareness, and multilingual QA grounding. It penalizes systems that require the
answer to be repeated in the query or depend on long document context to infer
relevance.

### Representative Failure Modes

BM25 fails when the answer label is absent from the query, which is common.
Dense retrieval may still fail by selecting a related entity from the same
franchise, film series, artist catalog, or biography. Hybrid retrieval can
inherit sparse false positives when a shared title word appears in the wrong
label, and it can still miss labels whose semantic association is too indirect.

Another failure mode comes from short documents. Because labels provide almost
no explanatory context, even a reranker has little text to compare against the
query. Systems may need external entity knowledge or training on similar
question-to-label retrieval to resolve these cases reliably.

### Training Data That May Help

Helpful training data includes Japanese entity QA, multilingual Mintaka-style
question-answer pairs, Wikidata-linked QA, entity linking, and hard negatives
made of plausible but wrong labels. Training should include complex question
types such as comparative, superlative, ordinal, multi-hop, first/last, and
intersection questions.

When reporting benchmark results, training should exclude the Mintaka examples
represented in this Nano split and avoid using exact evaluation question-label
pairs. Synthetic data can help if it pairs realistic Japanese complex questions
with short labels rather than full explanatory passages.

### Model Improvement Notes

Dense retrievers can improve by learning stronger representations for entity
labels and by aligning relation-style questions with answer names. Sparse
systems have limited headroom unless the query includes title overlap, but good
handling of Japanese titles, katakana names, and franchise terms can still
help. Rerankers need either strong prior knowledge encoded in the model or
candidate labels enriched by external descriptions; with raw short labels
alone, there is little textual evidence to inspect.

For hybrid search systems, this task suggests that dense retrieval should carry
more weight than BM25. Sparse matches can provide useful shortcuts, but the
central problem is semantic and entity-oriented.

## Example Data

| Query | Positive document |
| --- | --- |
| ジュラシック・パークの第2作目の映画の名前は何というですか？ [30 chars] | ジュラシック・ワールド/炎の王国 [16 chars] |
| 荒れ放題のホテルを本拠とし、U2が映画のサウンドトラックの作曲を手掛けた映画は何でしたか？ [45 chars] | ミリオンダラー・ホテル [11 chars] |
| どのアルバムはビートルズと一緒にレコードしたなかったでしょうか？ [32 chars] | アビイ・ロード [7 chars] |
| 映画『トワイライト』シリーズで一番長い映画は？ [23 chars] | ニュームーン/トワイライト・サーガ [17 chars] |
| ジョーズの監督の最初の奥さんは誰？ [17 chars] | エイミー・アーヴィング [11 chars] |

### Public Sources

- [Mintaka: A Complex, Natural, and Multilingual Dataset for End-to-End Question Answering](https://aclanthology.org/2022.coling-1.138/),
  COLING 2022.
- [amazon-science/mintaka](https://github.com/amazon-science/mintaka), source
  repository.
- [sbintuitions/JMTEB](https://huggingface.co/datasets/sbintuitions/JMTEB),
  Japanese embedding benchmark card.
- [hakari-bench/NanoJMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoJMTEB-v2),
  Nano benchmark dataset.
- [mteb/MintakaRetrieval](https://huggingface.co/datasets/mteb/MintakaRetrieval),
  source task dataset.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Mintaka: A Complex, Natural, and Multilingual Dataset for End-to-End Question Answering | 2022 | paper | [https://aclanthology.org/2022.coling-1.138/](https://aclanthology.org/2022.coling-1.138/) |
| amazon-science/mintaka | 2022 | repository | [https://github.com/amazon-science/mintaka](https://github.com/amazon-science/mintaka) |
| sbintuitions/JMTEB | 2024 | dataset card | [https://huggingface.co/datasets/sbintuitions/JMTEB](https://huggingface.co/datasets/sbintuitions/JMTEB) |

### Representative Snippets

| Query pattern | Positive document pattern |
| --- | --- |
| A Japanese question asking for the name of the second film in the Jurassic Park franchise. | A short Japanese film-title label for the correct franchise entry. |
| A question about a film set around a dilapidated hotel whose soundtrack was composed by U2. | A short film-title label. |
| A question asking which album was recorded with the Beatles. | A compact album-title label. |
| A question asking for the longest film in the Twilight series. | A short title label for the corresponding Twilight film. |
| A question asking who was the first wife of the director of Jaws. | A short person-name label. |
