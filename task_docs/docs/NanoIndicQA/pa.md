# NanoIndicQA / pa

## Overview

`NanoIndicQA / pa` is the Punjabi split of IndicQA retrieval. The queries are Punjabi reading-comprehension questions, and the documents are Punjabi evidence paragraphs.

This task evaluates Punjabi paragraph retrieval for QA. The model must identify the context paragraph that supports the answer, often when several passages share names, actors, films, historical events, or political terms.

## Details

### What the Original Data Measures

IndicQA is part of IndicXTREME from "Towards Leaving No Indic Language Behind". It is a cloze-style reading-comprehension task that MTEB repurposes as question-to-context retrieval.

In the Punjabi split, each query is a Punjabi question and the positive document is the source paragraph containing the answer evidence.

### Observed Data Profile

This Nano split contains 200 queries, 241 documents, and 200 positive qrels. Each query has exactly one positive. Queries average 63.51 characters, and documents average 1,423.51 characters.

Observed examples ask about Kashmiri Pandits leaving the valley, participation in a named world program tour, Bhagat Singh and a bomb inspired by Auguste Vaillant, Priyanka Chopra's 2006 Farhan Akhtar action thriller, and Shah Rukh Khan's collaboration in a musical romance. Documents are Punjabi paragraphs about politics, cinema, biography, and history.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.5983, hit@10 of 0.7600, and recall@100 of 0.9250. The candidate pool contains the full 241-document corpus. BM25 is strong when questions repeat distinctive names, film titles, places, or historical terms.

BM25 can still fail when several passages share the same celebrity, event, or political topic. It may retrieve the right broad subject without selecting the exact paragraph that contains the answer.

### Dense Evaluation Profile

The dense harrier-oss-270m profile reaches nDCG@10 of 0.6445, hit@10 of 0.8550, and recall@100 of 0.9800. Dense retrieval improves top-10 hit and recall over BM25.

This suggests that semantic matching helps connect Punjabi questions to supporting contexts beyond repeated words. Dense retrieval is useful when the answer relation is expressed indirectly in the paragraph.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate subset reaches nDCG@10 of 0.6885, hit@10 of 0.8750, and recall@100 of 0.9800. It uses 100 candidates per query, with four rank-101 safeguard positives.

Hybrid retrieval is the strongest profile in this split. It combines lexical anchors from names and titles with semantic question-context matching, improving top-10 ranking while preserving dense-level recall.

### Metric Interpretation for Model Researchers

`NanoIndicQA / pa` is a Punjabi context retrieval task where hybrid search is best. BM25 is a strong baseline, dense retrieval improves semantic matching, and reranking_hybrid gives the best top-10 ordering.

Since each query has one positive, nDCG@10 and hit@10 directly measure correct-context placement. Recall@100 is high for dense and hybrid, so reranking can focus on choosing the exact evidence paragraph.

### Query and Relevance Type Tendencies

Queries are Punjabi factual or cloze-style questions. Documents are paragraph-length contexts about politics, film, biography, history, and social events.

The relevance relation is evidence support: the positive paragraph contains the information needed to answer the query.

### Representative Failure Modes

BM25 may retrieve a paragraph with the same actor, film, or historical figure but not the requested fact. Dense retrieval may confuse related celebrity or history contexts. Hybrid retrieval reduces these failures but still needs answer-evidence discrimination.

Questions tied to film and actor biographies can be especially difficult because many paragraphs share names, years, and titles.

### Training Data That May Help

Useful training data includes Punjabi QA context retrieval, Punjabi Wikipedia passage retrieval, cross-lingual Indic QA training, and hard negatives from similar entertainment, history, and biography contexts.

Training should exclude this split's questions and positive context paragraphs.

### Model Improvement Notes

Improving this task requires Punjabi language coverage, entity-sensitive matching, and paragraph-level evidence ranking. Models should preserve names, film titles, years, and relation cues while handling question paraphrases.

For reranking, the model should check whether the paragraph contains the answer evidence rather than merely matching the named entity.

## Example Data

