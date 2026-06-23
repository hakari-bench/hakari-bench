# MNanoBEIR / NanoBEIR-th / NanoNFCorpus

## Overview

NanoNFCorpus in the Thai NanoBEIR slice is a biomedical and nutrition retrieval task derived from NFCorpus. The queries are Thai translated health and nutrition information needs, and the corpus contains Thai translated scientific or medical passages. The task measures whether a retriever can connect short health-related queries to long domain passages that discuss relevant conditions, interventions, ingredients, outcomes, or medical concepts. It is a compact diagnostic for Thai biomedical retrieval with broad relevant sets.

## Details

### What the Original Data Measures

NFCorpus was built for medical information retrieval with health and nutrition information needs and relevance judgments over scientific text. Queries may be short keyword phrases, foods, conditions, medical topics, or plain-language questions. Relevant documents can include scientific abstracts or passages that discuss the same condition, treatment, exposure, or outcome.

The Thai translated version adds Thai segmentation and biomedical terminology challenges. Many queries are extremely short, while the documents are long and technical. A model must infer the biomedical concept from sparse query text and retrieve many relevant passages, not just one document with the most obvious word overlap.

### Observed Data Profile

The task contains 50 queries, 2,953 documents, and 1,651 relevance judgments. It is highly multi-positive, with an average of 33.02 positives per query. The minimum is 1, the median is 23.5, the maximum is 100, and 47 queries are multi-positive, or 94.0% of the query set. This makes relevant-set coverage central to the task.

Queries average 22.62 characters, while documents average 1,387.38 characters. The query-document length gap is large. A short Thai phrase such as a food, nutrient, or condition may correspond to many long passages, and the relevant evidence may be only a small part of each document.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.2484, hit@10 of 0.6200, and recall@100 of 0.1538 using the top-500 BM25 candidate subset. Lexical matching is competitive at finding at least one relevant passage, but recall is very low relative to the large positive sets.

This indicates that exact biomedical term overlap can locate obvious matches but does not cover the evidence landscape. Thai translated terminology, synonyms, and broader medical concepts can all reduce lexical alignment. BM25 is therefore useful for precise anchors but weak as a complete candidate generator for this task.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.2133, hit@10 of 0.5400, and recall@100 of 0.1532. Dense retrieval is slightly weaker than BM25 on top-rank metrics and nearly the same on recall@100. This suggests that the dense model does not sufficiently capture the biomedical relevance structure in this Thai slice.

The result is plausible for short biomedical queries. General embedding similarity may retrieve medically related passages that are not judged relevant, while exact domain terms remain useful. Dense retrieval may need domain adaptation, Thai biomedical data, and harder contrastive supervision to separate closely related medical concepts.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.2520, hit@10 of 0.6000, and recall@100 of 0.1750. It uses a top-100 candidate range with an optional rank-101 safeguard; the observed candidate count ranges from 100 to 101, with 8 safeguard rows and a mean of 100.16 candidates. The hybrid profile has the best nDCG@10 and recall@100, while BM25 has the best hit@10.

This shows that combining lexical and dense evidence helps modestly, but the task remains difficult. The relevant sets are large, and all three modes recover only a small fraction of positives by rank 100. Hybrid search improves coverage by adding complementary candidates, yet it still needs a stronger biomedical reranker or domain retriever to make the broad relevant set accessible.

### Metric Interpretation for Model Researchers

For NanoNFCorpus-th, recall@100 is especially important because most queries have many positives. hit@10 can be misleading: finding one relevant passage does not mean the model covers the biomedical evidence set. nDCG@10 measures first-page usefulness, while recall@100 measures whether downstream review or reranking can access enough relevant material.

The method comparison shows a hard domain-transfer problem. BM25 remains useful because technical terms matter. Dense retrieval does not outperform lexical matching, suggesting that general semantic similarity is insufficient. reranking_hybrid is slightly best overall, but the low recall values indicate that Thai biomedical retrieval needs domain-specific modeling.

### Query and Relevance Type Tendencies

Queries include short health and nutrition needs such as healthy chocolate milkshakes, cholesterol-lowering studies, fava beans, what is really in chicken nuggets, and saturated fat. Relevant passages are scientific or medical texts, often describing objectives, methods, associations, interventions, or health outcomes.

The task rewards models that understand biomedical concepts, not just words. A query can map to many passages about a condition or ingredient, and different positives may discuss different outcomes or study designs. Ranking only the most literal matches misses much of the relevant set.

### Representative Failure Modes

Likely failures include retrieving passages with the same food or medical term but a different outcome, missing relevant passages that use synonyms, over-ranking generic health text, and failing to cover multiple positives. BM25 can be too narrow, while dense retrieval can be too broad or insufficiently domain-aware. Hybrid systems must balance exact terminology with semantic expansion.

### Training Data That May Help

Useful training data includes Thai biomedical retrieval, medical QA, nutrition search, scientific abstract ranking, and hard negatives from the same condition or intervention but different outcomes. Thai medical terminology resources and segmentation-aware preprocessing can help. For rerankers, multi-positive supervision is important because the task is primarily about coverage over many relevant passages.

