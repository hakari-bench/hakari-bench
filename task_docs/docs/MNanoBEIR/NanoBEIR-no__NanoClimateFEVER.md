# MNanoBEIR / NanoBEIR-no / NanoClimateFEVER

## Overview

NanoBEIR-no NanoClimateFEVER is a Norwegian climate-science fact-checking
retrieval task derived from CLIMATE-FEVER. Queries are translated climate
claims, and the retrieval target is one or more translated evidence passages
that support, refute, or contextualize the claim. The task combines short,
claim-like queries with long encyclopedic or scientific evidence documents,
making it useful for studying whether models can bridge compact factual
statements and detailed explanatory passages. It is also a strong multilingual
diagnostic because climate vocabulary is technical, domain-specific, and often
shared across relevant and non-relevant evidence.

## Details

### What the Original Data Measures

CLIMATE-FEVER extends FEVER-style claim verification to climate change claims
and evidence. In BEIR, it is treated as a retrieval task: systems must find
evidence passages relevant to a climate claim before any downstream label
decision can be made. The MNanoBEIR Norwegian version preserves this claim-to-
evidence structure in a compact multilingual setting. It measures whether a
retriever can connect Norwegian translated claims about warming, sea ice,
storms, carbon footprints, and climate attribution to longer passages that
contain the needed evidence.

### Observed Data Profile

This Nano subset contains 50 queries, 3,408 documents, and 148 positive qrels.
Unlike single-answer tasks, most queries have several acceptable evidence
documents: the average is 2.96 positives per query, with a minimum of 1, median
of 3.00, and maximum of 5. There are 44 multi-positive queries, covering 88.0%
of the query set. Queries are short, averaging 124.66 characters, while
documents are much longer at 1,524.22 characters on average. This length
contrast makes the task a classic claim-to-evidence retrieval problem: the
model must map a compressed assertion to the right explanatory document span.

### BM25 Evaluation Profile

BM25 uses the `bm25` top-500 candidate subset and scores nDCG@10 0.2099,
hit@10 0.5000, and recall@100 0.4730. These values show that lexical overlap is
not enough for many climate claims. BM25 can find positives when the claim and
document share distinctive terms, such as named climate phenomena or technical
phrases, but it struggles when the evidence uses broader scientific wording or
when several documents contain the same climate vocabulary. The recall score is
especially important: even with 500 lexical candidates, less than half of all
positive qrel rows appear within the top 100, so a purely lexical first stage
would leave many evidence documents unavailable to a reranker.

### Dense Evaluation Profile

Dense retrieval uses the `harrier_oss_v1_270m` top-500 candidate subset. It
achieves nDCG@10 0.3053, hit@10 0.6600, and recall@100 0.5811, improving over
BM25 across all reported metrics. The improvement matches the task structure:
embedding similarity is better able to connect a short claim to a semantically
related long evidence passage even when wording differs. Dense retrieval still
faces hard negatives, because climate documents often share many domain terms
while only some address the exact claim. The higher hit@10 suggests that dense
representations are effective for finding at least one evidence document per
claim, while the moderate recall@100 shows that collecting all relevant
evidence remains difficult.

### Reranking Hybrid Evaluation Profile

The reranking hybrid subset uses `reranking_hybrid` with top-100 candidates and
an optional rank-101 safeguard. Candidate counts range from 100 to 101, with a
mean of 100.06 and 3 safeguard rows. It reaches nDCG@10 0.2862, hit@10 0.6600,
and recall@100 0.6081. This profile is instructive: hybrid retrieval matches
dense hit@10, exceeds dense recall@100, but has lower nDCG@10 than dense. The
mixed pool therefore improves evidence coverage by adding complementary lexical
and semantic candidates, yet the first few ranks are not ordered as cleanly as
the dense subset. For model researchers, this is a case where hybrid search is
valuable for candidate generation, while a stronger reranker is needed to turn
that broader coverage into better top-rank precision.

### Metric Interpretation for Model Researchers

Because most queries have multiple positives, recall@100 should be read as
evidence coverage rather than simple query success. Hit@10 only asks whether at
least one positive evidence document appears early, while nDCG@10 rewards
placing relevant documents near the top. The observed pattern means dense and
hybrid systems are better than BM25 at getting a useful evidence document onto
the first page, but none of the three candidate profiles captures the full
evidence set reliably. For climate fact checking, this matters because a
downstream verifier may need several complementary passages to evaluate a
claim, not just one topically related document.

### Query and Relevance Type Tendencies

Queries are concise climate claims, often framed as assertions about trends,
causality, or scientific interpretation. Relevant documents are longer passages
that may provide background definitions, historical measurements, or evidence
about the mechanism behind the claim. Some positives may not repeat the claim's
surface wording directly, especially when the document explains a phenomenon
rather than restating the assertion. The task therefore favors retrievers that
represent domain semantics and evidence utility, while still respecting exact
technical terms such as place names, climate variables, and scientific
experiments.

### Representative Failure Modes

BM25 may retrieve documents that repeat climate terms but discuss a different
claim, such as general global warming effects instead of the specific causal
statement in the query. Dense models may retrieve broadly related climate
science passages that are semantically close but insufficient as evidence.
Hybrid systems can improve coverage but may include mixed-quality candidates
from both sides. Translation can add another source of mismatch: Norwegian
claims and evidence may use slightly different phrasing for the same scientific
concept, so models that depend on exact terminology can miss valid evidence.

