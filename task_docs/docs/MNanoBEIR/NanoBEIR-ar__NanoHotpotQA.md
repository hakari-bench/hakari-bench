# MNanoBEIR / NanoBEIR-ar / NanoHotpotQA

## Overview

NanoBEIR-ar / NanoHotpotQA is the Arabic NanoBEIR version of HotpotQA, the
multi-hop question answering benchmark introduced in
[HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question
Answering](https://arxiv.org/abs/1809.09600). Each query is an Arabic
translated multi-hop question, and the retrieval target is a pair of Arabic
translated Wikipedia passages that together provide the supporting evidence.
The Nano task contains 50 queries, 5,090 documents, and 100 positive qrels:
every query has exactly two positives. This makes the task fundamentally
different from single-page fact retrieval. A system must retrieve the full
evidence pair, not merely the most obvious entity page. The strongest candidate
view here is `reranking_hybrid`, which improves top-rank ordering while dense
retrieval provides strong semantic coverage.

## Details

### What the Original Data Measures

HotpotQA was designed to require reasoning over multiple Wikipedia documents.
The original dataset includes bridge questions, where one entity leads to
another through a relation, and comparison questions, where two entities must
be compared. Supporting facts are part of the dataset design, so retrieval is
not just a pre-processing detail: finding the supporting pages is central to
the task.

The Arabic NanoBEIR version keeps the evidence-set retrieval objective in
translated form. The model receives a question and must rank Wikipedia-style
passages. A relevant set usually includes one passage that identifies an
intermediate entity and another passage that supplies the requested attribute,
comparison, date, creator, member, or location. Complete retrieval requires
both.

### Observed Data Profile

The metadata records 50 queries, 5,090 documents, and 100 positive qrels. Every
query has two positives, so the average, median, minimum, and maximum positives
per query are all 2. Query text averages 72.76 characters, and documents
average 410.03 characters. The examples include questions about an actress in a
television series, a Japanese sword and its maker, a film written and directed
by a named person with music by another person, a football game at Sun Life
Stadium, and a music compilation by a band with another performance identity.

The examples show classic HotpotQA behavior: a query often names one entity but
asks for an attribute that is found through another entity. A retriever that
returns only the most lexically obvious page can look good by hit@10 but still
be incomplete for downstream answering.

### BM25 Evaluation Profile

The BM25 candidate subset reaches nDCG@10 = 0.6837, hit@10 = 0.9400, and
Recall@100 = 0.8900. BM25 is strong because HotpotQA questions contain visible
names, titles, places, sports teams, works, and relation phrases. These lexical
anchors often recover at least one supporting page, especially the page named
directly in the question.

BM25's limitation is the second hop. The indirectly required page may not share
many terms with the original question, or the relevant relation may be
expressed through a title, alias, occupation, creator, or membership link.
Sparse retrieval can therefore retrieve the obvious entity while missing the
bridge target or comparison counterpart.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` reaches nDCG@10 =
0.7365, hit@10 = 0.9800, and Recall@100 = 0.9400. Dense retrieval improves
over BM25 across all visible metrics, which suggests that embedding similarity
helps connect the question to the less lexical supporting page. It is
especially useful for bridge relations and comparison wording, where the second
document may be semantically linked rather than term-identical.

Dense retrieval still does not solve the whole task. It can retrieve one
semantically plausible page from the same entity neighborhood while missing the
other required support. It can also blur aliases, titles, or related works,
which matters when two pages are needed for a precise reasoning path.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset reaches nDCG@10 = 0.7798, hit@10 =
0.9800, and Recall@100 = 0.9400. Hybrid is the best top-rank ordering view,
while tying dense on hit@10 and Recall@100. This indicates that BM25's lexical
anchors still help order candidates even when dense retrieval already has
strong coverage. The hybrid pool has exactly 100 candidates per query and no
rank-101 safeguard rows, so the reported top-100 coverage is not dependent on
extra positive insertion.

For reranker experiments, hybrid is the most useful view because it exposes
both direct-name candidates and semantically connected second-hop candidates.
The reranker must learn to rank the evidence pair, not simply the nearest
single page.

### Metric Interpretation for Model Researchers

HotpotQA-ar should be interpreted as evidence-set retrieval. Hit@10 only says
that at least one positive appears near the top; it does not guarantee that
both supporting pages are available. Recall@100 is therefore especially
important, and query-level inspection should verify whether both positives are
retrieved. Dense retrieval and hybrid both improve Recall@100 over BM25, while
hybrid gives the best nDCG@10. That pattern suggests that lexical and semantic
signals are complementary for ordering multi-hop evidence.

A model that retrieves one page very confidently but misses the second page may
look adequate under simple hit metrics but still fail downstream QA. Strong
retrieval models for this task should optimize for complete support coverage.

### Query and Relevance Type Tendencies

Queries are Arabic multi-hop questions. They often combine a named entity with
a relation to another entity: actor to show, show to co-star, film to director,
composer to work, sports game to date, or band to alternate identity. Relevant
documents are short Wikipedia-style entity pages. Both positives are needed
because one passage usually establishes an intermediate link and the other
contains the answer-bearing attribute.

Lexical-heavy cases include exact titles and names. Dense-heavy cases include
bridge relations, aliases, and comparison structures where the second support
does not repeat much of the query. Hybrid retrieval is strongest when the first
support is lexical and the second support is semantic.

### Representative Failure Modes

BM25 can retrieve the page explicitly named in the query but miss the linked
page needed for the second hop. It can also rank pages with matching titles or
names above the correct supporting page. Dense retrieval can retrieve a
semantically related entity while confusing aliases, works, or people in the
same domain. In both cases, the common failure is incomplete evidence: one
positive is found, but the pair is not.

Good hard negatives are same-title works, related people from the same cast or
organization, pages connected to the first hop but not the answer, and
comparison counterparts that share type but are not part of the reasoning path.

### Arabic-Specific Notes

Arabic multi-hop retrieval must handle translated entity names, transliterated
titles, aliases, definite articles, and mixed-language proper nouns. Sparse
retrieval needs to preserve names and titles. Dense retrieval needs to connect
relations across translated phrasing and recognize when two passages form a
reasoning chain. Because each query requires two positives, ranking diversity
matters: retrieving several near-duplicates of the same hop is less useful than
retrieving both hops.

### Training and Leakage Notes

Training should exclude HotpotQA, BEIR, or NanoBEIR records likely to overlap
with these evaluation questions or supporting pages. Useful non-overlapping
data includes HotpotQA examples with supporting facts, Arabic or multilingual
multi-hop QA retrieval, Wikipedia hyperlink graph retrieval pairs, and
question-to-multiple-document supervision. Multi-positive training is required
because every query has exactly two positives.

### Model Improvement Hints

The main improvement target is complete support retrieval. First-stage
retrievers should preserve direct entity anchors while expanding to linked
support pages. Rerankers should learn whether a candidate completes the
reasoning path rather than whether it merely resembles the question. Pair-aware
or diversity-aware reranking can help when the candidate list contains many
variants of the first hop.

### Training Data That May Help

Useful training data includes non-overlapping HotpotQA training examples with
supporting facts, Arabic or multilingual multi-hop QA, hyperlink-based
Wikipedia retrieval pairs, bridge-question supervision, comparison-question
supervision, and hard negatives from the same entity neighborhood.

### Synthetic Data Guidance

Generate paired Arabic Wikipedia-style entity passages connected by hyperlinks,
shared types, dates, locations, occupations, creators, memberships, or aliases.
Then generate Arabic bridge and comparison questions that require both
passages. Positives should be both documents in the reasoning path; synthetic
questions answerable from only one passage are less useful for this task.

## Example Data

| Query | Positive document |
| --- | --- |
| شاركت بيني راي بريدجز في مسلسل كوميدي تلفزيوني مع أي ممثل آخر؟ [62 chars] | بيني راي بريدجز (ولدت في 29 يوليو 1990) ممثلة أمريكية. شاركت في العديد من الأعمال التلفزيونية مثل "لأجل حبك"، "القانون العائلي"، "ولد يلتقي العالم"، و"بيت الآباء". تشتهر بدورها في مسلسل "نصف ونصف" كشا... [200 / 208 chars] |
| من منح كاغانوي شيجيموتشي سيفًا صنعه مؤسس مدرسة موراماسا؟ [56 chars] | كاغانوي شيجيموتشي (加賀井 重望، 1561 – 27 أغسطس 1600) كان ساموراي يابانيًا في فترة أزوتشي-موموياما، خدم عشيرة أودا. كان حاكمًا على قلعة كاغانوي. خلال معركة كوماكي وناغاكوت، قاتل شيجيموتشي تحت قيادة والده ش... [200 / 457 chars] |
| أي فيلم كتب وأخرجه جوبي هارولد مع موسيقى كتبها صموئيل سيم؟ [58 chars] | سامويل سيم هو ملحن أفلام وتلفزيون. استطاع أن يحصل على الشهرة لأول مرة بموسيقى حازت على جوائز لسلسلة الدراما البريطانية "دونكيرك". منذ ذلك الحين، كتب الموسيقى لأعمال متنوعة من الأفلام والتلفزيون، وأحدث... [200 / 452 chars] |
| ما هو تاريخ مباراة كرة القدم الجامعية التي لعبت في ملعب صن لايف في ميامي جاردنز، فلوريدا، حيث هزم كل... [100 / 146 chars] | فريق كرة القدم كليمسون تايجرز لعام 2015 كان يمثل جامعة كليمسون في موسم كرة القدم NCAA Division I FBS لعام 2015. كان الفريق بقيادة المدرب الرئيسي دابو سويني في عامه السابع الكامل والثامن بشكل عام منذ ت... [200 / 1,006 chars] |
| Devil's Food هي مجموعة من الأغاني الفردية من فرقة روك أند رول أمريكية كانت معروفة أيضًا بأداء عروض ك... [100 / 120 chars] | Devil's Food هي مجموعة من الأغاني الفردية المفضلة من فرقة الروك الأمريكية Supersuckers، صدرت في أبريل 2005 عن طريق شركة Mid-Fi Records. [135 chars] |

### Public Sources

- [HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering](https://arxiv.org/abs/1809.09600), 2018.
- [HotpotQA official site](https://hotpotqa.github.io/).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663), 2021.
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595), 2025.
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-ar](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ar)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering | 2018 | task paper | [https://arxiv.org/abs/1809.09600](https://arxiv.org/abs/1809.09600) |
| HotpotQA official site |  | project page | [https://hotpotqa.github.io/](https://hotpotqa.github.io/) |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | [https://arxiv.org/abs/2104.08663](https://arxiv.org/abs/2104.08663) |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | [https://arxiv.org/abs/2502.13595](https://arxiv.org/abs/2502.13595) |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | [https://huggingface.co/collections/zeta-alpha-ai/nanobeir](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
