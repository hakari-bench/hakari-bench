# NanoMTEB-Misc / wmt19_de_fr

## Overview

`wmt19_de_fr` is a WMT19 German-French Cross-Lingual Semantic Discrimination
task. Queries are French news sentences, and documents are German candidate
sentences. The positive document is the German translation counterpart of the
French query. The Nano split contains 200 queries, 7,364 documents, and 200
positive qrels, with exactly one positive per query. Queries average 159.09
characters, and documents average 147.49 characters. The task is a sentence-
level cross-lingual equivalence test: a good model must retrieve the true
translation while rejecting semantically similar distractors.

## Details

### What the Original Data Measures

[Cross-Lingual Semantic Discrimination for Building Better Multilingual Embeddings](https://arxiv.org/abs/2502.08638)
introduces CLSD as a retrieval benchmark for multilingual embeddings. It uses
sentence-aligned parallel data and semantic distractors to test whether models
can distinguish true cross-lingual equivalents from plausible alternatives. The
[Andrianos/clsd_wmt19_21](https://huggingface.co/datasets/Andrianos/clsd_wmt19_21)
dataset card provides the WMT19 and WMT21 German-French/French-German variants.

In this split, a French sentence retrieves its German translation. Relevance is
translation equivalence, not broad topical similarity.

### Observed Data Profile

The split has 200 French queries, 7,364 German documents, and 200 positive
judgments. Every query has one positive. Sentences are news-style statements,
including political quotes, EU legal references, and public-affairs reporting.
Both sides are short enough that models must represent sentence meaning rather
than long-document context.

Examples include EU voting rights, populist arguments about Europe, George
Soros funding, participation in a party congress in Bonn, and the leadership of
a Brussels administration.

### BM25 Evaluation Profile

BM25 is weak, with nDCG@10 of 0.2204, hit@10 of 0.3450, and recall@100 of
0.6150. The low score is expected because the query and document are in
different languages. BM25 can only benefit from shared names, numbers, acronyms,
or cognate-like tokens that survive across French and German.

This task therefore exposes the limitation of lexical retrieval in cross-lingual
sentence matching. Term frequency is not the main signal; semantic translation
alignment is.

### Dense Evaluation Profile

Dense retrieval is dominant, with nDCG@10 of 0.9151, hit@10 of 0.9650, and
recall@100 of 0.9650. This indicates that harrier-oss-270m captures German-
French sentence equivalence very well for WMT19-style news sentences. It can
align paraphrastic translations even when surface words differ completely.

For model researchers, this split is a clean multilingual embedding diagnostic:
successful models must encode sentence-level meaning across French and German,
not merely language-specific token overlap.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` profile reaches nDCG@10 of 0.5447, hit@10 of 0.7700,
and recall@100 of 0.9800. It has higher recall@100 than dense retrieval, but
substantially worse top-10 ranking. Candidate lists contain 100 to 101 entries,
with four safeguard-positive rows.

This is a case where hybrid search improves candidate recoverability but lexical
evidence harms early ranking. For first-stage top results, dense retrieval is
clearly better; for a reranker, the hybrid pool may provide slightly broader
coverage.

### Metric Interpretation for Model Researchers

`wmt19_de_fr` is dense-favorable. BM25 is a poor baseline because the task is
cross-lingual. `reranking_hybrid` recovers more positives by rank 100 but does
not match dense top-10 quality. Since every query has one positive, nDCG@10 and
hit@10 directly measure whether the true translation is ranked early.

The main research value is testing cross-lingual semantic precision under
sentence-level distractors. Recall@100 matters for reranking experiments, but
top-10 dense ranking is the core signal.

### Query and Relevance Type Tendencies

Queries are French news sentences, and positives are German translations.
Sentences often include named entities, political concepts, quoted speech, and
EU institutional language. Distractors may share entities or topic while
changing the predicate or event detail.

Relevance is strict semantic equivalence. A sentence about the same event is not
positive unless it is the translation counterpart.

### Representative Failure Modes

BM25 fails when no names or numbers overlap. Dense retrieval can fail on subtle
translation distinctions, such as modality, negation, actor, or scope. Hybrid
retrieval can over-rank sentences sharing names or EU terms even when they are
not translations.

Near-translation distractors are the key challenge: they look topically close
but differ in meaning.

### Training Data That May Help

Useful training data includes German-French sentence retrieval, bitext mining,
translation-pair contrastive learning, and hard negatives from semantically
similar news sentences. Training should avoid WMT19 evaluation sentence pairs
and distractors overlapping this Nano split.

Synthetic data should create German-French sentence pairs from non-evaluation
parallel news, then generate distractors that preserve entities and topic but
change predicate, stance, number, actor, or event detail.

### Model Improvement Notes

Models should optimize strict cross-lingual sentence equivalence. Dense encoders
need fine-grained translation contrastive training. Rerankers should focus on
semantic entailment and contradiction across languages rather than lexical
overlap.

## Example Data

| Query | Positive document |
| --- | --- |
| L'article 20 du traité de l'UE dispose clairement que les citoyens de l'UE peuvent exercer leur droit de vote et d'éligibilité aux élections au Parlement européen "dans l'Etat membre" dans lequel ils ont leur lieu de résidence. [227 chars] | Artikel 20 des EU-Vertrages besagt klipp und klar, dass EU-Bürger „in dem Mitgliedstaat, in dem sie ihren Wohnsitz haben, das aktive und passive Wahlrecht bei den Wahlen zum Europäischen Parlament“ wahrnehmen können. [216 chars] |
| Il a de nombreux éléments pour étayer le credo qu'il ranime pour s'opposer aux sirènes des populistes et selon lequel c'est se fourvoyer que de vouloir quitter l'Europe: le changement climatique, l'imposition des entreprises du web, la migration - autant de défis pour lesquels le cadre de référence national est devenu trop petit. [331 chars] | Für sein nun wiederbelebtes Credo, dass entgegen den Sirenengesängen der Populisten der Rückzug aus Europa ein Holzweg ist, gibt es zahlreiche Belege: Klimawandel, Besteuerung der Internetkonzerne, Migration – für all diese Herausforderungen ist der nationale Bezugsrahmen zu klein geworden. [291 chars] |
| De fait, Soros est venu en soutien, dans les décennies passées, à de nombreuses associations et initiatives humanitaires, sociales, scientifiques et artistiques à hauteur de plusieurs millards. Cela concerne notamment des initiatives qui s'engagent en faveur des demandeurs d'asile. [282 chars] | Tatsächlich hat Soros in den vergangenen Jahrzehnten mit Milliardensummen zahlreiche humanitäre, soziale, wissenschaftliche und künstlerische Vereine und Initiativen unterstützt. Darunter sind auch solche, die sich für Asylsuchende einsetzen. [242 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Cross-Lingual Semantic Discrimination for Building Better Multilingual Embeddings | 2025 | Task paper | [https://arxiv.org/abs/2502.08638](https://arxiv.org/abs/2502.08638) |
| Andrianos/clsd_wmt19_21 | 2025 | Dataset card | [https://huggingface.co/datasets/Andrianos/clsd_wmt19_21](https://huggingface.co/datasets/Andrianos/clsd_wmt19_21) |

### Representative Snippets

| Query | Positive document |
| --- | --- |
| A French sentence about Article 20 of the EU treaty and voting rights. | The German translation stating that EU citizens can vote and stand in European Parliament elections in their Member State of residence. |
| A French sentence about arguments against withdrawing from Europe. | The German translation listing climate change, internet-company taxation, and migration as examples. |
| A French sentence about Soros supporting humanitarian and social initiatives. | The German translation describing decades of funding for such associations and initiatives. |
| C'est egalement pour cette raison qu'elle ne participe pas au congres du parti a Bonn. | Sie nimmt deshalb auch nicht an dem Parteitag in Bonn teil. |
| A French sentence about a German becoming head of a Brussels administration. | The German translation about a German again becoming the top chief of the Brussels authority. |
