# MNanoBEIR / NanoBEIR-sv / NanoNQ

## Overview

NanoNQ in the Swedish NanoBEIR slice is an answer-oriented Wikipedia retrieval task derived from Natural Questions. The queries are Swedish translated search questions, and the corpus contains Swedish translated answer passages. The task asks a model to retrieve the passage that contains or supports the answer. It is a compact benchmark for open-domain question answering retrieval, where short questions must be matched to answer-bearing passages rather than merely topically related Wikipedia text.

## Details

### What the Original Data Measures

Natural Questions was built from real search queries with Wikipedia evidence. In retrieval form, the key challenge is connecting a natural question to a passage that answers it. The relevant passage may include the answer directly, but it may also include surrounding context that establishes the fact, entity, location, or explanation requested by the query.

The Swedish translated version tests whether a model can handle short Swedish questions, translated entity descriptions, and titles or names that may remain partly in English. Many questions contain distinctive entities, dates, or quoted titles, but the answer relation still matters. A retriever should not stop at passages that merely share a name; it must find the passage that answers the question.

### Observed Data Profile

The task contains 50 queries, 5,035 documents, and 57 relevance judgments. Most queries have one positive passage, with an average of 1.14 positives per query. The minimum is 1, the median is 1.0, the maximum is 2, and 7 queries have multiple positives, or 14.0% of the query set. The task is therefore mostly single-answer retrieval.

Queries average 46.04 characters, while documents average 526.09 characters. The query is usually a concise natural-language question, and the document is a longer passage. This structure favors models that can map question intent to passage-level evidence rather than only matching isolated words.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.3026, hit@10 of 0.4400, and recall@100 of 0.6667 using the top-500 BM25 candidate subset. This indicates that lexical matching finds a useful fraction of answer passages by rank 100, but often fails to place them in the top 10. Many Swedish questions need semantic answer matching beyond exact term overlap.

BM25 is strongest when the query contains a distinctive title, person, place, or quoted phrase that appears in the answer passage. It is weaker when the passage expresses the answer relation indirectly or when translated wording differs from the question. The recall-to-nDCG gap suggests that BM25 is more useful as a candidate generator than as a final ranker here.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.5147, hit@10 of 0.6800, and recall@100 of 0.9123. Dense retrieval is clearly stronger than BM25, especially for top-10 quality and candidate coverage. This shows that embedding similarity captures question-answer semantics, paraphrase, and passage context that exact word matching misses.

This is the expected behavior for many Natural Questions style tasks. A dense model can connect "why" or "where" questions to explanatory passages even if the surface wording is not identical. Remaining errors likely involve ambiguous entities, similar passages about the same subject, or cases where the answer depends on a small factual detail rather than broad semantic similarity.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.3660, hit@10 of 0.5200, and recall@100 of 0.9298. It uses a top-100 candidate range with an optional rank-101 safeguard; the observed candidate count ranges from 100 to 101, with 2 safeguard rows and a mean of 100.04 candidates. The hybrid profile has the best recall@100, while dense retrieval has the strongest top-10 ranking.

This means hybrid search broadens the candidate pool by combining lexical and dense evidence, but its first-stage ordering is not as good as dense retrieval alone. For NanoNQ-sv, reranking_hybrid is valuable when a later reranker can use the high-recall pool. For direct top results, dense retrieval is the more aligned signal.

### Metric Interpretation for Model Researchers

nDCG@10 is the most practical top-rank metric because downstream QA and RAG systems usually consume only a few passages. hit@10 tells whether at least one answer-bearing passage is visible, while recall@100 tells whether a reranker has access to the answer. The task shows a clear difference between candidate recall and ranking quality.

BM25 has moderate recall but weak top-10 ranking. Dense retrieval provides both strong top-rank quality and high recall. reranking_hybrid slightly improves recall over dense but loses substantial nDCG@10. Researchers can use this task to evaluate whether a model is improving semantic answer matching or merely expanding candidate coverage.

### Query and Relevance Type Tendencies

Queries ask factual questions such as where Final Four is held, whether a film was originally a Disney film, why the Angel of the North exists, where the three-fifths compromise appears in the Constitution, and who sings with Michael Jackson on a song. Relevant passages are answer-bearing Wikipedia-style texts.

