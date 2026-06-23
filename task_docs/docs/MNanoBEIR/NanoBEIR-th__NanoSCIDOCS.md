# MNanoBEIR / NanoBEIR-th / NanoSCIDOCS

## Overview

NanoSCIDOCS in the Thai NanoBEIR slice is a scientific-document retrieval task derived from SCIDOCS and the SPECTER evaluation setting. The queries are Thai translated paper-title style descriptions, and the corpus contains Thai translated scientific abstracts. The task asks a retriever to find scientifically related papers rather than passages that answer a direct question. It is a compact benchmark for Thai academic search, paper recommendation behavior, and scientific semantic retrieval.

## Details

### What the Original Data Measures

SCIDOCS measures scientific document relatedness, with relevance based on relationships between papers such as topic, method, citation-like relatedness, or contribution similarity. In retrieval form, the query is a paper title or short scientific description, and relevant documents are abstracts from related papers. The task is therefore about academic relatedness, not fact lookup.

The Thai translated version adds challenges from Thai scientific phrasing, mixed technical vocabulary, and translated abstracts. Some technical terms and acronyms remain recognizable, while other terms are translated or paraphrased. A strong model must connect methods, research areas, and application settings even when exact wording differs.

### Observed Data Profile

The task contains 50 queries, 2,210 documents, and 244 relevance judgments. Every query is multi-positive, with an average of 4.88 positives per query. The minimum is 3, the median is 5.0, and the maximum is 5, so the benchmark consistently evaluates ranked relevant-set retrieval.

Queries average 69.08 characters, while documents average 820.44 characters. The query is usually a compact scientific title, and the document is a longer abstract. This creates a title-to-abstract matching problem: the model must infer the relevant scientific area and contribution from a short phrase.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.2641, hit@10 of 0.7600, and recall@100 of 0.5615 using the top-500 BM25 candidate subset. Lexical matching is moderately useful. Scientific titles often contain distinctive technical words, and BM25 can use those anchors to find at least one related abstract for many queries.

The recall@100 value also shows the limitation. Every query has several positives, and BM25 misses a large fraction of the related-paper set. It can over-rank papers with repeated technical terms while missing abstracts that describe a similar contribution using different language. For scientific retrieval, exact vocabulary is useful but incomplete.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.2915, hit@10 of 0.7600, and recall@100 of 0.6025. Dense retrieval improves nDCG@10 and recall@100 over BM25 while matching its hit@10. This suggests that embedding similarity captures some scientific relatedness beyond exact Thai term overlap.

The gain is modest rather than dramatic. Scientific relatedness can depend on fine-grained method, task, and contribution distinctions, and general dense similarity may still confuse adjacent subfields. Dense retrieval broadens the candidate set, but it does not fully solve multi-positive scientific ranking.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.3165, hit@10 of 0.7600, and recall@100 of 0.6270. It uses a top-100 candidate range with an optional rank-101 safeguard; the observed candidate count ranges from 100 to 101, with 2 safeguard rows and a mean of 100.04 candidates. This is the strongest overall profile among the three modes.

The hybrid result indicates that Thai SCIDOCS benefits from combining lexical scientific anchors with dense semantic similarity. BM25 contributes precise terminology, while dense retrieval expands to related abstracts with different wording. The hybrid profile improves both top-10 graded ranking and candidate coverage, making it the best first-stage configuration in this slice.

### Metric Interpretation for Model Researchers

Because every query has multiple positives, recall@100 matters more than hit@10 alone. A model can find one related paper early and still fail to cover the relevant set. nDCG@10 measures whether several related abstracts are ranked well in the first page, while recall@100 measures whether a later reranker has enough candidates.

The method comparison shows a gradual improvement from BM25 to dense to reranking_hybrid. That pattern suggests that neither lexical matching nor embedding similarity is sufficient by itself, but their combination helps scientific relatedness retrieval. Researchers can use this task to test domain-specific ranking, hard negatives from neighboring subfields, and hybrid retrieval design.

### Query and Relevance Type Tendencies

Queries include scientific titles such as a new multi-level DC-DC boost converter, sparse Gaussian Markov random field learning with Cholesky factorization, convolutional neural networks for large-scale image recognition, an RFID antenna design, and a digital heart-monitoring system. Relevant documents are abstracts from related scientific papers.

The task rewards models that understand technical phrases, devices, algorithms, architectures, and application domains. A same-field abstract may not be relevant if it solves a different problem, while a related abstract may use a different set of terms to describe a similar method or contribution.

### Representative Failure Modes

Likely failures include retrieving abstracts from the same broad field but a different contribution, over-ranking repeated acronyms or technical words, missing related papers that use translated synonyms, and ranking only one obvious positive while missing the rest. BM25 is brittle to vocabulary changes, while dense retrieval can blur neighboring scientific topics.

### Training Data That May Help

Useful training data includes scientific-paper retrieval, citation and co-citation ranking, paper recommendation data, multilingual academic abstracts, and hard negatives from the same field but different contribution. Thai scientific abstracts can help with local phrasing and terminology. For rerankers, close same-domain negatives are especially useful.

### Model Improvement Notes

