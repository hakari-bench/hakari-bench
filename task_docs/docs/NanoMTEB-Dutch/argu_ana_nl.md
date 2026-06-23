# NanoMTEB-Dutch / argu_ana_nl

## Overview

`NanoMTEB-Dutch / argu_ana_nl` is the Dutch ArguAna counterargument retrieval
task from MTEB-NL. Each query is a long Dutch argument, and the positive
document is the best opposing counterargument. The Nano split has 199 queries,
8,624 documents, and 199 positive qrel rows, with exactly one positive document
per query. Current diagnostics show dense retrieval as the strongest top-rank
profile, `reranking_hybrid` as the strongest recall@100 profile, and BM25 as
weaker because same-topic debate passages can share vocabulary while taking the
wrong stance.

## Details

### What the Original Data Measures

MTEB-NL describes ArguAna-NL as a Dutch version of the original ArguAna
argument-retrieval task, included to add argument and counterargument retrieval
coverage to Dutch embedding evaluation. The source dataset card identifies the
task as a BEIR-NL adaptation. No standalone Dutch ArguAna retrieval paper was
confirmed; the task interpretation relies on MTEB-NL, MTEB, and the source
dataset card.

The task measures retrieval of an opposing argumentative response. Relevance is
not just topic similarity: the retrieved document should rebut, qualify, or
oppose the query's claim.

### Observed Data Profile

The Nano split contains 199 queries, 8,624 documents, and 199 positive qrel
rows. Every query has exactly one positive document. Queries average 1,316.90
characters, while documents average 1,141.13 characters.

Queries and documents are long Dutch debate prose, often with claims, reasons,
examples, topic labels, and rhetorical framing. Observed topics include
abortion policy, climate and technology, vegetarianism, baseball collisions,
community radio, tobacco policy, health, and animal ethics.

### BM25 Evaluation Profile

The dataset-provided BM25 candidate subset contains 500 candidates per query and
achieves nDCG@10 = 0.2970, hit@10 = 0.6482, and recall@100 = 0.9246. BM25 can
find the general debate topic because long arguments expose many shared words.

Its weakness is argumentative relation. Same-topic documents with the same
policy vocabulary may support the query or discuss another aspect rather than
counter it. Lexical overlap is therefore a useful candidate-generation signal
but not enough for top-rank counterargument retrieval.

### Dense Evaluation Profile

The dense `harrier_oss_v1_270m` candidate subset contains 500 candidates per
query and achieves nDCG@10 = 0.3723, hit@10 = 0.7839, and recall@100 = 0.9749.
Dense retrieval is the strongest observed top-rank profile.

This suggests that embedding similarity captures Dutch argument-pair semantics
better than pure lexical overlap. It can connect a claim to an opposing response
that uses different wording or focuses on a different premise, consequence, or
policy frame.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset contains mostly 100 candidates per
query, with one query using a rank-101 safeguard row. It achieves nDCG@10 =
0.3529, hit@10 = 0.7538, and recall@100 = 0.9950. Hybrid retrieval has the best
recall@100 but remains below dense retrieval on top-rank metrics.

This makes hybrid search useful as a reranking candidate pool. It preserves the
positive for nearly every query, but the rank order still needs a model that
recognizes rebuttal stance and aspect-level opposition.

### Metric Interpretation for Model Researchers

This task is single-positive: each query has one annotated counterargument.
Hit@10 measures whether that document appears near the top. nDCG@10 is
sensitive to exact rank, and recall@100 measures whether the positive remains
available for a downstream reranker.

Because many same-topic arguments are plausible but uncredited, this benchmark
is a strong test of stance-aware retrieval. A model should retrieve the paired
counterargument, not merely any Dutch passage about the same issue.

### Query and Relevance Type Tendencies

Queries are long Dutch arguments about public policy, ethics, health, sport,
environment, media, and social issues. Relevant documents are opposing
counterarguments with shared topic context but different stance.

