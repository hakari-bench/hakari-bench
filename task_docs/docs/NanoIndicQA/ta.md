# NanoIndicQA / ta

## Overview

`NanoIndicQA / ta` is the Tamil split of IndicQA retrieval. The queries are Tamil reading-comprehension questions, and the documents are Tamil context paragraphs.

This task evaluates Tamil context retrieval and is the weakest BM25 profile among the NanoIndicQA splits reviewed here. Dense retrieval is much stronger, indicating that semantic question-context matching is especially important for this language split.

## Details

### What the Original Data Measures

IndicQA is a manually curated cloze-style reading-comprehension task introduced inside IndicXTREME in "Towards Leaving No Indic Language Behind". The MTEB retrieval adaptation evaluates retrieval of the context paragraph for each question.

In the Tamil split, the model must map Tamil questions to Tamil paragraphs that contain the relevant evidence.

### Observed Data Profile

This Nano split contains 200 queries, 253 documents, and 201 positive qrels. Queries have 1.005 positives on average, with a minimum of 1, a median of 1.0, and a maximum of 2. One query is multi-positive. Queries average 56.34 characters, and documents average 2,288.26 characters.

Observed examples ask about another name for Tiffin Top, a technically precise mathematical structure, the duration of Sri Lanka's civil war, Banda Singh Bahadur's desire to establish a multicultural state in Punjab, and the language origin of the word Hindu. Documents are long Tamil paragraphs about geography, religion, Sri Lankan history, Sikh history, and cultural concepts.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.2932, hit@10 of 0.4600, and recall@100 of 0.7413. The candidate pool contains the full 253-document corpus. This is a weak lexical profile.

Tamil questions can be short, use transliterated terms, or refer to concepts that are expressed differently in the paragraph. Long paragraphs may share broad religious, geographic, or historical vocabulary, which makes term overlap a poor discriminator.

### Dense Evaluation Profile

The dense harrier-oss-270m profile reaches nDCG@10 of 0.6415, hit@10 of 0.7900, and recall@100 of 0.9403. Dense retrieval is the strongest direct profile by a large margin.

This pattern shows that embedding similarity is critical for this split. Dense retrieval captures question-context relations that BM25 misses, including transliteration, paraphrase, and evidence embedded in long explanatory paragraphs.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate subset reaches nDCG@10 of 0.4551, hit@10 of 0.6100, and recall@100 of 0.9502. It uses 100 candidates per query, with 10 rank-101 safeguard positives.

Hybrid retrieval gives the best recall@100 but is far below dense retrieval on top-10 ranking. It can serve as a broad reranking pool, but dense retrieval is clearly the stronger first-stage ranker.

### Metric Interpretation for Model Researchers

`NanoIndicQA / ta` is a useful stress test for Tamil semantic retrieval. BM25 is much weaker than dense retrieval, so this split exposes models that rely too heavily on term overlap.

Since nearly every query has one positive, nDCG@10 and hit@10 directly measure whether the correct paragraph is ranked early. Hybrid's high recall shows that rerankers can recover from a broad pool, but first-stage ordering remains hard.

### Query and Relevance Type Tendencies

Queries are Tamil factual or cloze-style questions. Documents are long paragraphs about religion, geography, history, architecture, politics, and cultural concepts.

The relevance relation is evidence support: the positive paragraph contains the information required to answer the question.

### Representative Failure Modes

BM25 may retrieve passages with shared religious or geographic terms but no answer evidence. Dense retrieval may still confuse broad historical contexts when several paragraphs discuss the same region or tradition. Hybrid retrieval improves candidate coverage but needs reranking for exact paragraph support.

Transliterated names and concepts can be difficult when the query and paragraph use different forms.

### Training Data That May Help

Useful training data includes Tamil QA context retrieval, Tamil Wikipedia passage retrieval, Indic multilingual retrieval data, and hard negatives from related geography, religion, and history contexts.

Training should include transliterated terms and named entities, and exclude this split's questions and positive context paragraphs.

