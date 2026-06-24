# NanoBRIGHT / NanoBrightPsychologyLong

## Overview

NanoBrightPsychologyLong is the long-document Psychology StackExchange slice of NanoBRIGHT. Queries are detailed user posts about cognition, behavior, emotion, perception, or research terminology, while candidate documents are full cited pages or long source documents. The task measures whether a retriever can identify the source page that contains the psychological construct or evidence needed to answer the query, even when that evidence is only one section of a long article.

## Details

### What the Original Data Measures

BRIGHT's long-document StackExchange variants use complete source pages rather than short passages. For Psychology, that means a relevant document may be a long encyclopedia entry, popular psychology article, research-oriented page, or publisher page whose useful evidence is embedded among navigation text, examples, references, and adjacent concepts.

The task retains the core Psychology difficulty: users often describe an experience in everyday language, while the relevant source uses formal terms. The long-document version adds another layer because the correct source must be scored as relevant even if most of the page is not directly about the query.

### Observed Data Profile

The task contains 101 queries, 509 documents, and 116 relevance judgments. It is mostly single-positive: there are 1.15 positives per query on average, a minimum of 1, a median of 1.0, a maximum of 5, and 11 multi-positive queries, or 10.89% of the set.

Queries average 693.16 characters, matching the passage-level Psychology slice. Documents average 40,097.47 characters, so each candidate may contain multiple sections and substantial surrounding material. The small document count should not be mistaken for an easy task; document length creates heavy topical dilution.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.3010, hit@10 of 0.4554, and recall@100 of 0.7845 using the top-500 BM25 candidate subset. Lexical retrieval has good recall because long pages contain many terms, including formal construct names and related psychological vocabulary.

The top-rank quality remains limited. A long page can include many broadly relevant words without making the specific construct central. BM25 can find source pages that mention the right terms, but it often struggles to rank the exact supporting page high enough when the query uses lay phrasing or when the page contains broad psychology coverage.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.5069, hit@10 of 0.7426, and recall@100 of 0.8879. Dense retrieval is the strongest top-ranking profile in this task. It substantially improves over BM25 for nDCG@10 and hit@10.

This suggests that semantic matching is especially valuable for long psychology sources. The model can connect a user's scenario to a source page whose central topic or explanatory content aligns with the intended construct, even when exact wording differs. Dense retrieval is better at selecting the right page near the top.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.4149, hit@10 of 0.6337, and recall@100 of 0.9310. It uses a top-100 candidate range with an optional rank-101 safeguard; this task has 6 safeguard rows, candidate counts from 100 to 101, and a mean of 100.06 candidates.

The hybrid profile has the best recall@100 but does not beat dense retrieval at the top of the ranking. This means the combined sparse and dense pool is valuable for downstream reranking, while dense retrieval alone gives the strongest first-page ordering. The pattern separates candidate coverage from ranking quality.

### Metric Interpretation for Model Researchers

This task is a dense-favorable long-document benchmark with a hybrid recall advantage. BM25 retrieves many positives somewhere in the top 100 because long source pages contain useful terms. Dense retrieval ranks positives much better in the top 10. Reranking_hybrid gives the broadest positive coverage for reranker input.

Researchers should evaluate whether their models represent the specific psychological construct rather than only the page's broad topic. Long documents can obscure the small evidence-bearing span, so models that combine semantic document retrieval with section-level reranking may be especially effective.

### Query and Relevance Type Tendencies

Queries ask about phenomena such as normalization of extreme claims, flow, mental blocks, attention-seeking behavior, empathy gaps, perception, cognition, and social behavior. Relevant long documents may be encyclopedia pages, psychology articles, popular explanatory pages, or research-oriented resources.

The relevance relation is usually source-level support. A positive document contains the construct, example, or explanation needed for the answer, though the specific evidence may occupy only a small part of the page.

### Representative Failure Modes

Likely failures include ranking a long psychology page because it mentions related terms without supporting the specific phenomenon, missing the formal construct when the query is phrased as a personal scenario, over-weighting navigation or boilerplate, and confusing adjacent constructs such as flow, motivation, attention, and emotional state.

BM25 is exposed to long-page term dilution. Dense retrieval can still retrieve broadly similar but insufficient pages. Hybrid retrieval improves coverage but needs a reranker to recover dense-like top-rank precision.

### Training Data That May Help

Useful training data includes document-level psychology reference retrieval, cited-source retrieval from psychology forums, long-article QA with evidence grounding, and section-to-document supervision that maps answer-bearing spans back to full source pages.

Synthetic data should generate long psychology source pages with sections, definitions, examples, and research context, then write user-style questions about behavior, cognition, or measurement. Hard negatives should be long pages about adjacent constructs that are plausible but not the right explanation.

### Model Improvement Notes

Strong models should combine lay-language understanding with formal psychology terminology. Dense retrieval is the best observed first-stage ranker, so model training should emphasize scenario-to-construct mapping. Reranking_hybrid is useful when recall@100 matters, but the final ranking should inspect whether the relevant section actually supports the query.

Long-document systems may benefit from section-aware pooling, passage aggregation, or reranking over extracted evidence spans. The task is especially useful for testing whether full-page retrieval hides or preserves the evidence signal.

## Example Data

