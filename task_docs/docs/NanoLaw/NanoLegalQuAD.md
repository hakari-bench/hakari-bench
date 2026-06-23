# NanoLaw / NanoLegalQuAD

## Overview

`NanoLaw / NanoLegalQuAD` is a German legal question-to-document retrieval task.
Queries are concise German legal questions, and documents are long German legal
decisions that contain the answer or the relevant legal discussion. The Nano
split has 200 queries, 200 documents, and one positive document per query. The
documents are much longer than the questions, so the task tests whether a
retriever can find an answer-bearing judgment from a compact legal question.
Current diagnostics show BM25 as the strongest top-10 ranker, `reranking_hybrid`
as the best top-100 coverage profile, and dense retrieval as useful but clearly
weaker than lexical retrieval on this German legal corpus.

## Details

### What the Original Data Measures

The cited LegalQuAD work is associated with German legal document retrieval and
question answering. The MTEB LegalQuAD card describes the test data as German
questions and legal documents, with one relevant document for each query. No
freely accessible full paper text was confirmed during the metadata pass, so the
interpretation here relies on the DOI record, official dataset card, and
observed examples.

The task measures legal QA retrieval over long German court decisions. It is not
answer generation and not statute lookup. The model receives a short question
and must retrieve the decision containing the legal discussion needed to answer
it.

### Observed Data Profile

The Nano split contains 200 queries, 200 documents, and 200 positive qrel rows.
Every query has one positive document, with no multi-positive queries. Queries
average 71.94 characters, while documents average 19,481.02 characters.

Observed questions ask about definitions of constitutional hearing rights,
complaint value, return duties under an agency relationship, construction-start
coordination, shareholder contribution increases, detention grounds, interim
legal protection, advertising claims, and statutory default interest. Documents
are long judicial decisions with tenor, reasons, procedural context, and legal
analysis.

### BM25 Evaluation Profile

The dataset-provided BM25 candidate subset covers the 200-document corpus and
achieves nDCG@10 = 0.7420, hit@10 = 0.8650, and recall@100 = 0.9750. BM25 is
the strongest observed top-10 profile. Specific German legal terms such as
`Verzugszinsen`, `Haftgründe`, `rechtliches Gehör`, and statutory references
are strong lexical cues.

BM25's performance shows that exact legal terminology is central in this task.
The limitation is that the relevant answer can be buried inside a long
judgment, and several decisions can share the same legal vocabulary. Sparse
retrieval can rank a same-topic decision above the document that actually
contains the answer-bearing discussion.

### Dense Evaluation Profile

The dense `harrier_oss_v1_270m` candidate subset also covers 200 documents per
query. It achieves nDCG@10 = 0.5819, hit@10 = 0.7350, and recall@100 = 0.9200.
Dense retrieval is substantially below BM25. The gap suggests that exact
German legal wording, statutory terms, and long-document specificity matter
more than broad semantic similarity for this split.

Dense retrieval can help when the question paraphrases the answer passage, but
it may confuse judgments in the same legal domain. A single global embedding of
a long decision may also dilute the short answer-bearing passage that connects
the document to the question.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset contains 100 or 101 candidates per
query, with 3 safeguard positive rows and a mean of 100.015 candidates. It
achieves nDCG@10 = 0.7043, hit@10 = 0.8500, and recall@100 = 0.9850. Hybrid
retrieval improves over dense retrieval and gives the best top-100 coverage,
but it does not surpass BM25's top-10 ranking.

This pattern indicates that dense evidence adds useful candidates, while sparse
legal vocabulary remains the best early-ranking signal. For reranking systems,
the hybrid pool is valuable because it preserves slightly more positives, but
the final ranker must still focus on exact legal question-answer evidence.

### Metric Interpretation for Model Researchers

This is a single-positive task. Hit@10 measures whether the answer-bearing
decision appears in the first ten results, nDCG@10 rewards ranking it near the
top, and recall@100 measures whether candidate generation keeps it available
for reranking.

