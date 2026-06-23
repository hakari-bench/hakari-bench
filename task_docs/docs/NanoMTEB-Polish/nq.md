# NanoMTEB-Polish / nq

## Overview

`nq` is the Polish NanoMTEB version of a Natural Questions hard-negative retrieval task. Natural Questions was introduced from real anonymized Google search queries paired with Wikipedia evidence. This Polish split should be read as a localized open-domain QA retrieval task: short Polish fact-seeking questions retrieve Wikipedia-style passages that contain the answer. The observed examples ask about television judges, web-series release dates, amusement-park rides, actors, national parks, the Great Wall, Arctic research stations, films, Roman education, and U.S. presidential succession.

The Nano split contains 200 queries, 10,000 documents, and 251 positive relevance judgments. Queries average about 49 characters and documents about 617 characters. Most queries are close to single-answer retrieval: the average positives per query is 1.255, the median is 1, and the maximum is 3. This makes the task a precise passage-retrieval benchmark where a model must identify the answer-bearing passage among hard negatives.

## Details

### What the Original Data Measures

Natural Questions evaluates question answering over real search questions and Wikipedia evidence. In retrieval form, the task is to rank passages that contain the information needed to answer a natural-language question. The Polish hard-negative variant preserves that structure: the query is a short information need, and the relevant document is an encyclopedic passage that explicitly contains the answer.

This task differs from duplicate-question retrieval. A relevant passage does not need to phrase the question similarly. It needs to contain the answer entity, date, count, role, or definition. That makes semantic question-passage matching more important than title similarity.

### Observed Data Profile

The queries are short and often entity-centered. The documents are Wikipedia-like passages with names, dates, descriptions, and surrounding context. The Polish text includes translated prose, while many named entities remain recognizable. The candidate pool contains hard negatives, so documents may mention related entities or topics without answering the query.

Because most queries have only one positive, top-rank precision is especially important. A system that places the answer-bearing passage below several related passages will lose nDCG even if it has high recall at 100.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.3026, hit@10 of 0.5500, and recall@100 of 0.7649. This is a strong recall baseline because many factoid questions include distinctive entity names or surface terms. Exact matches for show titles, place names, actor names, or event names can bring answer passages into the top 100.

The weakness is top-ordering. A question may use short Polish wording while the answer passage contains expanded encyclopedic context. BM25 can also retrieve related Wikipedia passages that share entity names but do not answer the question. Term overlap is helpful, but it does not fully capture answer-bearing relevance.

### Dense Evaluation Profile

The dense `harrier-oss-270m` run is much stronger at top ranks, with nDCG@10 of 0.6154, hit@10 of 0.8400, and recall@100 of 0.9283. Dense retrieval is well suited to this task because it can match the meaning of a question to a passage that answers it, even when the wording differs. It can connect "who played Professor Proton" to a passage about Bob Newhart, or a question about the number of national parks in India to a list passage that contains the count.

This is one of the clearest dense-favorable profiles. The task requires semantic mapping from question to evidence passage, not duplicate wording. Dense retrieval captures that relation far better than BM25.

### Reranking Hybrid Evaluation Profile

`reranking_hybrid` reports nDCG@10 of 0.4363, hit@10 of 0.7000, and recall@100 of 0.9522. Candidate lists contain 100 to 101 items, and 9 rows use the positive safeguard. Hybrid retrieval has the best recall@100, but its top-10 ranking is much weaker than dense retrieval.

This means hybrid search is valuable as a candidate-generation strategy but not as the best direct ranking for this split. It includes answer passages very reliably, but the fusion with lexical candidates may introduce related entity passages above the true answer. A reranker can benefit from the hybrid pool if it can identify answer-bearing passages precisely.

### Metric Interpretation for Model Researchers

This task is strongly dense-favorable for direct retrieval. BM25 already retrieves many positives within the top 100, but dense retrieval greatly improves whether the answer passage appears in the first page. Hybrid retrieval maximizes candidate coverage, yet its lower nDCG@10 shows that high recall does not imply good final order.

Researchers should therefore treat `nq` as a diagnostic for question-to-evidence matching. A model that improves top-10 ranking over dense retrieval is likely better at recognizing answer-bearing passages. A model that improves recall@100 without top-rank gains may be useful as a first-stage candidate generator but not as a standalone retriever.

### Query and Relevance Type Tendencies

