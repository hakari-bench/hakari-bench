# NanoMTEB-German / german_dpr

## Overview

`german_dpr` is a German open-domain passage retrieval task derived from
GermanDPR. Queries are German fact questions, and documents are German Wikipedia
passages. The Nano split contains 200 queries, 2,876 documents, and 200
positive qrels, with exactly one positive passage per query. Queries average
63.735 characters, while documents average 1,290.31 characters. The task is a
German analogue of DPR-style QA retrieval: a model must rank the passage that
contains the answer evidence, often without an exact wording match between the
question and passage.

## Details

### What the Original Data Measures

[GermanQuAD and GermanDPR: Improving Non-English Question Answering and Passage Retrieval](https://arxiv.org/abs/2104.12741)
introduced GermanQuAD and GermanDPR to improve non-English QA and dense passage
retrieval. GermanDPR adapts German question-answer data into a retrieval setup
with German Wikipedia passages and hard negatives. The benchmark evaluates
whether a retriever can find an answer-bearing passage for a German question.

The task is closer to open-domain QA retrieval than to topical search. The
positive passage must support the answer, not merely discuss the same entity.
This makes it useful for testing German question understanding, entity
grounding, and passage-level semantic matching.

### Observed Data Profile

The split has 200 German queries, 2,876 documents, and 200 positive judgments.
Every query has one positive. Questions are usually short fact questions asking
"which", "when", "what", "where", or "why" style information. Documents are
German Wikipedia passages, often with a title prefix and compact explanatory
text.

Examples include questions about the death penalty in Iowa, university senate
membership, USB power supply, public transport in London, and the crash of a
Boeing 747 near Guam. The evidence may be a specific sentence inside a broader
article passage.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.4647, hit@10 of 0.8150, and recall@100 of 0.9800.
This shows that lexical matching is a strong candidate-generation signal in
German Wikipedia QA. Entity names, dates, technical terms, and title tokens
often overlap between the question and the answer passage.

However, BM25 is much weaker than dense retrieval at top-10 ranking. It can
retrieve the answer passage somewhere in the candidate list, but it may rank
lexically similar passages above the true answer-bearing one. German morphology
and paraphrase also reduce exact-match reliability.

### Dense Evaluation Profile

Dense retrieval is the strongest top-10 profile, with nDCG@10 of 0.7837,
hit@10 of 0.9450, and recall@100 of 0.9550. The dense model substantially
improves early ranking by aligning German question intent with passage meaning.
It can connect a concise question to answer evidence even when the passage uses
different wording or contains the answer inside a broader context.

The slight recall@100 deficit relative to BM25 shows that dense retrieval is
not universally safer as a candidate generator. It ranks better when it finds
the target, but BM25 still recovers a few positives that dense misses within
the first 100.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` profile reaches nDCG@10 of 0.6120, hit@10 of 0.9050,
and recall@100 of 1.0000. It has the best recall coverage, while dense remains
best for top-10 ordering. There are no safeguard rank-101 rows, so all positives
are naturally covered within the hybrid top-100 pool.

This is a useful hybrid-search case: lexical matching protects recall, dense
matching improves semantic coverage, and the combined candidate pool gives a
reranker complete opportunity to recover every positive. The top ranking still
needs a stronger reranking stage to match dense nDCG@10.

### Metric Interpretation for Model Researchers

`german_dpr` is dense-favorable at top-10 and hybrid-favorable for recall.
BM25 is strong enough to serve as a baseline candidate generator, but dense
retrieval better ranks answer-bearing passages. The hybrid profile is
especially relevant for reranking experiments because it reaches full
recall@100.

Since every query has exactly one positive, hit@10 is a straightforward measure
of whether the answer passage reaches an early result page. nDCG@10 adds rank
sensitivity, and recall@100 measures whether a downstream reader or reranker
can still recover the answer.

### Query and Relevance Type Tendencies

Queries are German fact questions over entities, institutions, dates, devices,
transport, geography, history, science, and events. Positive documents are
Wikipedia passages containing the answer evidence. Some questions are anchored
by entity names, while others depend on paraphrased relations or background
knowledge.

Relevance is evidence-based. A passage about the same topic is not necessarily
positive unless it contains the answer. This favors training with hard negatives
from the same article or nearby entities.

### Representative Failure Modes

BM25 can over-rank passages with shared names or title terms that do not contain
the answer. Dense retrieval can miss rare entities, technical terms, or exact
dates when semantic similarity is too broad. Hybrid retrieval can recover the
positive but still place it behind lexically attractive distractors.

Another failure mode is answer evidence buried in a longer passage. Models that
pool passages poorly may represent the broad article topic rather than the
specific answer sentence.

### Training Data That May Help

Useful training data includes non-overlapping GermanDPR train pairs, GermanQuAD
train contexts reformatted for retrieval, German Wikipedia question-to-passage
pairs, and German Wikipedia hard negatives selected by BM25 or dense retrieval.
Training should exclude GermanDPR test data, Nano queries, qrels, and positive
passages likely to overlap with the evaluation split.

Synthetic data should generate German Wikipedia-style passages with titles and
explicit answer evidence, then produce self-contained German fact questions
over entities, dates, counts, definitions, and locations. Negatives should be
topically close but answer a different question.

### Model Improvement Notes

Dense models should preserve German morphology, entity identity, and answer
evidence while avoiding broad topical matching. Hybrid systems should use BM25
for recall and a semantic reranker for top-ordering. Passage encoders can
benefit from training that emphasizes answer-bearing sentences inside longer
Wikipedia contexts.

## Example Data

| Query | Positive document |
| --- | --- |
| Seit wann gibt es in Iowa keine Todesstrafe mehr? [49 chars] | Todesstrafe_in_den_Vereinigten_Staaten In der Geschichte Iowas gab es 46 Hinrichtungen, davon 43 wegen Mord und drei wegen Vergewaltigung. Alle Getöteten waren Männer. 1872 wurde die Todesstrafe erstm... [200 / 538 chars] |
| Welche Personen sitzen im akademischen Senat? [45 chars] | Universität An der Spitze einer Universität steht ein Rektor oder Präsident, der in der Regel selbst ein Universitätsprofessor ist. Er wird üblicherweise unterstützt von mehreren Prorektoren beziehung... [200 / 1,042 chars] |
| Für welche Geräte konnte USB 1.0 auch als Stromzufuhr eingesetzt werden? [73 chars] | Universal_Serial_Bus Schon mit USB 1.0 war eine Stromversorgung angeschlossener Geräte über die USB-Kabelverbindungen möglich. Allerdings war die maximale Leistung nur für Geräte mit geringem Strombed... [200 / 896 chars] |
| Welche Institution organisiert den öffentlichen Verkehr in London? [66 chars] | London London ist Dreh- und Angelpunkt des Straßen-, Schienen- und Luftverkehrs im Vereinigten Königreich. Das Verkehrswesen fällt in die direkte Zuständigkeit des Mayor of London, des Oberbürgermeist... [200 / 617 chars] |
| Was war der Grund für den Absturz der Boeing 747-300 über Guam 1997? [68 chars] | Guam Am 6. August 1997 wurde eine Boeing 747-300 der Korean Airlines auf dem Korean-Air-Flug 801 von Seoul nach Agana (Guam) bei heftigem Regen gegen einen Hügel 5 km vor dem Flughafen Hagåtña gefloge... [200 / 1,542 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| GermanQuAD and GermanDPR: Improving Non-English Question Answering and Passage Retrieval | 2021 | Paper | [https://arxiv.org/abs/2104.12741](https://arxiv.org/abs/2104.12741) |
| GermanQuAD and GermanDPR ACL Anthology record | 2021 | Proceedings paper | [https://aclanthology.org/2021.mrqa-1.4/](https://aclanthology.org/2021.mrqa-1.4/) |
| mteb/GermanDPR | 2025 | Dataset card | [https://huggingface.co/datasets/mteb/GermanDPR](https://huggingface.co/datasets/mteb/GermanDPR) |

### Representative Snippets

| Query | Positive document excerpt |
| --- | --- |
| Seit wann gibt es in Iowa keine Todesstrafe mehr? | A German Wikipedia passage on capital punishment in the United States and Iowa abolitions. |
| Welche Personen sitzen im akademischen Senat? | A university passage explaining rector, president, vice presidents, and academic bodies. |
| Fur welche Gerate konnte USB 1.0 auch als Stromzufuhr eingesetzt werden? | A Universal Serial Bus passage describing early USB power for low-power devices. |
| Welche Institution organisiert den offentlichen Verkehr in London? | A London passage describing transport responsibility and the Mayor of London. |
| Was war der Grund fur den Absturz der Boeing 747-300 uber Guam 1997? | A Guam passage about Korean Air Flight 801 and the crash circumstances. |
