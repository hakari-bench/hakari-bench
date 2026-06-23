# NanoMTEB-Misc / wmt21_fr_de

## Overview

`wmt21_fr_de` is the reverse WMT21 German-French CLSD direction. Queries are
German news sentences, and documents are French candidate sentences. The
positive document is the French translation counterpart of the German query.
The Nano split contains 200 queries, 4,465 documents, and 200 positive qrels,
with exactly one positive per query. Queries average 174.99 characters, and
documents average 174.45 characters. The task evaluates German-to-French
sentence retrieval under semantic distractors, with finance and politics news
examples that often preserve names and numbers across languages.

## Details

### What the Original Data Measures

[Cross-Lingual Semantic Discrimination for Building Better Multilingual Embeddings](https://arxiv.org/abs/2502.08638)
presents CLSD as a benchmark for multilingual embeddings that must discriminate
true cross-lingual equivalents from semantically close distractors. The
[Andrianos/clsd_wmt19_21](https://huggingface.co/datasets/Andrianos/clsd_wmt19_21)
dataset card provides the WMT21 German-French retrieval tables used by MTEB.

This split reverses `wmt21_de_fr`: German sentences retrieve French
translations. Relevance is exact sentence equivalence.

### Observed Data Profile

The split has 200 German queries, 4,465 French documents, and 200 positive
judgments. Every query has one positive. The sentences are news translation
pairs involving political testimony, pension reform, investor capital, large
technology companies, GDP estimates, and COVID-era economic effects.

Shared names and numbers are common in the examples, which gives BM25 more
signal than in some other CLSD directions, but translation equivalence still
requires semantic alignment.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.4658, hit@10 of 0.6950, and recall@100 of 0.8050.
This is the strongest BM25 profile among the WMT CLSD splits in this batch,
likely because many WMT21 finance-news sentences contain shared companies,
dates, percentages, and names. Even so, BM25 remains far below dense retrieval.

Lexical overlap can identify likely candidates but cannot reliably distinguish
the true translation from same-entity distractors.

### Dense Evaluation Profile

Dense retrieval is strongest for top ranking, with nDCG@10 of 0.8954, hit@10
of 0.9350, and recall@100 of 0.9350. It captures German-French semantic
equivalence substantially better than BM25, though it is slightly less
near-ceiling than the WMT19 reverse direction.

This split is useful for checking whether a multilingual model maintains
sentence-level precision when shared names and numbers could tempt a lexical or
shallow semantic match.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` profile reaches nDCG@10 of 0.6999, hit@10 of 0.8750,
and recall@100 of 0.9900. It has the best recall@100 but does not match dense
top-10 ordering. Candidate lists contain 100 to 101 entries, with two
safeguard-positive rows.

Hybrid search is useful as a reranking pool because it recovers almost every
true translation by rank 100. Its early ranking is diluted by lexical
distractors that share names or figures but do not express the same sentence.

### Metric Interpretation for Model Researchers

`wmt21_fr_de` is dense-favorable at top-10 and hybrid-favorable for coverage.
BM25 is unusually competitive for a cross-lingual task but remains insufficient.
Since every query has one positive, nDCG@10 measures the rank of the true
French translation directly.

Researchers should focus on semantic discrimination errors, especially those
involving shared entities, dates, percentages, and market terms.

### Query and Relevance Type Tendencies

Queries are German news sentences, and positive documents are French
translations. Many examples contain named political figures, companies, dates,
and numeric values. Distractors can share those anchors while changing the
actual proposition.

Relevance is strict translation equivalence. Sentence pairs that discuss the
same topic but differ in detail are negatives.

### Representative Failure Modes

BM25 can over-rank French sentences with the same names or numbers but a
different statement. Dense retrieval can fail on subtle differences in
attribution, timing, amount, or actor. Hybrid retrieval improves recall but
pulls lexical distractors upward.

Financial and political news sentences often differ by one number, date, or
actor, so models need fine-grained cross-lingual proposition matching.

### Training Data That May Help

Useful training data includes German-French sentence retrieval, WMT-style news
bitext, multilingual contrastive training, and CLSD hard-negative objectives.
Hard negatives should share people, numbers, and institutions while changing
meaning. Training should avoid WMT21 evaluation pairs and overlapping
distractors.

Synthetic data should generate German-to-French retrieval pairs from unseen
parallel news sentences and add French distractors that preserve entities or
figures but correspond to different statements.

### Model Improvement Notes

Dense encoders should be trained for proposition-level equivalence across
German and French. Rerankers should verify numbers, dates, negation, actor, and
scope. Hybrid candidate pools are useful for recall, but lexical overlap should
not dominate final ranking.

## Example Data

| Query | Positive document |
| --- | --- |
| Am selben Tag kündigte das Büro des Premierministers an, dass Justin Trudeau, wie von der Opposition gefordert, zu einem noch zu bestimmenden Termin ebenfalls vor diesem Ausschuss aussagen wird. [194 chars] | Le même jour, le bureau du premier ministre a fait savoir que Justin Trudeau témoignerait lui aussi devant cette commission, comme l'exige l'opposition, à une date restant à déterminer. [185 chars] |
| Präsident Sebastian Piñera verkündete am 24. Juli eine historische Reform, die es den Chilenen erlaubt, 10 % ihrer privaten Rentenfonds vorzeitig zu entnehmen, um die durch die Covid-19-Pandemie verursachte Wirtschaftskrise zu bewältigen. [238 chars] | Le président Sebastian Piñera a promulgué le 24 juillet une réforme historique qui permet aux Chiliens le retrait anticipé de 10% de leurs fonds de retraite privés pour faire face à la crise économique entraînée par la pandémie de Covid-19. [240 chars] |
| Geringfügige Anpassungen sollen mehr Kapital für Investoren freisetzen und es so „den Unternehmen leichter machen, die benötigte Finanzierung zu erhalten und in unsere Wirtschaft zu investieren“, versichert der Vizepräsident der Europäischen Kommission Valdis Dombrovskis. [272 chars] | Des ajustements mineurs qui doivent libérer plus de capital pour les investisseurs et donc permettre aux "entreprises d'obtenir plus facilement les financements dont elles ont besoin et d'investir dans notre économie", assure le vice-président de la Commission européenne, Valdis Dombrovskis. [292 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Cross-Lingual Semantic Discrimination for Building Better Multilingual Embeddings | 2025 | Task paper | [https://arxiv.org/abs/2502.08638](https://arxiv.org/abs/2502.08638) |
| Andrianos/clsd_wmt19_21 | 2025 | Dataset card | [https://huggingface.co/datasets/Andrianos/clsd_wmt19_21](https://huggingface.co/datasets/Andrianos/clsd_wmt19_21) |

### Representative Snippets

| Query | Positive document |
| --- | --- |
| A German sentence about Justin Trudeau testifying before a committee. | The French translation saying the prime minister's office announced Trudeau would testify. |
| A German sentence about Sebastian Pinera's pension-fund reform. | The French translation about Chileans withdrawing 10 percent of private retirement funds. |
| A German sentence about freeing more capital for investors. | The French translation about helping companies obtain financing and invest. |
| A German sentence about Apple, Alphabet, Amazon, and second-quarter GDP. | The French translation about those companies publishing results and a GDP estimate. |
| A German sentence about Trudeau admitting a mistake during UNIS negotiations. | The French translation saying he admitted not withdrawing from discussions. |
