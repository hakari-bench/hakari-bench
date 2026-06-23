# NanoRTEB / NanoChatDoctor

## Overview

`NanoChatDoctor` is an English medical dialogue retrieval task from NanoRTEB. The query is a patient-style medical question or symptom description, and the relevant document is the corresponding doctor-style response from the ChatDoctor HealthCareMagic data. Each query has one positive response. The task tests retrieval under noisy consumer health language, long symptom descriptions, and paraphrase between patient wording and clinical advice. Dense retrieval has the best nDCG@10 and hit@10, while `reranking_hybrid` has the best recall@100.

## Details

### What the Original Data Measures

ChatDoctor introduced a medical chat model fine-tuned with domain knowledge and patient-doctor dialogues from an online consultation platform. The underlying data contains patient inputs and doctor-style outputs.

RTEB uses this resource as retrieval rather than advice generation. The benchmark asks whether a model can match a patient question to the response paired with it in the dataset. This is a retrieval benchmark and should not be interpreted as validating medical advice quality.

### Observed Data Profile

The Nano split contains 200 queries, 5,545 documents, and 200 positive qrel rows. Every query has exactly one positive. Queries average 441.09 characters, while response documents average 605.12 characters.

Example queries include cancer treatment history, missed birth control pills with pregnancy concern, pain management in thymic cancer, darkened epiglottis tissue with ear pain, and sperm count interpretation. The source language is often informal and can include misspellings, incomplete formatting, and mixed symptom history.

### BM25 Evaluation Profile

The BM25 candidate subset uses top-500 candidates and reaches nDCG@10 of 0.2952, hit@10 of 0.4050, and recall@100 of 0.6600. BM25 is moderately useful when patient symptoms, medications, or diagnoses are repeated in the response.

Its limitation is vocabulary mismatch. Patient descriptions often use lay phrasing, typos, and long context, while responses may use clinical terminology, general reassurance, or advice language. Many questions also share common symptom words, which weakens term-frequency ranking.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses top-500 candidates and reaches nDCG@10 of 0.5533, hit@10 of 0.6550, and recall@100 of 0.8150. Dense retrieval is the strongest top-rank profile.

This indicates that embedding similarity handles patient-to-response paraphrase better than lexical matching. It can connect symptoms, medical history, and likely advice even when the response uses different wording.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates, with 34 rows receiving the optional rank-101 safeguard. It reaches nDCG@10 of 0.4671, hit@10 of 0.6200, and recall@100 of 0.8300. Hybrid retrieval has slightly better recall@100 than dense retrieval but weaker early ranking.

This suggests that sparse signals help recover some responses containing exact symptoms or medications, while dense retrieval orders the best matches more effectively. A reranker can benefit from the hybrid candidate pool if it can handle noisy patient language.

### Metric Interpretation for Model Researchers

With one positive per query, nDCG@10 measures how early the paired response appears, hit@10 measures whether it appears in the first ten candidates, and recall@100 measures whether a reranker can access it.

For `NanoChatDoctor`, dense top-rank quality is important, but recall@100 also matters because medical dialogue matching often has many superficially similar responses. The benchmark evaluates dataset-pair retrieval, not clinical correctness.

### Query and Relevance Type Tendencies

Queries are patient-written medical descriptions with symptoms, history, medications, demographics, and concern statements. Relevant documents are doctor-style responses that may include explanation, triage suggestions, or general recommendations.

Relevance is the original paired response. A medically plausible answer can still be non-relevant if it is not the paired document for the query.

### Representative Failure Modes

Common failures include retrieving responses for similar symptoms but different patient histories, overmatching diagnosis names, missing misspelled or lay terms, and ranking generic medical advice above the paired response. BM25 is sensitive to repeated symptom tokens; dense retrieval can confuse common consultation patterns.

### Training Data That May Help

Useful training data includes medical QA retrieval, patient-forum question-to-answer ranking, clinical synonym expansion, and hard negatives from similar symptoms with different diagnoses or advice. Evaluation patient questions, responses, and qrels should be excluded.

### Model Improvement Notes

Models should learn robust patient-language normalization while preserving clinically important details such as duration, medication, age, and prior diagnosis. Hard negatives should share symptoms or drugs but differ in context or advice. Dense retrieval is the best first-stage ranker, while hybrid retrieval is useful for recall-oriented reranking pools.

