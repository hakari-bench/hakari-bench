# NanoMTEB-Scandinavian / tv2_nordretrieval

## Overview

`tv2_nordretrieval` is the Danish NanoMTEB-Scandinavian retrieval adaptation of TV2 Nord / Nordjylland News summarization data. The source material consists of Danish local-news articles with summaries. The Scandinavian benchmark converts the summarization format into retrieval by using a concise summary as the query and the matching full article as the relevant document. This makes the task summary-to-article retrieval, not general news categorization.

The Nano split contains 200 queries, 2,048 documents, and exactly 200 positive relevance judgments. Each query has one positive article. Queries average about 128 characters, while documents average about 1,441 characters. The observed items cover local politics, court decisions, port agreements, recycling investment, music reviews, elections, accidents, sports clubs, culture, and nature. A model must connect a compact summary to a longer article with quotes, background, and event chronology.

## Details

### What the Original Data Measures

Nordjylland News was created for Danish summarization using TV2 Nord news articles and summaries. The retrieval adaptation uses the summary as a query and the matching article as the target. The source is therefore a local-news summarization resource repurposed as retrieval.

This conversion produces a useful news-search setting. The summary usually states the key facts, while the article expands them with names, places, quotes, and context. The positive document is the exact article summarized by the query, not any article about the same municipality, organization, or event type.

### Observed Data Profile

Queries are longer than typical headlines and read like short article summaries. They often include named organizations, municipalities, direct facts, or a concise event outcome. Documents are full local-news articles with richer narrative structure. Each query has a single positive, so exact article retrieval is required.

The examples include a Supreme Court decision about the name `Lokalbanken`, a dispute between Royal Arctic Line and Aalborg Harbor, AVV investment in recycling, reception of Laura Mo's album `Motel`, and live election coverage. These summaries preserve many article facts, making lexical retrieval strong.

### BM25 Evaluation Profile

BM25 is very strong, with nDCG@10 of 0.8957, hit@10 of 0.9350, and recall@100 of 0.9850. Summary queries often reuse central names, locations, organizations, and event terms from the article. This gives term-frequency retrieval a high baseline.

The remaining difficulty comes from local-news similarity. Many articles may share the same municipality, sports team, political actor, or institution. BM25 can confuse stories that share names or event categories, especially when the summary is broad or the article contains repeated background terms.

### Dense Evaluation Profile

The dense `harrier-oss-270m` run is strongest at top ranks, with nDCG@10 of 0.9127, hit@10 of 0.9500, and recall@100 of 0.9750. Dense retrieval slightly improves final ranking by connecting the summary's meaning to the article's expanded narrative. It can help when the article uses different phrasing from the summary or when the relevant relation is event-level rather than keyword-level.

The dense advantage is modest because BM25 is already near ceiling. Still, it shows that semantic event matching adds value beyond named-entity overlap.

### Reranking Hybrid Evaluation Profile

`reranking_hybrid` reports nDCG@10 of 0.8998, hit@10 of 0.9450, and recall@100 of 1.0000. Candidate lists contain exactly 100 items, with no safeguard rows. Hybrid retrieval has perfect recall@100 but top-10 quality between BM25 and dense retrieval.

This makes hybrid useful as a first-stage candidate generator. It preserves every positive article, but dense retrieval is slightly better for direct top-ranked output. A reranker can use the hybrid pool to combine lexical entity signals with semantic event matching.

### Metric Interpretation for Model Researchers

This split is dense-favorable for direct ranking, BM25-strong overall, and hybrid-favorable for candidate recall. Because all three methods perform well, the task has a partial ceiling effect. It is most useful for evaluating fine-grained ranking among local-news articles that share places and entities.

Since every query has one positive, nDCG@10 and hit@10 measure exact summary-to-article retrieval. Recall@100 indicates whether the article survives first-stage retrieval for reranking. Hybrid's perfect recall is useful, while dense's better nDCG indicates stronger ordering.

### Query and Relevance Type Tendencies

Representative queries summarize local disputes, legal outcomes, environmental investments, album reviews, and election coverage. They often contain names such as Royal Arctic Line, Aalborg Havn, AVV, Hjørring, Laura Mo, or Spar Nord Bank. Relevant articles contain fuller context and quotations.

The model must distinguish the exact event. A summary about one local bank dispute should not retrieve a different article about the same bank or court. A summary about one municipal election should not retrieve general election coverage unless it is the matching article.

