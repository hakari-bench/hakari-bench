# NanoMTEB-Dutch / belebele_nld_latn_eng_latn

## Overview

`belebele_nld_latn_eng_latn` is a cross-lingual Belebele retrieval task in the
Dutch NanoMTEB group. The queries are English reading-comprehension questions,
and the retrieval corpus is made of Dutch passages. The Nano split contains 200
queries, 488 documents, and 200 positive relevance links, with exactly one
positive passage per query. It is therefore a compact but direct test of whether
a retrieval model can map an English question to the corresponding Dutch
evidence passage without relying on same-language lexical overlap.

The observed candidate statistics make this split primarily a multilingual
semantic alignment task. BM25 is weak because most query terms are English while
the documents are Dutch. Dense retrieval with `harrier_oss_v1_270m` is much
stronger, reaching very high top-10 and top-100 coverage. The reranking hybrid
candidate set recovers almost every positive passage by top 100, but its top-10
ranking is far below the dense candidate column because sparse lexical evidence
adds many shallow matches. This makes the task useful for diagnosing whether a
model's cross-lingual representations are strong enough to overcome the
vocabulary boundary between English questions and Dutch passages.

## Details

### What the Original Data Measures

[The Belebele Benchmark](https://arxiv.org/abs/2308.16884) defines Belebele as a
parallel multiple-choice reading-comprehension benchmark covering 122 language
variants. Its passages are derived from FLORES-200, and its questions are
constructed so that the answer should be grounded in the passage rather than in
external knowledge. In retrieval form, the answer options are not the central
object; the benchmark becomes a passage-selection problem where a question must
retrieve the passage that contains the relevant evidence.

The Dutch tasks in MTEB-NL use Belebele as multilingual and Dutch retrieval
material. This particular direction is cross-lingual: English questions are
matched against Dutch passages. As a result, the task measures whether an
embedding or reranking system can bridge translation-equivalent meanings. It is
less about long-document reasoning and more about passage-level semantic
alignment, named-entity preservation, and resistance to misleading topical
neighbors.

### Observed Data Profile

The corpus is small enough that every query can be compared against all 488
documents, but the single-positive setup still makes ranking errors visible.
Queries average 81.31 characters, while documents average 529.14 characters.
The length asymmetry is typical of reading-comprehension retrieval: a short
question must select a paragraph-length passage that contains several facts,
only one of which may answer the question.

Examples cover broad knowledge and news-style topics: the French Revolution,
early agriculture in New Zealand, subsistence agriculture, violent periods in
Chinese history, and Tutankhamun. Many English questions contain words that have
no direct surface match in the Dutch passage. A model that succeeds on this task
must connect concepts such as "working class citizens" to Dutch descriptions of
metric reform, republicanism, and national identity, or "subsistence
agriculture" to Dutch explanations of farming for a family's own needs.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 = 0.3288, hit@10 = 0.3800, and recall@100 = 0.4400 over the
488-document candidate set. This is the expected behavior for an English-to-
Dutch retrieval direction. BM25 rewards exact and near-exact term occurrence, so
it can still benefit from names, dates, loanwords, acronyms, and internationally
shared forms. However, most content words are separated by language, which means
the lexical signal is sparse and uneven.

The BM25 successes are likely concentrated in examples with preserved entities
or cognates. Questions about "China", "Tutankhamun", or specific organizations
can retain enough surface evidence to place a relevant passage somewhere in the
candidate list. Failures become common when the question asks for an abstract
property, a paraphrased reason, or a relation that is expressed only in Dutch.
For model researchers, this baseline is useful as a warning against treating
high lexical overlap as the default difficulty of Belebele. In this direction,
BM25 is mostly an entity and cognate detector, not a reliable comprehension
retriever.

### Dense Evaluation Profile

Dense retrieval with `harrier_oss_v1_270m` reaches nDCG@10 = 0.9306, hit@10 =
0.9850, and recall@100 = 0.9850. This is the dominant candidate profile for the
task. The numbers indicate that the dense model usually maps an English
question and its Dutch evidence passage into a shared semantic neighborhood,
even when the useful terms are translated or paraphrased.

The remaining dense errors are therefore especially informative. They are less
likely to be simple language mismatch errors and more likely to involve
fine-grained distinctions among same-topic passages. Belebele passages often
contain several related facts, so a dense model can retrieve a passage about the
right country, historical period, or scientific domain while missing the exact
answer-bearing paragraph. This split is a good probe for cross-lingual dense
alignment at the paragraph level: a strong model should keep the right language
bridge while still preserving the specific question intent.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate column reaches nDCG@10 = 0.4456, hit@10 =
0.5200, and recall@100 = 0.9900, with 100 to 101 candidates per query and two
rank-101 safeguard rows. Its recall is the best of the three candidate profiles,
which shows that combining sparse and dense evidence can recover almost every
positive passage within the reranking pool. Its top-10 ranking, however, is much
weaker than dense retrieval alone.

This contrast is the central lesson of the task. Hybrid search can emulate a
broad candidate-generation strategy by keeping dense semantic matches while also
including lexical matches from BM25. In this cross-lingual setting, the lexical
side adds coverage but also introduces many candidates whose apparent relevance
comes from names or shared forms rather than from translated meaning. A reranker
using this pool must learn to demote those shallow lexical matches and promote
the dense semantic positive. The column is therefore best interpreted as a high-
recall reranking input rather than as a strong final ranking.

### Metric Interpretation for Model Researchers

nDCG@10 is the most important metric for comparing final ranking quality here
because each query has one positive passage. A high nDCG@10 means the positive
is not merely found but placed near the top. Recall@100 is better interpreted as
candidate-pool quality: dense and reranking hybrid both find nearly all
positives by top 100, while BM25 misses more than half.

The difference between dense nDCG@10 and hybrid recall@100 is useful when
designing rerankers. If a reranker starts from the hybrid pool, the positive is
almost always available, but the initial order may be poor. If it starts from
dense retrieval, the positive is usually both available and already highly
ranked. This makes the split a good place to test whether reranking improves
cross-lingual precision or merely preserves an already strong dense order.

### Query and Relevance Type Tendencies

Queries are short comprehension questions asking for causes, descriptions,
locations, people, or historically correct statements. The positive document is
usually a Dutch paragraph containing the answer in context. Because the query
language is English, the strongest signal is translation-equivalent meaning, not
surface-word reuse.

The most reliable dense signals are event identity, named entities, and the
semantic relation requested by the question. The most unreliable sparse signals
are isolated names and broad topic words. A candidate can mention the right
historical period or location but still fail to answer the exact question.

### Representative Failure Modes

BM25 failures mostly come from missing translation equivalence. It cannot
directly connect English words such as "working class", "agriculture society",
or "subsistence" to their Dutch paraphrases unless a shared entity is present.
Dense failures are more subtle: the model may retrieve a semantically adjacent
Dutch passage that matches the topic but not the exact queried fact.

Hybrid failures combine both patterns. The candidate pool is broad, but the
initial ranking may overvalue lexical anchors from BM25 and undervalue the
cross-lingual semantic match. Reranking models evaluated on this task should be
checked for whether they can recover from that noisy hybrid order.

### Training Data That May Help

Useful training data includes English-to-Dutch QA retrieval pairs, multilingual
dense retrieval data with Dutch documents, translated reading-comprehension
examples with English queries, and Dutch passage retrieval hard negatives. The
most valuable negatives are Dutch passages that share an entity or topic with
the positive but answer a different question.

Training data should exclude the Belebele test questions and passages used by
this Nano split. Synthetic data can be built from short Dutch passages outside
the evaluation set, paired with English comprehension questions grounded in one
selected passage. The generated question should be answerable from the positive
passage and should avoid copying long translated phrases from the document.

### Model Improvement Notes

Improving this task requires robust English-Dutch semantic alignment and fine
passage discrimination. Better multilingual contrastive training should help
place translated question-passage pairs near each other. Hard-negative training
should focus on same-topic Dutch passages so that the model learns the exact
question intent rather than only the broad topic.

For rerankers, the key requirement is to treat the hybrid pool as noisy. The
positive is usually present, but not always near the top. A strong reranker
should use cross-lingual evidence and passage-level answerability to move the
positive above candidates that share only names, countries, or topical words.

## Example Data

| Query | Positive document |
| --- | --- |
| Which of the changes prompted by The French Revolution had a significant impact on working class citizens? [106 chars] | De Revolutie heeft grote sociale en politieke gevolgen gehad, zoals het gebruik van het metrieke stelsel, een verschuiving van de absolute monarchie naar republicanisme, nationalisme en de opvatting dat het land aan zijn inwoners toebehoort in plaats van een enkele leider. Voor alle mannelijke sollicitanten waren na de revolutie functies te verkrijgen, zodat de meest ambitieuze en geschikte kandidaten konden slagen. Hetzelfde geldt voor het leger. De legerrangen worden niet meer gebaseerd op iemands klasse maar op het kaliber van de persoon. De Franse Revolutie inspireerde ook in andere landen de onderdrukte arbeidersklasse tot een revolutie. [650 chars] |
| According to the passage, who may have started an agriculture society? [70 chars] | Voor een groot deel van de negentiende en twintigste eeuw geloofde men dat de vroegste inwoners van Nieuw-Zeeland de Maori waren, die jacht maakten die op enorme vogels genaamd moa's. De theorie leidde tot het idee dat het Maori-volk in een grote vloot uit Polynesië kwam en Nieuw-Zeeland veroverde op de Moriori, waarna er een agrarische samenleving werd gevormd. Er zijn echter nieuwe aanwijzingen dat de Moriori een groep Maori's waren op het vasteland die van Nieuw-Zeeland naar de eilanden van Chatham trokken en daar een persoonlijke, vredevolle gemeenschap opbouwden. Een andere stam op de Cathameilanden waren Maori die vanuit Nieuw-Zeeland zijn geëmigreerd. Ze noemden zichzelf de Moriori en na een paar schermutselingen en werden de Moriori uiteindelijk weggevaagd [774 chars] |
| Which of the following accurately describes the practice of subsistence agriculture? [84 chars] | Zelfvoorzienende landbouw is landbouw waarbij voldoende voedsel wordt geproduceerd om aan de behoeften van de boer en zijn gezin te voldoen. Landbouw met als doel levensonderhoud is een simpel systeem dat meestal biologisch is. Hierbij wordt opgeslagen zaad gebruikt dat afkomstig is uit de ecoregio, en dat wordt gecombineerd met wisselende gewassen of andere relatief eenvoudige technieken om de opbrengst te optimaal te maken. Vroeger werkten de meeste boeren in de zelfvoorzienende landbouw. In veel ontwikkelingslanden is dit nog steeds het geval. [552 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| The Belebele Benchmark: a Parallel Reading Comprehension Dataset in 122 Language Variants | 2023 | arXiv paper | [https://arxiv.org/abs/2308.16884](https://arxiv.org/abs/2308.16884) |
| facebookresearch/belebele | 2023 | repository | [https://github.com/facebookresearch/belebele](https://github.com/facebookresearch/belebele) |
| mteb/belebele |  | dataset card | [https://huggingface.co/datasets/mteb/belebele](https://huggingface.co/datasets/mteb/belebele) |
| MTEB-NL and E5-NL: Embedding Benchmark and Models for Dutch | 2025 | arXiv paper | [https://arxiv.org/abs/2509.12340](https://arxiv.org/abs/2509.12340) |

### Representative Snippets

| Query | Positive passage |
| --- | --- |
| Which changes prompted by the French Revolution had a significant impact on working class citizens? | A Dutch passage describes revolutionary reforms such as the metric system, republicanism, nationalism, and the idea that a country belongs to its inhabitants. |
| According to the passage, who may have started an agriculture society? | A Dutch passage discusses the Maori as early inhabitants of New Zealand, their hunting of moa, and a theory about agricultural society. |
| Which statement accurately describes subsistence agriculture? | A Dutch passage defines subsistence agriculture as farming mainly to feed the farmer's own family, with limited outside trade. |
| According to the passage, which period was one of China's most violent eras? | A Dutch passage summarizes Chinese dynasties and identifies the Warring States period as especially violent. |
| When did King Tutankhamun gain notoriety? | A Dutch passage explains that Tutankhamun is famous today, although he was not considered a major ruler in antiquity. |
