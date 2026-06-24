# NanoMLDR / hi

## Overview

`NanoMLDR / hi` is the Hindi split of NanoMLDR, a multilingual long-document
retrieval benchmark derived from MLDR. Hindi paragraph-grounded questions
retrieve full Hindi articles, where the answer-bearing passage may be buried
inside a long document. The Nano split has 159 queries, 2,858 documents, and
159 positive qrel rows, with exactly one positive document per query. Current
diagnostics show both BM25 and dense retrieval as weak and nearly tied, while
`reranking_hybrid` is the strongest profile across nDCG@10, hit@10, and
recall@100.

## Details

### What the Original Data Measures

MLDR was introduced with the M3-Embedding work as a multilingual long-document
retrieval benchmark. The dataset card describes sampling long documents,
selecting a paragraph, and generating a specific question from that paragraph.
The full document containing the answer-bearing paragraph is the retrieval
target.

For Hindi, this means the task measures long-document retrieval rather than
short-passage search. A model must connect a Devanagari question to a full
Hindi article whose relevant answer evidence may occupy only a small section.

### Observed Data Profile

The Nano split contains 159 queries, 2,858 documents, and 159 positive qrel
rows. Every query has exactly one positive document. Queries average 79.18
characters, while documents average 11,900.81 characters.

Observed examples include questions about railway-station districts,
constitutional schedules, Hindi font support on mobile devices, kidney tissue,
post-1947 cultural pilgrimage development, banking, biographies, universities,
anatomy, and public figures. The positive documents are long Hindi articles
that contain the answer-bearing paragraph among broad background material.

### BM25 Evaluation Profile

The dataset-provided BM25 candidate subset contains 500 candidates per query and
achieves nDCG@10 = 0.3184, hit@10 = 0.4277, and recall@100 = 0.6604. BM25 is
weak on this split. It can retrieve positives when exact Hindi names,
institutions, legal terms, or technical phrases match, but many questions use
general wording or refer to a paragraph that is not strongly represented by the
article title.

Long Hindi documents also contain many competing terms. Exact lexical overlap
can point to related articles rather than the full article containing the
answer paragraph, especially for constitutional, geographic, medical, or
cultural topics.

### Dense Evaluation Profile

The dense `harrier_oss_v1_270m` candidate subset contains 500 candidates per
query and achieves nDCG@10 = 0.3192, hit@10 = 0.4151, and recall@100 = 0.6604.
Dense retrieval is nearly tied with BM25 by nDCG@10 and recall@100, but slightly
lower by hit@10. This indicates that a single dense representation is also not
enough for Hindi long-document matching here.

The main issue is granularity. A full article embedding must summarize a long
document, while the question may target one paragraph about a schedule, device
support, anatomy detail, or historical development. The relevant local evidence
can be diluted by the rest of the article.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset contains mostly 100 candidates per
query, with 35 queries using a rank-101 safeguard row. It achieves nDCG@10 =
0.3883, hit@10 = 0.5220, and recall@100 = 0.7799. Hybrid retrieval is the best
observed profile, although absolute scores remain modest.

This split shows that Hindi MLDR benefits from combining lexical and semantic
signals, but also that both signals are individually weak. BM25 contributes
exact Devanagari anchors, while dense retrieval contributes broad semantic
matching. The hybrid candidate set retains more positives for reranking than
either method alone.

### Metric Interpretation for Model Researchers

This task is single-positive: each query has exactly one relevant long
document. Hit@10 measures whether that document appears near the top. nDCG@10
is sensitive to the rank of the single positive, and recall@100 measures whether
it remains available for reranking.

The Hindi MLDR profile is difficult for both sparse and dense retrieval. Unlike
Spanish or French MLDR, lexical overlap does not dominate; unlike many short
passage tasks, dense retrieval does not solve the problem either. Researchers
should consider chunk-level indexing, late interaction, and paragraph-aware
document aggregation.

### Query and Relevance Type Tendencies

