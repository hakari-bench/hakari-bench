# NanoMIRACL / sw

## Overview

`NanoMIRACL / sw` is the Swahili-oriented split of the MIRACL-style
multilingual monolingual retrieval benchmark. The task is intended to retrieve
Swahili Wikipedia passages for Swahili questions, although the repository
metadata labels the split as multilingual and notes both Swahili and English
signals. The Nano split has 200 queries, 10,000 documents, and 405 positive qrel
rows. Current diagnostics show dense retrieval as the strongest top-rank
profile, `reranking_hybrid` as the strongest recall profile, and BM25 as a
useful lexical baseline for names, countries, offices, and short factual terms.

## Details

### What the Original Data Measures

MIRACL was introduced as a multilingual ad hoc retrieval benchmark over
Wikipedia passages. Its design is monolingual for each language: Swahili
queries retrieve Swahili passages. The benchmark emphasizes native-language
questions, passage-level evidence, and human relevance judgments.

Swahili is one of the MIRACL languages connected to the TyDi/Mr. TyDi lineage.
The MIRACL framing adds passage-level relevance judgments over a segmented
Wikipedia corpus. For this split, the relevant item is a passage containing
answer evidence, not a translated answer or a short answer string.

### Observed Data Profile

The Nano split contains 200 queries, 10,000 documents, and 405 positive qrel
rows. Positives per query average 2.03, with a minimum of 1, a median of 2, and
a maximum of 8. There are 104 multi-positive queries, representing 52.0 percent
of the split. Queries average 38.33 characters, while documents average 278.02
characters.

The observed queries are primarily Swahili short fact questions, with forms such
as `Je`, `Nani`, `Mji`, `Nchi`, `Jina`, `Rais`, `Ni nini`, `lini`, and `ngapi`.
Some queries attach punctuation directly to words, such as `Je,rais` or
`Je,nani`. Topics include people, countries, political offices, geography,
science, medical terms, sports, music, animals, diseases, religion, and
definitions.

### BM25 Evaluation Profile

The dataset-provided BM25 candidate subset contains 500 candidates per query and
achieves nDCG@10 = 0.5852, hit@10 = 0.8550, and recall@100 = 0.9630. BM25 is
useful when the query contains distinctive Swahili or named-entity anchors such
as people, countries, clubs, organizations, scientific names, or office titles.

The sparse profile is limited by short questions and near-topic distractors.
Country, president, capital, border, animal, and music questions often share
many terms with related passages, while only one passage states the requested
relation. Punctuation variants and multilingual names also make exact matching
less reliable than a pure keyword interpretation would suggest.

### Dense Evaluation Profile

The dense `harrier_oss_v1_270m` candidate subset contains 500 candidates per
query and achieves nDCG@10 = 0.7872, hit@10 = 0.9350, and recall@100 = 0.9630.
Dense retrieval is the strongest observed profile by nDCG@10 and hit@10. It
ranks answer-bearing passages much higher than BM25 by matching the semantic
relation requested by the Swahili question.

Dense retrieval does not improve recall@100 over BM25 in this split; both have
the same observed recall. The main dense advantage is top-rank ordering, not
candidate coverage. This makes the split useful for testing whether a model can
rank the right evidence passage above related country, person, or definition
pages.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset contains exactly 100 candidates per
query, with no safeguard rows. It achieves nDCG@10 = 0.7292, hit@10 = 0.9250,
and recall@100 = 0.9975. Hybrid retrieval is below dense retrieval by nDCG@10
and hit@10, but it has the strongest top-100 positive coverage.

This profile shows the value of combining lexical and semantic retrieval for
Swahili. BM25 contributes exact names, countries, and short surface forms, while
dense retrieval contributes relation matching. The hybrid candidate set is
therefore the best source for downstream reranking, even though dense retrieval
alone places top evidence better.

### Metric Interpretation for Model Researchers

This task is multi-positive for 52.0 percent of queries. Hit@10 measures whether
at least one relevant passage appears near the top. nDCG@10 rewards ranking
relevant passages high, and recall@100 measures how much of the judged positive
set remains available for reranking.

The Swahili pattern separates top-rank quality from coverage. Dense retrieval is
best for direct evidence ranking, while `reranking_hybrid` is best for retaining
the positive set. BM25 remains important as a lexical anchor, especially where
queries contain names, countries, offices, and scientific terms.

### Query and Relevance Type Tendencies

Queries are short Swahili fact questions about people, presidents, countries,
capitals, borders, dates, clubs, animals, diseases, scientific names, music, and
definitions. Many require retrieving a specific attribute: founder, birth date,
capital, first president, border count, pregnancy duration, or scientific name.

Relevant documents are primarily Swahili Wikipedia passages with title context
and answer-bearing prose. The task rewards punctuation-robust token handling,
entity matching, and semantic relation selection. The multilingual metadata
note means models should also be robust to English names, loanwords, and
occasional language-detection noise.

### Representative Failure Modes

BM25 can retrieve near-country or geography pages before the passage that lists
Mozambique's bordering countries. A question about the first U.S. president can
retrieve pages about current or other national leaders before the U.S.
presidents passage. A question about giraffe pregnancy duration can retrieve
general pregnancy or weight-related vocabulary before the giraffe evidence. A
question about the scientific name of beans can retrieve related bean pages
before the passage naming `Phaseolus vulgaris`.

Dense retrieval can still choose a semantically related passage that lacks the
exact requested attribute. Hybrid retrieval reduces missing positives but still
needs reranking when several country, person, or scientific-term candidates are
plausible.

