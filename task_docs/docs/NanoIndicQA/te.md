# NanoIndicQA / te

## Overview

`NanoIndicQA / te` is the Telugu split of IndicQA retrieval. The queries are Telugu reading-comprehension questions, and the documents are Telugu context paragraphs.

This task evaluates Telugu evidence paragraph retrieval. It has the longest average document length among the NanoIndicQA splits reviewed here, so models must handle long paragraphs and identify the context containing the answer evidence.

## Details

### What the Original Data Measures

IndicQA is a manually curated cloze-style reading-comprehension task introduced as part of IndicXTREME in "Towards Leaving No Indic Language Behind". The MTEB version turns it into question-to-context retrieval.

In the Telugu split, each query is a Telugu factual question and the positive document is the source paragraph that contains the answer.

### Observed Data Profile

This Nano split contains 200 queries, 250 documents, and 200 positive qrels. Each query has exactly one positive. Queries average 64.96 characters, and documents average 2,936.18 characters.

Observed examples ask where Pondicherry was established, who demanded the abolition of loans and the talukdari system for economic benefit, who later conquered Gujarat and Bengal, what Shah Jahan built as a gift of love, and whom Pratap Singh kept attacking. Documents are long Telugu paragraphs about colonial history, political movements, Mughal history, Taj Mahal, and biographies.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.7674, hit@10 of 0.8800, and recall@100 of 0.9400. The candidate pool contains the full 250-document corpus. BM25 is the strongest direct ranker in this split.

The strong BM25 profile suggests that Telugu questions often repeat distinctive names, dates, places, and historical terms from the context. Exact lexical matching is highly informative despite the long document length.

### Dense Evaluation Profile

The dense harrier-oss-270m profile reaches nDCG@10 of 0.7186, hit@10 of 0.8500, and recall@100 of 0.9250. Dense retrieval is strong but below BM25.

This indicates that semantic matching helps, but exact Telugu term overlap is especially valuable for this split. Dense retrieval may retrieve related history or biography contexts without preserving the exact named entity or date needed.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate subset reaches nDCG@10 of 0.7582, hit@10 of 0.8600, and recall@100 of 0.9750. It uses 100 candidates per query, with five rank-101 safeguard positives.

Hybrid retrieval has the strongest recall@100 and nearly matches BM25 on nDCG@10. It is a good reranking pool because it combines BM25's exact evidence anchors with dense semantic matching.

### Metric Interpretation for Model Researchers

`NanoIndicQA / te` is a BM25-favored Telugu context retrieval task. This contrasts with many other IndicQA splits where dense retrieval is clearly stronger. The difference is useful for diagnosing whether a model respects exact Telugu lexical evidence.

Since each query has one positive, nDCG@10 and hit@10 directly measure correct-context placement. Recall@100 shows that hybrid retrieval gives the broadest candidate coverage for downstream reranking.

### Query and Relevance Type Tendencies

Queries are Telugu factual or cloze-style questions. Documents are long paragraphs about history, literature, politics, geography, Mughal rulers, colonial events, and cultural monuments.

The relevance relation is evidence support: the positive paragraph contains the fact required to answer the question.

### Representative Failure Modes

BM25 may retrieve a paragraph with repeated names but the wrong relation or event. Dense retrieval may choose a semantically related long history passage that lacks the exact answer. Hybrid retrieval improves candidate coverage but still needs evidence-aware ranking.

The long document length can hide the answer inside a large paragraph, which makes downstream answer extraction or reranking important.

### Training Data That May Help

Useful training data includes Telugu QA context retrieval, Telugu Wikipedia passage retrieval, multilingual IndicQA training, and hard negatives from other long biography, literature, history, or political paragraphs.

Training should exclude this split's questions and positive context paragraphs.

### Model Improvement Notes

Improving this task requires Telugu lexical precision and long-context evidence matching. Models should preserve named entities, dates, places, titles, and historical relations.

For reranking, the model should check whether the paragraph contains the exact answer evidence rather than only matching a broad topic or era.

## Example Data