### Training Data That May Help

Helpful training data includes non-overlapping climate fact-checking examples,
scientific claim-evidence retrieval, FEVER-style multilingual evidence
selection, and Norwegian or Scandinavian scientific QA. Hard negatives should
share climate terminology with the claim but fail to support, refute, or
explain the exact assertion. Training should avoid overlap with CLIMATE-FEVER,
BEIR, NanoBEIR, and translated evidence records likely to appear in this
benchmark.

### Model Improvement Notes

This task rewards systems that combine domain-aware semantic retrieval with
precise evidence discrimination. Dense retrieval is the strongest single
candidate profile here, but reranking hybrid has the best recall@100, so a
practical architecture would use hybrid candidate generation and then apply a
reranker trained for claim-evidence matching. Improvements should target
short-query to long-document alignment, scientific terminology, and
multi-positive evidence coverage. For model comparison, the difference between
hit@10 and recall@100 is especially useful: it separates systems that can find
one plausible evidence passage from systems that can recover the broader
evidence set.

## Example Data

| Query | Positive document |
| --- | --- |
| Fra 1970 til 1998 var det en oppvarmingsperiode som økte temperaturen med omtrent 0,7 grader Fahrenheit, noe som bidro til å skape bevegelsen for klimaendringer. [161 chars] | Paleocen (uttales pronˈpæliəˌsiːn, _ ˈpæ - , _ - lioʊ - ) eller Paleocen, «den gamle nylige», er en geologisk epoke som varte fra omtrent 66 til 56 millioner år siden. Det er den første epoken i Paleogen-perioden i den moderne Kenozoiske æra. Som med mange geologiske perioder, er lagene som definerer epokens begynnelse og slutt godt identifisert, men de eksakte alderene forblir usikre. Paleocen-epoken omfatter to store hendelser i Jordens historie. Den begynte med massedødsutbruddet ved slutten av Kritt, kjent som Kritt-Paleogen (K-Pg) grensen. Dette var en tid preget av utryddelsen av ikke-fugledinosaurer, store marine reptiler og mye annen fauna og flora. Utryddelsen av dinosaurene etterlot tomme økologiske nisjer over hele verden. Paleocen endte med Paleocen-Eocen Termisk Maksimum, en geologisk kort (ca. 0,2 millioner år) periode preget av ekstreme endringer i klima og karbonkretsløp. Navnet «Paleocen» kommer fra gammelgresk og refererer til den «gamle (e)» (παλαιός, palaios) «nye»... [1,000 / 1,051 chars] |
| Faktisk går trenden nedover, selv om den ikke er signifikant. [61 chars] | Solens syklus eller solmagnetisk aktivitetssyklus er en omtrent 11-årige syklus i solens aktivitet (inkludert endringer i nivåene av solstråling og utkast av solmateriale) og utseende (endringer i antall og størrelse på solflekker, flarer og andre fenomener). Disse endringene har blitt observert (gjennom endringer i solens utseende og endringer på jorden, som nordlys) i århundrer. Endringene på solen forårsaker effekter i rommet, i atmosfæren og på jordens overflate. Selv om det er den dominerende variabelen i solaktivitet, oppstår det også uforutsigbare svingninger. [573 chars] |
| Lokale og regionale havnivåer fortsetter å vise den vanlige naturlige variasjonen, stiger på noen steder og synker på andre. [124 chars] | Middelhøyde over havet (MSL) (forkortet bare havnivå) er et gjennomsnittsnivå av overflaten på ett eller flere av Jordens hav, hvorfra høyder som høyder kan måles. MSL er en type vertikal datumsstandardisert geodetisk referansepunkt som brukes, for eksempel, som et kartdato i kartografi og sjønavigasjon, eller i luftfart, som standardhavnivå der atmosfærisk trykk måles for å kalibrere høyde og, følgelig, flynivåer for fly. En vanlig og relativt enkel middelhøyde over havet-standard er midtpunktet mellom middelhøy og middellavvann ved en bestemt sted. Havnivåer kan påvirkes av mange faktorer og er kjent for å ha variert sterkt over geologiske tidsrom. Nøyaktig måling av variasjoner i MSL kan gi innsikt i pågående klimaendringer, og havnivåstigning har blitt mye sitert som bevis på pågående global oppvarming. Begrepet over havnivå henviser vanligvis til over middelhøyde over havet (AMSL). [899 chars] |

### Public Sources

- [CLIMATE-FEVER](https://arxiv.org/abs/2012.00614).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).
- [NanoBEIR-no dataset](https://huggingface.co/datasets/hakari-bench/NanoBEIR-no).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| CLIMATE-FEVER | 2020 | task paper | [https://arxiv.org/abs/2012.00614](https://arxiv.org/abs/2012.00614) |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | [https://arxiv.org/abs/2104.08663](https://arxiv.org/abs/2104.08663) |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | [https://arxiv.org/abs/2502.13595](https://arxiv.org/abs/2502.13595) |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | [https://huggingface.co/collections/zeta-alpha-ai/nanobeir](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
