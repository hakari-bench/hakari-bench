# NanoIndicQA / hi

## Overview

`NanoIndicQA / hi` is the Hindi split of IndicQA retrieval. The queries are Hindi reading-comprehension questions, and the documents are Hindi context paragraphs that support the answer.

This task evaluates Hindi evidence paragraph retrieval. The model must rank the context paragraph that contains the answer evidence, often among long biographical, historical, or political paragraphs with overlapping vocabulary.

## Details

### What the Original Data Measures

IndicQA is part of IndicXTREME, introduced in "Towards Leaving No Indic Language Behind". It is a manually curated cloze-style reading-comprehension task across Indic languages.

In the MTEB retrieval formulation, the question is the query and the source context paragraph is the document. The Hindi split tests context retrieval for Hindi QA rather than answer extraction.

### Observed Data Profile

This Nano split contains 200 queries, 261 documents, and 201 positive qrels. Queries have 1.005 positives on average, with a minimum of 1, a median of 1.0, and a maximum of 2. One query is multi-positive. Queries average 56.91 characters, and documents average 2,550.77 characters.

Observed examples ask about Art Deco buildings, the caste background of the Nanda dynasty, a temple construction in Bengal without Akbar's permission, Akbar's reign, and the renaming of Prayagraj to Allahabad. Several sampled questions target long biography or historical passages.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.4545, hit@10 of 0.6400, and recall@100 of 0.8856. The candidate pool contains the full 261-document corpus. BM25 is weaker here than in several other IndicQA splits.

The weakness comes from long Hindi paragraphs that share broad political, historical, and biographical vocabulary. Exact term matching may retrieve a paragraph about Akbar, Mughal history, or architecture without selecting the exact context needed for the question.

### Dense Evaluation Profile

The dense harrier-oss-270m profile reaches nDCG@10 of 0.6511, hit@10 of 0.7900, and recall@100 of 0.8557. Dense retrieval is the strongest direct ranking profile.

Dense retrieval improves top-10 ranking substantially, suggesting that semantic question-context matching helps with long Hindi paragraphs. Its recall@100 is lower than BM25, so it is better at ranking the top results than at broad candidate coverage.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate subset reaches nDCG@10 of 0.5738, hit@10 of 0.7300, and recall@100 of 0.9652. It uses 100 candidates per query, with seven rank-101 safeguard positives.

Hybrid retrieval gives the best recall@100 but does not match dense retrieval on top-10 ranking. It is therefore valuable as a reranking pool, while dense retrieval is the stronger first-stage ranker.

### Metric Interpretation for Model Researchers

`NanoIndicQA / hi` is a Hindi small-corpus context retrieval task where dense and hybrid profiles serve different roles. Dense retrieval is better for immediate top-10 quality, while hybrid retrieval is better for candidate coverage.

Since almost every query has one positive, nDCG@10 and hit@10 are direct measures of correct-context placement. Recall@100 diagnoses whether the candidate generator supplies the positive to a downstream reranker.

### Query and Relevance Type Tendencies

Queries are Hindi factual or cloze-style questions. Documents are long Hindi context paragraphs, often about Indian history, rulers, architecture, cities, religion, and political events.

The relevance relation is evidence support. The positive paragraph contains the fact or explanation needed to answer the query.

### Representative Failure Modes

BM25 may retrieve a paragraph with the same named entity but the wrong event or date. Dense retrieval may select a semantically similar biography or historical passage without the exact evidence. Hybrid retrieval improves recall but still requires reranking for precise support.

Long paragraphs can dilute the answer signal because many unrelated facts appear in one context.

### Training Data That May Help

Useful training data includes Hindi extractive QA, Hindi Wikipedia passage retrieval, multilingual IndicQA context retrieval, and hard negatives from the same biography, region, dynasty, or political topic.

Training should exclude this split's questions and positive context paragraphs.

### Model Improvement Notes

Improving this task requires Hindi language coverage, long-context handling, and evidence-sensitive ranking. Models should preserve named entities, dates, places, and relation cues while handling paraphrased questions.

For reranking, the model should verify that the paragraph contains the requested answer evidence rather than simply matching a broad historical topic.

## Example Data