## Example Data

| Query | Positive document |
| --- | --- |
| My wife that is 31yrs old had a major operation 6mos ago. She had thymic cancer with 3 large malignant thymomas pressed against her right lung her heart and her liver ..they removed her right lung and removed then reconstructed part of her pericardium (lining of her heart) and the tumor on her liver was completely encapsulated so they didn t take a slice of her liver like he though he would have to . Dr. Calhoun of uc davis who is a straight up stud removed 100% of the tumors it looks like so fa... [500 / 1,183 chars] | Thanks for the query from the history it is quite evident your wife had shad a very tough time but from the diagnosis of malignant Thomas I have to tell you that it means the liver has got metastasis from the Thomas that is what they mean by the dark spots in the liver, and mostly they want to resect it now I would suggest you talk to the oncologist who's in charge of the case for a clear-cut explanation take care. [418 chars] |
| Okay so the past two months I have missed my first birth control pill, I finally got back on track this month and I am 10 days into the packet. I had intercourse last tuesday and have been feeling more than off. Nausea, fatigue, headaches, slightly sore breasts, cramping, a bittle bit of being emotional, dehydrated. Just all out deeling horrible. Ive taken pregnancy tests but I feel it could be too soon. And would I be feeling these pregnancy symptoms so soon after? Also, could it just be that I... [500 / 534 chars] | Hello, Thanks for writing to us. Irregular intake of birth control pill & unprotected sex close to your fertile period or ovulation day (occurs 14 days prior to due date) are quite risky for being pregnant. In this case, I suggest you to undergo one home pregnancy test if you miss your next period. Above clinical features are quite relevant with possible pregnancy. Common symptoms of pregnancy [396 chars] |
| Hi iI have been diagnoed with thymic cancer, I do not like to take the drugs for pain that are prescribed,as they have side effects that are harsh.So instead i have been taking ibuprophen .for abot 4 months ,as dosage recommended, I have beenexperiencing respitory issues lately and wonder if this is the cause.I have been doing radiation and chemo treaments ,it has shown improvement in all aspects except for my breathing .I read an article on cleveland clinic facebook this mourning that said this... [500 / 728 chars] | Thy mic cancer causes respiratory distress. After a thy mic tumor is found and tests have been done to get a sense of its Factors important in choosing a treatment include the type and stage of the cancer, whether it is respectable (able to be completely removed with surgery), and whether you have any other serious medical problems. Because thy mic cancer is rare, it is often hard to accurately predict the effectiveness of treatment strategies, and in many cases the best way to treat this cancer is still not preselecting a treatment plan is an important decision, and you should take the time to think about all of your choices. The main treatments for thymus cancer are [676 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| ChatDoctor: A Medical Chat Model Fine-Tuned on a Large Language Model Meta-AI (LLaMA) Using Medical Domain Knowledge | 2023 | task paper | [https://arxiv.org/abs/2303.14070](https://arxiv.org/abs/2303.14070) |
| lavita/ChatDoctor-HealthCareMagic-100k | 2023 | dataset card | [https://huggingface.co/datasets/lavita/ChatDoctor-HealthCareMagic-100k](https://huggingface.co/datasets/lavita/ChatDoctor-HealthCareMagic-100k) |
| Introducing RTEB: A New Standard for Retrieval Evaluation | 2025 | benchmark article | [https://huggingface.co/blog/rteb](https://huggingface.co/blog/rteb) |

### Representative Snippets

| Query | Relevant document excerpt |
| --- | --- |
| A patient describes a spouse with thymic cancer, lung removal, and concern about liver involvement. | The response discusses metastasis concern and advises oncology follow-up. |
| A patient missed birth control pills and reports nausea and fatigue after intercourse. | The response discusses pregnancy risk and suggests testing or consultation. |
| A patient with thymic cancer asks about using ibuprofen instead of prescribed pain medication. | The response discusses thymic cancer symptoms and treatment considerations. |
| A patient reports darkened epiglottis tissue, ear pain, appetite increase, and weight gain. | The response asks about endoscopic findings and differentiates throat symptoms. |
| A patient asks about semen analysis after a spouse's laparoscopic surgery. | The response interprets semen volume, viscosity, pH, and sperm count ranges. |
