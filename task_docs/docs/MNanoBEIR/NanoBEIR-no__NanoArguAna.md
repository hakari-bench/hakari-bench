# MNanoBEIR / NanoBEIR-no / NanoArguAna

## Overview

NanoBEIR-no NanoArguAna is a Norwegian argument retrieval task derived from
ArguAna, the BEIR argument-counterargument benchmark. Each query is a long
argumentative passage, and the target document is the paired counterargument or
closely responding argument in the translated Norwegian corpus. The task is
small in query count but demanding in discourse structure: a model must compare
topic, stance, premise, and response relation across passages that often share
many topical words. For public-facing benchmark documentation, this task is a
good example of retrieval where lexical overlap is helpful but not sufficient,
because the correct item is selected by argumentative fit rather than by a short
factoid answer.

## Details

### What the Original Data Measures

ArguAna was introduced for argument retrieval and argument matching, with
queries and documents drawn from debate-style or argumentative text. In BEIR,
the task is used as a zero-shot retrieval benchmark where systems must retrieve
the argument that best responds to a given argumentative passage. The MNanoBEIR
Norwegian version keeps that retrieval shape while using a compact Nano subset
and translated Norwegian text. The resulting task measures whether embedding
and lexical systems can preserve fine-grained argumentative relationships after
translation, including disagreement, rebuttal, concession, and premise-level
matching.

### Observed Data Profile

This Nano subset contains 50 queries, 3,635 documents, and 50 positive qrels.
Every query has exactly one positive document, so the ranking target is narrow:
retrieval quality depends on placing a single paired response high in the list.
The text is unusually long for a NanoBEIR task, with queries averaging 1,090.36
characters and documents averaging 987.00 characters. These long passages give
retrievers many repeated nouns, entities, and issue terms, but they also create
many near-topic distractors. A high-scoring model therefore needs more than
topic classification; it must recognize which passage answers, opposes, or
directly develops the query's argument.

### BM25 Evaluation Profile

BM25 uses the `bm25` top-500 candidate subset. It reaches nDCG@10 0.3096,
hit@10 0.5600, and recall@100 0.8800. The recall score shows that exact and
near-exact term matching can usually bring the positive document into a broad
candidate pool, which is expected for long argumentative passages with shared
topic vocabulary. The weaker top-10 ranking indicates the harder part of the
task: many documents can discuss the same policy issue, institution, or social
claim while not being the paired counterargument. BM25 is most useful here as a
candidate generator and as a diagnostic for lexical anchoring, but its top ranks
can overvalue repeated issue terms and underweight stance reversal or response
structure.

### Dense Evaluation Profile

Dense retrieval uses the `harrier_oss_v1_270m` top-500 candidate subset. It
scores nDCG@10 0.3985, hit@10 0.6600, and recall@100 0.9200, outperforming BM25
on all three reported measures. This suggests that embedding similarity captures
some of the semantic and argumentative relationship that lexical matching alone
misses. The gain is especially meaningful for Norwegian translated prose,
because a dense model can connect paraphrased premises and response patterns
even when exact word overlap is not dominant. The remaining gap to perfect
recall and ranking still matters: dense similarity may collapse several
same-topic arguments together, especially when the correct pair depends on a
specific rebuttal relation rather than broad semantic relatedness.

### Reranking Hybrid Evaluation Profile

The reranking hybrid subset uses `reranking_hybrid` with top-100 candidates and
an optional rank-101 safeguard. Candidate counts range from 100 to 101, with a
mean of 100.08 and 4 safeguard rows. It reaches nDCG@10 0.3656, hit@10 0.6800,
and recall@100 0.9200. The hybrid setup matches dense recall and slightly
improves hit@10, but its nDCG@10 falls between BM25 and dense. For this task,
the hybrid pool successfully emulates a mixed lexical-semantic retrieval stage,
yet the best early ordering remains closer to dense behavior. Researchers
should read this as a sign that combining BM25 and dense evidence helps cover
more positives in the first page, while a final reranker still needs to model
argument response quality to beat the dense ordering consistently.

### Metric Interpretation for Model Researchers

Because each query has one positive, hit@10 and recall@100 are direct coverage
signals, while nDCG@10 is sensitive to the exact position of that single
positive. A model that raises hit@10 without improving nDCG@10 is finding the
right document on the first page but not ranking it near the top. In NanoArguAna,
that distinction is important: candidate generation can succeed through topic
matching, but final ranking requires stance and discourse understanding. The
dense and hybrid scores indicate that semantic matching is valuable, while the
BM25 recall confirms that lexical evidence should not be ignored. Strong
systems should therefore be evaluated on both candidate coverage and early-rank
precision.

### Query and Relevance Type Tendencies

Queries are full argumentative passages rather than short information needs.
They often include claims, supporting reasons, concrete examples, and policy
terms. Relevant documents tend to respond to the same controversy but may
invert the stance, question a premise, or provide a counterexample. This creates
a high risk of same-topic false positives: documents about the same airport,
reform, religion, cybersecurity, or public policy issue can look close without
being the intended response. The task favors systems that represent discourse
roles and argumentative intent, not only shared entities or topical clusters.

### Representative Failure Modes

Lexical systems may over-rank passages that repeat a query's topic words while
arguing from the wrong angle. Dense systems may retrieve semantically broad
near-neighbors that discuss the same social issue but fail to answer the exact
premise. Hybrid systems may inherit both problems if the candidate pool is not
followed by a reranker that can compare claim, evidence, and rebuttal
structure. Translation also adds risk: idiomatic argumentative phrasing can make
the Norwegian text less direct than the source, so models that rely on surface
templates may miss the intended relation.

### Training Data That May Help