### Representative Failure Modes

BM25 may retrieve articles sharing a municipality, organization, or sports team but describing a different event. Dense retrieval may retrieve semantically similar local-news stories with the same event type, such as another court decision or political dispute. Hybrid retrieval can preserve the right article but still rank a close same-location distractor above it.

Another failure mode is over-weighting quoted or background names. Local-news articles often mention multiple people and institutions. The summary's central event should drive retrieval, not incidental mentions.

### Training Data That May Help

Useful training data includes non-overlapping Danish news summary/article pairs, Danish headline-to-article retrieval pairs, local-news same-location hard negatives, and Danish summarization retrieval data. Training should exclude Nano summary queries, qrels, and matching TV2 Nord article texts.

Hard negatives should share municipality, organization, team, or topic but describe a different event. These are much more informative than random Danish news negatives.

### Model Improvement Notes

Dense models can improve by representing event-level equivalence between summaries and full articles. Sparse systems can improve through named-entity and location handling, but they need safeguards against same-entity distractors. Hybrid systems are strong for recall and should be paired with rerankers that compare event details.

For evaluation, this split rewards exact local-news item retrieval. The strongest systems should retrieve the matching article even when multiple articles share the same regional context.

## Example Data

| Query | Positive document |
| --- | --- |
| Højesteret har tirsdag afgjort, at Lokalbanken i Nordsjælland ikke har patent på navnet "Lokalbanken... [100 / 184 chars] | Danmarks højeste retsinstans, Højesteret i København, besluttede tirsdag, at andre end Lokalbanken i Nordsjælland godt må bruge navnet. Derfor er direktøren for Spar Nord Bank også ganske glad. - Vi f... [200 / 1,259 chars] |
| Royal Arctic Line A/S og Aalborg Havn A/S er uenige på en række punkter, oplyser Aalborg Havn A/S. N... [100 / 137 chars] | Forhandlingerne har siden oktober bølget frem og tilbage mellem Aalborg Havn A/S og Royal Arctic Line A/S. Målet var at forlænge den nuværende aftale omkring Grønlandstrafikken helt frem til 2025 - og... [200 / 1,351 chars] |
| Det nordjyske affaldsselskab AVV’s bestyrelse har besluttet, at en del af virksomhedens egenkapital... [100 / 183 chars] | Det er en ordning, der gør, at det nordjyske affaldsselskab AVV med hovedsæde i Hjørring kan genanvende mere og bidrage positivt til verdensmål og klimamålsætninger. Finansieringen sker ved at begræ... [200 / 1,205 chars] |
| Den unge sangerinde Laura Mo får pæne ord med på vejen for sit nye album "Motel". [81 chars] | Stjernerne drysser ned over hende og ligeledes de pæne ord. Laura Mo udgav den 12. marts sit andet album "Motel" og det er blevet taget pænt imod af anmelderne. Hun har blandt andet fået fem stjerner... [200 / 707 chars] |
| Sidste stemme er afgivet, og nu skal det nye byråd findes. Følg valget på tætteste hold lige her. [97 chars] | Kan Mogens Jespersen genvinde titlen som borgmester eller vil Leif Skaarup og de røde partier vinde så mange mandater, at de kan vippe ham af tronen? Han er ny mand på posten, og i 2013 oplevede S lig... [200 / 744 chars] |

### Source Reference Table

| Source | What it contributes |
| --- | --- |
| Scandinavian Embedding Benchmarks | Retrieval conversion for summarization datasets. |
| Nordjylland News datasheet | Official Danish Foundation Models source description. |
| Danoliterate thesis | Danish summarization scenario context. |
| Hugging Face dataset card | Source article-summary dataset access. |

### Representative Snippets

- A summary says the Supreme Court ruled that `Lokalbanken` is not exclusively owned as a name; the article describes the dispute and Spar Nord's reaction.
- A summary says Royal Arctic Line and Aalborg Harbor disagree on several points; the article describes negotiations and the contract period.
- A summary says AVV will invest equity in recycling improvements; the article explains recycling of plastic-metal and paper-cardboard fractions.
- A summary says singer Laura Mo received positive words for `Motel`; the article describes reviews of the album.
- A summary says the last vote has been cast and the new city council must be found; the article follows local election results and candidates.
