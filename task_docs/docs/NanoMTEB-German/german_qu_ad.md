# NanoMTEB-German / german_qu_ad

## Overview

`german_qu_ad` is a GermanQuAD retrieval task. Queries are native German
extractive-QA questions, and documents are German Wikipedia paragraphs. The Nano
split contains 200 queries, 474 documents, and 200 positive qrels, with one
positive paragraph per query. Queries average 54.88 characters, and documents
average 1,941.05 characters. This is a compact, high-precision evidence
retrieval task: the model must find the paragraph that contains the answer, not
only a topically related page. It is useful for evaluating German QA retrieval
where lexical overlap is strong but paraphrase and answer localization still
matter.

## Details

### What the Original Data Measures

[GermanQuAD and GermanDPR: Improving Non-English Question Answering and Passage Retrieval](https://arxiv.org/abs/2104.12741)
introduced GermanQuAD as a German extractive QA dataset inspired by SQuAD and
built from German Wikipedia. Annotators wrote German questions for answer spans
in context paragraphs, with an emphasis on native target-language supervision.
The retrieval version uses the question as the query and the answer-bearing
paragraph as the positive document.

This task measures paragraph evidence retrieval. A model must map a German
question to the context that supports the answer, while avoiding nearby
Wikipedia paragraphs that share entities or topics but do not contain the
needed fact.

### Observed Data Profile

The Nano split has 200 queries, 474 documents, and 200 positive judgments.
Every query has exactly one positive. The small corpus means the nominal top-500
candidate lists cover all documents. Questions are short and natural, while
documents are medium-length Wikipedia paragraphs with page titles and section
context.

Examples ask about environmental organizations in India, seilless elevators,
integration of Black populations in France, Oklahoma City's climate zone, and
daylight-saving-time changes. Many positives are lexically obvious, but some
require recognizing a paraphrased answer relation.

### BM25 Evaluation Profile

BM25 is the strongest profile, with nDCG@10 of 0.9458, hit@10 of 0.9950, and
recall@100 of 1.0000. This is a highly lexical German QA retrieval split.
Entity names, title terms, and answer-bearing phrases often appear in both the
query and the positive paragraph. Because the corpus has only 474 documents,
BM25 also has complete top-100 coverage.

The near-ceiling BM25 score is informative: this task is less useful for testing
whether a model can beat lexical retrieval and more useful for checking whether
semantic models avoid losing easy answer-bearing passages.

### Dense Evaluation Profile

Dense retrieval is also strong, with nDCG@10 of 0.9321, hit@10 of 0.9550, and
recall@100 of 0.9600. Dense ranking is close to BM25 but loses a few positives
within the top-100 candidate depth. This suggests that semantic matching works
well for GermanQuAD-style questions, but exact lexical anchors remain important
for full coverage.

For model researchers, dense failures on this split are worth inspecting
closely. They often indicate over-smoothing of named entities, titles, or
specific answer cues rather than a broad lack of German semantic understanding.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` profile reaches nDCG@10 of 0.9427, hit@10 of 0.9650,
and recall@100 of 1.0000. It restores full recall like BM25 and stays close to
BM25 at top-10 ranking, though it does not exceed the lexical baseline. There
are no safeguard-positive rows.

The hybrid result is best interpreted as a robust candidate pool. It combines
the recall safety of lexical matching with semantic evidence, but the task is
already so lexically favorable that the hybrid ranking has little room to
improve over BM25.

### Metric Interpretation for Model Researchers

`german_qu_ad` is BM25-favorable and near ceiling for first-stage retrieval.
nDCG@10 and hit@10 measure whether the positive paragraph appears almost
immediately, while recall@100 mainly confirms candidate recoverability. Dense
models should be expected to perform well; substantial underperformance is a
signal of German entity or answer-evidence weakness.

Because each query has one positive, metrics are straightforward. A miss means
the model failed to retrieve the single paragraph that contains the answer,
even though the corpus is small and the lexical signal is often strong.

### Query and Relevance Type Tendencies

Queries are short German QA questions over Wikipedia content. Positive
documents are paragraphs that explicitly contain the answer. Topics include
science, geography, politics, social issues, technology, and history.

Relevance is answer evidence, not broad topicality. Same-article negatives can
be difficult when they share the page title but lack the answer sentence.

### Representative Failure Modes

BM25 can fail when the question is paraphrased or when the positive paragraph
uses different wording from the query. Dense retrieval can fail by retrieving a
semantically related paragraph that lacks the answer span, or by losing rare
German names and technical terms. Hybrid retrieval can recover coverage but
still inherit lexical ordering mistakes.

Since the task is compact, errors are likely to be fine-grained rather than
caused by broad corpus search difficulty.

### Training Data That May Help

Useful training data includes non-overlapping GermanQuAD train question-context
pairs, German Wikipedia question-to-passage retrieval pairs, native German
paraphrase and reformulation data for QA questions, and hard negatives from
related Wikipedia pages and sections. Training should exclude GermanQuAD test
data, Nano queries, qrels, and positive passages likely to overlap with the
evaluation split.

Synthetic data should use German Wikipedia-style paragraphs with titles,
sections, entities, dates, definitions, and numeric facts, then generate
self-contained German QA questions with explicit answer evidence in the
paragraph.

### Model Improvement Notes

Models should preserve exact German entity and title information while handling
question paraphrase. Dense encoders should be trained not to collapse same-topic
paragraphs. Rerankers can focus on answer-bearing sentence detection, since the
main challenge is selecting the paragraph that actually supports the answer.

## Example Data

| Query | Positive document |
| --- | --- |
| Was versuchen die Umweltorganisationen wie CSE in Indien zu verbessern? [71 chars] | Rajasthan === Umweltorganisationen fördern traditionelles Sammeln von Regenwasser === Umweltorganisationen in Indien, wie das Centre for Science and Environment (CSE), haben vor über 20 Jahren damit begonnen, die alten traditionellen Methoden des Regenwassersammelns zu dokumentieren und Pilotprojekte aufzubauen. In Rajasthan heißen die einfachsten Lösungen für die Bauern ''Johads.'' Ein Johad ist ein halbmondförmiger Teich, der so in der Landschaft liegt, dass er in der Regenzeit viele kleine Bäche und Quellen aus einer größeren Umgebung auffangen kann. Jeder Johad ist anders in Größe und Form, je nach Bodenbeschaffenheit oder Topographie. Dieser kleine See entsteht durch Anhäufen von Erdwällen. Ihre Funktion ist, Wasser zu stauen, das die Menschen nach der Regenzeit nutzen. Noch wichtiger sind sie allerdings für das Grundwasser. Denn die enormen Niederschläge würden sonst weggespült werden und zu Landerosionen führen. Durch das Anstauen hat das Wasser aber genug Zeit, um langsam im Bo... [1,000 / 1,933 chars] |
| Wann muss man die Zieletage in seillosen Aufzügen auswählen? [60 chars] | Aufzugsanlage === Seilloser Aufzug === An der RWTH Aachen im Institut für Elektrische Maschinen wurde ein seilloser Aufzug entwickelt und ein Prototyp aufgebaut. Die Kabine wird hierbei durch zwei elektromagnetische Synchron-Linearmotoren angetrieben und somit nur durch ein vertikal bewegliches Magnetfeld gehalten bzw. bewegt. Diese Arbeit soll der Entwicklung von Aufzugsanlagen für sehr hohe Gebäude dienen. Ein Ziel ist der Einsatz mehrerer Kabinen pro Schacht, die sich unabhängig voneinander steuern lassen. Bei Auswahl des Fahrtziels vor Fahrtantritt (d. h. noch außerhalb des Aufzug) wird ein bestimmter Fahrkorb in einem der Aufzugsschächte für die Fahrt ausgewählt, mit der sich der geplante Transport am schnellsten durchführen lässt. Der Platzbedarf für die gesamte Aufzugsanlage könnte somit um ein oder mehrere Schächte reduziert werden. Da die Kabinen seillos betrieben werden, ist ein Schachtwechsel ebenfalls denkbar. Hiermit können weitere Betriebsstrategien für die seillose Aufzu... [1,000 / 1,766 chars] |
| Warum sind Schwarze aus Überseegebieten in Frankreich tendenziell besser integriert als Schwarze aus Schwarzafrika? [115 chars] | Schwarze ==== Frankreich ==== Die Bevölkerung Frankreichs setzt sich aus zahlreichen Ethnien zusammen, darunter sind 2,5 bis 5 Millionen schwarze Menschen. Die meisten von ihnen sind Einwanderer oder deren Nachkommen aus den afrikanischen und karibischen Kolonien Frankreichs. Amtliche Zahlen gibt es nicht, weil bei Volkszählungen nicht nach ethnischen oder religiösen Kategorien gefragt wird. Die Einwanderung Dunkelhäutiger ins Mutterland hat eine lange Vorgeschichte. Die Bewohner der ''vieilles colonies'' in der Karibik sowie der ''Quatre Communes'' im Senegal hatten seit 1848 das französische Bürgerrecht und entsandten Abgeordnete in die Nationalversammlung, etwa Blaise Diagne. Unter den Vorfahren des berühmten Schriftstellers Alexandre Dumas befand sich eine schwarze Sklavin aus Haiti, weswegen er oft rassistisch beleidigt wurde. In der Zwischenkriegszeit und besonders nachdem alle Bewohner der Kolonien 1946 das Wahlrecht erhalten hatten, gab es in französischen Regierungen oft schwa... [1,000 / 3,198 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| GermanQuAD and GermanDPR: Improving Non-English Question Answering and Passage Retrieval | 2021 | Paper | [https://arxiv.org/abs/2104.12741](https://arxiv.org/abs/2104.12741) |
| GermanQuAD and GermanDPR ACL Anthology record | 2021 | Proceedings paper | [https://aclanthology.org/2021.mrqa-1.4/](https://aclanthology.org/2021.mrqa-1.4/) |
| mteb/germanquad-retrieval | 2025 | Dataset card | [https://huggingface.co/datasets/mteb/germanquad-retrieval](https://huggingface.co/datasets/mteb/germanquad-retrieval) |

### Representative Snippets

| Query | Positive document excerpt |
| --- | --- |
| Was versuchen die Umweltorganisationen wie CSE in Indien zu verbessern? | A Rajasthan passage about environmental organizations promoting traditional rainwater collection. |
| Wann muss man die Zieletage in seillosen Aufzugen auswahlen? | An elevator passage about a seilless prototype and destination-floor selection. |
| Warum sind Schwarze aus Uberseegebieten in Frankreich tendenziell besser integriert als Schwarze aus Schwarzafrika? | A France-related passage on Black populations and integration context. |
| In welcher Klimazone liegt Oklahoma City? | An Oklahoma City climate passage identifying the humid subtropical climate zone. |
| In welcher Jahreszeit wird auf die Sommerzeit umgestellt? | A daylight-saving-time passage explaining spring and autumn clock changes. |