Queries are Hindi paragraph-grounded questions about locations, constitutional
rules, mobile-device language support, anatomy, culture, biographies,
institutions, and article-specific factual details. Some contain strong entity
names, while others ask with broad descriptive wording.

Relevant documents are long Hindi articles with title context and answer-bearing
paragraphs. The task rewards Devanagari handling, exact entity matching,
paragraph-to-document linking, and robust retrieval when the title is broader
than the question.

### Representative Failure Modes

BM25 can retrieve related Hindi articles with shared legal, geographic,
technical, or cultural terms while missing the positive document. Dense
retrieval can select a broad semantically related article whose overall topic is
close but whose text lacks the answer paragraph. Both methods struggle when the
question refers to a small local detail inside a long article.

Hybrid retrieval improves recall but still leaves many positives outside the top
ranks. A reranker should inspect chunks or paragraphs and not rely only on a
single full-document score.

### Training Data That May Help

Useful training data includes Hindi long-document QA retrieval pairs, Hindi
Wikipedia article retrieval, multilingual MLDR training data outside this Nano
split, and entity-sharing Hindi hard negatives. Training should include long
Hindi documents where relevance is determined by one paragraph.

Synthetic data can help when it samples a paragraph from a long Hindi
encyclopedic article, generates a grounded Hindi question, and uses the full
article as the positive document. Hard negatives should share entities,
professions, institutions, legal terms, or places without containing the answer
paragraph.

### Model Improvement Notes

Dense retrievers should move beyond single-vector full-document encoding for
Hindi MLDR. Sparse systems need better Hindi tokenization, normalization, and
weighting for Devanagari terms, but lexical matching alone is insufficient.
Hybrid and reranking systems should use paragraph-aware evidence signals.

For hybrid systems, `NanoMLDR / hi` is a case where combining BM25 and dense
retrieval helps, but the next improvement requires better long-document
representation rather than simple score fusion.

## Example Data