The task rewards debate-aspect matching, stance awareness, and long-form Dutch
semantic retrieval. It penalizes models that collapse supporting and opposing
arguments into one topical neighborhood.

### Representative Failure Modes

BM25 can retrieve same-topic same-stance passages because they share many
keywords. Dense retrieval can retrieve a semantically related argument that does
not answer the claim. Hybrid retrieval can preserve the positive but rank a
nearby topic match higher.

Rerankers should identify the query's claim, the candidate's stance, and
whether the candidate attacks or qualifies a premise, consequence, analogy, or
policy framing.

### Training Data That May Help

Useful training data includes non-overlapping Dutch argument-counterargument
retrieval pairs, Dutch debate corpora with stance or rebuttal labels,
translated multilingual argument-mining data with overlap removed, and native
Dutch or Flemish policy discussion pairs. The ArguAna-NL test queries, qrels,
and positive documents used by this Nano split should be excluded from training.

Synthetic data can generate paired Dutch arguments and counterarguments about
public-policy, ethics, health, sport, and environment topics. Positives should
clearly rebut the query. Hard negatives should include same-topic passages with
the wrong stance or a different debated aspect.

### Model Improvement Notes

Dense retrievers should encode stance and rebuttal structure in Dutch, not only
topic. Sparse systems should preserve topic vocabulary but need stance-aware
reranking. Cross-encoders should compare claim, warrant, and rebuttal relation
between query and candidate.

For hybrid systems, `NanoMTEB-Dutch / argu_ana_nl` is a candidate-generation
success case: `reranking_hybrid` nearly covers all positives. The main
opportunity is reranking that turns that coverage into dense-level or better
nDCG@10.

## Example Data

| Query | Positive document |
| --- | --- |
| Tegenstand tegen abortus provocatus in late fase maakt deel uit van een strategie die erop gericht is abortus in het algemeen te verbieden. Abortus provocatus in late fase vormt een klein percentage van alle abortussen, maar vanuit medisch en psychologisch oogpunt zouden ze het minst controversieel moeten zijn. De reden voor deze focus is dat abortussen in late fase het meest evident onaangenaam zijn, omdat foetussen in late fase meer op baby's lijken dan embryo's of foetussen in een eerder ontw... [500 / 804 chars] | zwangerschap filosofie ethiek leven gezin huis zou partiële geboorte-abortussen verbieden Hoewel veel mensen die tegen partiële geboorte-abortus zijn, ook tegen abortus in het algemeen zijn, is er geen noodzakelijk verband, aangezien partiële geboorte-abortus een bijzonder gruwelijke vorm van abortus is. Dit komt om de reeds uitgelegde redenen: het omvat een opzettelijke, moorddadige fysieke aanval op een halfgeboren baby, van wie we zeker weten dat hij pijn zal voelen en zal lijden als gevolg. We accepteren dat er een legitiem medisch debat bestaat over de vraag of embryo's en vroegere foetussen pijn voelen; in dit geval is er geen dergelijk debat, en daarom is partiële geboorte-abortus uniek gruwelijk en uniek onrechtvaardig. [738 chars] |
| Nieuwe technologie heeft de wereld herhaaldelijk revolutionair veranderd door monumentale uitvindingen als landbouw, staal, antibiotica en microchips. En naarmate de technologie verbeterde, verbeterde ook het tempo waarin de technologie zich verbeterde. Er wordt voorspeld dat er tussen 2000 en 2050 32 keer meer verandering zal zijn dan tussen 1950 en 2000. Te midden hiervan zullen veel grote geesten zich richten op emissiereductie en klimaatregelingstechnologieën. Dus, zelfs als de meest ernstig... [500 / 1,095 chars] | Climate House gelooft dat we te laat zijn met de wereldwijde klimaatverandering Technologische verbeteringen zullen vrijwel zeker worden ontwikkeld voor degenen die het zich kunnen veroorloven (zoals de meeste technologie). Klimaatverandering zal echter de grootste gevolgen hebben voor arme landen die zich geen mitigatie kunnen veroorloven. Mogelijk betekent het vermogen om de rijken te beschermen niet dat we niet te laat zijn met de wereldwijde klimaatverandering. [470 chars] |
| Vegetarisch eten vermindert het risico op voedselvergiftiging. Bijna alle gevaarlijke vormen van voedselvergiftiging worden via vlees of eieren overgedragen. Zo worden Campylobacter-bacteriën, de meest voorkomende oorzaak van voedselvergiftiging in Engeland, meestal aangetroffen in rauw vlees en gevogelte, niet-gepasteuriseerde melk en onbehandeld water. Salmonella komt van rauw vlees, gevogelte en zuivelproducten en de meeste gevallen van Escherichia coli (E-coli) voedselvergiftiging treden op... [500 / 945 chars] | dieren milieu algemene gezondheid gezondheid algemeen gewicht filosofie ethiek Voedselveiligheid en -hygiëne zijn zeer belangrijk voor iedereen, en overheden moeten maatregelen nemen om hoge standaarden te garanderen, met name in restaurants en andere plaatsen waar mensen hun voedsel vandaan halen. Maar voedselvergiftiging kan overal voorkomen. "Mensen geven niet graag toe dat de bacteriën uit hun eigen huis zouden kunnen komen" [1], en hoewel vlees bijzonder kwetsbaar is voor besmetting, zijn er bacteriën die via groenten kunnen worden overgedragen, bijvoorbeeld Listeria monocytogenes via rauwe groenten. [2] Bijna driekwart van de zoönotische transmissies wordt veroorzaakt door pathogenen van wilde dieren; zelfs sommige die door vee zouden kunnen zijn veroorzaakt, zoals vogelgriep, zouden evengoed van wilde dieren kunnen komen. Er is weinig dat we kunnen doen aan de overdracht van dergelijke ziekten, behalve door nauw contact te verminderen. Een overstap naar vegetarisme kan dergelijk... [1,000 / 1,743 chars] |