The metrics show a lexical German legal QA retrieval profile. BM25 is best for
top ranking, hybrid is best for coverage, and dense retrieval alone is not
competitive with sparse retrieval. Models should therefore be evaluated for
legal term preservation, not only semantic question-document similarity.

### Query and Relevance Type Tendencies

Queries are concise German legal questions. Relevant documents are long court
decisions containing the answer or the relevant legal reasoning. The query may
refer to a statute, procedural concept, or legal definition, while the positive
document contains a broader factual and procedural context.

The task rewards models that can match short legal questions to answer-bearing
passages inside long decisions. It also requires distinguishing decisions that
share the same legal vocabulary but answer different questions.

### Representative Failure Modes

BM25 can fail when many judgments contain the same statute or doctrinal phrase.
Dense retrieval can fail by ranking a semantically related legal decision that
does not answer the specific question. Hybrid retrieval can include the positive
but still need a reranker to identify the passage that answers the question.

Long documents create another failure mode: the relevant evidence may be a
small paragraph inside a decision, while the rest of the document is unrelated
to the query.

### Training Data That May Help

Useful training data includes German legal QA, question-to-judgment retrieval,
long-document German legal search, and same-statute hard negatives. Synthetic
data should pair concise German legal questions with full decisions that
contain answer-bearing passages, and should include hard negatives with similar
legal terms but different answers.

Comparable evaluation should exclude NanoLegalQuAD questions, qrels, and
positive German legal documents.

### Model Improvement Notes

Dense retrievers need better handling of German legal terminology and
long-document answer localization. Sparse systems benefit from robust German
compound handling, statute references, and legal phrase matching. Rerankers
should identify whether a candidate judgment contains the answer-bearing legal
discussion, not just the same legal topic.

For hybrid systems, `NanoLegalQuAD` supports a sparse-first design with dense
signals used to broaden candidate coverage.

## Example Data