| Query | Positive document |
| --- | --- |
| मेड़ता रोड रेलवे स्टेशन किस जिले में स्थित है? [46 chars] | नागौर नागौर (Nagaur) भारत के राजस्थान राज्य के नागौर ज़िले में स्थित एक ऐतिहासिक नगर है। अपने धार्मिक स्थलों के लिए प्रसिद्ध यह शहर ज़िले का मुख्यालय भी है। परिचय नागौर जिला 26°25' और 27°40' उत्तरी अक्षांश और 73°10' और 75°15' पूर्वी देशांतर के बीच स्थित है। यह सात जिलों बीकानेर , चुरू , सीकर , जयपुर, अजमेर, पाली, जोधपुर के बीच स्थित है । नागौर राजस्थान का पाँचवाँ सबसे बड़ा जिला है, जिसका विशाल भूभाग १७,७१८ वर्ग किलोमीटर में फैला है। इसका भौगोलिक विस्तार मैदान, पहाड़ियों, रेत के टीलों का एक अच्छा संयोजन है और इस तरह यह महान भारतीय थार रेगिस्तान का एक हिस्सा है। नागौर का वर्तमान जिला राजस्थान राज्य के केंद्र में एक स्थान पाता है। यदि हम राजस्थान के मानचित्र पर एक क्रॉस बनाते हैं तो इस क्रॉस का केंद्र नागौर जिले में पड़ता है। राज्यों के विलय से पहले, नागौर तत्कालीन जोधपुर राज्य का हिस्सा था। स्वतंत्रता के बाद, नागौर को देश में उस स्थान के रूप में चुने जाने का सम्मान मिला, जहां से 2 अक्टूबर 1959 को भारत के पहले प्रधानमंत्री स्वर्गीय श्री जवाहरलाल नेहरू द्वारा लोकतांत्रिक विकेंद्रीकरण प्रक्... [1,000 / 20,341 chars] |
| यदि विधान परिषद् है तो, उसके सभापति और उपसभापति के वेतन और भत्ते क्या हैं? [74 chars] | सातवीं अनुसूची भारत के संविधान में राज्य सरकारों और केन्द्र सरकार के मध्य मुद्दों अथवा अधिकारों के बंटवारे के लिए विभिन्न अनुसूचियाँ परिभाषित की गयी हैं। इनमें से महत्त्वपूर्ण अनुच्छेद २४५ और २४६ के अन्तर्गत आते हैं। भारतीय संविधान की सातवीं अनुसूची राज्यों और संघ के मध्य के अधिकारों को उल्लिखित करती है। इसमें तीन सूचियाँ हैं: 1) संघ सूची, 2) राज्य सूची और 3) समवर्ती सूची। संघ सूची (अनुच्छेद 246) भारत की और उसके प्रत्येक भाग की रक्षा, जिसके अंतर्गत रक्षा के लिए तैयारी और ऐसे सभी कार्य हैं, जो युद्ध के समय युद्ध के संचालन और उसकी समाप्ति के पश्चात्‌ प्रभावी सैन्यवियोजन में सहायक हों। नौसेना, सेना और वायुसेना; संघ के अन्य सशस्त्र बल। क. संघ के किसी सशस्त्र बल या संघ के नियंत्रण के अधीन किसी अन्य बल का या उसकी किसी टुकड़ी या यूनिट का किसी राज्य में सिविल शक्ति की सहायता में अभिनियोजन; ऐसे अभिनियोजन के समय ऐसे बलों के सदस्यों की शक्तियाँ, अधिकारिता, विशेषाधिकार और दायित्व।) छावनी क्षेत्रों का परिसीमन, ऐसे क्षेत्रों में स्थानीय स्वशासन, ऐसे क्षेत्रों के भीतर छावनी प्राधिकारियों का गठन और उन... [1,000 / 23,699 chars] |
| आपके फोन में हिन्दी फॉण्ट उपलब्ध है क्या? [41 chars] | मोबाइल उपकरणों में हिन्दी समर्थन मोबाइल फोन आजकल हर व्यक्ति की आवश्यकता बन चुका है। इण्टरनेट पर हिन्दी के प्रयोक्ता ऐसा फोन चाहते हैं जिससे कि वे अपने फोन पर भी हिन्दी का प्रयोग कर सकें जिसमें कि हिन्दी साइटों की सर्फिंग, ईमेल, गपशप, ब्लॉगिंग, ट्विटिंग आदि शामिल हैं। अब प्रश्न उठता है कि मोबाइल फोन में हिन्दी का समर्थन किस रूप में है। मोबाइल में हिन्दी समर्थन के मुख्य रूप से तीन पहलू हैं। हिन्दी टैक्स्ट डिस्पले हिन्दी टैक्स्ट इनपुट हिन्दी भाषा इण्टरफेस हिन्दी पाठ्य प्रदर्शन मोबाइल पर हिन्दी पाठ्य अथवा टैक्स्ट का प्रदर्शन हो सकता है या नहीं? यदि फोन में हिन्दी दिख ही नहीं सकती तो इनपुट तो होगा ही नहीं, हिन्दी समर्थन की यह पहली शर्त है। कुछ फोनों में हिन्दी प्रदर्शन का पूर्ण समर्थन होता है। कुछ में आंशिक यूनिकोड समर्थन होने से हिन्दी दिखाई तो देती है लेकिन सही रूप से नहीं यानी मात्राएँ एवं संयुक्ताक्षर सही रूप से प्रकट नहीं होते और हिन्दी बिखरी हुई सी दिखाई देती है। इसका कारण है कि फोन में हिन्दी फॉण्ट तो होता है परन्तु फोन का कॉम्पलैक्स स्क्रिप्ट लेआउट इंजन हिन्दी का समर्थन नहीं करता अर... [1,000 / 18,819 chars] |

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
| A Hindi question asking which district a railway station is in. | A long article about Nagaur or a related location. |
| A constitutional question about salary and allowances. | A long article about the Seventh Schedule or constitutional provisions. |
| A question about Hindi font availability on phones. | A long article about Hindi support on mobile devices. |
| A question asking for more information about kidney tissue. | A long article about the kidney. |
| A question about cultural pilgrimage development after 1947. | A long article about Mathura or cultural pilgrimage context. |