Representative queries ask who judged Dancing on Ice in 2014, when season 5 of RWBY came out, when the Alton Towers log flume closed, who played Professor Proton in The Big Bang Theory, and how many national parks are in India. These are direct information needs with expected factual answers.

Relevant passages usually contain the answer plus supporting context. They may not repeat the question wording. The model must locate the passage that states the answer, not merely a passage about the same show, park, person, or country.

### Representative Failure Modes

BM25 may retrieve passages that share a title or entity but answer a different question. Dense retrieval may retrieve semantically close passages about the same entity that lack the requested fact. Hybrid retrieval can include both, increasing recall but also adding distractors near the top.

Hard negatives are especially challenging when they mention the correct entity but omit the requested date, count, or role. A good retriever must understand which attribute the question asks for.

### Training Data That May Help

Useful training data includes Natural Questions training data outside the evaluation records, Polish Wikipedia QA retrieval pairs, multilingual QA datasets, and hard negatives from related but non-answering passages. Data should emphasize answer-bearing evidence rather than duplicate wording.

Hard negatives should include passages about the same entity that do not contain the answer, passages that contain a different date or count, and passages about adjacent entities in the same list or franchise.

### Model Improvement Notes

Dense models can improve by better representing question focus, answer type, and evidence-bearing passages in Polish. Sparse systems can improve through entity matching and token normalization, but they will still struggle when answer evidence is phrased differently. Hybrid systems are useful for recall, especially if paired with a reranker trained to identify answer support.

For evaluation, nDCG@10 is the primary signal for direct QA retrieval quality, while recall@100 measures whether the answer passage is available for downstream reranking or reader models. This split clearly separates those roles.

## Example Data

| Query | Positive document |
| --- | --- |
| którzy byli sędziami tańca na lodzie 2014 [41 chars] | Taniec na lodzie Phillip Schofield i Christine Bleakley powrócili do współobecności. Dean, Torvill i Karen Barber powrócili, by mentorować celebrytów. Robin Cousins, Jason Gardiner, Barber i Ashley Roberts powrócili z odpowiednio dziewiątą, ósmą, siódmą i drugą serią na The Ice Panel. Kuzyni byli nieobecni przez 6 i 7 tygodni z powodu komentowania Zimowych Igrzysk Olimpijskich 2014, więc były sędzia Nicky Slater powrócił na jego miejsce, a Barber był tymczasowym sędzią głównym. [483 chars] |
| kiedy wyjdzie sezon 5 rubinu? [29 chars] | Lista odcinków RWBY RWBY to trwająca amerykańska seria internetowa w stylu anime, stworzona przez Rooster Teeth Productions. Premiera odbyła się 18 lipca 2013 r. Na stronie internetowej Rooster Teeth, a odcinki zostały później przesłane na YouTube i strony strumieniowe, takie jak Crunchyroll. Wydano cztery sezony, określane jako „Tomy”, z których piąty trwa od premiery 14 października 2017 r.[1] Do października 2017 r. wydano 54 odcinki, które są określane jako „Rozdziały”. [479 chars] |
| kiedy w alton towers zamknięto koryto z bali? [45 chars] | Korytarz (wieże Alton) The Flume był log Flume w Alton Towers w Staffordshire. Został otwarty w 1981 roku i został odnowiony w 2004 roku, co zbiegło się z jego sponsorowaniem przez Imperial Leather. Przejażdżka była rynną z bali o tematyce kąpielowej z trzema kroplami. W momencie otwarcia była to najdłuższa atrakcja z bali na świecie. Atrakcja została zamknięta w 2015 roku i została usunięta rok później w celu przekształcenia obszaru w kolejkę górską SW8. [460 chars] |

### Source Reference Table

| Source | What it contributes |
| --- | --- |
| Natural Questions paper | Original task definition using real search queries and Wikipedia evidence. |
| Natural Questions project page | Official dataset context. |
| MTEB task card | Polish hard-negative retrieval packaging. |

### Representative Snippets

- A query asks who the judges were on Dancing on Ice 2014; relevant passages list returning judges and mentors.
- A query asks when RWBY season 5 came out; relevant documents provide series and episode-release context.
- A query asks when the Alton Towers log flume closed; relevant passages describe the ride and its operating history.
- A query asks who played Professor Proton in The Big Bang Theory; relevant documents identify Bob Newhart.
- A query asks how many national parks are in India; relevant passages give the count and protected-area context.