| Query | Positive document |
| --- | --- |
| పాండిచేరి ఏ భాగంలో స్థాపించబడింది? [34 chars] | 1793 లో ఫ్రెంచ్ విప్లవం యుద్ధాల మధ్య పాండిచేరి ముట్టడిలో బ్రిటిష్ వారు ఈ ప్రాంతాన్ని తిరిగి స్వాధీనం చేసుకున్నారు. 1814 లో ఫ్రాన్స్‌కు తిరిగి ఇచ్చారు. 1954 మార్చి 18న , పాండిచేరిలోని పురపాలక సంఘాలు భా... [200 / 1,362 chars] |
| ఆర్థిక ప్రయోజనాల కోసం రుణాలు మరియు తాలూఖదారీ వ్యవస్థను రద్దు చేయాలని డిమాండ్ చేసింది ఎవరు? [90 chars] | 1938 చివర్లో భారతదేశానికి తిరిగిరాగానే దేశ రాజకీయాల్లో నిమగ్నుడయ్యాడు. ముస్లింలీగ్‌ని మంత్రివర్గాల్లో చేర్చుకోకపోవడం కాంగ్రెస్ అహంకారమనీ, ద్రోహమనీ భావించిన జిన్నా అప్పటినుంచీ కాంగ్రెస్‌పై దారుణమైన విమ... [200 / 14,467 chars] |
| సైన్యాలు తరువాత గుజరాత్ మరియు బెంగాల్‌ను జయించింది ఎవరు? [56 chars] | నిర్ణయించాడు. బైరామ్ ఖాన్ తర్వాత మక్కాకు వెళ్ళేమార్గంలో ఒక ఆఫ్ఘన్ చేతిలో హత్యకు గురయ్యాడు. 1560 లో అక్బరు సైనిక చర్యలను కొనసాగించాడు. తన పెంపుడు సోదరుడు ఆధమ్ ఖాన్, ముఘల్ కమాండర్ పీర్ ముహమ్మద్ ఖాన్ ఆధ్... [200 / 6,714 chars] |
| తన ప్రేమకు కానుకగా షాజహాన్ దేన్ని కట్టాడు? [42 chars] | 1631వ సంవత్సరంలో షాజహాన్ చక్రవర్తిగా ఉన్న కాలంలో మొఘల్ సామ్రాజ్యం గొప్ప సంపదతో ఉండేది, ఆ సమయంలో షాజహాన్ మూడవ భార్య అయిన ముంతాజ్ మహల్ వారి పధ్నాలుగో సంతానం గౌహరా బేగానికి జన్మనిస్తూ మరణించడంతో షాజహాన్... [200 / 1,072 chars] |
| ప్రతాప్ సింగ్ ఎవరి పైన దాడి చేస్తూనే ఉన్నాడు? [45 chars] | నిర్ణయించాడు. బైరామ్ ఖాన్ తర్వాత మక్కాకు వెళ్ళేమార్గంలో ఒక ఆఫ్ఘన్ చేతిలో హత్యకు గురయ్యాడు. 1560 లో అక్బరు సైనిక చర్యలను కొనసాగించాడు. తన పెంపుడు సోదరుడు ఆధమ్ ఖాన్, ముఘల్ కమాండర్ పీర్ ముహమ్మద్ ఖాన్ ఆధ్... [200 / 6,714 chars] |

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
| A Telugu question asking in which part Pondicherry was established. | A paragraph about French and British control of Pondicherry and its later merger with India. |
| A question asking who demanded the abolition of loans and talukdari systems for economic benefit. | A long paragraph about Jinnah, Congress, Muslim League politics, and policy demands. |
| A question asking who later conquered Gujarat and Bengal. | A paragraph about Akbar, Bairam Khan, Mughal military activity, and expansion. |
| A question asking what Shah Jahan built as a gift of love. | A paragraph about Mumtaz Mahal, Shah Jahan, and the Taj Mahal. |
| A question asking whom Pratap Singh kept attacking. | A Mughal-history paragraph about Akbar's campaigns and regional conflict. |
