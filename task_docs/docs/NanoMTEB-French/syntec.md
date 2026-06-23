# NanoMTEB-French / syntec

## Overview

`syntec` is a French legal and workplace-policy retrieval task built from the
Syntec collective bargaining agreement. Queries are natural employee-style
questions, and documents are article-level provisions from the agreement. The
Nano split contains 100 queries, 90 documents, and 100 positive qrels, with one
positive article per query. Documents average 1,226.27 characters, so the model
must often identify the relevant clause inside a structured article rather than
only match a title. The task is compact, but it is useful for evaluating French
retrieval models on semi-legal domain text where terminology, abbreviations,
article numbering, and policy paraphrase all matter.

## Details

### What the Original Data Measures

[MTEB-French: Resources for French Sentence Embedding Evaluation and Analysis](https://arxiv.org/abs/2405.20468)
introduced SyntecRetrieval as a French retrieval dataset. The source material is
the Syntec collective bargaining agreement, with articles used as documents and
queries written to test article retrieval. The domain is legal and
employment-policy oriented, but the wording is often closer to workplace
guidance than to highly specialized statutory text.

In retrieval terms, the task measures whether a model can map a practical
question about employment conditions to the governing agreement article. The
positive article may contain formal article headings, modification notes,
exceptions, and lists, while the query may use everyday employee wording.

### Observed Data Profile

The Nano split has 100 French queries, 90 documents, and 100 positive judgments.
Queries average 72.80 characters, and documents average 1,226.27 characters.
All queries have exactly one positive. The small document pool means each
candidate list covers the full corpus, but top-rank ordering is still
meaningful because several articles can share policy vocabulary.

Questions cover topics such as severance, patents, paid leave, overtime,
medical checks after foreign travel, seniority, Sunday work, and classifications.
Documents preserve article numbers and formal clause structure, so retrieval
quality depends on both lexical legal terms and semantic alignment between a
question and the applicable provision.

### BM25 Evaluation Profile

BM25 performs reasonably well, reaching nDCG@10 of 0.7180, hit@10 of 0.8900,
and recall@100 of 1.0000. Because the corpus has only 90 documents, every
positive is available within the candidate list; the main issue is whether BM25
orders the right article near the top. Lexical matching helps when the query
contains terms such as "licenciement", "conges", "heures supplementaires", or
"deplacement a l'etranger" that also appear in the agreement.

BM25 is weaker when an employee question paraphrases a legal concept, uses an
abbreviation, or asks about a practical condition that is expressed formally in
the article. The task therefore remains a useful lexical-vs-semantic diagnostic
even though the candidate pool is small.

### Dense Evaluation Profile

The dense harrier-oss-270m candidates are strongest on this task, with nDCG@10
of 0.8660, hit@10 of 0.9700, and recall@100 of 1.0000. Dense retrieval appears
to benefit from mapping practical questions to formal policy language. This is
exactly the kind of paraphrase that a pure term-frequency method can miss: an
employee may ask what they are entitled to, while the article states conditions,
exceptions, and compensation rules in a different style.

For model researchers, `syntec` is a small but clean signal that semantic
retrieval can add value in French domain-specific text. A dense model that does
well here likely captures policy concepts, not only surface article titles.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` profile reaches nDCG@10 of 0.8463, hit@10 of 0.9800,
and recall@100 of 1.0000. It is close to dense retrieval and has the highest
hit@10, but dense keeps a slight advantage in nDCG@10. There are no safeguard
rows because all 90 documents fit inside the hybrid candidate depth.

This is a case where hybrid search is robust but not clearly dominant. The
lexical component preserves exact legal terminology, while the dense component
helps bridge paraphrase. The final top ordering still depends on whether the
candidate scoring emphasizes the exact governing article rather than a
semantically adjacent article.

### Metric Interpretation for Model Researchers

`syntec` is dense-favorable at top-10 ranking, with BM25 still strong and all
methods achieving full recall by 100. Because recall is saturated, the key
metric is nDCG@10: it measures whether the model ranks the governing article
before related but incorrect provisions. The gap between BM25 and dense
indicates that semantic matching is important for workplace-policy questions,
but the high BM25 baseline shows that terminology overlap remains valuable.

The single-positive setup makes false positives easy to diagnose. If a model
ranks an article about a nearby policy area above the positive article, the
error is not a recall failure but a legal/semantic discrimination failure.

### Query and Relevance Type Tendencies

Queries are practical French questions from an employee or employer perspective.
They ask about rights, limits, obligations, and conditions. Positive documents
are formal articles containing the clause that resolves the question.

Relevance is article-level. A document may mention the same topic but be wrong
if it governs a different condition or worker category. This makes adjacent
article negatives especially useful for training and evaluation analysis.

### Representative Failure Modes

BM25 can over-rank articles with shared terms but the wrong legal condition.
Dense retrieval can over-generalize policy concepts and rank a semantically
related article that does not answer the specific question. Both methods can be
confused by abbreviations, article modification notes, and long documents where
the relevant clause is only a small part of the text.

Hybrid retrieval reduces some of these risks by combining exact legal terms and
semantic paraphrase, but it still needs a reranker or stronger scoring model to
resolve fine-grained article distinctions.

### Training Data That May Help

Useful training data includes French collective-agreement QA pairs, French
labor-law FAQ to article retrieval data, non-overlapping employment-policy
question-article pairs, and hard negatives from adjacent agreement articles.
Training should exclude Nano queries, qrels, and Syntec article positives used
in this evaluation.

Synthetic data should preserve article numbers, clause structure, exceptions,
and modification notes. Questions should be natural employee wording about
leave, seniority, Sunday work, travel, classifications, termination, invention
rights, and overtime.

### Model Improvement Notes

Strong models should handle both legal terminology and everyday paraphrase.
Dense encoders should be trained with domain-specific hard negatives so that
they distinguish the governing article from nearby provisions. Rerankers should
pay attention to conditions and exceptions, because those details often decide
which article is actually relevant.

## Example Data

| Query | Positive document |
| --- | --- |
| Puis-je justifier d'une indemnité de licenciement si cela fait-il plus de 2 ans que je suis dans cette entreprise ? [115 chars] | Article 18 : Indemnité de licenciement – Conditions d’attribution Modification Avenant n° 7 du 5/07/1991 Il est attribué à tout salarié licencié justifiant d’au moins 2 années d’ancienneté une indemnité de licenciement distincte de l’indemnité éventuelle de préavis. Cette indemnité de licenciement n’est pas due dans le cas où le licenciement est intervenu pour faute grave ou lourde. Cette indemnité sera réduite de 1/3 lorsque le salarié sera pourvu par l’employeur, avant la fin de la période de préavis, d’un emploi équivalent et accepté par l’intéressé en dehors de l’entreprise. Ce tiers restant sera versé à l’intéressé si la période d’essai dans le nouvel emploi reste sans suite. [690 chars] |
| Mon entreprise a déposé un brevet sur mon invention. A quoi ai-je droit ? [73 chars] | Article 75 : Invention des salariés dans le cadre des activités professionnelles Dispositions générales : Les règles relatives aux inventions des salariés sont fixées par la loi n° 78-742 du 13 juillet 1978 modifiant et complétant la loi n° 68-1 du 2 janvier 1968 tendant à valoriser l’activité inventive et à modifier le régime des brevets d’invention. Conformément aux dispositions de l’article 1er (alinéa 1) de la loi de 1978, sont réputées appartenir à l’employeur les inventions faites par le salarié dans l’exécution soit d’un contrat de travail comportant une mission inventive qui correspond à ses fonctions effectives, soit d’études et de recherches qui lui sont explicitement confiées. Les formalités que le salarié et l’employeur doivent effectuer l’un envers l’autre, notamment la déclaration d’invention du salarié, les communications de l’employeur et l’accord entre le salarié et l’employeur, sont précisées par le décret n° 79-797 du 4 septembre 1979, modifié par le décret n° 84-684... [1,000 / 3,628 chars] |
| Quelle est la période de prise de congés ? [42 chars] | Article 25 : Période de congés Les droits à congé s’acquièrent du 1er juin de l’année précédente au 31 mai de l’année en cours. La période de prise de ces congés, dans tous les cas, est de treize mois au maximum. Aucun report de congés ne peut être toléré au-delà de cette période sauf demande écrite de l’employeur. L’employeur peut soit procéder à la fermeture totale de l’entreprise dans une période située entre le 1er mai et le 31 octobre, soit établir les congés par roulement après consultation du comité d’entreprise (ou à défaut des délégués du personnel) sur le principe de cette alternative. Si l’entreprise ferme pour les congés, la date de fermeture doit être portée à la connaissance du personnel au plus tard le 1er mars de chaque année. [753 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| MTEB-French: Resources for French Sentence Embedding Evaluation and Analysis | 2024 | Paper | [https://arxiv.org/abs/2405.20468](https://arxiv.org/abs/2405.20468) |
| lyon-nlp/mteb-fr-retrieval-syntec-s2p | 2024 | Dataset card | [https://huggingface.co/datasets/lyon-nlp/mteb-fr-retrieval-syntec-s2p](https://huggingface.co/datasets/lyon-nlp/mteb-fr-retrieval-syntec-s2p) |

### Representative Snippets

| Query | Positive document excerpt |
| --- | --- |
| Puis-je justifier d'une indemnite de licenciement si cela fait plus de 2 ans que je suis dans cette entreprise ? | Article 18 on severance indemnity and the seniority condition for attribution. |
| Mon entreprise a depose un brevet sur mon invention. A quoi ai-je droit ? | Article 75 on employee inventions in the context of professional activities. |
| Quelle est la periode de prise de conges ? | Article 25 on the period during which paid leave rights are acquired and taken. |
| J'ai le droit de faire combien d'heures supplementaires sans l'accord de l'inspecteur du travail ? | Article 33 on overtime and compensation for ETAM staff. |
| Y a-t-il un examen medical obligatoire au retour d'un deplacement a l'etranger ? | Article 73 on medical checks after prolonged foreign stays. |
