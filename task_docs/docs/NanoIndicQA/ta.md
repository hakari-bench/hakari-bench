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
| டிஃபின் டாப்பின் மற்ற பெயர் என்ன? [33 chars] | 1880 ஆம் ஆண்டு நிலச்சரிவில் அழிந்துபோன நைனா தேவி கோயில் பின்னாளில் மீண்டும் கட்டப்பட்டது. இது நைனி ஏரியின் வடக்குப்புறக் கரையில் காணப்படுகிறது. இந்தக் கோயிலில் இருக்கும் கடவுளான மா நைனா தேவி நேத்ராக்கள் அல்லது கண்களைக் குறிக்கிறது. நைனா தேவியின் பக்கவாட்டில் இருப்பவர்கள் மாதா காளியும் கணேச பெருமானும் ஆவர். காட்டிற்குள் இருக்கும் செயிண்ட். ஜான் தேவாலயம் 1844ஆம் ஆண்டில் நிறுவப்பட்டது என்பதுடன், நைனா தேவி கோயிலில் இருந்து கிட்டத்தட்ட அரை மைல் தொலைவில் (மல்லிடால்) நகரத்தின் வடக்கு மூலையில் அமைந்திருக்கிறது. இந்த தேவாலயம் கல்கத்தா பிஷப்பான டேனியல் வில்சனின் நினைவாக பெயரிடப்பட்டது, இவர் 1844ஆம் ஆண்டில் இந்த தேவாலயத்தின் நிறுவுதலுக்காக நைனிடாலுக்கு வருகை புரிந்தபோது உடல் நலமில்லாமல் போன பின்னர் காட்டின் நுனியிலிருந்த கட்டி முடிக்கப்படாத வீட்டில் தூங்கும்படி கேட்டுக்கொள்ளப்பட்டார். (பார்க்க நைனிடாலுக்கான இலக்கிய பார்வைக்குறிப்பு பக்கத்திலிருந்து எடுக்கப்பட்ட ஜோசையா பேட்மேன் கட்டுரை. ) 1880 ஆம் ஆண்டில் ஏற்பட்ட நிலச்சரிவில் மரணமடைந்தவர்களின் பெயர்கள் பலிபீடத்தில் இருக்கும் பித்தளைத் தகட்டில் பொற... [1,000 / 2,917 chars] |
| தொழில்நுட்ப சிறப்பு மற்றும் துல்லியமான கணித அறிவைக் கொண்ட தனித்துவமான அமைப்பின் பெயர் என்ன? [91 chars] | 1600 ஆண்டுகாலப் பழமை வாய்ந்த சிகிரியா ஓவியங்கள் பண்டைய இலங்கையின் கலைச் சிறப்பை வெளிக்காட்டுகின்றன. இது உலகின் பண்டைக்கால நகரத் திட்டமிடலின் ஒரு உதாரணமாகக் காணப்படுகிறது. இது இலங்கையில் உள்ள ஏழு உலக மரபுரிமைக் களங்களில் ஒன்றாக யுனெசுக்கோவினால் அறிவிக்கப்பட்டுள்ளது. இவை தவிர, கோடைகாலத்துக்கென மாரிகால நீரைச் சேமித்து வைக்கக்கூடிய பாரிய நீர்த்தேக்கங்கள் மற்றும் நீர் காவும் வாய்க்கால்கள் என்பனவும் குறிப்பிடத்தக்க கட்டடக்கலைச் சிறப்புக்களாகும். இவற்றுள் சில வாய்க்கால்கள் மைலுக்கு ஒரு அங்குலம் என்ற நுட்பமான சாய்வையுடையனவாக உள்ளன. அணைக்குள் இருக்கும் கலிங்கல் தொட்டி எனப்படும் தனித்துவம் மிக்க அமைப்பு துல்லியமான கணித அறிவுடனான தொழில்நுட்பச் சிறப்புடையதாகும். இது அணைக்கட்டின் மீதான அழுத்தத்தை குறைவாகப் பேணியவாறே நீரை வெளியேற்ற உதவுகிறது. பண்டைய இலங்கை உலகிலேயே முதலாவது மருத்துவமனையைக் கொண்டது. இது 4ம் நூற்றாண்டில் மிகிந்தலையில் நிறுவப்பட்டது. மேலும் இது பண்டைய உலகில் கறுவா ஏற்றுமதியில் முதன்மை பெற்றிருந்தது. ரோமப் பேரரசு உள்ளிட்ட ஐரோப்பிய நாகரிகங்களுடன் இது நெருங்கிய தொடர்பைப் பேணியது. உதாரணமாக... [1,000 / 4,916 chars] |
| இலங்கையில் எத்தனை ஆண்டுகள் உள்நாட்டுப் போர் நடந்தது? [52 chars] | 1959ல் கடும்போக்கு பௌத்த பிக்கு ஒருவனால் பண்டாரநாயக்க படுகொலை செய்யப்பட்டார். 1960ல் S. W. R. D. பண்டாரநாயக்கவின் மனைவியான சிறிமாவோ பண்டாரநாயக்க பிரதமராகப் பதவியேற்றார். 1962இல் ஏற்பட்ட கலகத்தையும் வெற்றிகரமாக எதிர்கொண்டார். இவரது இரண்டாம் பதவிக்காலத்தின்போது அரசு சமவுடமைப் பொருளாதாரக் கொள்கைகளைக் கடைப்பிடித்தது. சோவியத் ஒன்றியம் மற்றும் சீனாவுடன் உறவுகளைப் பலப்படுத்திய அதேவேளை அணிசேராக் கொள்கையையும் கடைப்பிடித்தது. 1971இல், இலங்கையில் மாக்சியப் புரட்சி ஏற்பட்டது. எனினும், இது உடனடியாக அடக்கப்பட்டது. 1972ல் மேலாட்சி நிலை ஒழிக்கப்பட்டு நாடு குடியரசானது. நாட்டின் பெயரும் சிறீ லங்கா என மாற்றப்பட்டது. சிறுபான்மையினருக்கெதிரான அடக்குமுறைகளும் சிங்கள மற்றும் தமிழ் அரசியல் தலைவர்களால் தூண்டப்பட்ட இன உணர்ச்சியும் 1970களில் வட பகுதியில் தமிழ்ப் போராட்ட இயக்கங்களின் வளர்ச்சிக்கு வழிகோலின. நாட்டின் பின்தங்கிய பிரதேசத்து மாணவர்களுக்கும் பல்கலைக்கழகக் கல்வியை வழங்கும் முகமாக சிறிமாவோ அரசாங்கத்தினால் கொண்டுவரப்பட்ட தரப்படுத்தல் முறையினால், பல்கலைக்கழகங்களில் திறமைவாய்ந்த தமிழ் மாணவர்களுக்கான வாய்ப்ப... [1,000 / 3,363 chars] |

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
