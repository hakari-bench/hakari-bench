# MNanoBEIR / NanoBEIR-th / NanoNFCorpus

## Overview

NFCorpus is biomedical and nutrition retrieval. `NanoBEIR-th__NanoNFCorpus`
uses Thai translated health queries and scientific passages.

## Details

### What the Original Data Measures

[NFCorpus](https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf)
uses health information needs with relevance judgments. BEIR includes it as
domain retrieval, and MMTEB provides multilingual context.

### Observed Data Profile

The task has 50 queries, 2,953 documents, and 1,651 qrels. It is highly
multi-positive, averaging 33.02 positives. Queries average 22.62 characters, and
documents average 1,387.38 characters.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.3243 and hit@10 = 0.6400. Multi-positive scientific
ranking remains harder than finding one lexical match.

### Training Data That May Help

Use Thai biomedical retrieval, medical QA, scientific abstract ranking, and
multi-positive training. Exclude NFCorpus, BEIR, and NanoBEIR overlaps.

### Synthetic Data Guidance

Generate Thai health keyword queries from biomedical passages, preserving
multiple positives for the same condition or outcome.

## Example Data

| Query | Positive document |
| --- | --- |
| นมปั่นช็อกโกแลตเพื่อสุขภาพ (26 chars) | วัตถุประสงค์ เพื่อศึกษาความสัมพันธ์ระหว่างการบริโภคเชอร์รี่และความเสี่ยงต่อการเกิดโรคเกาต์ซ้ำในบุคคลที่เป็นโรคเกาต์ วิธีการ เราได้ดำเนินการศึกษากรณีข้ามเพื่อพิจารณาความสัมพันธ์ของชุดปัจจัยเสี่ยงที่คาดการณ์ได้กับการเกิดโรคเกาต ... [truncated 225 chars](1492 chars) |
| การศึกษาการลดคอเลสเตอรอล (24 chars) | ภูมิหลัง: หนึ่งในปัญหาหลักในการควบคุมคอเลสเตอรอลในเลือดผ่านการแทรกแซงทางโภชนาการดูเหมือนว่าจะเป็นความจำเป็นในการปรับปรุงการปฏิบัติตามของผู้ป่วย เป้าหมาย: เพื่อสำรวจคำถามมากมายเกี่ยวกับอุปสรรคและแรงจูงใจในการปฏิบัติตามอาหารที่ ... [truncated 225 chars](1601 chars) |
| ถั่วฟาวา (8 chars) | ในช่วง 20 ปีที่ผ่านมา ความสนใจที่เพิ่มขึ้นในชีวเคมี โภชนาการ และเภสัชวิทยาของ L-arginine ได้นำไปสู่การศึกษาอย่างกว้างขวางเพื่อสำรวจบทบาททางโภชนาการและการรักษาของมันในการรักษาและป้องกันความผิดปกติทางเมตาบอลิซึมในมนุษย์ หลักฐาน ... [truncated 225 chars](1078 chars) |
| ไก่นักเก็ตมีอะไรอยู่จริงๆ? (26 chars) | วัตถุประสงค์: เพื่อตรวจสอบเนื้อหาของนั๊กเก็ตไก่จากร้านอาหารฟาสต์ฟู้ดระดับชาติ 2 แห่ง ข้อมูลพื้นฐาน: นั๊กเก็ตไก่ได้กลายเป็นส่วนประกอบหลักของอาหารอเมริกัน เราต้องการตรวจสอบองค์ประกอบปัจจุบันของอาหารที่ผ่านการแปรรูปอย่างมากนี้ ว ... [truncated 225 chars](662 chars) |
| ไขมันอิ่มตัว (12 chars) | ความสนใจเพิ่มขึ้นในความเป็นไปได้ที่การบริโภคอาหารของมารดาในระหว่างตั้งครรภ์อาจมีอิทธิพลต่อการพัฒนาความผิดปกติจากภูมิแพ้ในเด็ก การศึกษาที่มีลักษณะเป็น prospective ในปัจจุบันได้ตรวจสอบความสัมพันธ์ระหว่างการบริโภคอาหารที่เลือกซึ ... [truncated 225 chars](1839 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-th |
| Task / split | NanoNFCorpus |
| Hugging Face dataset | [hakari-bench/NanoBEIR-th](https://huggingface.co/datasets/hakari-bench/NanoBEIR-th) |
| Language | th |
| Category | natural_language |
| Queries | 50 |
| Documents | 2,953 |
| Positive qrels | 1,651 |
| Positives per query avg | 33.02 |
| Positives per query min / median / max | 1 / 23.5 / 100 |
| Multi-positive queries | 47 (94.00%) |
| BM25 nDCG@10 | 0.3243 |
| BM25 hit@10 | 0.6400 |
| Query length avg chars | 22.62 |
| Document length avg chars | 1,387.38 |

### Public Sources

- [NFCorpus](https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf), [BEIR](https://arxiv.org/abs/2104.08663), [MMTEB](https://arxiv.org/abs/2502.13595), and [NanoBEIR](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-th](https://huggingface.co/datasets/hakari-bench/NanoBEIR-th)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| NFCorpus: A Full-Text Learning to Rank Dataset for Medical Information Retrieval | 2016 | task paper | https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | https://arxiv.org/abs/2104.08663 |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | https://arxiv.org/abs/2502.13595 |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | https://huggingface.co/collections/zeta-alpha-ai/nanobeir |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: MNanoBEIR
  backing_dataset: NanoBEIR-th
  dataset_id: hakari-bench/NanoBEIR-th
  task_name: NanoNFCorpus
  split_name: NanoNFCorpus
  language: th
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-th__NanoNFCorpus.md
  source_research: {primary_source_type: task_paper, paper_pdf_or_html_checked: true, no_paper_note: null}
  counts: {queries: 50, documents: 2953, positive_qrels: 1651}
  positives_per_query: {average: 33.02, min: 1, median: 23.5, max: 100, multi_positive_queries: 47, multi_positive_query_percent: 94.0}
  text_stats_chars: {query_mean: 22.62, document_mean: 1387.382323}
  bm25: {ndcg_at_10: 0.3243007643, hit_at_10: 0.64, source: dataset_bm25_column}
```