### Model Improvement Notes

Improving this task requires Tamil semantic coverage, transliteration robustness, and long-context evidence ranking. Models should preserve names, places, religious terms, dates, and conceptual relations.

For reranking, the model should verify that the paragraph contains the exact answer evidence rather than a related topic.

## Example Data

| Query | Positive document |
| --- | --- |
| டிஃபின் டாப்பின் மற்ற பெயர் என்ன? [33 chars] | 1880 ஆம் ஆண்டு நிலச்சரிவில் அழிந்துபோன நைனா தேவி கோயில் பின்னாளில் மீண்டும் கட்டப்பட்டது. இது நைனி ஏரியின் வடக்குப்புறக் கரையில் காணப்படுகிறது. இந்தக் கோயிலில் இருக்கும் கடவுளான மா நைனா தேவி நேத்ராக்க... [200 / 2,917 chars] |
| தொழில்நுட்ப சிறப்பு மற்றும் துல்லியமான கணித அறிவைக் கொண்ட தனித்துவமான அமைப்பின் பெயர் என்ன? [91 chars] | 1600 ஆண்டுகாலப் பழமை வாய்ந்த சிகிரியா ஓவியங்கள் பண்டைய இலங்கையின் கலைச் சிறப்பை வெளிக்காட்டுகின்றன. இது உலகின் பண்டைக்கால நகரத் திட்டமிடலின் ஒரு உதாரணமாகக் காணப்படுகிறது. இது இலங்கையில் உள்ள ஏழு உலக ம... [200 / 4,916 chars] |
| இலங்கையில் எத்தனை ஆண்டுகள் உள்நாட்டுப் போர் நடந்தது? [52 chars] | 1959ல் கடும்போக்கு பௌத்த பிக்கு ஒருவனால் பண்டாரநாயக்க படுகொலை செய்யப்பட்டார். 1960ல் S. W. R. D. பண்டாரநாயக்கவின் மனைவியான சிறிமாவோ பண்டாரநாயக்க பிரதமராகப் பதவியேற்றார். 1962இல் ஏற்பட்ட கலகத்தையும் வெ... [200 / 3,363 chars] |
| பஞ்சாபில் ஒரு பன்முக கலாச்சார அரசை நிறுவ விரும்பியது யார்? [58 chars] | 1713 ஆம் ஆண்டில், பன்டா சிங் பகதூர் பஞ்சாபில் ஒரு பன்முக கலாச்சார அரசை நிறுவ விரும்பினார். இதற்காக முகலாயர்களுடன் இவர் தளர்ச்சியின்றி போராடினார். அவரது அரசு தனது வீழ்ச்சிக்கு முன்னதாக ஒரு வருடத்திற்கு... [200 / 1,988 chars] |
| எந்த மொழியிலிருந்து ஹிந்து உருவானது? [36 chars] | 'இந்து' என்ற சொல் 'சிந்து' (Sindhu) என்ற சமஸ்கிருதச் சொல்லிலிருந்து ஈரானிய மொழியான பாரசீக மொழி மூலமாக உருவான ஒரு சொல் ஆகும். இந்து என்ற சொல் முதன்முதலில் பாரசீகத்தினரால் ஒரு புவியியல் சொல்லாக, அதாவது... [200 / 1,524 chars] |

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
| A Tamil question asking another name for Tiffin Top. | A paragraph about Naina Devi temple, Naini Lake, and local geography or landmarks. |
| A question asking for the name of a structure with technical excellence and precise mathematical knowledge. | A paragraph about Sigiriya paintings, ancient city planning, and world heritage context. |
| A question asking how many years Sri Lanka's civil war lasted. | A paragraph about Sri Lankan political history, Bandaranaike, and conflict. |
| A question asking who wanted to establish a multicultural state in Punjab. | A paragraph about Banda Singh Bahadur and conflict with the Mughals. |
| A question asking which language the word Hindu came from. | A paragraph explaining the term Hindu, Sindhu, Sanskrit, Persian, and geographic usage. |
