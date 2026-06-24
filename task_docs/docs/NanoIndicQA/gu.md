# NanoIndicQA / gu

## Overview

`NanoIndicQA / gu` is the Gujarati split of IndicQA retrieval. The queries are Gujarati reading-comprehension questions, and the documents are Gujarati evidence paragraphs from a small context corpus.

This task evaluates whether a model can retrieve the Gujarati paragraph that supports a question. The relevant unit is the full context paragraph, not a short extracted answer.

## Details

### What the Original Data Measures

IndicQA is part of IndicXTREME, introduced in "Towards Leaving No Indic Language Behind". It was designed as a manually curated cloze-style reading-comprehension benchmark for Indic languages.

The retrieval version pairs each question with its source context paragraph. In the Gujarati split, the benchmark tests Gujarati paragraph selection over history, geography, cultural, and encyclopedic content.

### Observed Data Profile

This Nano split contains 200 queries, 248 documents, and 201 positive qrels. Queries have 1.005 positives on average, with a minimum of 1, a median of 1.0, and a maximum of 2. Only one query has two positives. Queries average 61.01 characters, and documents average 960.50 characters.

Observed examples ask about monsoon timing in Delhi, Ahmedabad as the "Manchester of the East", Akbar's imperial ambitions, the full name of BEIC, and mountain ranges between Kutch and Sindh. Documents are Gujarati paragraphs about cities, history, rulers, geography, and institutions.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.6060, hit@10 of 0.6900, and recall@100 of 0.9055. The candidate pool contains the full 248-document corpus. BM25 works when questions repeat distinctive Gujarati names, places, dates, or terms from the context.

BM25 is weaker when the correct paragraph is identified by context rather than repeated words. Historical and geographic paragraphs can share names and related vocabulary, which makes exact term matching insufficient.

### Dense Evaluation Profile

The dense harrier-oss-270m profile reaches nDCG@10 of 0.7487, hit@10 of 0.8600, and recall@100 of 0.9652. Dense retrieval is the strongest direct ranking profile.

This suggests that semantic paragraph matching helps substantially for Gujarati IndicQA. Dense retrieval can connect a question to the right context even when the question does not repeat the same phrase as the evidence sentence.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate subset reaches nDCG@10 of 0.7207, hit@10 of 0.8300, and recall@100 of 0.9701. It uses 100 candidates per query, with six rank-101 safeguard positives.

Hybrid retrieval has the best recall@100 but trails dense retrieval on top-10 ranking. It is therefore useful as a reranking pool, while dense retrieval is the stronger direct ranker for this split.

### Metric Interpretation for Model Researchers

`NanoIndicQA / gu` is a small-corpus Gujarati context retrieval task with mostly one positive per query. nDCG@10 and hit@10 directly reflect whether the correct context appears near the top.

The profile is dense-favored. BM25 provides a useful lexical baseline, but dense retrieval improves ranking substantially. Hybrid retrieval gives slightly better candidate coverage, which can help downstream rerankers.

### Query and Relevance Type Tendencies

Queries are Gujarati factual or cloze-style questions. Documents are paragraph-length contexts, often about Indian cities, rulers, historical institutions, geography, and cultural facts.

The relevance relation is paragraph evidence support. A positive paragraph contains the information needed to answer the question.

### Representative Failure Modes

BM25 may retrieve a paragraph about the same city, ruler, or region but not the specific fact requested. Dense retrieval may confuse semantically similar historical or geographic contexts. Hybrid retrieval reduces candidate misses but still needs exact evidence discrimination.

The small corpus can make recall look high, but ranking the exact context in the top 10 remains the meaningful challenge.

### Training Data That May Help

Useful training data includes Gujarati context QA, Gujarati Wikipedia retrieval, IndicQA-style multilingual pairs, and hard negatives about nearby people, places, historical periods, or geographic regions.

Training should exclude this split's questions and positive context paragraphs.

### Model Improvement Notes

Improving this task requires Gujarati semantic coverage and evidence-aware ranking. Models should preserve named entities, dates, locations, and factual relations while handling question paraphrases.

For reranking, the key behavior is checking whether the paragraph actually contains the answer evidence, not just whether it shares the topic.

## Example Data

