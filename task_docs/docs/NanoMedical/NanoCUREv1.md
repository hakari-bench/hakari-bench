# NanoMedical / NanoCUREv1

## Overview

`NanoMedical / NanoCUREv1` is an English clinical passage retrieval task derived from CURE, a benchmark for clinical understanding and retrieval evaluation. Queries are healthcare-provider-style clinical questions, and relevant documents are biomedical article passages that contain evidence for diagnosis, treatment, contraindication, measurement, or clinical implications. The original CURE dataset was designed for point-of-care retrieval across multiple medical domains, including dentistry, dermatology, gastroenterology, genetics, neurology, orthopedics, otorhinolaryngology, plastic surgery, psychiatry, pulmonology, and related specialties. This Nano split is strongly multi-positive, making it a useful test of both evidence ranking and broad clinical candidate coverage.

## Details

### What the Original Data Measures

CURE measures clinical retrieval for healthcare providers. The original benchmark contains expert-written queries and article-derived passages, with relevance labels for passages that answer or partially address the clinical information need. Unlike general biomedical search, CURE is oriented toward practical clinical questions, including treatment choice, surgical technique, contraindications, diagnosis, and specialty-specific evidence.

The source corpus is drawn from biomedical articles, so documents usually contain article titles followed by evidence-bearing passages. The task requires linking a concise clinical question to the relevant passage content, not only to a shared medical topic.

### Observed Data Profile

The Nano split contains 200 queries, 10,000 documents, and 5,181 positive qrel rows. Queries have 25.905 positives on average, with a median of 18 and a maximum of 100. There are 171 multi-positive queries, or 85.5% of the query set. Queries average 75.89 characters, while documents average 604.21 characters.

The examples include intermaxillary fixation screw placement, 3D printed splints in orthognathic surgery, endoscopic treatment of massive arterial epistaxis, temporomandibular joint symptoms, and tooth whitening compounds. Many documents contain specialist terminology, abbreviations, study-design language, and clinical outcome statements.

### BM25 Evaluation Profile

The BM25 candidate subset uses top-500 candidates and reaches nDCG@10 of 0.4693, hit@10 of 0.9000, and recall@100 of 0.5314. BM25 is useful because clinical questions often repeat procedure names, anatomy, abbreviations, and treatment terms. It can usually find at least one relevant passage for many queries.

The main limitation is fine-grained clinical relevance. Shared medical terminology does not guarantee that a passage answers the exact clinical question. Abbreviations can be ambiguous, and same-topic passages may differ by indication, contraindication, patient population, outcome, or procedure step.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses top-500 candidates and reaches nDCG@10 of 0.5003, hit@10 of 0.8700, and recall@100 of 0.5862. Dense retrieval improves nDCG@10 and recall@100 over BM25, but BM25 has a slightly higher hit@10. This indicates complementary strengths: dense retrieval better captures clinical meaning and passage-level evidence, while sparse retrieval can still find exact terminology quickly.

The dense gains are important because many questions ask for implications or clinical relations that are not expressed with identical wording in the passage.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates, with 14 queries carrying a rank-101 safeguard positive. It reaches nDCG@10 of 0.5262, hit@10 of 0.9000, and recall@100 of 0.6126. This is the strongest overall profile, combining BM25's exact clinical term coverage with dense retrieval's semantic evidence matching.

The hybrid pool is therefore a strong candidate source for reranking. It exposes more relevant clinical passages while preserving high first-page hit behavior.

### Metric Interpretation for Model Researchers

This is a many-positive clinical retrieval task. Hit@10 indicates whether the system finds at least one useful passage, but recall@100 is essential because a clinical question may have many valid passages across studies. nDCG@10 measures whether high-quality evidence appears early enough for a provider-facing search workflow.

Hybrid retrieval is the best candidate-generation baseline in this split, while dense retrieval provides the strongest standalone semantic signal.

### Query and Relevance Type Tendencies

Queries are concise clinical questions, often asking "which", "what", "how", or "is" about procedures, symptoms, contraindications, measurements, or treatment implications. Relevant documents are biomedical article-title plus passage snippets.

The relevance relation is clinical answerability. A passage should answer the clinical information need or supply relevant evidence, not merely mention the same disease or procedure.

### Representative Failure Modes

Common failures include abbreviation ambiguity, retrieving a same-procedure passage with the wrong clinical relation, confusing indication and contraindication, missing specialty-specific terminology, and over-ranking broad review passages. Sparse systems may over-match procedure names; dense systems may under-rank exact acronyms or rare specialist terms.

### Training Data That May Help

Useful training data includes non-overlapping clinical question-to-passage pairs, biomedical evidence retrieval data, medical QA retrieval data with passage-level grounding, and clinical abbreviation or specialty-specific hard-negative training. CURE evaluation queries, CURE positive passages, and near-duplicate mined biomedical passages should be excluded for clean evaluation.

### Model Improvement Notes

Models should preserve exact clinical terminology while improving semantic relation matching. Hard negatives should share the same medical topic but differ by diagnosis, treatment, contraindication, patient context, or outcome. Multi-positive training is important because many questions have numerous relevant passages.

## Example Data

### Public Sources

- [CURE: A Dataset for Clinical Understanding & Retrieval Evaluation](https://arxiv.org/abs/2412.06954), 2024.
- [CURE KDD DOI record](https://doi.org/10.1145/3711896.3737435), 2025.
- [clinia/CUREv1](https://huggingface.co/datasets/clinia/CUREv1), source dataset.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| CURE: A Dataset for Clinical Understanding & Retrieval Evaluation | 2024 | arXiv paper | https://arxiv.org/abs/2412.06954 |
| CURE: A Dataset for Clinical Understanding & Retrieval Evaluation | 2025 | KDD proceedings DOI | https://doi.org/10.1145/3711896.3737435 |
| clinia/CUREv1 | 2024 | source dataset | https://huggingface.co/datasets/clinia/CUREv1 |

### Representative Snippets

| Query | Relevant document excerpt |
| --- | --- |
| Which are the factors that should be taken in consideration when deciding the location of IMF screws placement? | A passage about MMF screw placement, chosen with respect to fracture location and surgical considerations. |
| Which are the disadvantages of 3D printed splints in orthognathic surgery? | A passage comparing additive and subtractive CAD-CAM techniques for producing orthognathic surgical splints. |
| Which are the advantages of endoscopic approach to treat massive arterial epistaxis? | A passage about endoscopic sphenopalatine artery ligation for refractory posterior epistaxis. |
| What are the typical temporomandibular joint symptoms that can appear in a patient undergoing maxillomandibular advancement? | A passage describing temporomandibular chronic dislocation and related clinical presentation. |
| What are the primary compounds used in tooth whitening products? | A passage discussing sodium bicarbonate, hydrogen peroxide, and enamel whitening effects. |