### Public Sources

- [MTEB-NL and E5-NL: Embedding Benchmark and Models for Dutch](https://arxiv.org/abs/2509.12340),
  2025.
- [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316),
  2023.
- [clips/beir-nl-arguana](https://huggingface.co/datasets/clips/beir-nl-arguana).
- [MTEB project repository](https://github.com/embeddings-benchmark/mteb).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| MTEB-NL and E5-NL: Embedding Benchmark and Models for Dutch | 2025 | arXiv paper | [https://arxiv.org/abs/2509.12340](https://arxiv.org/abs/2509.12340) |
| MTEB: Massive Text Embedding Benchmark | 2023 | arXiv paper | [https://arxiv.org/abs/2210.07316](https://arxiv.org/abs/2210.07316) |
| clips/beir-nl-arguana |  | dataset card | [https://huggingface.co/datasets/clips/beir-nl-arguana](https://huggingface.co/datasets/clips/beir-nl-arguana) |
| MTEB project repository |  | repository | [https://github.com/embeddings-benchmark/mteb](https://github.com/embeddings-benchmark/mteb) |

### Representative Snippets

| Query pattern | Positive document pattern |
| --- | --- |
| A Dutch argument that late-stage abortion opposition is a route to banning abortion generally. | A counterargument separating late-stage abortion policy from abortion policy in general. |
| A Dutch argument that technology can keep solving major human problems. | A counterargument about climate change, inequality, and late intervention. |
| A Dutch argument that vegetarian diets reduce food-poisoning risk. | A counterargument emphasizing broader food safety and hygiene. |
| A Dutch argument that baseball collisions are traditional. | A counterargument saying collisions are less central than assumed. |
| A Dutch argument that community radio gives people a voice. | A counterargument warning that community radio can also be misused. |