| Query | Positive document |
| --- | --- |
| आर्ट डेको शैली की इमारतें दुनिया में सबसे अधिक कहाँ हैं ? [57 chars] | इनके वास्तु घटकों में यूरोपीय प्रभाव साफ दिखाई देता है, जैसे जर्मन गेबल, डच शैली की छतें, स्विस शैली में काष्ठ कला, रोमन मेहराब साथ ही परंपरागत भारतीय घटक भी दिखते हैं। कुछ इंडो सेरेनिक शैली की इमारतें भी हैं, जैसे गेटवे ऑफ इंडिया। आर्ट डेको शैली के निर्माण मैरीन ड्राइव और ओवल मैदान के किनारे दिखाई देते हैं। मुंबई में मायामी के बाद विश्व में सबसे अधिक आर्ट डेको शैली की इमारतें मिलती हैं। नये उपनगरीय क्षेत्रों में आधुनिक इमारतें अधिक दिखती हैं। मुंबई में अब तक भारत में सबसे अधिक गगनचुम्बी इमारतें हैं। इनमें ९५६ बनी हुई हैं और २७२ निर्माणाधीन हैं। (२००९ के अनुसार) १९९५ में स्थापित, मुंबई धरोहर संरक्षण समिति (एम.एच.सी.सी) शहर में स्थित धरोहर स्थलों के संरक्षण का ध्यान रखती है। मुंबई में दो यूनेस्को विश्व धरोहर स्थल हैं – छत्रपति शिवाजी टर्मिनस और एलीफेंटा की गुफाएं शहर के प्रसिद्ध पर्यटन स्थलों में नरीमन पाइंट, गिरगांव चौपाटी, जुहू बीच और मैरीन ड्राइव आते हैं। एसेल वर्ल्ड यहां का थीम पार्क है, जो गोरई बीच के निकट स्थित है। यहीं एशिया का सबसे बड़ा थीम वाटर पार्क, वॉटर किंगडम भी है। मुंबई क... [1,000 / 2,032 chars] |
| नंदवंश के राजा किस वर्ण से संबंधित थे? [38 chars] | इतिहास की जानकारी के अनेक विवरण पुराणों, जैन और बौद्ध ग्रंथों एवं यूनानी इतिहासकारों के वर्णन में प्राप्त होते हैं। तथापि इतना निश्चित रूप से कहा जा सकता है कि नंद एक राजवंश था जिसकी अधिकांश प्रकृतियाँ भारतीय शासन परंपरा की थी। कर्टियस कहता है कि सिकंदर के समय शाषक का पिता वास्तव में एक गरीब नाई का बेटा था, यूनानी लेखकों के वर्णनों से ज्ञात होता है कि वह "वर्तमान राजा" अग्रमस् अथवा जंड्रमस् (चंद्रमस ? ) था, जिसकी पहचान धनानंद से की गई है। उसका पिता महापद्मनंद था, जो कर्टियस के उपयुक्त कथन से क्षत्रिय वर्ण का ठहरता है। कुछ पुराण ग्रंथ और जैन ग्रंथ "परिशिष्ट पर्वन् में भी उसे नाई का पुत्र कहा गया है। इन अनेक संदर्भों से केवल एक बात स्पष्ट होती है कि नंदवंश के राजा न्यायी क्षत्रिय वर्ण के थे। नंदवंश का प्रथम और सर्वप्रसिद्ध राजा हुआ। पुराणग्रंथ उसकी गिनती शैशुनागवंश में ही करते हैं, किंतु बौद्ध और जैन अनुत्रुटियों में उसे एक नए वंश (नंदवंश) का प्रारंभकर्ता माना गया है, जो सही है। उसे जैन ग्रंथों में उग्रसेन (अग्रसेन) और पुराणों में महापद्मपति भी कहा गया है। पुराणों के कलियुगराजवृत्तांतवले... [1,000 / 2,643 chars] |
| अकबर की अनुमति के बिना बंगाल में मंदिर का निर्माण किसने शुरू किया था ? [70 chars] | अकबर के हिन्दू सामंत उसकी अनुमति के बगैर मंदिर निर्माण तक नहीं करा सकते थे। बंगाल में राजा मानसिंह ने एक मंदिर का निर्माण बिना अनुमति के आरंभ किया, तो अकबर ने पता चलने पर उसे रुकवा दिया और १५९५ में उसे मस्जिद में बदलने के आदेश दिए। अकबर के लिए आक्रोश की हद एक घटना से पता चलती है। हिन्दू किसानों के एक नेता राजा राम ने अकबर के मकबरे, सिकंदरा, आगरा को लूटने का प्रयास किया, जिसे स्थानीय फ़ौजदार, मीर अबुल फजल ने असफल कर दिया। इसके कुछ ही समय बाद १६८८ में राजा राम सिकंदरा में दोबारा प्रकट हुआ और शाइस्ता खां के आने में विलंब का फायदा उठाते हुए, उसने मकबरे पर दोबारा सेंध लगाई और बहुत से बहुमूल्य सामान, जैसे सोने, चाँदी, बहुमूल्य कालीन, चिराग, इत्यादि लूट लिए, तथा जो ले जा नहीं सका, उन्हें बर्बाद कर गया। राजा राम और उसके आदमियों ने अकबर की अस्थियों को खोद कर निकाल लिया एवं जला कर भस्म कर दिया, जो कि मुस्लिमों के लिए घोर अपमान का विषय था। बाद के वर्षों में अकबर को अन्य धर्मों के प्रति भी आकर्षण हुआ। अकबर का हिंदू धर्म के प्रति लगाव केवल मुग़ल साम्राज्य को ठोस बनाने के ही लिए नही था वरन उसकी हिंद... [1,000 / 3,441 chars] |

### Source Reference Table

| Source | Role |
| --- | --- |
| [Towards Leaving No Indic Language Behind](https://arxiv.org/abs/2212.05409) | IndicXTREME and IndicQA benchmark paper. |
| [mteb/IndicQARetrieval](https://huggingface.co/datasets/mteb/IndicQARetrieval) | MTEB retrieval task dataset card. |
| [ai4bharat/IndicQA](https://huggingface.co/datasets/ai4bharat/IndicQA) | Upstream IndicQA dataset card. |
| [hakari-bench/NanoIndicQA](https://huggingface.co/datasets/hakari-bench/NanoIndicQA) | Nano benchmark dataset containing this split. |

### Representative Snippets

| Query Pattern | Positive Document Pattern |
| --- | --- |
| A Hindi question asking where Art Deco buildings are most numerous. | A paragraph about architectural influences, European forms, and Mumbai-style built heritage. |
| A question asking which varna the Nanda dynasty kings belonged to. | A historical paragraph drawing on Puranic, Jain, Buddhist, and Greek accounts of the Nandas. |
| A question asking who began building a temple in Bengal without Akbar's permission. | A paragraph about Akbar's religious policy and Raja Man Singh's temple construction. |
| A question asking who ruled Delhi from 1542 to 1605. | A long paragraph about Akbar, his religious interests, and rule. |
| A question asking in which year Prayagraj was named Allahabad. | A paragraph about Akbar and historical naming context. |
