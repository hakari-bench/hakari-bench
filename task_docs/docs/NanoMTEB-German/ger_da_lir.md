# NanoMTEB-German / ger_da_lir

## Overview

`ger_da_lir` is a German legal information retrieval task based on GerDaLIR.
Queries are long German legal reasoning passages, and documents are full German
court decisions. The Nano split contains 200 queries, 10,000 documents, and 235
positive qrels. Queries average 879.53 characters, while documents average
18,071.48 characters, making this one of the long-document retrieval tasks in
the Nano set. The task is useful for evaluating whether retrieval models can
connect a legal argument passage to relevant precedent cases, not merely match
short keywords or titles.

## Details

### What the Original Data Measures

[GerDaLIR: A German Dataset for Legal Information Retrieval](https://aclanthology.org/2021.nllp-1.13/)
defines a German legal IR benchmark from Open Legal Data case documents. The
benchmark uses legal passages as queries and referenced cases as relevant
documents. Citations and references are sanitized, so a model should not solve
the task by copying citation strings; it must retrieve precedent-like documents
from legal content.

This makes the task different from open-domain QA. The query is already a dense
legal passage with procedural and statutory context, and the document is a full
case decision. Relevance depends on precedent reasoning, case context, or
juridical connection rather than on a short answer span.

### Observed Data Profile

The split has 200 German queries, 10,000 documents, and 235 positive judgments.
Most queries have one positive, but 29 queries, or 14.5%, have multiple
positives; the maximum is four. The long query and document lengths mean that
both term-frequency models and embedding models must cope with diluted signals,
boilerplate, and repeated legal phrasing.

Documents include court headers, procedural history, legal reasoning, dates,
sanitized references, and statute-like placeholders. Queries often describe a
legal standard or judicial finding and expect the retriever to locate a case
that supports or parallels that reasoning.

### BM25 Evaluation Profile

BM25 is the strongest top-10 profile, reaching nDCG@10 of 0.5360, hit@10 of
0.7050, and recall@100 of 0.8383. This reflects the importance of exact German
legal terms, statutes, court language, and procedural phrases. In long legal
documents, specialized vocabulary can be a strong anchor even when the document
is much longer than the query.

The result also shows why this task is not solved by BM25. Many German legal
decisions share generic terms and boilerplate, while the positive case may be
connected through a legal issue rather than direct wording. BM25 can retrieve a
large share of positives, but it can also over-rank documents that share common
legal formulas without the relevant precedent relation.

### Dense Evaluation Profile

Dense retrieval is much weaker, with nDCG@10 of 0.2920, hit@10 of 0.4150, and
recall@100 of 0.6340. The task is challenging for dense models because both
queries and documents are long, domain-specific, and packed with legal
terminology. A general multilingual embedding model may compress away the
statutory and procedural details that distinguish one case from another.

For model researchers, this is a warning case: semantic similarity alone is not
enough if the model does not represent legal-domain concepts, citations after
sanitization, court context, and fine-grained procedural language. Improvements
on this task likely require legal-domain training or long-document retrieval
strategies.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` profile reaches nDCG@10 of 0.4461, hit@10 of 0.6300,
and recall@100 of 0.8468. It has slightly higher recall@100 than BM25 while
remaining below BM25 in top-10 ranking. Candidate lists contain 100 to 101 rows,
with 29 safeguard-positive rows.

This is a clear hybrid-search pattern: lexical matching provides strong early
ranking, while the hybrid candidate pool exposes a few more positives for
downstream reranking. The top ordering still favors BM25, but the hybrid pool
may be more useful if a legal reranker can exploit the additional recovered
positives.

### Metric Interpretation for Model Researchers

`ger_da_lir` is BM25-favorable at the top of the ranking and hybrid-favorable
for candidate coverage. Dense-only retrieval is substantially weaker. This
combination suggests that legal terminology, exact phrase overlap, and statute
or procedure language dominate first-stage retrieval, while semantic models need
domain adaptation to compete.

nDCG@10 measures whether the most relevant precedent documents appear early.
Recall@100 measures candidate recoverability for reranking. Because the task
has some multi-positive queries, recall should be interpreted across all
relevant cases, not only one target document.

### Query and Relevance Type Tendencies

Queries are long German legal passages, not short questions. They discuss legal
standards, administrative decisions, medical or social law claims, civil
procedure, or judicial review. Relevant documents are full court decisions that
serve as cited or substantively related precedents.

Relevance is legal-contextual. A document may share statutes or terminology but
still be wrong if it does not support the same line of reasoning. This makes
same-court, same-statute, and same-procedure hard negatives valuable.

### Representative Failure Modes

BM25 can retrieve documents with shared legal boilerplate but the wrong
precedent relation. Dense retrieval can blur distinct legal issues because the
documents are long and domain-specific. Hybrid retrieval can improve coverage
while still ranking generic legal similarity above the true precedent.

Long-document truncation is also a risk. If a model only embeds the beginning of
a decision, it may miss the reasoning section that makes the case relevant.

### Training Data That May Help

Useful training data includes non-overlapping GerDaLIR train examples, German
court-decision citation retrieval pairs, German legal passage-to-case relevance
pairs, and hard negatives from the same statute or court. Training should
exclude GerDaLIR test data, Nano queries, qrels, and positive case documents
likely to overlap with the evaluation split.

Synthetic data should use non-evaluation German legal decisions and create
legal argument passages that imply one or more relevant precedent cases.
Generated examples should preserve courts, statutes, procedural posture,
findings, and sanitized references without copying evaluation material.

### Model Improvement Notes

Models need legal-domain representations and long-document handling. Dense
encoders may benefit from passage-level indexing, late interaction, or training
on legal citation pairs. Rerankers should compare legal issue, procedural
posture, and reasoning rather than relying only on shared statute terms.

## Example Data

| Query | Positive document |
| --- | --- |
| Die Entscheidung des Landgerichts, die Beklagte zur Erteilung der Auskunft durch Vorlage eines notar... [100 / 1,431 chars] | Tenor Die Rechtsbeschwerde gegen den Beschluss des 0. Familiensenats in Freiburg des Oberlandesgerichts Karlsruhe vom [DATE] wird auf Kosten des Antragsgegners zurückgewiesen. Von Rechts wegen Gründe... [200 / 11,013 chars] |
| Der Vergütungsanspruch des Krankenhauses entsteht unmittelbar mit Inanspruchnahme der Leistung durch... [100 / 1,165 chars] | Der Antragsteller wendet sich mit seinem Normenkontrollantrag gegen die am [DATE] bekannt gemachte städtebauliche Entwicklungssatzung der Antragsgegnerin für das Wohnbaugebiet „B.“ am südöstlichen Ort... [200 / 32,444 chars] |
| Die Auslegung der in §§ 0 Abs. 0, 0 NHundG enthaltenen Vorgaben ergibt, dass das erwähnte Erforderni... [100 / 1,335 chars] | Die Beschwerde des Antragsgegners gegen den Beschluss des Verwaltungsgerichts, mit dem dieses die aufschiebende Wirkung der gegen den Bescheid des Antragsgegners vom [DATE] gerichteten Klage des Antra... [200 / 15,391 chars] |
| Zwar ergibt sich aus [REF] das Erfordernis, dass die Begründung einen bestimmten Antrag enthalten mu... [100 / 818 chars] | Tenor Die Beschwerde wird zurückgewiesen. Der Antragsteller trägt die Kosten des Beschwerdeverfahrens mit Ausnahme etwaiger außergerichtlicher Kosten der Beigeladenen, die diese selbst trägt. Der Stre... [200 / 16,881 chars] |
| Die gerichtliche Kontrolle einer behördlichen Ermessensentscheidung beschränkt sich gemäß [REF] dara... [100 / 667 chars] | Der Beklagte gewährte der Klägerin im [DATE] eine Zuwendung von bis zu 0 0 0 DM aus Mitteln der Finanzhilfen des Bundes für Investitionen zur Verbesserung der Verkehrsverhältnisse der Gemeinden als An... [200 / 14,680 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| GerDaLIR: A German Dataset for Legal Information Retrieval | 2021 | Paper | [https://aclanthology.org/2021.nllp-1.13/](https://aclanthology.org/2021.nllp-1.13/) |
| MTEB: Massive Text Embedding Benchmark | 2023 | Paper | [https://arxiv.org/abs/2210.07316](https://arxiv.org/abs/2210.07316) |
| mteb/GerDaLIR | 2025 | Dataset card | [https://huggingface.co/datasets/mteb/GerDaLIR](https://huggingface.co/datasets/mteb/GerDaLIR) |

### Representative Snippets

| Query | Positive document excerpt |
| --- | --- |
| A German passage about the duty to provide a notarized estate inventory. | A full court decision with family-law reasoning and procedural disposition. |
| A passage about hospital remuneration and statutory requirements. | A long administrative-law decision with urban-development and review context. |
| A passage interpreting requirements in the Lower Saxony dog law. | A decision discussing suspensive effect and an administrative order. |
| A passage about whether a missing explicit application is harmless. | A decision on complaint procedure, costs, and legal-protection objective. |
| A passage on judicial review of administrative discretion. | A decision involving public funding and administrative discretion. |