A model targeting this task should improve scientific relatedness and relevant-set coverage. Sparse systems need terminology normalization without losing technical specificity. Dense systems need domain-specific contrastive training. Hybrid systems are promising here, but the final ranking should be tuned to distinguish genuinely related papers from same-field distractors.

## Example Data

| Query | Positive document |
| --- | --- |
| ตัวแปลงแรงดันสูงหลายระดับ DC-DC ใหม่ [36 chars] | บทคัดย่อ: ตัวแปลงแรงดันไฟฟ้าหลายระดับกำลังกลายเป็นตัวเลือกใหม่สำหรับการแปลงพลังงานในแอปพลิเคชันที่มีพลังงานสูง ตัวแปลงแรงดันไฟฟ้าหลายระดับมักจะสังเคราะห์คลื่นแรงดันไฟฟ้าขั้นบันไดจากแรงดันไฟฟ้าของตัวเก... [200 / 799 chars] |
| การเรียนรู้ฟิลด์สุ่มมาร์คอฟเกาส์เซียนที่เบาบางอย่างรวดเร็วโดยอิงจากการแยกแฟกเตอร์โชเลสกี้ [89 chars] | Please provide the text you would like to have translated into Thai. [68 chars] |
| การใช้เครือข่ายประสาทเทียมแบบพับซ้อนในการรู้จำภาพขนาดใหญ่ [57 chars] | ในงานนี้เราศึกษาผลกระทบของความลึกของเครือข่ายคอนโวลูชันต่อความแม่นยำในบริบทการรู้จำภาพขนาดใหญ่ ผลงานหลักของเราคือการประเมินเครือข่ายที่มีความลึกเพิ่มขึ้นอย่างละเอียด ซึ่งแสดงให้เห็นว่าการปรับปรุงที่สำ... [200 / 747 chars] |
| เสาอากาศวงแหวนแบนราบแบบกว้างที่มีการหมุนเวียนแบบวงกลมสำหรับระบบ RFID [68 chars] | ในเอกสารนี้เสนอเทคนิคการให้อาหารแบบแถบที่มีการเลี้ยวไปข้างหน้า (HMS) เพื่อให้ได้การจับคู่ความต้านทานที่ดีและรูปแบบการแผ่รังสีแบบกว้างขวางที่สมมาตรสำหรับเสาอากาศพatch ที่มีการขับเคลื่อนเดียวแบบวงกว้างท... [200 / 1,112 chars] |
| การออกแบบแอปพลิเคชันเสมือนจริงเพื่อการศึกษาเกี่ยวกับกายวิภาคของหัวใจมนุษย์ [74 chars] | ในเอกสารนี้ เราได้นำเสนอการออกแบบและพัฒนาอุปกรณ์รวมใหม่สำหรับการวัดอัตราการเต้นของหัวใจโดยใช้ปลายนิ้วเพื่อปรับปรุงการประมาณอัตราการเต้นของหัวใจ เนื่องจากโรคที่เกี่ยวข้องกับหัวใจมีแนวโน้มเพิ่มขึ้นทุกวั... [200 / 1,051 chars] |

### Source Reference Table

| Item | Reference |
| --- | --- |
| Original task context | [SPECTER](https://arxiv.org/abs/2004.07180) |
| Retrieval benchmark framing | [BEIR](https://arxiv.org/abs/2104.08663) |
| Multilingual benchmark context | [MMTEB](https://arxiv.org/abs/2502.13595) |
| NanoBEIR collection | [NanoBEIR on Hugging Face](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
| NanoBEIR-th dataset | [hakari-bench/NanoBEIR-th](https://huggingface.co/datasets/hakari-bench/NanoBEIR-th) |

Representative query and positive abstract snippets:

| Query | Positive document snippet |
| --- | --- |
| ตัวแปลงแรงดันสูงหลายระดับ DC-DC ใหม่ | บทคัดย่อ: ตัวแปลงแรงดันไฟฟ้าหลายระดับกำลังกลายเป็นตัวเลือกใหม่สำหรับการแปลงพลังงาน... |
| การเรียนรู้ฟิลด์สุ่มมาร์คอฟเกาส์เซียนที่เบาบางอย่างรวดเร็วโดยอิงจากการแยกแฟกเตอร์โชเลสกี้ | Please provide the text you would like to have translated into Thai. |
| การใช้เครือข่ายประสาทเทียมแบบพับซ้อนในการรู้จำภาพขนาดใหญ่ | ในงานนี้เราศึกษาผลกระทบของความลึกของเครือข่ายคอนโวลูชันต่อความแม่นยำ... |
| เสาอากาศวงแหวนแบนราบแบบกว้างที่มีการหมุนเวียนแบบวงกลมสำหรับระบบ RFID | ในเอกสารนี้เสนอเทคนิคการให้อาหารแบบแถบที่มีการเลี้ยวไปข้างหน้า... |
| การออกแบบแอปพลิเคชันเสมือนจริงเพื่อการศึกษาเกี่ยวกับกายวิภาคของหัวใจมนุษย์ | ในเอกสารนี้ เราได้นำเสนอการออกแบบและพัฒนาอุปกรณ์รวมใหม่สำหรับการวัดอัตราการเต้นของหัวใจ... |