| Query | Positive document |
| --- | --- |
| Asking for illogical things to make extreme views normal? A couple of months back I was reading an article about how politicians were asking to make decisions that are way beyond possible (name it unreasonable, unacceptable, illogical) just as a medium of getting extreme views to become (to be seen as) normal and/or acceptable. What is the name of this effect? [363 chars] | Skip to main content clock menu more-arrow no yes mobile [ Vox homepage ](/) * ## Give [ Give ](http://vox.com/pages/support- now?itm_campaign=contribute&itm_medium=site&itm_source=navigation) * ## Newsletters [ Newsletters ](http://vox.com/pages/newsletters/?itm_campaign=contribute&itm_medium=site&itm_source=navigation) ## Site search Search Search ## Vox main menu * [ Explainers ](/explainers) * [ Crossword ](https://www.vox.com/21523212/crossword-puzzles-free-daily-printable) * [ Video ](/videos) * [ Podcasts ](/pages/podcasts) * [ Politics ](/politics) * [ Policy ](/policy) * [ Culture ](/culture) * [ Science ](/science) * [ Technology ](/technology) * [ Climate ](/climate) * [ Health ](/health) * [ Money ](/money) * [ Life ](/life) * [ Future Perfect ](/future-perfect) * [ Newsletters ](/newsletters) * More * [ Explainers ](/explainers) * [ Israel-Hamas war ](/2023/10/7/23907683/israel-hamas-war-news-updates-october-2023) * [ 2024 election ](/2024-elections) * [ Tax season ](/even... [1,000 / 14,364 chars] |
| What term can describe the feeling that a job just does itself? Is there a term that can describe that a job, however exhausting it might be, just does itself? Meaning, for example, that all doubt concerning how you're doing a job, whether or not you should do the job instead of something else, or any doubt of the value you're creating is just not there? As an example, I saw an interview where an author was asked how much effort it took to write a particular book. The answer was "No effort at al... [500 / 943 chars] | Jump to content Main menu Main menu move to sidebar hide Navigation * [ Main page ](/wiki/Main_Page "Visit the main page \[z\]") * [ Contents ](/wiki/Wikipedia:Contents "Guides to browsing Wikipedia") * [ Current events ](/wiki/Portal:Current_events "Articles related to current events") * [ Random article ](/wiki/Special:Random "Visit a randomly selected article \[x\]") * [ About Wikipedia ](/wiki/Wikipedia:About "Learn about Wikipedia and how it works") * [ Contact us ](//en.wikipedia.org/wiki/Wikipedia:Contact_us "How to contact Wikipedia") * [ Donate ](https://donate.wikimedia.org/wiki/Special:FundraiserRedirector?utm_source=donate&utm_medium=sidebar&utm_campaign=C13_en.wikipedia.org&uselang=en "Support us by donating to the Wikimedia Foundation") Contribute * [ Help ](/wiki/Help:Contents "Guidance on how to use and edit Wikipedia") * [ Learn to edit ](/wiki/Help:Introduction "Learn how to edit Wikipedia") * [ Community portal ](/wiki/Wikipedia:Community_portal "The hub for editors"... [1,000 / 132,869 chars] |
| What is the term for the "knowing what you think but can't explain it" phenomenon? I think we all experience this phenomenon once in a while, and I am experiencing it right now. It's the feeling that whatever word one tries to say it seems to be wrong (for them) or confusing (for the listeners), and would require a period of time to think out the right word that they have already known. If severed, it can lead to frustration, but it's not really about feeling insecurity. What is the word for tha... [500 / 504 chars] | Jump to content Main menu Main menu move to sidebar hide Navigation * [ Main page ](/wiki/Main_Page "Visit the main page \[z\]") * [ Contents ](/wiki/Wikipedia:Contents "Guides to browsing Wikipedia") * [ Current events ](/wiki/Portal:Current_events "Articles related to current events") * [ Random article ](/wiki/Special:Random "Visit a randomly selected article \[x\]") * [ About Wikipedia ](/wiki/Wikipedia:About "Learn about Wikipedia and how it works") * [ Contact us ](//en.wikipedia.org/wiki/Wikipedia:Contact_us "How to contact Wikipedia") * [ Donate ](https://donate.wikimedia.org/wiki/Special:FundraiserRedirector?utm_source=donate&utm_medium=sidebar&utm_campaign=C13_en.wikipedia.org&uselang=en "Support us by donating to the Wikimedia Foundation") Contribute * [ Help ](/wiki/Help:Contents "Guidance on how to use and edit Wikipedia") * [ Learn to edit ](/wiki/Help:Introduction "Learn how to edit Wikipedia") * [ Community portal ](/wiki/Wikipedia:Community_portal "The hub for editors"... [1,000 / 23,048 chars] |

### Source Reference Table

| Item | Reference |
| --- | --- |
| Original benchmark paper | [BRIGHT](https://arxiv.org/abs/2407.12883) |
| Project page | [BRIGHT project page](https://brightbenchmark.github.io/) |
| Source dataset | [xlangai/BRIGHT](https://huggingface.co/datasets/xlangai/BRIGHT) |
| NanoBRIGHT dataset | [hakari-bench/NanoBRIGHT](https://huggingface.co/datasets/hakari-bench/NanoBRIGHT) |

Representative query and positive source snippets:

| Query | Positive document snippet |
| --- | --- |
| What is it called when extreme claims make extreme views seem normal? | A long article discusses how repeated extreme statements can alter perceived normality. |
| What term describes work that seems to do itself despite effort? | A long reference page contains a section on flow and challenges to maintaining it. |
| What is the term for knowing what you mean but being unable to explain it? | A long mental-block page discusses difficulty expressing or accessing thought. |
| Why would someone say shocking things to enjoy others' reactions? | A psychology article discusses excessive attention-seeking behavior. |
| What term describes being unable to see beyond one's current emotional state? | A long reference page explains the hot-cold empathy gap. |
