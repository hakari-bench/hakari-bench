# NanoMTEB-German / gov_service

## Overview

`gov_service` is a German public-service retrieval task based on Munich
municipal service data. Queries are citizen questions about administrative
procedures, and documents are service descriptions. The Nano split contains 200
queries, 105 documents, and 200 positive qrels, with exactly one positive
service page per query. Queries average 63.875 characters, while documents
average 1,248.46 characters. The task is a practical FAQ-to-service matching
benchmark: a model must identify the municipal page that answers a procedural
question about requirements, documents, fees, appointments, deadlines, or
eligibility.

## Details

### What the Original Data Measures

No standalone task paper was confirmed for this dataset. The interpretation is
based on the official
[it-at-m/LHM-Dienstleistungen-QA](https://huggingface.co/datasets/it-at-m/LHM-Dienstleistungen-QA)
dataset card, MTEB metadata, and observed Nano data. The dataset card describes
questions and answers derived from City of Munich administration service pages,
with a format inspired by GermanQuAD.

The task measures citizen-facing service retrieval. The positive document is a
service description, not an encyclopedic passage. A model must map an everyday
question to the correct administrative service and avoid related services with
similar vocabulary.

### Observed Data Profile

The split has 200 German queries, 105 documents, and 200 positive judgments.
Every query has one positive. The corpus is small, but service pages reuse many
administrative terms such as application, documents, permit, appointment, fee,
and deadline. Documents include titles, prerequisites, required materials,
costs, procedural notes, and responsible offices.

Examples cover holiday-program supervisors, Heilpraktiker examinations, housing
benefit applications, smoke-detector operation, passport procedures, and
business permissions. The key challenge is procedural intent, not broad topic.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.6132, hit@10 of 0.8350, and recall@100 of 0.9950.
The small corpus and repeated service terminology make BM25 useful, but it does
not dominate. Many service pages share generic administrative words, so exact
term frequency can over-rank related procedures that do not answer the specific
question.

BM25 is most reliable when the query includes a distinctive service name or
document type. It is less reliable when the citizen question paraphrases the
procedure or asks about a condition expressed in formal service-page language.

### Dense Evaluation Profile

Dense retrieval is strongest, with nDCG@10 of 0.7903, hit@10 of 0.9550, and
recall@100 of 0.9950. The dense model appears to bridge everyday citizen wording
and formal municipal descriptions. This is important because users may ask "what
do I need to do" while the service text states requirements, fees, and
procedural conditions in administrative language.

The dense result indicates that semantic matching is valuable even in a small
corpus. It helps distinguish intent, such as eligibility versus cost, required
documents versus appointments, or a specific permit transfer versus a general
license page.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` profile reaches nDCG@10 of 0.6959, hit@10 of 0.8950,
and recall@100 of 1.0000. It provides the best coverage, while dense retrieval
has the best top-10 ordering. There are no safeguard-positive rows, and each
candidate list contains 100 entries.

This pattern suggests that hybrid search is a strong candidate generator for a
public-service reranker. Lexical matching preserves service names and document
terms, while dense matching helps with paraphrased citizen questions. A reranker
would then need to resolve the exact procedural page.

### Metric Interpretation for Model Researchers

`gov_service` is dense-favorable for top-10 ranking and hybrid-favorable for
recall. BM25 is useful but weaker because administrative pages share many
generic terms. nDCG@10 reflects whether the correct service page is ranked early
enough for a citizen-facing system, while recall@100 shows whether a reranker
has access to the right page.

Because each query has exactly one positive, errors can be inspected as service
selection failures. A wrong result is often a related procedure rather than an
unrelated document.

### Query and Relevance Type Tendencies

Queries are German citizen questions about public-service procedures. They ask
what is required, where to apply, how much something costs, whether an action is
allowed, when an exam or appointment occurs, and which office is responsible.
Positive documents are Munich municipal service descriptions.

Relevance is procedural answerability. A page about the same service category
is not enough if it does not answer the asked requirement or step.

### Representative Failure Modes

BM25 can over-rank services with common administrative words such as "Antrag",
"Unterlagen", or "Erlaubnis". Dense retrieval can confuse related procedures if
they satisfy similar intent patterns. Hybrid retrieval can recover the correct
page but still rank a generic service page above the specific one.

Another failure mode is missing the distinction between eligibility, required
documents, fees, and appointment logistics. These are separate user intents even
when the same service page vocabulary appears.

### Training Data That May Help

Useful training data includes non-overlapping LHM-Dienstleistungen-QA train
questions, German municipal FAQ and service-description retrieval pairs,
citizen question to public-service page mappings, and hard negatives from
related administrative services. Training should exclude LHM-Dienstleistungen-QA
test data, Nano queries, qrels, and positive service texts likely to overlap
with the evaluation split.

Synthetic data should create German municipal service pages with requirements,
forms, deadlines, fees, appointments, and responsible offices, then generate
citizen questions grounded in those details. Hard negatives should be related
services from the same administrative domain.

### Model Improvement Notes

Strong models should bridge informal citizen language and formal service-page
language. Dense encoders need to preserve procedural intent, while rerankers
should compare the question against the specific requirement, document, fee, or
deadline stated in the service text. Same-category negatives are important for
avoiding overly broad service matching.

## Example Data

| Query | Positive document |
| --- | --- |
| Was bietet die Abteilung Ferienangebote/Familienpass für die Betreuer:innen an? [79 chars] | Betreuer-innen für Ferienangebote Betreuer*innen für Ferienangebote Du hast Freude im Umgang mit Kindern und Jugendlichen, bist mindestens 18 Jahre alt und suchst einen sinnvollen Ferienjob? Dann meld... [200 / 1,283 chars] |
| Was kostet die Heilpraktikerprüfung? [36 chars] | Allgemeine Heilpraktikererlaubnis kertätigkeit in München: Wenn Ihr amtlicher Wohnsitz nicht im Stadtgebiet München liegt, legen Sie Ihren Mietvertrag, Anstellungsvertrag oder andere Dokumente bei, di... [200 / 1,243 chars] |
| Wo muss ich anrufen, wenn ich Fragen zum Thema Ferienangebote habe? [67 chars] | Betreuer-innen für Ferienangebote leitungen und Fachkräfte - eine faire Aufwandsentschädigung, sowie freie Unterkunft und Verpflegung - Tätigkeitsnachweis über dein ehrenamtliches Engagement Benötigte... [200 / 1,108 chars] |
| Wo bekomme ich einen Antrag auf Wohngeld? [41 chars] | Wohngeld – Mietzuschuss für Mietwohnungen Nachweis Kontoauszüge vorlegen, dürfen Sie Verwendungszweck bzw. Empfänger einer Überweisung – nicht aber deren Höhe - schwärzen, wenn es sich um besondere Ka... [200 / 1,262 chars] |
| Woher weiß ich als Mieter wie meine Rauchmelder funktionieren? [62 chars] | Rauchmelder werden? Die Rauchwarnmelder müssen so eingebaut oderangebracht und betrieben werden, dass Brandrauchfrühzeitig erkannt und gemeldet wird. Genaue Angabenzur Standortwahl, Montage und Wartun... [200 / 1,174 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| it-at-m/LHM-Dienstleistungen-QA | 2022 | Dataset card | [https://huggingface.co/datasets/it-at-m/LHM-Dienstleistungen-QA](https://huggingface.co/datasets/it-at-m/LHM-Dienstleistungen-QA) |
| MTEB: Massive Text Embedding Benchmark | 2023 | Paper | [https://arxiv.org/abs/2210.07316](https://arxiv.org/abs/2210.07316) |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | Paper | [https://arxiv.org/abs/2502.13595](https://arxiv.org/abs/2502.13595) |

### Representative Snippets

| Query | Positive document excerpt |
| --- | --- |
| Was bietet die Abteilung Ferienangebote/Familienpass fur die Betreuer:innen an? | A service page for holiday-program supervisors describing activities and support. |
| Was kostet die Heilpraktikerprufung? | A Heilpraktiker permit page containing examination and fee information. |
| Wo muss ich anrufen, wenn ich Fragen zum Thema Ferienangebote habe? | A holiday-program service page with contact and participation details. |
| Wo bekomme ich einen Antrag auf Wohngeld? | A housing-benefit service page explaining documents and application procedure. |
| Woher weiss ich als Mieter wie meine Rauchmelder funktionieren? | A smoke-detector page discussing operation, installation, and maintenance information. |