The task rewards precise entity grounding and question-type understanding. "Where" questions need locations, "why" questions need explanations, and "who" questions need people. A passage can be topically related but still fail if it does not answer the requested relation.

### Representative Failure Modes

Likely failures include retrieving a passage about the same entity but not the requested fact, confusing works or people with similar names, missing the answer when translated wording differs, and over-ranking broad background passages. BM25 may overvalue repeated names or titles, while dense retrieval may retrieve semantically related passages that do not contain the exact answer.

### Training Data That May Help

Useful training data includes Swedish open-domain QA, multilingual question-passage retrieval, Wikipedia evidence retrieval, and hard negatives that share entities but do not answer the question. Translated QA data can help if evaluation overlap is avoided. For rerankers, same-entity non-answer passages are particularly useful hard negatives.

### Model Improvement Notes

A model targeting this task should improve answer-bearing passage discrimination. Dense retrieval is the strongest direct baseline and should be refined with question-answer hard negatives. Sparse systems need query expansion and normalization for Swedish questions and translated entity text. Hybrid systems should exploit their high recall with a reranker that can identify the actual answer relation.

## Example Data

| Query | Positive document |
| --- | --- |
| Var hålls Final Four detta år? [30 chars] | NCAA Division I:s herrarnas basketturnering 2018 var en turnering med utslagning för 68 lag för att kora herrarnas nationella mästare i collegebasket för NCAA Division I för säsongen 2017–18. Den 80:e... [200 / 323 chars] |
| Var Nattens Häxer ursprungligen en Disney-film? [47 chars] | Nightmare Before Christmas uppstod från ett dikt skrivet av Tim Burton 1982, medan han arbetade som animatör på Walt Disney Feature Animation. Efter framgången med Vincent samma år började Walt Disney... [200 / 612 chars] |
| Varför finns Ängeln i norr? [27 chars] | Enligt Gormley hade en ängel tre betydelser: först, att symbolisera att kolgruvarbetare arbetade under platsen för dess uppförande i två århundraden; andra, att förstå övergången från en industriell t... [200 / 303 chars] |
| Var i grundlagen nämndes tre-femtedelskompromissen ursprungligen? [65 chars] | Tre-femtedelskompromissen finns i Artikel 1, Avsnitt 2, Paragraf 3 i USA:s konstitution, som lyder: [99 chars] |
| Vem sjunger "Someone's Watching Me" tillsammans med Michael Jackson? [68 chars] | "Somebody's Watching Me" är en låt av den amerikanska sångaren Rockwell från hans debutalbum Somebody's Watching Me (1984). Den släpptes som Rockwells debutsingel och förstasingel från albumet den 14... [200 / 348 chars] |

### Source Reference Table

| Item | Reference |
| --- | --- |
| Original dataset | [Natural Questions](https://aclanthology.org/Q19-1026/) |
| Retrieval benchmark framing | [BEIR](https://arxiv.org/abs/2104.08663) |
| Multilingual benchmark context | [MMTEB](https://arxiv.org/abs/2502.13595) |
| NanoBEIR collection | [NanoBEIR on Hugging Face](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
| NanoBEIR-sv dataset | [hakari-bench/NanoBEIR-sv](https://huggingface.co/datasets/hakari-bench/NanoBEIR-sv) |

Representative query and positive passage snippets:

| Query | Positive document snippet |
| --- | --- |
| Var hålls Final Four detta år? | NCAA Division I:s herrarnas basketturnering 2018 var en turnering med utslagning för 68 lag... |
| Var Nattens Häxer ursprungligen en Disney-film? | Nightmare Before Christmas uppstod från ett dikt skrivet av Tim Burton 1982... |
| Varför finns Ängeln i norr? | Enligt Gormley hade en ängel tre betydelser: först, att symbolisera att kolgruvarbetare arbetade... |
| Var i grundlagen nämndes tre-femtedelskompromissen ursprungligen? | Tre-femtedelskompromissen finns i Artikel 1, Avsnitt 2, Paragraf 3 i USA:s konstitution... |
| Vem sjunger "Someone's Watching Me" tillsammans med Michael Jackson? | "Somebody's Watching Me" är en låt av den amerikanska sångaren Rockwell från hans debutalbum... |