### Training Data That May Help

Useful training data includes non-overlapping MIRACL Swahili training data,
Swahili Wikipedia question-to-passage retrieval pairs, Swahili open-domain QA
evidence retrieval datasets, and multilingual African-language QA pairs with
explicit Swahili evidence passages. Hard negatives should include related
countries, people, institutions, animals, diseases, and scientific terms.

Synthetic data can help when it creates Swahili Wikipedia-style passages with
titles, aliases, dates, locations, offices, borders, scientific names,
definitions, and factual evidence. Generated questions should use varied `Je`,
`Nani`, `Mji`, `Nchi`, `Jina`, `Rais`, `Ni nini`, `lini`, and `ngapi` forms,
including realistic punctuation and spacing variants. Comparable evaluation
should exclude upstream development/test data or other MIRACL-derived examples
likely to overlap with this Nano split.

### Model Improvement Notes

Dense retrievers should preserve their strong top-rank behavior while improving
coverage toward the hybrid profile. Sparse systems need robust token handling
for Swahili punctuation, names, and loanwords, plus better ranking of relation
evidence over topic overlap. Rerankers should combine exact names and country
signals with answer-relation matching.

For hybrid systems, `NanoMIRACL / sw` supports `reranking_hybrid` as a
high-recall candidate stage. Dense retrieval sets the top-rank quality target,
while hybrid retrieval supplies broader positive coverage for reranking.

## Example Data

| Query | Positive document |
| --- | --- |
| Chelsea F.C. ilizinduliwa lini? [31 chars] | Chelsea F.C. Chelsea Football Club ni klabu ya mpira wa miguu ya nchini Uingereza iliyo na maskani yake Fulham, London. Klabu hii ilianzishwa mwaka 1905, na kwa miaka mingi sana imekuwa ikishiriki lig... [200 / 359 chars] |
| Rais wa kwanza wa Gabon aliitwa nani? [37 chars] | Omar Bongo Kiongozi huyo amevunja rekodi ya kuwa Rais aliyekaa muda mrefu marakani kuliko Rais yeyote barani Afrika. Rais huyo amefariki dunia akiwa na umri wa miaka 73, ambapo ameiongoza Gabon kwa mi... [200 / 1,263 chars] |
| Je,nani mwanzilishi wa mziki wa hIhop nchini Tanzania? [54 chars] | Machozi Jasho na Damu Halkadhalika ame-enzi kazi ya mwanzilishi halisi wa rap ya Kiswahili nchini Tanzania bwana Edward Mtui (maarufu kama Fresh XE) kwa kuchukua kiitikio chake cha "Piga Makofi" ambac... [200 / 412 chars] |
| Nigeria ilipata huru mwaka gani? [32 chars] | Ahmadu Bello Katika uchaguzi wa kwanza uliofanyika Kaskazini mwa Nigeria mwaka 1952, Bwana Ahmadu Bello alishinda [[kiti[[ cha bunge cha Kaskazini, na kuwa mwanachama wa [[baraza tendaji]] kikanda kam... [200 / 1,289 chars] |
| Nani alikuwa rais wa kwanza Urusi? [34 chars] | Boris Yeltsin Boris Nikolayevich Yeltsin () (kwa herufi za Kirusi huita:Бори́с Никола́евич Е́льцин) (1 Februari 1931 - 23 Aprili 2007) alikuwa rais wa kwanza wa Urusi baada ya mwisho wa ukomunisti. Al... [200 / 454 chars] |

### Public Sources

- [Making a MIRACL: Multilingual Information Retrieval Across a Continuum of Languages](https://arxiv.org/abs/2210.09984),
  2022.
- [MIRACL: A Multilingual Retrieval Dataset Covering 18 Diverse Languages](https://aclanthology.org/2023.tacl-1.63/),
  2023.
- [MIRACL GitHub repository](https://github.com/project-miracl/miracl).
- [miracl/miracl-corpus](https://huggingface.co/datasets/miracl/miracl-corpus),
  source corpus dataset.
- [hakari-bench/NanoMIRACL](https://huggingface.co/datasets/hakari-bench/NanoMIRACL),
  Nano benchmark dataset.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Making a MIRACL: Multilingual Information Retrieval Across a Continuum of Languages | 2022 | paper | [https://arxiv.org/abs/2210.09984](https://arxiv.org/abs/2210.09984) |
| MIRACL: A Multilingual Retrieval Dataset Covering 18 Diverse Languages | 2023 | paper | [https://aclanthology.org/2023.tacl-1.63/](https://aclanthology.org/2023.tacl-1.63/) |
| MIRACL GitHub repository |  | project repository | [https://github.com/project-miracl/miracl](https://github.com/project-miracl/miracl) |
| miracl/miracl-corpus |  | dataset card | [https://huggingface.co/datasets/miracl/miracl-corpus](https://huggingface.co/datasets/miracl/miracl-corpus) |

### Representative Snippets

| Query pattern | Positive document pattern |
| --- | --- |
| A Swahili question asking when Chelsea F.C. was founded. | A passage about Chelsea Football Club and its 1905 founding. |
| A question asking who Gabon's first president was. | A passage about Omar Bongo or Gabon political leadership. |
| A question asking who founded Tanzanian hip-hop. | A music-history passage naming the relevant founder. |
| A question asking when Nigeria gained independence. | A passage about Nigerian political history or independence context. |
| A question asking who the first president of Russia was. | A passage about Boris Yeltsin and post-Soviet Russia. |
