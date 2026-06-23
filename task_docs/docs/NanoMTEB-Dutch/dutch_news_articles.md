# NanoMTEB-Dutch / dutch_news_articles

## Overview

`dutch_news_articles` is a Dutch news retrieval task from MTEB-NL. Queries are
short NOS-style news headlines, and documents are Dutch news article bodies or
summaries. The Nano split contains 200 queries, 10,000 documents, and 200
positive qrel rows, with one positive article per query. It tests whether a
retrieval model can map a concise headline to the matching article in a Dutch
current-affairs corpus.

This is a high-signal headline-to-article task rather than a difficult
paraphrase-only retrieval problem. BM25 is very strong because headlines and
articles often share named entities, event nouns, locations, and distinctive
phrases. Dense retrieval with `harrier_oss_v1_270m` has the highest nDCG@10,
while `reranking_hybrid` has the highest hit@10 and recall@100. The task is
useful for measuring precise event matching, especially whether a model ranks
the exact article above other articles about the same person, place, or news
topic.

## Details

### What the Original Data Measures

[MTEB-NL and E5-NL](https://arxiv.org/abs/2509.12340) includes
DutchNewsArticlesRetrieval as a native Dutch retrieval task. The source
metadata points to the public Dutch News Articles Kaggle dataset, described as
articles scraped from the NOS website. No standalone retrieval paper was
confirmed for this task, so the interpretation is based on the MTEB-NL paper,
the Kaggle source record, the Hugging Face dataset card, and observed Nano
examples.

In retrieval form, the task asks a model to retrieve the article body that
corresponds to a headline-like query. This differs from duplicate-question
retrieval: the query is not a paraphrased forum question, but a short news
title that intentionally summarizes one article. The main challenge is event-
level disambiguation among many related news documents.

### Observed Data Profile

The split contains 200 queries over 10,000 documents. Queries average 48.96
characters, while documents average 1,146.66 characters. Documents are much
longer than the query and can contain several entities, quotes, secondary
events, and background details. The positive article is usually identifiable by
the headline's main event.

Examples include a police officer dismissed after drug use, primary school
children becoming unwell during a cooking lesson, IS taking control of a
refugee camp near Damascus, parliamentary concerns about a mission in Ukraine,
and children dying in a fire in Mexico. These examples show that the task
rewards matching the central news event, not merely retrieving an article that
mentions the same country or institution.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 = 0.8868, hit@10 = 0.9350, and recall@100 = 0.9750 over
top-500 candidate lists. This is a very strong lexical baseline. Headlines
often reuse distinctive words from the article, and news writing repeats names,
locations, organizations, and event nouns. BM25 can therefore identify the
matching article for most queries.

The remaining errors are likely event-disambiguation errors. A headline may
mention a common institution, country, or person that appears in several
documents. Some headlines summarize the article in a compressed way, while the
article uses broader or more detailed wording. BM25 is strongest when the
headline and article share rare terms, but weaker when the central event is
expressed indirectly.

### Dense Evaluation Profile

Dense retrieval with `harrier_oss_v1_270m` reaches nDCG@10 = 0.8996, hit@10 =
0.9200, and recall@100 = 0.9450. Dense retrieval has the highest nDCG@10, which
suggests that it ranks the positive article slightly better when the headline
is a semantic summary rather than a direct lexical extract. It can connect a
short event description with a longer article body that uses related but not
identical phrasing.

Dense retrieval has lower hit@10 and recall@100 than BM25 and hybrid retrieval.
This indicates that exact names and event terms still matter in a news corpus.
When dense similarity overgeneralizes, it may retrieve same-topic articles that
are semantically close but not the specific article behind the headline.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate column reaches nDCG@10 = 0.8954, hit@10 =
0.9600, and recall@100 = 0.9950, with 100 to 101 candidates per query and one
rank-101 safeguard row. It has the best positive coverage and the best hit@10,
while dense retrieval has a slightly higher nDCG@10. This means the hybrid pool
is extremely reliable as a candidate source for reranking.

The hybrid result fits the task structure. BM25 contributes exact names,
locations, and event vocabulary; dense retrieval contributes semantic headline-
to-body matching. A reranker starting from this pool should almost always have
the positive article available and can focus on choosing the exact event match
among same-topic candidates.

### Metric Interpretation for Model Researchers

With one positive article per query, nDCG@10 measures how highly the matching
article is ranked. Hit@10 measures short-list success, and recall@100 measures
candidate-generation coverage. The scores are high across all methods, so this
task is less about basic retrieval feasibility and more about small ranking
differences among strong systems.

BM25's strength should be taken seriously. A dense model that only matches
broad news semantics may underperform lexical retrieval on named-event tasks.
The best systems should combine exact entity matching with semantic event
matching, then use reranking for same-entity hard negatives.

### Query and Relevance Type Tendencies

Queries are concise Dutch headlines. They usually identify an event by a small
number of entities, locations, and actions. Relevant documents are the full
article or article summary corresponding to that headline.

The relevance type is article identity. A document about the same country,
political actor, or disaster is not sufficient unless it is the article
summarized by the headline. This makes same-entity negatives important.

### Representative Failure Modes

BM25 can fail when a headline compresses the event and the article uses
different wording, or when several articles share the same named entity. Dense
retrieval can fail when it retrieves a semantically similar article about the
same topic but not the exact event. Hybrid retrieval can still over-rank a
same-entity candidate if both sparse and dense signals point to the wrong
article.

Hard negatives are likely to be articles about the same person, organization,
country, or ongoing story. Rerankers should compare the main event, not just
the topic.

### Training Data That May Help

Useful training data includes non-overlapping Dutch headline-to-article pairs,
Dutch news search logs with clicked articles, public Dutch title-body article
pairs with overlap removed, and same-entity hard negatives from Dutch news
corpora. Any source likely to contain the same NOS titles, article bodies,
qrels, or sampled evaluation rows should be excluded or audited.

Synthetic data can be generated from Dutch news articles outside the evaluation
set. Generate concise headlines that identify one event, actor, and location,
then pair them with same-topic hard negatives. The headline should summarize
the article without copying long article spans.

### Model Improvement Notes

Improving this task is mainly about precision among strong candidates. Dense
models should learn event identity and not only topical similarity. Sparse
signals are important because names and locations are often decisive. Rerankers
should be trained with same-entity negatives so they learn to prefer the
article matching the headline's exact event.

The task is also useful as a calibration check: if a model performs poorly
here, it may be losing obvious Dutch lexical or named-entity information.

## Example Data

| Query | Positive document |
| --- | --- |
| Hoofdagent weg na drugsgebruik [30 chars] | Een 50-jarige hoofdagent van de regiopolitie Gelderland-Midden is ontslagen wegens "zeer ernstig plichtsverzuim". Dat heeft de politie bekendgemaakt. De politieman bleek al lange tijd harddrugs te gebruiken. Vanwege de privacy van de agent wil een woordvoerder niet zeggen hoe lang en wat voor drugs hij gebruikte. De hoofdagent werkte in het district Rivierenland. [365 chars] |
| Basisschoolleerlingen onwel tijdens kookles [43 chars] | In een buurthuis in Linden in Noord-Brabant zijn basisschoolleerlingen onwel geworden tijdens het koken, schrijft Omroep Brabant. Elf kinderen werden uit voorzorg naar het ziekenhuis gebracht. Een van de kinderen had zich tijdens de les met een mes in een vinger gesneden. Andere kinderen voelden zich benauwd worden toen ze het bloed zagen. Ook klaagden er kinderen over een vreemde lucht in het gebouw. De brandweer vermoedde in eerste instantie dat de benauwdheid werd veroorzaakt door koolmonoxide, maar dat bleek niet geval. Waardoor het wel werd veroorzaakt is niet duidelijk. Een woordvoerder van de gemeente Cuijk zegt dat 'een opeenstapeling van emoties' de kinderen mogelijk te veel is geworden. BloedDe directeur van de basisschool zegt tegen Omroep Brabant dat hij zich niet voor kan stellen dat een bloedende vinger voor dit soort massale ademhalingsproblemen zorgt. 'Ik wacht de resultaten van het onderzoek af.' Uit voorzorg zal het ventilatiesysteem van het dorpshuis worden nagekeken... [1,000 / 1,001 chars] |
| 'IS heeft vluchtelingenkamp bij Damascus in handen' [51 chars] | IS heeft het Palestijnse vluchtelingenkamp Yarmouk bij de Syrische hoofdstad Damascus in handen. De moslimterroristen bezitten nu ongeveer de helft van het kamp, zegt een hoge Palestijnse functionaris. In Yarmouk, waar ongeveer 20.000 Palestijnen verblijven, zouden de terroristen de belangrijkste doorgangswegen bezetten. Daardoor kan de hulp van de VN de vluchtelingen niet bereiken en zijn er in Yarmouk bijna geen voedsel, water en medicijnen meer. IS wordt bijgestaan door strijders van al-Nusra. Islamitische Staat en al-Nusra voeren in Syrië elk hun eigen strijd, maar in Yarmouk trekken ze samen op. De strijders van al-Nusra hebben ervoor gezorgd dat IS in het Palestijnse kamp kon infiltreren. De aanval van de terroristen op het kamp begon woensdag. IS komt nu steeds dichter bij Damascus. Het is niet duidelijk hoeveel mensen gewond zijn geraakt of zijn gedood bij de aanval. [888 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| MTEB-NL and E5-NL: Embedding Benchmark and Models for Dutch | 2025 | arXiv paper | [https://arxiv.org/abs/2509.12340](https://arxiv.org/abs/2509.12340) |
| Dutch News Articles |  | dataset card | [https://www.kaggle.com/datasets/maxscheijen/dutch-news-articles](https://www.kaggle.com/datasets/maxscheijen/dutch-news-articles) |
| clips/mteb-nl-news-articles-ret |  | dataset card | [https://huggingface.co/datasets/clips/mteb-nl-news-articles-ret](https://huggingface.co/datasets/clips/mteb-nl-news-articles-ret) |
| MTEB project repository |  | repository | [https://github.com/embeddings-benchmark/mteb](https://github.com/embeddings-benchmark/mteb) |

### Representative Snippets

| Query | Positive passage |
| --- | --- |
| Hoofdagent weg na drugsgebruik | A Dutch article says a regional police officer was dismissed for serious misconduct after long-term hard-drug use. |
| Basisschoolleerlingen onwel tijdens kookles | A Dutch article reports that primary school children became unwell during a cooking lesson and were taken to hospital as a precaution. |
| IS heeft vluchtelingenkamp bij Damascus in handen | A Dutch article reports that IS took control of part of the Yarmouk Palestinian refugee camp near Damascus. |
| Kamerzorgen over missie Oekraine | A Dutch article describes parliamentary concerns about the safety of people searching for remains and luggage in the Ukraine crash area. |
| Zeven kinderen omgekomen bij brand in Mexico | A Dutch article reports that seven children died in a residential fire in Mexico City. |