### Model Improvement Notes

A model targeting this task should improve biomedical concept normalization and broad relevant-set recall. Sparse systems need synonym expansion and Thai-aware tokenization for medical terms. Dense systems need biomedical domain adaptation and hard negatives for closely related concepts. Hybrid systems are promising, but should be evaluated on recall and nDCG rather than only first-positive discovery.

## Example Data

| Query | Positive document |
| --- | --- |
| นมปั่นช็อกโกแลตเพื่อสุขภาพ [26 chars] | วัตถุประสงค์ เพื่อศึกษาความสัมพันธ์ระหว่างการบริโภคเชอร์รี่และความเสี่ยงต่อการเกิดโรคเกาต์ซ้ำในบุคคลที่เป็นโรคเกาต์ วิธีการ เราได้ดำเนินการศึกษากรณีข้ามเพื่อพิจารณาความสัมพันธ์ของชุดปัจจัยเสี่ยงที่คาด... [200 / 1,492 chars] |
| การศึกษาการลดคอเลสเตอรอล [24 chars] | ภูมิหลัง: หนึ่งในปัญหาหลักในการควบคุมคอเลสเตอรอลในเลือดผ่านการแทรกแซงทางโภชนาการดูเหมือนว่าจะเป็นความจำเป็นในการปรับปรุงการปฏิบัติตามของผู้ป่วย เป้าหมาย: เพื่อสำรวจคำถามมากมายเกี่ยวกับอุปสรรคและแรงจูง... [200 / 1,601 chars] |
| ถั่วฟาวา [8 chars] | ในช่วง 20 ปีที่ผ่านมา ความสนใจที่เพิ่มขึ้นในชีวเคมี โภชนาการ และเภสัชวิทยาของ L-arginine ได้นำไปสู่การศึกษาอย่างกว้างขวางเพื่อสำรวจบทบาททางโภชนาการและการรักษาของมันในการรักษาและป้องกันความผิดปกติทางเม... [200 / 1,078 chars] |
| ไก่นักเก็ตมีอะไรอยู่จริงๆ? [26 chars] | วัตถุประสงค์: เพื่อตรวจสอบเนื้อหาของนั๊กเก็ตไก่จากร้านอาหารฟาสต์ฟู้ดระดับชาติ 2 แห่ง ข้อมูลพื้นฐาน: นั๊กเก็ตไก่ได้กลายเป็นส่วนประกอบหลักของอาหารอเมริกัน เราต้องการตรวจสอบองค์ประกอบปัจจุบันของอาหารที่ผ... [200 / 662 chars] |
| ไขมันอิ่มตัว [12 chars] | ความสนใจเพิ่มขึ้นในความเป็นไปได้ที่การบริโภคอาหารของมารดาในระหว่างตั้งครรภ์อาจมีอิทธิพลต่อการพัฒนาความผิดปกติจากภูมิแพ้ในเด็ก การศึกษาที่มีลักษณะเป็น prospective ในปัจจุบันได้ตรวจสอบความสัมพันธ์ระหว่า... [200 / 1,839 chars] |

### Source Reference Table

| Item | Reference |
| --- | --- |
| Original dataset | [NFCorpus](https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf) |
| Retrieval benchmark framing | [BEIR](https://arxiv.org/abs/2104.08663) |
| Multilingual benchmark context | [MMTEB](https://arxiv.org/abs/2502.13595) |
| NanoBEIR collection | [NanoBEIR on Hugging Face](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
| NanoBEIR-th dataset | [hakari-bench/NanoBEIR-th](https://huggingface.co/datasets/hakari-bench/NanoBEIR-th) |

Representative query and positive passage snippets:

| Query | Positive document snippet |
| --- | --- |
| นมปั่นช็อกโกแลตเพื่อสุขภาพ | วัตถุประสงค์ เพื่อศึกษาความสัมพันธ์ระหว่างการบริโภคเชอร์รี่และความเสี่ยงต่อการเกิดโรคเกาต์ซ้ำ... |
| การศึกษาการลดคอเลสเตอรอล | ภูมิหลัง: หนึ่งในปัญหาหลักในการควบคุมคอเลสเตอรอลในเลือดผ่านการแทรกแซงทางโภชนาการ... |
| ถั่วฟาวา | ในช่วง 20 ปีที่ผ่านมา ความสนใจที่เพิ่มขึ้นในชีวเคมี โภชนาการ และเภสัชวิทยาของ L-arginine... |
| ไก่นักเก็ตมีอะไรอยู่จริงๆ? | วัตถุประสงค์: เพื่อตรวจสอบเนื้อหาของนั๊กเก็ตไก่จากร้านอาหารฟาสต์ฟู้ดระดับชาติ... |
| ไขมันอิ่มตัว | ความสนใจเพิ่มขึ้นในความเป็นไปได้ที่การบริโภคอาหารของมารดาในระหว่างตั้งครรภ์... |
