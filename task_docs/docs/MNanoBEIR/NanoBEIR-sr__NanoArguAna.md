# MNanoBEIR / NanoBEIR-sr / NanoArguAna

## Overview

NanoBEIR-sr NanoArguAna is a Serbian argument retrieval task derived from
ArguAna. Queries are long translated argumentative passages, and the target
document is the paired counterargument or closely responding argument. The task
is useful for evaluating retrieval systems that must go beyond topical
similarity: many documents may discuss the same debate issue, but the relevant
document is the one that responds to the query's stance, premise, or
argumentative structure. This makes it a compact benchmark for long-form
discourse matching in Serbian.

## Details

### What the Original Data Measures

ArguAna is used in BEIR as an argument retrieval task where relevance depends
on argumentative relation, stance, and response suitability. The MNanoBEIR
Serbian version preserves this structure after translation. It measures
whether a model can retrieve the correct counterargument or paired response
from a corpus of long argumentative passages. The task is difficult because
topical overlap is common, but correct retrieval requires understanding which
passage actually answers the argument being made.

### Observed Data Profile

This Nano subset contains 50 queries, 3,635 documents, and 50 positive qrels.
Every query has exactly one positive document, so the ranking target is narrow.
Queries are long, averaging 1,182.86 characters, and documents average 989.77
characters. The long text gives lexical retrievers many possible anchors, but
it also creates many same-topic distractors. A model must distinguish
substantive response relation from general debate-topic similarity.

### BM25 Evaluation Profile

BM25 uses the `bm25` top-500 candidate subset. It reaches nDCG@10 0.2817,
hit@10 0.5000, and recall@100 0.8400. The recall score shows that lexical
matching often brings the positive into a broad candidate pool, but the weak
top-10 ranking shows that term frequency is not enough for this Serbian
argument task. Long passages can share many nouns, policy terms, or examples
without forming the correct counterargument relation. BM25 is therefore useful
as a lexical candidate generator, but it struggles to order passages by stance
and premise-level response.

### Dense Evaluation Profile

Dense retrieval uses the `harrier_oss_v1_270m` top-500 candidate subset. It
scores nDCG@10 0.4187, hit@10 0.7000, and recall@100 0.9400, clearly
outperforming BM25. This suggests that embedding similarity captures more of
the semantic and argumentative relation between query and response than exact
term matching. Dense retrieval is especially useful when the counterargument
uses different wording, reframes the issue, or attacks a premise rather than
repeating the same surface terms. Remaining errors likely come from
same-topic arguments that are semantically close but not the intended pair.

### Reranking Hybrid Evaluation Profile

The reranking hybrid subset uses `reranking_hybrid` with top-100 candidates and
an optional rank-101 safeguard. Candidate counts range from 100 to 101, with a
mean of 100.04 and 2 safeguard rows. It reaches nDCG@10 0.3625, hit@10 0.6600,
and recall@100 0.9600. The hybrid profile has the best top-100 coverage but
does not match dense early ranking. This indicates that combining lexical and
semantic signals is effective for collecting the positive candidate, while a
stronger argument-aware reranker is needed to exploit the pool and place the
paired response at the very top.

### Metric Interpretation for Model Researchers

Because each query has one positive, hit@10 is a direct first-page success
measure and recall@100 indicates whether the positive is available to a
reranker. nDCG@10 shows how highly the correct response is ranked. The dense
profile is strongest for early ranking, while reranking hybrid gives the best
coverage. This makes NanoArguAna-sr useful for separating encoder quality from
candidate generation quality: a good first stage should keep the positive in
the pool, and a good reranker should identify the actual counterargument.

### Query and Relevance Type Tendencies

Queries are long Serbian argumentative passages about public reform, airport
expansion, choice overload, cyberattacks, religion, and free speech. Relevant
documents usually discuss the same controversy but respond from a different
stance or challenge a specific premise. The retrieval target is not merely a
same-topic passage; it is the argument that functions as the appropriate
response. Models need to preserve topic, stance, premise, and discourse role.

### Representative Failure Modes

BM25 may over-rank passages with repeated issue terms but the wrong
argumentative role. Dense models may retrieve semantically related arguments
that address the same controversy but not the same premise. Hybrid retrieval
can recover the correct passage more reliably, but its candidate order can
still contain strong same-topic distractors. Translation can also soften stance
markers or rhetorical cues, which makes response matching harder.

### Training Data That May Help

Helpful training data includes non-overlapping argument retrieval, debate
counterargument pairs, stance-aware retrieval, Serbian or multilingual argument
mining, and hard-negative debate passages. Hard negatives should address the
same topic while answering a different premise or taking an incompatible
stance. Training should exclude ArguAna, BEIR, NanoBEIR, and likely translated
overlaps.

### Model Improvement Notes

NanoArguAna-sr is a strong diagnostic for long-form argument retrieval. Dense
retrieval is the best single ranker, while reranking hybrid provides the best
candidate coverage. Improvements should focus on long-context representation,
stance detection, premise-response modeling, and reranking over same-topic
hard negatives. A practical architecture would use hybrid generation for
coverage and a discourse-aware reranker for final ordering.

## Example Data

