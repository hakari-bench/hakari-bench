# MNanoBEIR / NanoBEIR-de / NanoArguAna

## Overview

NanoBEIR-de / NanoArguAna is the German NanoBEIR version of ArguAna, an
argument retrieval benchmark where the query is a long argument and the
relevant document is its best counterargument. The original task is introduced
in [Retrieval of the Best Counterargument without Prior Topic
Knowledge](https://aclanthology.org/P18-1023/). This Nano task contains 50
German translated query arguments, 3,635 German translated candidate arguments,
and exactly one positive counterargument per query. Both queries and documents
are long, averaging more than 1,100 characters. The task tests whether a
retriever can identify stance opposition and argumentative fit, not just topical
similarity. Dense retrieval is the strongest top-rank signal, while
`reranking_hybrid` gives the best top-100 candidate coverage.

## Details

### What the Original Data Measures

ArguAna frames retrieval as finding a counterargument that addresses the same
controversial issue and aspect as the query argument while taking the opposite
stance. The important relation is rebuttal or counterargumentation. A document
that discusses the same topic but supports the same side is not the target.

The German NanoBEIR version keeps that objective in translated form. The input
is a long German argument with claims, premises, examples, and sometimes
citations. The relevant document is a German counterargument that contests the
same issue. This makes the task useful for evaluating long-document embeddings
and stance-aware retrieval.

### Observed Data Profile

The metadata records 50 queries, 3,635 documents, and 50 positive qrels. Every
query has exactly one positive. Query text averages 1,243.08 characters, and
document text averages 1,142.27 characters. Examples cover House of Lords
reform, Heathrow expansion, choice overload, cyber attacks by non-state actors,
religious speech, gender roles, economic outcomes, reparations, Syria, and free
higher education.

The long text shape gives the model many topical cues, but it also creates many
distractors. A same-topic passage may share vocabulary with the query while
arguing for the wrong side. The retrieval target is the argumentative move:
which document best counters the query's reasoning.

### BM25 Evaluation Profile

The BM25 candidate subset reaches nDCG@10 = 0.3453, hit@10 = 0.5600, and
Recall@100 = 0.9200. BM25 can identify the debate neighborhood because long
arguments repeat issue terms, named entities, policy words, and evidence
phrases. It is useful for preserving topic anchors in very long German text.

BM25's weakness is stance and rebuttal selection. Counterarguments and
supporting arguments often share the same vocabulary, so sparse matching can
rank a same-side argument above the true counterargument. It can also overweight
long passages with many shared policy terms while missing the specific premise
being attacked.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` reaches nDCG@10 =
0.4738, hit@10 = 0.8200, and Recall@100 = 0.9600. Dense retrieval is clearly
stronger than BM25 for top-rank ordering. This suggests that embedding
similarity captures aspect-level argumentative relatedness better than term
overlap alone.

Dense retrieval can still confuse topical similarity with opposition. It may
rank a semantically close argument that discusses the same controversy but does
not rebut the query. Still, the dense profile indicates that semantic
representations are essential for German ArguAna.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset reaches nDCG@10 = 0.4422, hit@10 =
0.7400, and Recall@100 = 0.9800. Hybrid is not the best top-rank sorter because
dense has higher nDCG@10 and hit@10, but it is the safest candidate pool. The
metadata records one row with the optional rank-101 safeguard, and the top-100
coverage is the best among the three candidate views.

For reranker experiments, hybrid is valuable because it combines BM25's topic
anchors with dense candidates that better match argumentative relation. The
reranker can then focus on stance opposition and rebuttal quality.

### Metric Interpretation for Model Researchers

This task separates top-rank counterargument selection from candidate coverage.
Dense retrieval is the strongest direct retriever, showing that long German
argument retrieval needs semantic structure beyond word overlap. Hybrid gives
the best Recall@100, which matters for reranking because the true
counterargument must first be present in the candidate pool.

A model that improves lexical recall but not nDCG@10 may retrieve the right
topic without selecting the counterargument. A model that improves nDCG@10
should be checked for stance sensitivity, not just semantic closeness.

### Query and Relevance Type Tendencies

Queries are long German debate arguments. Relevant documents are long
counterarguments that address the same issue and aspect from the opposite
stance. The examples show public-policy, social, economic, legal, and
international-relations debates. Many passages include evidence lists or
citations, so surface overlap is common even among wrong candidates.

Lexical-heavy cases involve named policies, institutions, places, or political
terms. Dense-heavy cases involve opposing arguments that phrase the rebuttal
differently. Hybrid retrieval is useful when topic anchoring and stance-aware
semantic matching are both needed.

### Representative Failure Modes

BM25 can retrieve same-topic same-stance documents because they share issue
vocabulary. Dense retrieval can retrieve a semantically close argument that
does not actually rebut the query. Both can miss the specific aspect under
debate, such as economic consequence, moral principle, legal feasibility, or
empirical evidence. Good hard negatives are same-topic arguments with the wrong
stance or arguments that attack a different premise.

### German-Specific Notes

German argument retrieval involves long compound-rich text, translated debate
style, named institutions, policy vocabulary, and sentence structures that can
bury the key claim. Sparse retrieval needs tokenization that handles compounds
and preserves named entities. Dense retrieval needs robust long-text pooling so
the core claim and rebuttal relation are not diluted by supporting detail.

### Training and Leakage Notes

Training should exclude ArguAna, BEIR, or NanoBEIR records likely to overlap
with these evaluation arguments. Useful non-overlapping data includes
argument-counterargument pairs, stance-aware retrieval datasets, debate portal
argument pairs, German or multilingual argument mining corpora, and hard
negatives with the same topic but wrong stance.

### Model Improvement Hints

The main improvement target is stance-aware semantic retrieval. First-stage
retrievers should keep debate-topic anchors while ranking the actual
counterargument above same-side passages. Rerankers should compare true
counterarguments against same-topic wrong-stance negatives and learn which
premise or conclusion is being rebutted.

### Training Data That May Help

Useful training data includes non-overlapping argument-counterargument pairs,
German debate data, multilingual stance retrieval, pro/con argument pairs,
claim rebuttal datasets, and synthetic long arguments with explicit opposing
stances.

### Synthetic Data Guidance

Generate paired German pro and con arguments for controversial topics. Each
pair should share the issue and aspect but reverse stance. Include premises,
conclusion, evidence, and policy consequences. Positives should rebut the query
argument; hard negatives should discuss the same topic while supporting the
same side or attacking a different premise.

## Example Data

| Query | Positive document |
| --- | --- |
| Die Öffentlichkeit zeigt sich reformunwillig. Ob die Reform des Oberhauses in der aktuellen wirtschaftlichen Lage Priorität haben sollte, ist umstritten, ganz zu schweigen davon, ob eine Koalitionsregierung solche Maßnahmen ü ... [truncated 225 chars](666 chars) | Die Wahlreform lässt sich nicht mit Reformen im House of Lords vergleichen. Zudem sollte man eine durch politische Rhetorik irreführte Öffentlichkeit nicht mit Gleichgültigkeit verwechseln. Oft geben Wähler an, gleichgültig z ... [truncated 225 chars](461 chars) |
| Der Ausbau von Heathrow ist für die Wirtschaft von entscheidender Bedeutung. Der Ausbau von Heathrow würde viele bestehende Arbeitsplätze sichern und gleichzeitig neue schaffen. Derzeit sichert Heathrow etwa 250.000 Arbeitspl ... [truncated 225 chars](1355 chars) | Die Geschäftswelt ist keineswegs einig in ihrer angeblichen Unterstützung für eine dritte Start- und Landebahn. Umfragen deuten darauf hin, dass viele einflussreiche Unternehmen die Erweiterung in Wirklichkeit nicht unterstüt ... [truncated 225 chars](1548 chars) |
| Menschen werden mit zu vielen Wahlmöglichkeiten konfrontiert, was sie unglücklicher macht. Werbung überfordert viele Menschen durch das endlose Bedürfnis, zwischen konkurrierenden Anforderungen an ihre Aufmerksamkeit zu entsc ... [truncated 225 chars](1218 chars) | Menschen sind unzufrieden, weil sie nicht alles haben können, nicht weil sie zu viele Wahlmöglichkeiten haben und sich dadurch gestresst fühlen. Tatsächlich spielen Werbeanzeigen eine entscheidende Rolle dabei, dass Menschen ... [truncated 225 chars](1040 chars) |
| Cyberangriffe werden häufig von nicht-staatlichen Akteuren durchgeführt, wie Cyberterroristen oder Hacktivisten (soziale Aktivisten, die hacken), ohne jede Beteiligung des tatsächlichen Staates. Zum Beispiel wurde 2007 ein ma ... [truncated 225 chars](1157 chars) | Im Falle eines Angriffs durch nicht-staatliche Akteure sind sich viele Praktiker des Völkerrechts einig, dass der Staat sich weiterhin in Selbstverteidigung wehren kann, wenn ein anderer Staat 'unwillig oder unfähig ist, effe ... [truncated 225 chars](641 chars) |
| Weil Religion die Gewissheit des Glaubens fördert, lässt sich göttlich inspirierter Hass leicht nutzen, um gewaltsame Handlungen und diskriminierende Praktiken zu rechtfertigen und zu fördern. Die Meinungsfreiheit muss zurück ... [truncated 225 chars](1247 chars) | Niemand wird durch die Worte eines anderen gezwungen, Gewaltakte zu begehen; es ist ihre eigene Entscheidung, dies zu tun. Ebenso gibt es viele Menschen, die Ansichten vertreten könnten, die als homophob betrachtet werden, ab ... [truncated 225 chars](709 chars) |

### Public Sources

- [Retrieval of the Best Counterargument without Prior Topic Knowledge](https://aclanthology.org/P18-1023/), 2018.
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663), 2021.
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595), 2025.
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-de](https://huggingface.co/datasets/hakari-bench/NanoBEIR-de)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Retrieval of the Best Counterargument without Prior Topic Knowledge | 2018 | task paper | https://aclanthology.org/P18-1023/ |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | https://arxiv.org/abs/2104.08663 |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | https://arxiv.org/abs/2502.13595 |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | https://huggingface.co/collections/zeta-alpha-ai/nanobeir |
