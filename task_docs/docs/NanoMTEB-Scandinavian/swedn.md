# NanoMTEB-Scandinavian / swedn

## Overview

`swedn` is the Swedish NanoMTEB-Scandinavian retrieval adaptation of SWE-DN, a Dagens Nyheter summarization corpus. The source resource contains Swedish news articles with headlines, summaries, article text, and categories. The Scandinavian benchmark converts this into retrieval by using a headline as the query and marking both the compact summary and the full article as positives. The task therefore evaluates headline-to-news retrieval with a two-positive structure.

The Nano split contains 200 queries, 2,046 documents, and 400 positive relevance judgments. Every query has exactly two positives. Queries average about 45 characters, while documents average about 2,896 characters. The documents range from short preambles to long news and opinion articles. Queries are often editorial, quoted, or headline-like, so the model must connect compressed journalistic phrasing to both the article summary and the full article.

## Details

### What the Original Data Measures

SWE-DN was created as a Swedish summarization resource based on Dagens Nyheter articles. In the retrieval adaptation, summarization pairs are repurposed: the headline becomes the query, while the lead summary and the article body become retrievable positives. This means the task is not topical news classification. It asks whether a retriever can identify the two textual forms of the same news item.

The two-positive design is important. A good system should retrieve both the short summary and the longer article. The summary may share concise wording with the headline, while the full article may contain more background, quotes, and context.

### Observed Data Profile

The queries are Swedish headlines, sometimes written as quotes or opinion statements. Documents are much longer and include preambles, full article text, political commentary, public debate, and named entities. Because every query has exactly two positives, the task measures whether the model can connect a headline to both summary-level and article-level representations.

The examples include pedestrian traffic safety, berry picking, school law and EU migrants, changing political truths, and children's nutrition. The headlines can be compact and rhetorical, while articles expand the argument or event.

### BM25 Evaluation Profile

BM25 is strong, with nDCG@10 of 0.7081, hit@10 of 0.8950, and recall@100 of 0.8375. Headlines often reuse names, phrases, or issue terms from the corresponding article or summary. This gives lexical retrieval a useful base, especially for quoted phrases and distinctive topic words.

The limitation is headline abstraction. Some headlines are editorial or compressed and do not repeat the article's main vocabulary directly. A headline may express a stance or quote, while the full article contains background and argumentation. BM25 can find many positives but misses some cases where the lexical bridge is weak.

### Dense Evaluation Profile

The dense `harrier-oss-270m` run is strongest at top ranks, with nDCG@10 of 0.7757, hit@10 of 0.9100, and recall@100 of 0.9025. Dense retrieval improves because it can connect the meaning of a headline to the broader article content. It is especially helpful for opinion-style or abstractive headlines.

The dense gain is meaningful even though BM25 is already strong. It indicates that headline-to-article retrieval is not purely a title matching task. Semantic alignment between the headline's compressed claim and the article's expanded discussion matters.

### Reranking Hybrid Evaluation Profile

`reranking_hybrid` reports nDCG@10 of 0.7398, hit@10 of 0.8800, and recall@100 of 0.9400. Candidate lists contain 100 to 101 items, and 2 rows use the positive safeguard. Hybrid retrieval has the best recall@100 but lower top-10 quality than dense retrieval.

This suggests that lexical and dense candidates are complementary for preserving both positives, especially when one positive is a summary and the other is a full article. However, the fused ranking can place same-topic news distractors above the exact match. Dense retrieval remains the best direct ranking profile.

### Metric Interpretation for Model Researchers

This split is dense-favorable for top-ranked retrieval and hybrid-favorable for candidate recall. BM25 is already strong because headlines and articles often share content words, but dense retrieval improves semantic alignment. Hybrid retrieval is useful when the goal is to keep both summary and article positives available for reranking.

The two-positive structure should guide interpretation. Recall@100 measures how often the system preserves the summary and the full article. nDCG@10 measures whether those positives appear high enough for direct use. A model that retrieves only one of the two positives may look adequate by hit@10 but still miss part of the task design.

### Query and Relevance Type Tendencies