| Query | Positive document |
| --- | --- |
| ਬਹੁਤ ਸਾਰੇ ਲੇਖਕਾਂ ਅਨੁਸਾਰ, ਇਸ ਦਹਾਕੇ ਵਿੱਚ 140,000 ਕਸ਼ਮੀਰੀ ਪੰਡਿਤਾਂ ਵਿੱਚੋਂ ਲਗਭਗ ਕਿੰਨੇ ਘਾਟੀ ਛੱਡ ਗਏ ਸਨ ? [97 chars] | 1901 ਦੀ ਇਸੇ ਜਨਗਣਨਾ ਅਨੁਸਾਰ, ਕਸ਼ਮੀਰ ਘਾਟੀ ਦੇ ਵਿੱਚ, ਕੁੱਲ ਆਬਾਦੀ 1,157,394 ਦਰਜ ਕੀਤੀ ਗਈ ਸੀ ਜਿਸ ਵਿੱਚ 1,083,766, ਜਾਂ 93.6% ਆਬਾਦੀ ਮੁਸਲਮਾਨਾਂ ਦੀ ਸੀ ਅਤੇ ਹਿੰਦੂਆਂ ਦੀ ਗਿਣਤੀ 60,641 ਸੀ। ਜੰਮੂ ਰਿਆਸਤ ਦੇ ਹਿੰਦੂਆਂ ਵਿੱਚ, ਜਿਨ੍ਹਾਂ ਦੀ ਗਿਣਤੀ 626,177 (ਜਾਂ ਸਾਰੇ ਰਾਜ ਦੇ ਹਿੰਦੂਆਂ ਦੀ ਗਿਣਤੀ ਦਾ 90.87%) ਸੀ, ਸਭ ਤੋਂ ਮਹੱਤਵਪੂਰਨ ਜਾਤੀ ਬ੍ਰਾਹਮਣਾਂ (186,000) ਦੀ ਸੀ। ਰਾਜਪੂਤਾਂ ਦੀ ਗਿਣਤੀ 167,000, ਖੱਤਰੀਆਂ ਦੀ ਗਿਣਤੀ 48,000 ਅਤੇ ਠੱਕਰਾਂ ਦੀ ਗਿਣਤੀ 93,000 ਸੀ। "1911 ਦੀ ਜਨਗਣਨਾ ਅਨੁਸਾਰ, ਕਸ਼ਮੀਰ ਅਤੇ ਜੰਮੂ ਦੀ ਕੁੱਲ ਆਬਾਦੀ ਵਧ ਕੇ 3,158,126 ਹੋ ਗਈ ਸੀ। ਜਿਸ ਵਿੱਚ 2,398,320 (75.94%) ਮੁਸਲਮਾਨ ਸਨ, 696,830 (22.06%) ਹਿੰਦੂ, 31,658 (1%) ਸਿੱਖ, ਅਤੇ 36,512 (1.16%) ਬੋਧੀ ਸਨ। ਬ੍ਰਿਟਿਸ਼ ਭਾਰਤ ਦੀ ਆਖਰੀ ਜਨਗਣਨਾ ਜੋ ਕਿ 1941 ਵਿੱਚ ਹੋਈ ਸੀ ਕਸ਼ਮੀਰ ਅਤੇ ਜੰਮੂ ਦੀ ਕੁੱਲ ਆਬਾਦੀ ਲਗਭਗ 3,945,000 ਸੀ, ਜਿਸ ਵਿੱਚ 2,997,000 (75.97%) ਮੁਸਲਮਾਨ, 808,000 (20.48%) ਹਿੰਦੂ ਅਤੇ 55,000 (1.39%) ਸਿੱਖ ਸਨ। ਕਸ਼ਮੀਰੀ ਪੰਡਿਤ, ਜਿਹੜੇ ਕਿ ਕਸ਼ਮੀਰ ਦੇ ਹਿੰਦੂ ਹਨ, ਜਿਨ੍ਹਾਂ ਦੀ ਆਬਾਦੀ ਡੋਗਰਾ ਰਾਜ (1846-1947) ਦੇ ਸਮੇਂ ਤੋਂ ਲਗਭਗ 4 ਤੋਂ 5% ਸੀ, ਅਤੇ ਜਿਸਦੇ 20% ਹਿੱਸੇ ਨੇ 1950 ਤੱਕ ਕਸ਼ਮੀਰ ਘਾਟੀ ਨੂੰ ਛੱਡ ਦਿੱਤਾ ਸੀ, ਅਤੇ ਮਗਰੋਂ 1990 ਦੇ ਦਹਾਕੇ ਵਿੱਚ ਵੀ ਇਨ੍ਹਾਂ ਦੀ ਵੱਡ... [1,000 / 1,137 chars] |
| ਉਸਨੇ ਵਰਲਡ ਪ੍ਰੋਗਰਾਮ ਟੂਰ ਨਾਮਕ ਵਿੱਚ ਹਿੱਸਾ ਲਿਆ? [43 chars] | 2007 ਵਿਚ ਚੋਪੜਾ ਮਿਸ ਇੰਡੀਆ ਮੁਕਾਬਲੇ ਵਿੱਚ ਜੱਜਾਂ ਦੇ ਪੈਨਲ ਵਿਚ ਸੀ। ਉਸ ਨੇ ਕਿਹਾ, "ਮਿਸ ਇੰਡੀਆ ਹਮੇਸ਼ਾ ਵਿਸ਼ੇਸ਼ ਬਣੇ ਰਹਿਣਗੇ, ਇਹ ਉਹ ਥਾਂ ਹੈ ਜਿੱਥੇ ਇਹ ਸਭ ਮੇਰੇ ਲਈ ਸ਼ੁਰੂ ਹੋਇਆ. ਅਤੇ ਹੋ ਸਕਦਾ ਹੈ ਕਿ ਜੇ ਮੈਂ ਤਾਜ ਨਹੀਂ ਜਿੱਤਿਆ ਹੁੰਦਾ ਤਾਂ ਇਹ ਉਹ ਥਾਂ ਹੁੰਦੀ ਜਿੱਥੇ ਇਹ ਸਭ ਖਤਮ ਹੋ ਗਿਆ ਹੁੰਦਾ। " ਉਸਨੇ ਮਿਸ ਵਰਲਡ 2009 ਵਿੱਚ ਇੱਕ ਜੱਜ ਵਜੋਂ ਕੰਮ ਕੀਤਾ। ਉਸਨੇ ਭਾਰਤ ਦੀ ਆਜ਼ਾਦੀ ਦੀ 60 ਵੀਂ ਵਰ੍ਹੇਗੰਢ ਦਾ ਜਸ਼ਨ ਮਨਾ ਰਹੇਐਨ ਡੀ ਟੀ ਟੀ ਵੀ ਸ਼ੋਅ ਜੈ ਜਵਾਨ ਦੇ ਵਿਸ਼ੇਸ਼ ਐਪੀਸੋਡ ਲਈ ਪੂਰਬੀ ਭਾਰਤ ਦੇ ਟੇਂਗਾ ਵਿੱਚ ਜਵਾਨ ਫੌਜਾਂ ਦਾ ਦੌਰਾ ਕੀਤਾ। 2010 ਵਿੱਚ, ਉਸਨੇ ਕਲਰਜ਼ ਚੈਨਲ 'ਤੇ ਰਿਆਲਟੀ ਸ਼ੋਅ ਫੀਅਰ ਫੈਕਟਰ: ਖਤਰੋਂ ਕੇ ਖਿਲਾੜੀ ਦੀ ਤੀਜੀ ਸੀਜ਼ਨ ਦੀ ਮੇਜ਼ਬਾਨੀ ਕੀਤੀ ਜੋ ਪਿਛਲੇ ਮੇਜ਼ਬਾਨ ਅਕਸ਼ੇ ਕੁਮਾਰ ਤੋਂ ਲਿਆ ਗਿਆ ਸੀ। ਮੁਕਾਬਲੇਬਾਜ਼ਾਂ ਦੇ ਅਨੁਸਾਰ, ਲੜੀ ਦੀ ਮੇਜ਼ਬਾਨੀ ਵਿੱਚ, ਚੋਪੜਾ "ਇੱਕ ਸਚੇਤਕ ਤਾਨਾਸ਼ਾਹੀ ਵਿੱਚ ਪਰਿਵਰਤਿਤ ਹੋ ਗਈ ਸੀ",ਅਤੇ ਲਗਾਤਾਰ ਮੁਕਾਬਲੇਬਾਜ਼ਾਂ ਨੂੰ ਕੰਮ ਕਰਨ ਲਈ ਪ੍ਰੇਰਿਤ ਕਰਦੀ ਸੀ। ਇਹ ਸਾਬਤ ਕਰਨ ਲਈ ਕਿ ਹੈ ਉਹ ਪਿਛਲੇ ਦੋ ਸੀਜ਼ਨਾਂ ਦੀ ਮੇਜ਼ਬਾਨੀ ਕਰਨ ਵਾਲੇ ਅਕਸ਼ੈ ਕੁਮਾਰ ਨੂੰ ਟੱਕਰ ਦੇ ਸਕਦੀ ਹੈ, ਉਸਨੇ ਆਪਣੇ ਖੁਦ ਦੇ ਜ਼ਿਆਦਾਤਰ ਸਟੰਟ ਅਦਾ ਕੀਤੇ ਹਨ। ਸ਼ੋਅ ਦੀ ਸ਼ੁਰੂਆਤੀ ਰੇਟਿੰਗ.ਪਿਛਲੇ ਦੋ ਸੀਜ਼ਨਾਂ ਦੇ ਵਿੱਚ ਸਭ ਤੋਂ ਉਪਰ ਰਹੀ। ਪ੍ਰਦਰਸ਼ਨ ਦੀ ਆਲੋਚਕਾਂ ਨੇ ਪ੍ਰਸ਼ੰਸਾ ਕੀਤੀ ਅਤੇ... [1,000 / 1,427 chars] |
| ਫਰਾਂਸ ਦੇ ਅਰਾਜਕਤਾਵਾਦੀ ਨੇ ਅਗਸਟਸ ਵੇਲਟ ਤੋਂ ਪ੍ਰਭਾਵਿਤ ਹੋ ਕੇ ਕਿਹੜੀ ਥਾਂ ਬੰਬ ਸੁਟਿਆ? [74 chars] | 1929 ਵਿੱਚ, ਉਸਨੇ ਐਚ ਐਸ ਆਰ ਏ ਲਈ ਆਪਣੇ ਉਦੇਸ਼ ਲਈ ਵੱਡੇ ਪੈਮਾਨੇ 'ਤੇ ਪ੍ਰਚਾਰ ਹਾਸਲ ਕਰਨ ਲਈ ਇੱਕ ਨਾਟਕੀ ਐਕਟ ਦਾ ਪ੍ਰਸਤਾਵ ਰੱਖਿਆ। ਪੈਰਿਸ ਵਿੱਚ ਚੈਂਬਰ ਆਫ਼ ਡਿਪਟੀਜ਼ ਉੱਤੇ ਬੰਬ ਸੁੱਟਣ ਵਾਲੇ, ਫਰਾਂਸੀਸੀ ਅਰਾਜਕਤਾਵਾਦੀ ਅਗਸਟਸ ਵੈੱਲਟ ਤੋਂ ਪ੍ਰਭਾਵਿਤ, ਭਗਤ ਸਿੰਘ ਨੇ ਕੇਂਦਰੀ ਵਿਧਾਨ ਸਭਾ ਦੇ ਅੰਦਰ ਬੰਬ ਵਿਸਫੋਟ ਕਰਨ ਦੀ ਯੋਜਨਾ ਬਣਾਈ। ਨਾਮਾਤਰ ਇਰਾਦਾ ਪਬਲਿਕ ਸੇਫਟੀ ਬਿੱਲ ਅਤੇ ਵਪਾਰ ਵਿਵਾਦ ਐਕਟ ਦੇ ਵਿਰੁੱਧ ਵਿਰੋਧ ਕਰਨਾ ਸੀ, ਜਿਸ ਨੂੰ ਅਸੈਂਬਲੀ ਵੱਲੋਂ ਰੱਦ ਕਰ ਦਿੱਤਾ ਗਿਆ ਸੀ ਪਰ ਵਾਇਸਰਾਏ ਦੁਆਰਾ ਉਸ ਦੀ ਵਿਸ਼ੇਸ਼ ਸ਼ਕਤੀਆਂ ਦਾ ਇਸਤੇਮਾਲ ਕਰਦੇ ਹੋਏ ਬਣਾਇਆ ਜਾ ਰਿਹਾ ਸੀ; ਅਸਲ ਇਰਾਦਾ ਤਾਂ ਆਪਣੇ ਆਪ ਨੂੰ ਗ੍ਰਿਫਤਾਰ ਕਰਵਾਉਣ ਦਾ ਸੀ ਤਾਂ ਜੋ ਉਹ ਅਦਾਲਤ ਨੂੰ ਉਨ੍ਹਾਂ ਦੇ ਪ੍ਰਚਾਰ ਦਾ ਪ੍ਰਸਾਰ ਕਰਨ ਲਈ ਇੱਕ ਮਾਧਿਅਮ ਦੇ ਤੌਰ ਤੇ ਵਰਤ ਸਕਣ। ਐਚਐਸਆਰਏ ਦੀ ਲੀਡਰਸ਼ਿਪ ਸ਼ੁਰੂ ਵਿੱਚ ਭਗਤ ਸਿੰਘ ਦੀ ਬੰਬਾਰੀ ਵਿੱਚ ਹਿੱਸਾ ਲੈਣ ਦਾ ਵਿਰੋਧ ਕਰਦੀ ਸੀ ਕਿਉਂਕਿ ਉਹ ਨਿਸ਼ਚਿਤ ਸਨ ਕਿ ਸਾਂਡਰਸ ਦੀ ਗੋਲੀਬਾਰੀ ਵਿੱਚ ਉਸ ਦੀ ਪਹਿਲਾਂ ਦੀ ਸ਼ਮੂਲੀਅਤ ਸੀ ਕਿ ਉਸ ਦੀ ਗ੍ਰਿਫ਼ਤਾਰੀ ਉਸ ਦੇ ਫਾਂਸੀ ਦਾ ਨਤੀਜਾ ਹੋਵੇਗੀ ਅਤੇ ਦਲ ਦੇ ਆਗੂਆਂ ਦੀ ਬਹੁ ਗਿਣਤੀ ਉਨ੍ਹਾੰ ਨੂੰ ਭਵਿੱਖ ਦੇ ਜਹੀਨ ਆਗੂ ਦੇ ਤੌਰ ਤੇ ਬਚਾ ਕੇ ਰਖਣ ਦੇ ਹੱਕ ਵਿੱਚ ਸੀ। ਪਰ, ਉਨ੍ਹਾਂ ਨੇ ਆਖਿਰਕਾਰ ਫ਼ੈਸਲਾ ਕੀਤਾ ਕਿ ਉਹ ਉਨ੍ਹਾਂ ਦਾ ਸਭ ਤੋਂ ਢੁਕਵਾਂ ਉਮੀਦਵਾਰ ਹੈ। ਵਾਦ ਵਿਵਾਦ ਤੋਂ ਬਾਦ ਅੰਤ ਵ... [1,000 / 2,900 chars] |

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
| A Punjabi question asking how many Kashmiri Pandits left the valley in a decade. | A paragraph about Kashmir valley population, religious composition, and political context. |
| A question asking whether a person participated in a World Program Tour. | A paragraph about Priyanka Chopra, Miss India, and career events. |
| A question asking where a French anarchist inspired Bhagat Singh to throw a bomb. | A paragraph about HSRA, Auguste Vaillant, and the Central Legislative Assembly bombing. |
| A question asking the name of Priyanka Chopra's last 2006 Farhan Akhtar action thriller. | A paragraph about Priyanka Chopra's film roles and releases. |
| A question asking with whom Khan's second collaboration in a musical romance was. | A paragraph about the 1997 film Dil To Pagal Hai, Yash Chopra, and the role of Rahul. |