| Query | Positive document |
| --- | --- |
| દિલ્હીમાં ચોમાસાના પવનો આવવાની તારીખ કઈ છે? [43 chars] | )થી 48 °C (118 °F) જેટલાં રહે છે. તેનું વાર્ષિક સરેરાશ તાપમાન 25° સે. (77° ફે. ) છે; તેનું માસિક સરેરાશ તાપમાન 13°સે. થી 32°સે. (56° ફે. થી 90° ફે. [147 chars] |
| ક્યાં શહેરને "માન્ચેસ્ટર ઓફ ધ ઇસ્ટ" તરીકે પણ ઓળખવામાં આવતું હતું? [65 chars] | અંગ્રજોના શાસનકાળ દરમિયાન અમદાવાદ એક મુખ્ય નગર બની ગયું. અહીં તેમણે કોર્ટ, નગરપાલિકા વગેરે સ્થાપ્યાં. કાપડની મિલોને કારણે અમદાવાદ 'પૂર્વનું માંચેસ્ટર' પણ કહેવાતું હતું. મે ૧૯૬૦થી નવા બનેલા ગુજરાત રાજ્યનું પાટનગર બન્યુ. ગાંધીનગર નવું પાટનગર બનવા છતાં અમદાવાદની મહત્તા એવી જ રહી છે. ૧૯૭૪માં એલ. ડી. કોલેજ ઓફ એન્જિનિયરિંગના છાત્રાલયના ભોજનાલયમાં દરમાં ૨૦%નો વધારો થતા તેનો વિરોધ શરૂ થયો, જે નવનિર્માણ આંદોલનમાં પરિણમ્યો અને ભારતના ઈતિહાસમાં સૌપ્રથમ (અને માત્ર એકવાર) ચૂંટાયેલા મુખ્યમંત્રી - ચીમનભાઈ પટેલે આંદોલનને કારણે રાજીનામું આપવું પડ્યું. [540 chars] |
| અન્ય મધ્યયુગીન શાસકોની જેમ કોણ એક મહાન સામ્રાજ્યવાદી હતા? [57 chars] | અન્ય મધ્યયુગીન શાસકોની જેમ અકબર પણ એક મહાન સામ્રાજ્યવાદી હતો. અને તેને પોતાનુ રાજ્ય ઉત્તરે અફઘાનિસ્તાન કાશ્મીરની દક્ષિણે મૈસુર સુધી તથા પશ્ચિમે ગુજરાતની પુર્વમાં બંગાળ સુધી ફેલાવવાની મહત્વાકાંક્ષા હતી. આ આશયથી અકબરે ૧૫૬૨ થી ૧૬૦૫ સુધીમાં અનેક લડાઈઓ કરી અને તેમા મોટાભાગની જીતો મેળવીને ભારતભરમા પોતાના સમ્રાજ્યનો વિસ્તાર કર્યો તથા ભારતને એકતા પણ આપી. અકબરનાં મોટાભાગના યુદ્ધો ખુબજ ઝડપી તથા આક્રમક હોવા છતા મટાભાગે ઉદારતાનો અંશ હતો. અકબરે ૧૫૬૨ થી ૧૬૦૧ સુધીમા અનુક્રમે માળવા, જબલપુર પાસેનુ ગોંદવાના, રણથંભેર, કાલિંજર, ચિતોડ (મેવાડ), જોધપુર, ગુજરાત, બંગાળ, કાબુલ, કાશ્મિર, સિંઘ, કટ્દહાર, અહમદનગર જીતી લીધા ગોંડવાનામાં વીર નારાયણે મુઘલોને સખત લડાઈ આપીને શહીદી વહોરી. અકબરે ફક્ત૯ દિવસમાં ૯૬૫ કિ. મી. ની મજલ કાપીને ગુજરાતના અંતિમ સુલતાન મુઝફ્ફ્રશાહ ત્રીજાને આખરી પરાજય આપીને ગુજરાતને મુઘલ સામ્રાજ્યમાં સમાવી લીધું. આનાથી મુઘલ સમ્રાજ્યને બંદરનો લાભ મળતા તેના વ્યાપાર-વાણિજ્યનો વિકાસ થયો. સ 1567માં ચિતૌડગઢ પર હુમલો કરીંને ચિતૌડ જીતી લીધું આં યુદ્ધ માં અકબરે 30,000 જેટલા નિર્દોષ ચિત્તોડ વાસીઓ નો વધ કરવી તેની... [1,000 / 1,639 chars] |

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
| A Gujarati question asking when monsoon winds arrive in Delhi. | A climate paragraph giving temperature ranges and seasonal context. |
| A question asking which city was known as the "Manchester of the East". | A paragraph about Ahmedabad under British rule, textile mills, and state capital history. |
| A question asking who was a great imperialist like other medieval rulers. | A paragraph about Akbar's ambitions and territorial expansion. |
| A question asking for the full name of BEIC. | A paragraph about Mughal decline and later political or institutional context. |
| A question asking which mountain range lies between Kutch and Sindh. | A geography paragraph about Aravalli branches, Sahyadri ranges, forests, and rainfall areas. |