| Query | Positive document |
| --- | --- |
| Wie ist das rechtliche Gehör nach Art. 103 Abs. 1 GG definiert? [64 chars] | TenorDer Antrag auf Zulassung der Berufung wird abgelehnt.Der Kläger trägt die Kosten des Zulassungsverfahrens; Gerichtskosten werden nicht erhoben.1G r ü n d e2Der Antrag auf Zulassung der Berufung hat keinen Erfolg. Die Berufung ist weder wegen des geltend gemachten Zulassungsgrundes eines Verfahrensmangels (dazu I.) noch der grundsätzlichen Bedeutung (dazu II.) zuzulassen.3I. Die Berufung ist zunächst nicht aufgrund des von dem Kläger gerügten Verfahrensmangels der Versagung rechtlichen Gehörs nach § 78 Abs. 3 Nr. 3 AsylG i. V. m. § 138 Nr. 3 VwGO zuzulassen.4Das rechtliche Gehör als prozessuales Grundrecht (Art. 103 Abs. 1 GG) sichert den Beteiligten ein Recht auf Information, Äußerung und Berücksichtigung mit der Folge, dass sie ihr Verhalten eigenbestimmt und situationsspezifisch gestalten können und mit ihren Ausführungen und Anträgen durch das Gericht gehört werden. Das Gericht ist jedoch nicht verpflichtet, den Ausführungen eines Beteiligten in der Sache zu fol... [1,000 / 13,780 chars] |
| Welchen Wert hat das Beschwerdeverfahren? [41 chars] | TenorDie Beschwerde des Beschwerdeführers vom 27.04.2018 gegen den Beschluss des Amtsgerichts – Familiengericht – Bochum vom 21.03.2018 (57 F 17/18) in Verbindung mit dem Beschluss vom 03.04.2018 wird zurückgewiesen.Die Kosten des Beschwerdeverfahrens werden dem Beschwerdeführer auferlegt.Der Wert des Beschwerdeverfahrens wird auf 3.000,00 € festgesetzt.Die Rechtsbeschwerde wird zugelassen.1Gründe:2I.3Der am ##.##.2000 geborene Beschwerdeführer ist Staatsangehöriger der Republik Guinea. Durch Beschluss des Amtsgerichts – Familiengericht – Bochum vom 25.11.2016 wurde für ihn das Ruhen der elterlichen Sorge festgestellt und Vormundschaft angeordnet. Zum Vormund wurde die jetzige Verfahrensbevollmächtigte des Beschwerdeführers bestellt.4Durch den angefochtenen Beschluss vom 21.03.2018, hinsichtlich der Beschlussformel berichtigt durch Beschluss vom 03.04.2018, hat das Familiengericht deklaratorisch festgestellt, dass die Vormundschaft beendet ist, weil der Beschwerdeführer mit V... [1,000 / 11,601 chars] |
| Muss der Beauftragte dem Auftraggeber erhaltene Gegenstände zur Ausführung des Auftrages zurückgeben? [101 chars] | Tenor1E n t s c h e i d u n g s g r ü n d e :2##blob##nbsp;3##blob##nbsp;4Die in förmlicher Hinsicht unbedenkliche Berufung hat nach demErgebnis der zweitinstanzlichen Beweisaufnahme keinen Erfolg.5Das Landgericht hat die Beklagte im rechtlichen Ausgangspunkt zuRecht aus §§ 667, 665, 669, 398 BGB zur Zahlung verurteilt. DieKreissparkasse K. hat ihren Anspruch auf Rückerstattung desBetrages, der aus dem hier streitigen Überweisungsvorgang derBeklagten gutgeschrieben wurde, an den Kläger abgetreten.6Da die Beklagte den ihr von der Kreissparkasse K. erteiltenAuftrag nicht ordnungsgemäß ausgeführt hat, ist sie diesergegenüber zur Rückerstattung verpflichtet.7Nach § 667 BGB ist der Beauftragte verpflichtet, demAuftraggeber alles, was er zur Ausführung des Auftrags erhält,herauszugeben. Die Anweisung der Kreissparkasse K. an die Beklagte,auf dem Konto des Herrn "U.H." einen Betrag gutzuschreiben, stellteinen Auftrag im Sinne der §§ 667 ff. BGB zwischen denKreditinstituten dar. Dur... [1,000 / 13,258 chars] |

### Public Sources

- [Towards Intelligent Legal Advisors for Document Retrieval and Question-Answering in German Legal Documents](https://doi.org/10.1109/AIKE52691.2021.00011),
  2021.
- [mteb/LegalQuAD](https://huggingface.co/datasets/mteb/LegalQuAD), source
  dataset card.
- [hakari-bench/NanoLaw](https://huggingface.co/datasets/hakari-bench/NanoLaw),
  Nano benchmark dataset.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Towards Intelligent Legal Advisors for Document Retrieval and Question-Answering in German Legal Documents | 2021 | IEEE DOI record | [https://doi.org/10.1109/AIKE52691.2021.00011](https://doi.org/10.1109/AIKE52691.2021.00011) |
| LegalQuAD | 2025 | Hugging Face dataset card | [https://huggingface.co/datasets/mteb/LegalQuAD](https://huggingface.co/datasets/mteb/LegalQuAD) |

### Representative Snippets

| Query pattern | Positive document pattern |
| --- | --- |
| A German question asking for the definition of legal hearing under Article 103(1) GG. | A long court decision discussing the constitutional hearing issue in its reasons. |
| A question asking the value of a complaint procedure. | A decision containing the procedural value determination. |
| A question about whether an agent must return objects received for carrying out an order. | A civil-law decision discussing return obligations and evidence. |
| A question asking with whom construction start was coordinated. | A decision about interim relief or construction-related procedure. |
| A question about whether shareholders can be obligated to increase contributions. | A decision addressing shareholder contribution duties. |