Representative queries include `Gående är oskyddade i trafiken`, `Det är inte gratis att plocka bär`, quoted statements about school law, political truths, and feeding children blood-based food instead of vegetarian meals. These are headline-style queries that may contain a stance, quote, or compressed claim.

Relevant documents include both concise summaries and long article bodies. The model must retrieve the exact news item, not just a related article about the same issue. Same-section and same-date negatives can be close distractors.

### Representative Failure Modes

BM25 may retrieve articles that share a named entity or political topic but are not the same story. Dense retrieval may retrieve semantically similar opinion pieces or debate articles that express a related stance. Hybrid retrieval can preserve more positives but still suffer from same-topic news distractors.

Another failure mode is retrieving only one positive type. A model may find the summary but not the article, or the article but not the summary. Because both are valid positives, a robust retriever should handle both short and long document forms.

### Training Data That May Help

Useful training data includes non-overlapping SWE-DN headline-summary-article pairs, Swedish news title-to-article retrieval pairs, same-section and same-date hard negatives, and multi-positive news retrieval examples. Training should exclude Nano headlines, qrels, and matching SWE-DN summary or article documents.

Hard negatives should share named entities, section, date, or event type but describe a different story. They help the model distinguish exact news-item retrieval from broad topic matching.

### Model Improvement Notes

Dense models can improve by representing headline semantics, article summaries, and long Swedish news text jointly. Sparse systems can improve through headline field weighting and named-entity handling, but they will struggle with abstract or opinion-style headlines. Hybrid systems are valuable for recall, especially when the downstream stage can rerank both summary and full-article candidates.

For evaluation, researchers should consider both the single-hit behavior and the two-positive coverage. This task rewards retrieving the matched news item in multiple textual forms.

## Example Data

| Query | Positive document |
| --- | --- |
| Gående är oskyddade i trafiken [30 chars] | Tror många cyklister glömmer att oavsett var en gående person befinner sig i trafiken så räknas de fortfarande som oskyddade gentemot all annan fordonstrafik och enligt lagen räknas cykel som ett ford... [200 / 419 chars] |
| Det är inte gratis att plocka bär [33 chars] | Skogens bär ingår i ett ekologiskt system och är knappast till för enbart människan. Det är inte gratis att plocka bär. Det kostar både tid och pengar. Det kräver utrustning och transporter. Väl på pl... [200 / 351 chars] |
| ”Skollagen ger barnen rätt till skolgång” [41 chars] | På DN-debatt (24/6) skriver regeringens nationelle samordnare för arbetet med utsatta EES-medborgare Martin Valfridsson tillsammans med Rickard Klerfors, om EU-migranters barns rätt till skolgång. De... [200 / 4,289 chars] |
| ”Etablerade sanningar i politiken gäller inte längre” [53 chars] | Årets riksdagsval tydliggjorde att historiskt etablerade sanningar om väljarkåren inte längre gäller. Profetior från erfarna statsvetare om hur stora försprång som är möjliga att hämta in kom på skam,... [200 / 7,338 chars] |
| ”Ge barnen blodmat i stället för vegetariskt” [45 chars] | Det är inte bara en fråga om klimatet när man som förskolan Gitarren i Umeå väljer bort kött och köttprodukter till barn. Ingen talar om viktiga mineraler som barnen går miste om. Det är väl känt att... [200 / 1,382 chars] |

### Source Reference Table

| Source | What it contributes |
| --- | --- |
| Scandinavian Embedding Benchmarks | Retrieval conversion for Scandinavian tasks. |
| SWE-DN resource page | Official source resource description. |
| SuperLim paper | Summarization-task context for SWE-DN. |
| MTEB task card | Retrieval packaging of the SWE-DN task. |

### Representative Snippets

- A headline says pedestrians are unprotected in traffic; relevant documents discuss cyclists and pedestrians as vulnerable road users.
- A headline says picking berries is not free; relevant documents discuss time, equipment, transport, and ecological considerations.
- A quoted headline says school law gives children the right to schooling; relevant documents discuss EU migrant children's schooling rights.
- A quoted headline says established political truths no longer apply; relevant documents discuss election results and voter assumptions.
- A quoted headline recommends blood-based food instead of vegetarian meals for children; relevant documents discuss nutrition and iron.
