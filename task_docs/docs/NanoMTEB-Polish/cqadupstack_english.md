# NanoMTEB-Polish / cqadupstack_english

## Overview

`cqadupstack_english` is the Polish NanoMTEB version of the English-language forum subset from CQADupStack. Although the original Stack Exchange community concerns English usage, grammar, punctuation, pronunciation, and style, this task presents the duplicate-question retrieval problem through Polish translated text. The goal is to retrieve forum questions that ask the same underlying English-language question as the query. This creates a distinctive retrieval setting: the documents discuss English grammar and usage, but the benchmark language is Polish, so models must handle translated explanations of another language's linguistic phenomena.

The Nano task contains 200 queries, 10,000 candidate documents, and 1,356 positive relevance judgments. Queries average about 47 characters and documents about 488 characters. The task has many duplicate clusters: 98 of the 200 queries have more than one positive document, the average number of positives per query is 6.78, and the largest cluster has 79 positives. This makes the task a strong test of whether a model can recover many different formulations of the same grammar or usage question.

## Details

### What the Original Data Measures

The original CQADupStack task measures duplicate-question retrieval in community question answering data. In the English subset, the subject matter is not general web search but questions about the English language: word choice, punctuation, capitalization, sentence structure, idioms, pronunciation, and grammatical acceptability. Relevance means that two questions ask the same or nearly the same language-use problem, not simply that they mention the same word or punctuation mark.

For retrieval models, this is a subtle task. Many questions include tiny surface differences that matter, such as "part" versus "a part", the use of an article in a title, or the choice between a hyphen, en dash, and em dash. Other questions ask broad recurring issues, such as whether a sentence can end with a preposition. A model must identify when examples are interchangeable and when a small linguistic distinction changes the actual question.

### Observed Data Profile

The Polish version adds an extra layer of abstraction. The query and document text are Polish, but the underlying concepts are English-language phenomena. Some source terms, quoted examples, punctuation symbols, and English words remain visible in the text. This produces a mixed representation where Polish explanatory prose surrounds English examples. Strong models need to preserve the role of the quoted English fragment while understanding the Polish question around it.

The task is cluster-heavy. The median number of positives is 1, but almost half of the queries have multiple positives, and several broad grammar topics have many duplicates. This means a model can perform well on some queries through exact overlap, but high recall requires recognizing repeated community questions across many paraphrases and examples.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.3188, hit@10 of 0.4850, and recall@100 of 0.2817. The lexical baseline is weaker here than in many technical duplicate tasks. BM25 can succeed when the query contains a distinctive punctuation term, quoted English word, or repeated phrase. For example, exact mentions of hyphen, dash, capitalization, preposition, or a quoted expression can provide useful anchors.

However, English-language usage questions are often paraphrased through different examples. Two users may ask the same grammar question with different sentences, different nouns, or different explanatory wording. In the Polish translation, inflection and translated phrasing further reduce direct token overlap. BM25 therefore misses many relevant duplicates, especially when the shared issue is conceptual rather than lexical.

### Dense Evaluation Profile

The dense `harrier-oss-270m` run is clearly stronger, with nDCG@10 of 0.3926, hit@10 of 0.6100, and recall@100 of 0.3783. Dense retrieval is better suited to this subset because it can connect questions about the same grammatical phenomenon even when the examples differ. It can also use the semantic frame of the Polish explanation, such as choosing between punctuation marks or asking whether a syntactic construction is acceptable.

The dense advantage indicates that the task is not mostly a keyword search problem. A model must represent linguistic intent: what distinction is being asked about, what part of the example is important, and whether two posts are asking the same rule-level question. Dense similarity captures more of this structure than term frequency alone.

### Reranking Hybrid Evaluation Profile

`reranking_hybrid` reports nDCG@10 of 0.3725, hit@10 of 0.5800, and recall@100 of 0.3776. Its recall is nearly identical to dense retrieval, but its top-10 ranking is lower. Candidate lists contain 100 to 101 items, and 45 rows required the relevance safeguard for reranking diagnostics. This suggests that hybrid fusion preserves many of the same positives as dense retrieval, but the final ordering is less favorable for the highest ranks.

The result is important for reranking experiments. Hybrid candidates still provide a broad candidate pool that mixes exact lexical anchors with semantic matches, which can be valuable for a cross-encoder. But for direct first-stage ranking on this task, dense retrieval is the stronger profile. Researchers should therefore distinguish between hybrid as a candidate-generation strategy and hybrid as the final ranked output.

### Metric Interpretation for Model Researchers

This subset is a good example of a task where dense retrieval is stronger than BM25 and also slightly stronger than the hybrid ranking at the top. BM25's lower recall@100 shows that exact lexical evidence alone is insufficient for many grammar duplicates. Dense retrieval's higher nDCG@10 and hit@10 show that embedding similarity better captures the recurring language-use intent.

