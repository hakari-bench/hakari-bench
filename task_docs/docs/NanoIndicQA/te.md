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
| పాండిచేరి ఏ భాగంలో స్థాపించబడింది? [34 chars] | 1793 లో ఫ్రెంచ్ విప్లవం యుద్ధాల మధ్య పాండిచేరి ముట్టడిలో బ్రిటిష్ వారు ఈ ప్రాంతాన్ని తిరిగి స్వాధీనం చేసుకున్నారు. 1814 లో ఫ్రాన్స్‌కు తిరిగి ఇచ్చారు. 1954 మార్చి 18న , పాండిచేరిలోని పురపాలక సంఘాలు భారతదేశంతో వెంటనే విలీనం కావాలని కోరుతూ అనేక తీర్మానాలను ఆమోదించాయి. కొన్ని రోజుల తరువాత, కారకల్‌లోని పురపాలక సంఘాలు ఇలాంటి తీర్మానాలను ఆమోదించాయి. మంత్రులుగా భావించే ఫ్రెంచ్ ఇండియన్ కౌన్సిలర్లు, ప్రతినిధులు ఈ తీర్మానాలకు పూర్తి మద్దతు ఇస్తున్నట్లు అసెంబ్లీ అధ్యక్షుడికి తెలిపారు. ఈ పురపాలక సంఘాలు ఫ్రెంచ్ జనాభామొత్తంలో సుమారు 90 శాతం ప్రాతినిధ్యం వహిస్తున్నాయి. ప్రజల కోరికలను అమలు చేయడానికి అత్యవసరమైన చర్యలు తీసుకోవాలని వారు ఫ్రాన్సు ప్రభుత్వాన్ని కోరారు. ప్రజల సాంస్కృతిక, ఇతర హక్కులను పూర్తిగా గౌరవిస్తామని భారత ప్రభుత్వం స్పష్టం చేసింది. ఫ్రాన్సు చట్టప్రకారం సార్వభౌమత్వాన్ని వెంటనే బదిలీ చేయమని వారు అడగలేదు. పరిపాలన వాస్తవ బదిలీ వెంటనే జరగాలని, రాజ్యాంగ సమస్య పరిష్కారం అయ్యేవరకు ఫ్రెంచ్ సార్వభౌమాధికారం కొనసాగిస్తూ, భారతదేశం, ఫ్రాన్సు రెండూ తమ రాజ్యాంగాల్లో అవసరమైన మార్పులు చేయాలని వారి సూచనల... [1,000 / 1,362 chars] |
| ఆర్థిక ప్రయోజనాల కోసం రుణాలు మరియు తాలూఖదారీ వ్యవస్థను రద్దు చేయాలని డిమాండ్ చేసింది ఎవరు? [90 chars] | 1938 చివర్లో భారతదేశానికి తిరిగిరాగానే దేశ రాజకీయాల్లో నిమగ్నుడయ్యాడు. ముస్లింలీగ్‌ని మంత్రివర్గాల్లో చేర్చుకోకపోవడం కాంగ్రెస్ అహంకారమనీ, ద్రోహమనీ భావించిన జిన్నా అప్పటినుంచీ కాంగ్రెస్‌పై దారుణమైన విమర్శలు చేయసాగాడు. కాంగ్రెస్ ఫాసిస్ట్ సంస్థ అనీ, ఇస్లాం ప్రమాదంలో పడిందనీ జిన్నా విమర్శలు చేయసాగాడు. వీటి విషయంలో సూటిగా ఉదాహరణలు ఇవ్వమనీ నెహ్రూ సవాలు చేసినా, అది పట్టించుకోకుండా జిన్నా మళ్ళీ వేర్వేరు ఆరోపణలు చేస్తూ పోవడమనే వ్యూహాన్ని తొలిసారిగా అమల్లో పెట్టసాగాడు. ముస్లింలను ఆకట్టుకునేందుకు ముస్లిం రైతులతో సభలు ఏర్పాటుచేసి వారికి ప్రయోజనకరంగా ఉండేలా ఋణాలను, తాలూక్దారి విధానాన్ని రద్దుచేయమని కోరాలని, తద్వారా ముస్లిం నాయకులు భయాందోళనలు రేకెత్తించే విధానాలకు విరుగుడుగా ముస్లిం జనబాహుళ్యపు ఆర్థిక ప్రయోజనాల ద్వారా ఆకర్షించగలమని నెహ్రూ భావించాడు. కానీ దీర్ఘకాలం సాగాల్సిన ఈ వ్యూహాలు మతకల్లోలాలు, హింస, అభద్రతాభావం వ్యాప్తి మధ్యలో సాగలేదు. కాంగ్రెస్ పార్టీలో అధ్యక్షుడు సుభాష్ చంద్రబోస్‌కీ, గాంధీకి నడుమ అంతర్గత వివాదం ప్రారంభమైంది. 1938లో జవాహర్ నుంచి కాంగ్రెస్ అధ్యక్ష పదవి స్వీకరించిన బోస్ 1939లో మర... [1,000 / 14,467 chars] |
| సైన్యాలు తరువాత గుజరాత్ మరియు బెంగాల్‌ను జయించింది ఎవరు? [56 chars] | నిర్ణయించాడు. బైరామ్ ఖాన్ తర్వాత మక్కాకు వెళ్ళేమార్గంలో ఒక ఆఫ్ఘన్ చేతిలో హత్యకు గురయ్యాడు. 1560 లో అక్బరు సైనిక చర్యలను కొనసాగించాడు. తన పెంపుడు సోదరుడు ఆధమ్ ఖాన్, ముఘల్ కమాండర్ పీర్ ముహమ్మద్ ఖాన్ ఆధ్వర్యంలో మొఘల్ సైన్యం మాల్వా మీద దాడి చేసింది. ఆఫ్ఘన్ పాలకుడు బజ్ బహదూర్ సారంగ్పూర్ యుద్ధంలో ఓడిపోయి తన అంతఃపురాన్ని నిధిని, యుద్ధ ఏనుగులను వదిలి ఖండేషుకు పారిపోయాడు శరణు జొచ్చాడు. ప్రారంభ విజయం సాధించినప్పటికీ ఈ పోరాటం అక్బరు దృష్టిలో ఒక విపత్తుగా భావించబడింది. అతని పెంపుడు సోదరుడు లొంగిపోయిన రక్షణ దళం, వారి భార్యలు, పిల్లలు, ముస్లిం వేదాంతులు, ముహమ్మదు వారసులు అయిన సయ్యదు సన్యాసులను నరమేధం చేయమని ఆదేశించి మద్య ఆసియాలో ముఘల్ చరిత్రకు మొదటిసారిగా మచ్చ తీసుకుని వచ్చాడు. అక్బరు వ్యక్తిగతంగా మాల్వాకు వెళ్ళి ఆధం ఖాన్ను పదవి నుండి తొలగించాడు. పిర్ ముహమ్మద్ ఖాన్ బజ్ బహదూరుగా పంపబడ్డాడు. కాని ఖండేషు, బెరార్ పాలకుల కూటమి చేతిలో పీరు ముహమ్మదు ఖాను పరాజయం పాలైయ్యారు. బజ్ బహదూర్ తాత్కాలికంగా మాల్వా నియంత్రణను తిరిగి పొందాడు. తరువాత సంవత్సరంలో అక్బరు మరొక మొఘల్ సైన్యాన్ని పంపి మాల్వాను ఆక్రమించుకుని సా... [1,000 / 6,714 chars] |

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
