# NanoMLDR / ar

## Overview

`NanoMLDR / ar` is the Arabic split of NanoMLDR, a multilingual long-document
retrieval benchmark derived from MLDR. Arabic queries retrieve long Arabic
documents, usually full encyclopedia-style articles, where the answer-bearing
paragraph may be only a small part of the positive document. The Nano split has
150 queries, 4,766 documents, and 150 positive qrel rows, with exactly one
positive document per query. Current diagnostics show BM25 as the strongest
profile by nDCG@10, hit@10, and recall@100, while dense retrieval is much weaker
on these long Arabic documents and `reranking_hybrid` sits between the two.

## Details

### What the Original Data Measures

MLDR was introduced with the M3-Embedding work as a multilingual long-document
retrieval benchmark. The dataset card describes a construction process in which
long articles are sampled, a paragraph is selected, and a specific question is
generated from that paragraph. The retrieval target is the full document that
contains the answer-bearing paragraph.

For Arabic, this means the task is not ordinary short-passage retrieval. A
retriever must map a specific Arabic question to a long Arabic article that may
contain many unrelated sections, historical details, named entities, and
background material. The benchmark measures long-document candidate selection,
not extraction of the final answer span.

### Observed Data Profile

The Nano split contains 150 queries, 4,766 documents, and 150 positive qrel
rows. Every query has exactly one positive document. Queries average 71.09
characters, while documents average 12,006.83 characters. The long document
length is the central property of the task.

Observed questions ask about information embedded in lengthy Arabic articles on
economics, ancient empires, crusades, New Testament topics, topography,
Indochina war history, aviation or military history, geography, and historical
events. The question is usually specific, but the positive document can be a
large article whose title is broader than the asked paragraph.

### BM25 Evaluation Profile

The dataset-provided BM25 candidate subset contains 500 candidates per query and
achieves nDCG@10 = 0.7604, hit@10 = 0.8733, and recall@100 = 0.9533. BM25 is the
strongest observed profile on this split. Long Arabic documents contain many
opportunities for exact overlap with generated questions, including named
entities, dates, places, technical phrases, and historical terminology.

This is a long-document setting where term presence is often valuable. If a
question asks about a specific military campaign, religious episode, geographic
concept, or historical figure, the full article may contain rare lexical
anchors that BM25 can match even when the answer paragraph is buried deep in the
document.

### Dense Evaluation Profile

The dense `harrier_oss_v1_270m` candidate subset contains 500 candidates per
query and achieves nDCG@10 = 0.4443, hit@10 = 0.5667, and recall@100 = 0.7600.
Dense retrieval is much weaker than BM25 on this Arabic long-document split.
The likely difficulty is representing a very long document with a single dense
embedding or limited pooling signal.

The query may match one paragraph, but the document embedding must also absorb
many other topics and sections. Dense similarity can therefore drift toward
articles that are semantically related in broad theme while missing the full
article that contains the exact answer-bearing paragraph.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset contains mostly 100 candidates per
query, with eight queries using a rank-101 safeguard row. It achieves nDCG@10 =
0.6181, hit@10 = 0.7667, and recall@100 = 0.9467. Hybrid retrieval improves
substantially over dense retrieval but remains below BM25 on top-rank and
coverage metrics.

This pattern indicates that lexical evidence is especially important for Arabic
MLDR. Dense retrieval contributes semantic matches, but the strongest signal is
often exact overlap with rare names, event terms, and article-specific
phrases. Hybrid search is still useful as a reranking candidate source, but it
does not surpass BM25 here.

### Metric Interpretation for Model Researchers

This task is single-positive: each query has one relevant long document.
Hit@10 measures whether that document appears near the top. nDCG@10 is
sensitive to the exact rank of the single positive, and recall@100 measures
whether the document survives for reranking.

The Arabic MLDR pattern is a strong warning for dense long-document retrieval:
a general dense embedding can underperform exact lexical matching when the
answer signal is a small paragraph inside a long article. Models should be
evaluated for paragraph-aware indexing, late interaction, chunk aggregation, or
hybrid retrieval rather than only full-document dense similarity.

### Query and Relevance Type Tendencies

Queries are specific Arabic questions about facts, causes, symbols, military
events, religious narratives, geography, and historical consequences. They are
generated from a paragraph but evaluated against the full article.

Relevant documents are long Arabic articles with broad title context and many
non-answer sections. The task rewards rare-term recall, article-level evidence
coverage, and the ability to connect a local answer paragraph to its full
document.