Useful training data includes argument-counterargument pairs, stance-aware
retrieval data, debate response selection, peer-review argument mining, and
multilingual Norwegian or Scandinavian paraphrase data. Hard negatives should
share the topic and many terms with the query while differing in stance,
premise, or response target. To keep evaluation meaningful, training mixtures
should avoid overlap with ArguAna, BEIR, NanoBEIR, and translated versions of
the same argument records.

### Model Improvement Notes

This task is a strong test bed for retrieval models that claim to understand
long-form semantic relations. Improvements are likely to come from better
long-context pooling, contrastive training with same-topic hard negatives, and
rerankers that compare argumentative roles explicitly. BM25 remains useful as a
lexical safety net, but the observed scores show that dense semantic evidence is
the stronger single signal for this Norwegian subset. A production-style system
would likely use hybrid candidate generation followed by a cross-encoder or
late-interaction model trained to distinguish response relevance from topical
similarity.

## Example Data

| Query | Positive document |
| --- | --- |
| Offentligheten er likegyldig overfor reformer. Det er usikkert om reform av Overhuset bør være en topprioritet i den nåværende økonomiske situasjonen, ikke å snakke om om en koalisjonsregjering ville kunne innføre og gjennomføre slike tiltak. Forsøk på å reformere Overhuset har blitt utsatt gang på gang, noe som viser Underhuset sitt motvilje mot endringer. En holdning som uten tvil gjenspeiles i den britiske offentlighetens mening – som vist ved resultatet av den siste folkeavstemningen om alte... [500 / 587 chars] | AV-kampanjen kan ikke sammenlignes med reformer i Overhuset. Man bør ikke forveksle en misinformert offentlighet på grunn av politisk spin med likegyldighet. Ofte uttrykker velgere at de er likegyldige fordi de føler at de ikke kan gjøre noe, at stemmen deres ikke teller. Reformer som sikrer at de som styrer landet blir direkte valgt av folket vil hjelpe til med å motvirke disse følelsene. [392 chars] |
| Utvidelse av Heathrow er avgjørende for økonomien. Utvidelse av Heathrow vil sikre mange eksisterende jobber samt skape nye. For tiden støtter Heathrow rundt 250 000 jobber. Til dette kommer hundretusener flere som er avhengige av turisme i London, som er avhengig av gode transportforbindelser som Heathrow. Å miste konkurransedyktighet overfor andre europeiske flyplasser kan bety at man mister muligheten til å skape nye jobber, og risikerer å miste noen av de som allerede eksisterer. Utvidelse a... [500 / 1,191 chars] | Forretningsmiljøet er langt fra enig i sin antatte støtte til en tredje rullebane. Undersøkelser tyder på at mange innflytelsesrike bedrifter faktisk ikke støtter utvidelsen. Et brev som uttrykte bekymring ble underskrevet av Justin King, administrerende direktør i J Sainsbury, og BskyB’s James Murdoch. Derfor er det feil å se forretningsmiljøet som én stemme som krever utvidelse. Vi bør også huske på, når vi vurderer alternativer til Heathrows nye rullebane, som en ny rullebane på en annen London-flyplass eller en helt ny flyplass, at disse sannsynligvis vil ha en lignende økonomisk påvirkning som utvidelsen av Heathrow. Hvis det er forbindelsene som er viktig for å tiltrekke seg bedrifter og turister, så lenge forbindelsen er med London, spiller det ingen rolle hvilken flyplass forbindelsen er fra. Det kan være mindre behov for at flyplassen skal være en hub-flyplass hvis vi er fokusert på fordeler for London, som Bob Ayling, tidligere administrerende direktør i British Airways, utta... [1,000 / 1,173 chars] |
| Mennesker blir gitt for mange valgmuligheter, noe som gjør dem mindre lykkelige. Reklame fører til at mange blir overveldet av den endeløse behovet for å velge mellom konkurrerende krav på oppmerksomheten – dette kalles valgtyranni eller valgoverbelastning. Nylig forskning tyder på at folk i gjennomsnitt er mindre lykkelige enn de var for 30 år siden – til tross for at de er bedre stilt og har mye flere valg når det gjelder hva de skal bruke pengene sine på. Påstandene i reklame påvirker folk st... [500 / 902 chars] | Folk er ulykkelige fordi de ikke kan få alt, ikke fordi de får for mange valg og finner det stressende. Faktisk spiller reklame en avgjørende rolle i å sikre at folk bruker pengene sine på det mest passende produktet for seg selv. Hvis reklame ikke var tillatt, ville folk sløse penger på et førstevalgsprodukt, når de egentlig ville ha valgt et annet. En meta-analyse som inkluderte forskning fra 50 uavhengige studier fant ingen betydelig sammenheng mellom valg og angst, men spekulerte i at variasjonen i studiene åpnet for muligheten for at valgstress kunne være knyttet til visse svært spesifikke og ennå dårlig forståtte forutsetninger. 1 ^ Scheibehenne, Benjamin; Greifeneder, R. & Todd, P. M. (2010). 'Kan det være for mange valg? En meta-analytisk gjennomgang av valgstress.' Journal of Consumer Research 37: 409-425. [827 chars] |

### Public Sources

- [Argument Mining for Understanding Peer Reviews](https://aclanthology.org/P18-1023/).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).
- [NanoBEIR-no dataset](https://huggingface.co/datasets/hakari-bench/NanoBEIR-no).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Argument Mining for Understanding Peer Reviews | 2018 | task paper | [https://aclanthology.org/P18-1023/](https://aclanthology.org/P18-1023/) |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | [https://arxiv.org/abs/2104.08663](https://arxiv.org/abs/2104.08663) |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | [https://arxiv.org/abs/2502.13595](https://arxiv.org/abs/2502.13595) |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | [https://huggingface.co/collections/zeta-alpha-ai/nanobeir](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
