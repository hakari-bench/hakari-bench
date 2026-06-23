# NanoMTEB-Dutch / belebele_nld_latn_nld_latn

## Overview

`belebele_nld_latn_nld_latn` is the same-language Dutch Belebele retrieval task
in NanoMTEB-Dutch. Dutch reading-comprehension questions retrieve Dutch
passages. The Nano split contains 200 queries, 488 documents, and 200 positive
qrel rows, with one relevant passage for every query. Compared with the cross-
lingual Belebele directions, this task removes the language-bridge problem and
instead asks whether a model can rank the correct Dutch evidence passage above
other compact Dutch passages.

The evaluation profile shows a strong lexical baseline, an even stronger dense
baseline, and the best top-10 score from `reranking_hybrid`. BM25 reaches high
top-10 accuracy because the query and document are both Dutch and many
questions reuse distinctive words, entities, or phrases. Dense retrieval
improves the ranking by capturing paraphrases and semantic question intent. The
hybrid candidate column combines these signals effectively: it has the highest
nDCG@10 and the highest recall@100, making this split a useful example where
lexical and embedding evidence are complementary rather than competing.

## Details

### What the Original Data Measures

[The Belebele Benchmark](https://arxiv.org/abs/2308.16884) is a parallel
reading-comprehension benchmark built across 122 language variants. Its
passages are based on FLORES-200 material, and the questions are designed to be
answerable from the passage. In the retrieval formulation used here, a model is
not selecting an answer option; it is selecting the passage that supports the
question.

The Dutch MTEB-NL benchmark includes Belebele retrieval to measure Dutch
embedding quality on reading-comprehension style passage retrieval. This Nano
task keeps that basic structure but uses a compact 200-query evaluation split.
Because both query and document are Dutch, the task is a clean same-language
probe for Dutch passage retrieval, semantic paraphrase handling, and robust
ranking among short translated passages.

### Observed Data Profile

The split has 200 single-positive queries over 488 Dutch documents. Queries
average 69.39 characters, while documents average 529.14 characters. The short
query and longer passage setup produces a typical passage retrieval problem:
the relevant document usually contains the requested answer alongside several
other facts, so the model must match the exact information need rather than
only the broad topic.

Representative examples ask about a shooting event, temporary detention rules,
the Chandrayaan-1 moon probe, rewriting the Clean Air Act, and suspension of the
NBA season. These questions often contain strong lexical cues, but correct
ranking still requires understanding the relation requested by the question:
which statement is true, what must detainees receive, which statement is not
true, who proposed a policy change, or what organization suspended an event.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 = 0.8364, hit@10 = 0.9150, and recall@100 = 0.9700 over
the 488-document candidate set. This is a strong sparse baseline. Query terms
and passage terms are in the same language, and many Dutch questions include
distinctive nouns, named entities, or quoted phrases that appear in the
positive passage. In this task, term-frequency and exact-word evidence often
places the correct passage very near the top.

The remaining BM25 errors identify the semantic portion of the benchmark. BM25
can confuse passages that share an event, policy name, person, or location but
answer a different question. It is also weaker when a query asks for an
inference, an exception, or a statement-level judgment such as "which of the
following is not true." For researchers, the high BM25 score means dense models
should be compared against a serious lexical baseline rather than against a
weak keyword system.

### Dense Evaluation Profile

Dense retrieval with `harrier_oss_v1_270m` reaches nDCG@10 = 0.8899, hit@10 =
0.9600, and recall@100 = 0.9650. Dense retrieval improves the top-10 ranking
over BM25, which suggests that embedding similarity is capturing paraphrase,
question intent, and passage-level answerability beyond simple word overlap.
The slight drop in recall@100 relative to BM25 is small, but it shows that
lexical cues still recover a few positives that the dense model ranks too low.

The dense model's strength is most relevant for questions where the answer is
not signaled by a single rare word. It can connect a Dutch question to a passage
that expresses the same event or relation with different wording. Its likely
failure mode is topical overgeneralization: a same-topic passage may be close
in embedding space even when it does not contain the exact answer requested by
the query.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate column reaches nDCG@10 = 0.8999, hit@10 =
0.9500, and recall@100 = 0.9900, with 100 to 101 candidates per query and two
rank-101 safeguard rows. This is the strongest overall profile in the task. It
does not dominate every individual metric: dense retrieval has a slightly
higher hit@10, while BM25 has slightly higher recall@100 than dense. But the
hybrid column combines the best parts of both signals and gives the strongest
top-ranked ordering by nDCG@10.

This pattern is important because it differs from the cross-lingual Belebele
directions. Here, BM25 is not just adding noisy entity matches; it contributes
useful Dutch lexical evidence. Dense retrieval contributes semantic matching
and paraphrase tolerance. The hybrid pool therefore emulates a practical search
system where sparse and dense retrieval complement each other, and a reranker
can benefit from both candidate sources.

### Metric Interpretation for Model Researchers

Because each query has one positive passage, nDCG@10 mostly reflects how high
that single positive is placed. Hit@10 asks whether the positive is present in
the first ten candidates, and recall@100 measures whether the candidate source
is suitable for a downstream reranker. In this task, all three retrieval modes
are viable candidate generators, but their strengths differ.

BM25 is already high enough that a dense model must add real semantic ranking
value. Dense retrieval does add that value in nDCG@10 and hit@10. The hybrid
column is best interpreted as a reranking input with very high positive
coverage and strong initial ordering. It is a useful benchmark for whether a
reranker can take advantage of both exact Dutch lexical evidence and dense
semantic similarity.

### Query and Relevance Type Tendencies

The queries are Dutch comprehension questions over short-to-medium passages.
They ask for factual identification, causal explanation, statement validation,
or the role of a named person or institution. The positive passage usually
contains the answer explicitly, but it may appear within a paragraph that
includes several other facts.

Relevant passages are not long documents with many possible answers. They are
compact evidence passages, so ranking quality depends on identifying the exact
answer-bearing paragraph. This makes the task sensitive to hard negatives that
share the same event, organization, date, or topic.

### Representative Failure Modes

BM25 can fail when the question and passage use different wording for the same
fact, or when another passage shares the most distinctive terms but answers a
different question. Dense retrieval can fail when it retrieves a semantically
near Dutch passage that matches the general topic but not the requested detail.

Hybrid failures are likely to occur when lexical and dense evidence both point
to plausible but incomplete passages. For example, a passage may mention the
same policy or organization but not the action asked about by the query. Such
cases are good targets for reranker training because they require answerability
rather than topic recognition.

### Training Data That May Help

Useful training data includes Dutch reading-comprehension retrieval pairs,
Dutch QA-to-passage retrieval data, non-overlapping Belebele-style translated
data, and Dutch hard-negative passage ranking data. The most useful negatives
are same-topic Dutch passages with shared entities but different answers.

Training and synthetic data should exclude Belebele test questions and passages
used by this Nano split. Synthetic data can use short Dutch news or
encyclopedic passages outside the evaluation set, paired with Dutch questions
that target a specific fact, cause, person, location, or exception. The positive
passage should explicitly contain the answer, while negatives should be
semantically close enough to test fine ranking.

### Model Improvement Notes

The most direct way to improve this task is to combine precise Dutch lexical
matching with semantic passage understanding. Dense models should be trained to
distinguish answer-bearing paragraphs from same-topic distractors, not only to
retrieve generally related passages. Sparse-aware training or hybrid distillation
may also help because BM25 already captures many useful Dutch cues.

For rerankers, the task rewards using both sources of evidence. A strong system
should preserve lexical matches when they identify the correct passage, but it
should override them when a semantically clearer answer-bearing passage is
available. This makes the split a practical diagnostic for Dutch hybrid search
rather than a pure dense-only benchmark.

## Example Data

| Query | Positive document |
| --- | --- |
| Welke uitspraak over het evenement waar de schietpartij plaatsvond, is juist? [77 chars] | Er waren op zijn minst 100 mensen op het feest aanwezig die de eerste huwelijksdag vierden van een koppel dat vorig jaar trouwde. Er stond een formeel verjaardagsevenement gepland voor een latere datum, volgens de ambtenaren. Het stel trouwde een jaar geleden in Texas en vierde het in Buffalo met vrienden en familie. De 30-jarige echtgenoot is in Buffalo geboren en een van de vier personen die bij de schietpartij zijn gedood, maar zijn vrouw is niet gewond geraakt. [469 chars] |
| Wat moeten arrestanten volgens het tijdelijke contactverbod dat in de tekst wordt genoemd, krijgen om langer dan 24 uur te mogen worden vastgehouden? [149 chars] | In de afgelopen 3 maanden zijn er meer dan 80 arrestanten uit de Central Booking-inrichting vrijgelaten zonder dat ze officieel zijn aangeklaagd. In april van dit jaar heeft rechter Glynn een tijdelijk contactverbod tegen de faciliteit uitgevaardigd om zo de vrijlating van mensen af te dwingen die 24 uur na hun verbalisering nog werden vastgehouden en voor wie nog geen hoorzitting van een gerechtscommissaris mogelijk was. De commissaris bepaalt, indien van toepassing, de borgtocht en maakt de aanklachten formeel die zijn ingediend door de arresterende agent. De aanklachten worden vervolgens in het computersysteem van de staat ingevoerd, waarna de zaak wordt bijgehouden. Vanaf de hoorzitting heeft de verdachte ook recht op een snel proces. [748 chars] |
| Welke uitspraak over de maansonde van de Chandrayaan-1 is niet waar? [68 chars] | De onbemande ruimtesonde Chandrayaan-1 wierp zijn Moon Impact Probe (MIP) uit, die vervolgens met 1,5 kilometer per seconde (3000 mijl per uur) over de oppervlakte van de maan werd geslingerd en met succes in de buurt van de zuidpool van de maan landde. De maansonde bevatte naast drie belangrijke wetenschappelijke instrumenten ook een afbeelding van de Indiase vlag, die er aan alle kanten is opgeschilderd. [409 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| The Belebele Benchmark: a Parallel Reading Comprehension Dataset in 122 Language Variants | 2023 | arXiv paper | [https://arxiv.org/abs/2308.16884](https://arxiv.org/abs/2308.16884) |
| facebookresearch/belebele | 2023 | repository | [https://github.com/facebookresearch/belebele](https://github.com/facebookresearch/belebele) |
| mteb/belebele |  | dataset card | [https://huggingface.co/datasets/mteb/belebele](https://huggingface.co/datasets/mteb/belebele) |
| MTEB-NL and E5-NL: Embedding Benchmark and Models for Dutch | 2025 | arXiv paper | [https://arxiv.org/abs/2509.12340](https://arxiv.org/abs/2509.12340) |

### Representative Snippets

| Query | Positive passage |
| --- | --- |
| Welke uitspraak over het evenement waar de schietpartij plaatsvond, is juist? | A Dutch passage says at least 100 people attended a celebration for a couple's first wedding anniversary, with a formal birthday event planned later. |
| Wat moeten arrestanten krijgen om langer dan 24 uur te mogen worden vastgehouden? | A Dutch passage discusses releases from Central Booking and a temporary court order requiring detainees to be formally charged. |
| Welke uitspraak over de maansonde van de Chandrayaan-1 is niet waar? | A Dutch passage describes Chandrayaan-1 releasing its Moon Impact Probe and the probe's successful impact near the lunar south pole. |
| Wie stelde voor om de Clean Air Act te herschrijven? | A Dutch passage says Prime Minister Stephen Harper agreed to send the government's Clean Air Act to an all-party committee for review. |
| Welke van de volgende heeft de NBA besloten op te schorten? | A Dutch passage explains that the NBA suspended its professional basketball season after a player tested positive during the COVID-19 pandemic. |