### Representative Failure Modes

Dense retrieval can select an article that is broadly similar to the question
but does not contain the answer paragraph. This is especially likely for
historical or religious topics where many long articles share names, places, and
themes. BM25 can fail when the answer is paraphrased or when the query uses
terms that appear in several related articles.

Hybrid retrieval can include the positive document but still rank another
lexically and semantically plausible long article higher. Rerankers need access
to paragraph-level evidence or chunked document signals to choose correctly.

### Training Data That May Help

Useful training data includes Arabic long-document QA retrieval pairs,
multilingual MLDR training data outside this Nano split, Arabic Wikipedia
retrieval data, and entity-sharing long-document hard negatives. Training should
include positives where only one paragraph in a long document answers the
question.

Synthetic data can help when it samples a paragraph from a long Arabic
encyclopedic article, generates a specific grounded Arabic question, and uses
the whole article as the positive document. Hard negatives should be long Arabic
articles from the same entity class, period, country, or topic that do not
contain the answer-bearing paragraph.

### Model Improvement Notes

Dense retrievers should avoid relying only on a single full-document vector for
very long Arabic articles. Chunked retrieval, late interaction, paragraph-aware
pooling, or multi-vector document representations are likely more appropriate.
Sparse systems should preserve rare Arabic names, dates, and event terms while
handling morphology and spelling variation.

For hybrid systems, `NanoMLDR / ar` suggests using BM25 as a strong candidate
generator and adding semantic reranking carefully. The current hybrid candidate
set improves over dense but does not beat BM25, so rerankers must be validated
against lexical long-document baselines.

## Example Data

| Query | Positive document |
| --- | --- |
| ما هي الأسباب التي دفعت الفرنسيين إلى مواجهة الجموع المسلحة الألمانية في آسيا الصغرى؟ [85 chars] | الحملة الصليبية الثانية كانت ثاني حملة صليبية رئيسية تنطلق من أوروبا، دُعي إليها عام 1145 كرد فعل على سقوط إمارة الرها في العام الذي سبق. حيث كانت الرها (إديسا) أول مملكة مسيحية تقام خلال الحملة الصليبية الأولى (1096 - 1099) وكانت أول مملكة تسقط كذلك. دعا إلى الحملة الثانية البابا إيجين الثالث، وكانت أول حملة يقودها ملوك أوروبا، وهم لويس السابع ملك فرنسا وكونراد الثالث ملك ألمانيا، وبمساعدة عدد من نبلاء أوروبا البارزين. تحركت جيوش الملكين كل على حدة في أوروبا، وأخرهم بعض الشيء الإمبراطور البيزنطي مانويل كومينوسوبعد عبور الجيوش للمناطق البيزنطية من الأناضول، هُزم كلا الجيشين على يد السلاجقة المسلمين، كل على حدة. ووصل كل من لويس وكونراد وشراذم جيوشهما إلى القدس عام1148 م، وهناك حاولوا السيطرة على دمشق وهناك اتبعوا نصيحة اتضح أنها سيئة بالهجوم على دمشق، حيث فشلوا فشلاً ذريعاً. كانت الحملة الصليبية الثانية إلى الشرق هزيمة للصليبين ونصراً للدويلات الإسلامية. وأدت نتائجها إلى فتح المسلمين للقدس من جديد وقيام الحملة الصليبية الثالثة في نهاية القرن الثاني عشر الميلادي بعد سلسلة من الأحداث في ا... [1,000 / 20,202 chars] |
| ما هي أحداث النص المذكور التي تتعلق بيهودا وبطرس؟ [49 chars] | نظرة العهد الجديد لحياة المسيح أو حياة يسوع بحسب العهد الجديد وفقاً للعهد جديد فأن: يسوع المسيح ولد في بيت لحم كما توجب أن يولد بحسب ما تنبأ عنه النبي ميخا. تذكر الاناجيل الأربعة: متى، مرقس، لوقا، ويوحنا شهادات حية مما رأوه وتعلموه وكانوا شهودا له لما عمل من أعمال. كانت ولادته معجزية من غير أب، إذ حل الروح القدس على مريم العذراء، فحبلت به، ثم ولدته في بيت لحم، كما جاء في الكتاب المقدس. يؤمن المسيحيون أنه صُلب ومات من أجل دفع ثمن خطايا جميع البشر، كي لا يهلك كل من يؤمن به، بل تكون له الحياة الأبدية. ثم قام من قبره في اليوم الثالث، قاهرا الموت بالموت، كما تنبأ عنه في العهد القديم. ثم ظهر لتلاميذه وبقي معهم أربعين يوماً ومن ثم صعد إلى السماء، وجلس عن يمين الآب وسوف يأتي في اليوم الأخير ليدين الأحياء والأموات وملكه لن يكون له انقضاء. حياته وتعاليمه بحسب الكتاب المقدس تعتبر الأناجيل القانونية الأربعة: متى، مرقس، لوقا، ويوحنا المنابع الرئيسية الأساسية بالنسبة للتقليد المسيحي للحصول على معلومات عن حياة المسيح. النسب والعائلة بين الأناجيل الأربعة اختصت بشارتي متى ولوقا فقط بالحديث عن نسب يسوع... [1,000 / 15,908 chars] |
| ما هي الرموز الاصطلاحية المستخدمة لتمثيل المظاهر السطحية؟ [57 chars] | الطبوغرافيا أو إرَاثَة أو سمات سطح الأرض أو علم التضاريس هو تمثيل دقيق لسطح الأرض بعناصره الطبيعية والبشرية (أي مهتم بتضاريس سطح الأرض) وهي علم توقيع ورسم الهيئات الطبيعة والاصطناعية بمقياس ويرسم وبرموز اصطلاحية متفق عليها دوليا على قطعة من ورق أو ما شبه ذلك تسمى بالخريطة وهذه الأخيرة عبارة عن رسم هندسي مصغر لجزء من الأرض التي توضح كل المعالم والمظاهر ذات الأهمية الاستراتيجية. الاسم الطبوغرافيا مصطلح يوناني مركب من كلمتين: طبو TOPO وتعني الأرض أو المكان وغرافيا GRAPHIE وتعني الرسم والتمثيل البياني للتضاريس. الهدف من الطبوغرافية تهدف الدراسة الطبوغرافية إلى استغلال إمكانات مظهر السطح في كل التحليلات والاستنتاجات المتعلقة به أو بأحد العناصر المجسدة والقائمة بشرية كانت أو حيوية وفي وضعها كإمكانية أو عائق وفيما يلي بعض الميادين المستعملة للطبوغرافية. تشكل الطبوغرافية أساسا خرائطيا لدراسة جل مشاريع التخطيط والاستصلاح واستعمال أسطح أي كل ما يتعلق باستعمال خرائط مظاهر السطح بما في ذلك الهندسية المدنية والأشغال العمومية والبناء واستعمال الأرض في مختلف الاختصاصات. رسم الخريطة الطبوغرافية بعد عر... [1,000 / 23,514 chars] |