| Query | Positive document |
| --- | --- |
| Javnost je apatična prema reformi. Da li bi reforma Doma lordova trebalo da bude glavni prioritet u trenutnoj ekonomskoj klimi je upitno, a kamoli da li bi koaliciona vlada bila sposobna da pokrene i sprovede takve mere. Pokušaji reforme Doma lordova su odlagani iznova i iznova, što pokazuje rezerve Donjeg doma prema promenama. [1] Osećanje koje bez sumnje odjekuje u javnom mujenju Britanaca – kao što je pokazao nedavni ishod glasanja o alternativnom glasanju – javnost je ili protiv ideje promen... [500 / 737 chars] | Kampanja za alternativni glas ne može se porediti sa reformom Doma lordova, štaviše, ne treba mešati neinformisanu javnost usled političkog spinovanja sa apatijom. Često glasači izražavaju da su apatični jer osećaju da ne mogu ništa promeniti, da njihov glas neće biti računat: reforma koja obezbeđuje da ljudi koji vode zemlju budu direktno birani od strane naroda pomogla bi u suzbijanju ovih osećanja. [404 chars] |
| Proširenje Hitroua je od vitalnog značaja za ekonomiju. Širenje Hitroua bi osiguralo mnoga postojeća radna mesta, kao i stvaranje novih. Trenutno, Hitrou podržava oko 250.000 radnih mesta. [1] Povrh toga, još stotine hiljada zavise od turističke trgovine u Londonu, koja se oslanja na dobre transportne veze poput Hitroua. Gubljenje konkurentnosti pred drugim evropskim aerodromima ne samo da bi moglo da podrazumeva propuštanje mogućnosti stvaranja novih radnih mesta, već i gubitak nekih od onih ko... [500 / 1,430 chars] | Poslovna zajednica je daleko od jedinstva u svom navodnom podržavanju treće piste. Ankete pokazuju da mnoge uticajne kompanije zapravo ne podržavaju proširenje. Pismo izražavajući zabrinutost potpisali su Džastin King, izvršni direktor J Sainsburyja, i Džejms Mardok iz BskyB-a. [1] Stoga je pogrešno predstavljati poslovnu zajednicu kao jedinstven glas koji zahteva proširenje. Takođe treba imati na umu, kada razmatramo alternative novoj pisti u Hitrou, poput nove piste na drugom londonskom aerodromu ili potpuno novog aerodroma, da bi one verovatno imale sličan ekonomski uticaj kao proširenje Hitroua. Ako su veze ono što je bitno za privlačenje poslova i turista, onda sve dok je veza sa Londonom, nije bitno sa kog aerodroma se stiže. Čak možda neće biti potrebe da aerodrom bude čvorišni, ako smo fokusirani na koristi za London, kao što je Bob Ejling, bivši izvršni direktor British Airwaysa, izjavio da bi Hitrou trebalo da bude usmeren na putnike koji žele da dođu u London, a ne samo kao... [1,000 / 1,272 chars] |
| Ljudi imaju previše izbora, što ih čini manje srećnim. Oglašavanje dovodi do toga da su mnogi preplavljeni beskrajnom potrebom da odlučuju između konkurentskih zahteva koji se bore za njihovu pažnju – ovo je poznato kao tiranija izbora ili preopterećenje izborom. Nedavna istraživanja pokazuju da su ljudi u proseku manje srećni nego pre 30 godina – uprkos tome što su u boljem materijalnom stanju i imaju mnogo više izbora stvari na koje mogu da troše novac1. Tvrdnje iz reklama nasrću na ljude, pod... [500 / 1,016 chars] | Ljudi su nesrećni jer ne mogu da imaju sve, a ne zato što im se daje previše izbora i to im stvara stres. Zapravo, reklame igraju ključnu ulogu u obezbeđivanju da novac koji ljudi imaju potroše na najprikladniji proizvod za sebe. Da reklame nisu dozvoljene, ljudi bi trošili novac na prvi proizvod koji vide, a kad bi imali izbor, očigledno bi se odlučili za neki drugi. Meta-analiza koja je obuhvatila istraživanja iz 50 nezavisnih studija nije pronašla značajnu vezu između izbora i anksioznosti, ali je pretpostavila da razlike u studijama ostavljaju mogućnost da preopterećenje izborom može biti povezano sa određenim veoma specifičnim i još uvek slabo shvaćenim preduslovima1. 1 ^ Scheibehenne, Benjamin; Greifeneder, R. &amp; Todd, P. M. (2010). "Can There Ever be Too Many Options? A Meta-Analytic Review of Choice Overload" . Journal of Consumer Research 37: 409-425. [876 chars] |

### Public Sources

- [Argument Mining for Understanding Peer Reviews](https://aclanthology.org/P18-1023/).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).
- [NanoBEIR-sr dataset](https://huggingface.co/datasets/hakari-bench/NanoBEIR-sr).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Argument Mining for Understanding Peer Reviews | 2018 | task paper | [https://aclanthology.org/P18-1023/](https://aclanthology.org/P18-1023/) |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | [https://arxiv.org/abs/2104.08663](https://arxiv.org/abs/2104.08663) |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | [https://arxiv.org/abs/2502.13595](https://arxiv.org/abs/2502.13595) |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | [https://huggingface.co/collections/zeta-alpha-ai/nanobeir](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