At the same time, the hybrid recall being close to dense means lexical evidence is not irrelevant. Quoted words, punctuation names, and grammatical terms can still be highly diagnostic. A strong reranker should benefit from a candidate pool that includes both the dense semantic matches and the lexical matches around exact English examples.

### Query and Relevance Type Tendencies

Representative queries ask about generic uses of "it", choosing among en dash, em dash, and hyphen, ending a sentence with a preposition, capitalizing the definite article in a name, or distinguishing "part" from "a part". These are not broad topical categories; they are precise language-use questions. Relevant documents often discuss the same linguistic issue with different example sentences or slightly different explanatory setup.

The task also contains many cases where a surface word is not enough to define relevance. Two posts may both mention an article, a dash, or a preposition, but the actual question can differ. Conversely, two duplicates may share few Polish tokens because their examples and framing differ. This makes the task sensitive to both over-literal and over-broad matching.

### Representative Failure Modes

BM25-style retrieval may over-rank posts that share a quoted English word or a punctuation term while asking a different rule question. For example, many questions can mention dashes, but some ask about punctuation style, some about ranges, and some about compound modifiers. Dense retrieval may retrieve posts that are semantically adjacent within grammar discussion but not duplicates, such as two questions about articles that concern different article rules.

Another failure mode is losing the role of the embedded English example. The surrounding Polish text may ask whether a phrase is grammatical, whether a word choice is natural, or whether punctuation is acceptable. A model that treats the English fragment as ordinary topical text can miss which part of the example defines relevance.

### Training Data That May Help

Useful training data includes duplicate-question pairs from language forums, paraphrased grammar questions, multilingual explanations of English examples, and hard negatives where the same quoted word appears in a different linguistic question. Translation-style data can help because the benchmark text is Polish while the subject matter is English.

For reranking, hard negatives should be chosen from near-duplicate grammar topics: multiple questions about articles, multiple questions about dashes, or multiple questions about prepositions that differ in the specific rule being asked. These examples teach the model to separate same-topic retrieval from true duplicate-question retrieval.

### Model Improvement Notes

Dense models should focus on representing the relation between the Polish explanation and the embedded English language example. Improvements in cross-lingual or translation-aware sentence representation may help, even though the visible benchmark language is Polish. Models should also preserve small lexical distinctions because grammar questions can turn on a single word, punctuation mark, or article.

Sparse systems may benefit from better tokenization of quoted English fragments and Polish morphology, but this task is unlikely to become BM25-dominant because many positives are paraphrased. Hybrid systems should be evaluated with care: they may be excellent for candidate recall while not necessarily improving the final top-10 ranking without a strong reranker.

## Example Data

| Query | Positive document |
| --- | --- |
| Ogólne „to” [11 chars] | Do czego odnosi się „to” w „pada deszcz”? Chciałem pozostawić tytuł pytania bez zmian, aby nie odrywać się od zabawy `:)`. W każdym razie > pada deszcz. Co pada? Czy to niebo? Chmury? Pogoda? Deszcz? Co to jest"? Jakieś spostrzeżenia historyczne dotyczące oświadczenia? [269 chars] |
| Jak przebić zakres dzielonych liczb? [36 chars] | Kiedy powinienem używać pauzy, pauzy i łącznika? Generalnie wiem, jak używać myślnika, ale kiedy powinienem użyć en-dash zamiast em-myślnika, a kiedy powinienem użyć myślnika zamiast em-myślnika? [195 chars] |
| Wybieranie między „z czym eksperymentować” a „z czym eksperymentować” [69 chars] | Kiedy należy kończyć zdanie przyimkiem? Jak wielu innych, często kończę zdanie przyimkiem. Tak, wzdrygam się. Zwykle przepisuję zdanie, ale czasami (w e-mailach) po prostu z tym żyję. _Do_ _z_... wiesz kim jesteś. Czy powinienem dalej walczyć na tym, czy jest to w porządku w niektórych okolicznościach? [303 chars] |

### Source Reference Table

| Source | What it contributes |
| --- | --- |
| CQADupStack paper | Original Stack Exchange duplicate-question retrieval construction. |
| MTEB paper | Benchmark context for retrieval and embedding-model evaluation. |
| CLARIN-KNEXT dataset card | Polish translated English-forum subset used by the task. |
| MTEB task card | Task packaging and retrieval benchmark interface. |

### Representative Snippets

- A query about generic uses of "it" maps to documents asking about the same pronoun behavior in English.
- A query about en dash, em dash, and hyphen maps to posts comparing punctuation choices in similar contexts.
- A query about sentence-final prepositions maps to duplicates about whether such constructions are acceptable.
- A query about capitalizing the definite article in a name maps to documents about title and name capitalization rules.
- A query about "part" versus "a part" maps to posts about the same article-sensitive word-choice distinction.