### Public Sources

- [M3-Embedding: Multi-Linguality, Multi-Functionality, Multi-Granularity Text Embeddings Through Self-Knowledge Distillation](https://arxiv.org/abs/2402.03216),
  2024.
- [M3-Embedding ACL Anthology version](https://aclanthology.org/2024.findings-acl.137/),
  2024.
- [Shitao/MLDR dataset card](https://huggingface.co/datasets/Shitao/MLDR).
- [hakari-bench/NanoMLDR](https://huggingface.co/datasets/hakari-bench/NanoMLDR),
  Nano benchmark dataset.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| M3-Embedding: Multi-Linguality, Multi-Functionality, Multi-Granularity Text Embeddings Through Self-Knowledge Distillation | 2024 | benchmark paper | [https://arxiv.org/abs/2402.03216](https://arxiv.org/abs/2402.03216) |
| M3-Embedding ACL Anthology version | 2024 | paper | [https://aclanthology.org/2024.findings-acl.137/](https://aclanthology.org/2024.findings-acl.137/) |
| MLDR: Multilingual Long-Document Retrieval dataset | 2024 | dataset card | [https://huggingface.co/datasets/Shitao/MLDR](https://huggingface.co/datasets/Shitao/MLDR) |

### Representative Snippets

| Query pattern | Positive document pattern |
| --- | --- |
| An Arabic question about causes in a historical military campaign. | A long article about a crusade or campaign containing the relevant paragraph. |
| A question about Judas and Peter in a religious narrative. | A long article about New Testament views of Jesus' life. |
| A question about symbols for surface features. | A long article about topography and conventional map symbols. |
| A question about casualties in an Indochina war campaign. | A long article about the First Indochina War. |
| A question about the effect of a commander assassination. | A long article about assassination or World War II military history. |
