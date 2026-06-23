# NanoRTEB / NanoCUREv1

## Overview

`NanoCUREv1` is an English clinical and biomedical passage retrieval task from NanoRTEB. The query is a short clinician-oriented medical question, and relevant documents are biomedical passages that can support the answer. The task is strongly multi-positive, with many relevant passages per query. BM25 is already strong because clinical terminology is distinctive, dense retrieval improves nDCG@10 and recall@100, and `reranking_hybrid` is the strongest overall profile by combining medical term overlap with semantic evidence matching.

## Details

### What the Original Data Measures

CURE is a clinical understanding and retrieval evaluation dataset designed for point-of-care information needs. It includes expert-written queries spanning multiple medical domains, with relevant passages drawn from clinical and biomedical sources.

RTEB includes the English CUREv1 subset as a realistic biomedical retrieval benchmark. The Nano task asks whether models can retrieve useful evidence passages for concise clinical questions.

### Observed Data Profile

The Nano split contains 182 queries, 10,000 documents, and 5,163 positive qrel rows. Queries average 77.16 characters, while documents average 603.96 characters. Positives per query average 28.37, with a minimum of 1, a median of 20, and a maximum of 100. There are 171 multi-positive queries, about 93.96% of the split.

Example questions ask about self-cutting or self-drilling screws, bad splits in sagittal split osteotomies, endoscopic treatment of massive arterial epistaxis, white spot lesions from fixed orthodontic appliances, and dental injuries associated with facial fractures.

### BM25 Evaluation Profile

The BM25 candidate subset uses top-500 candidates and reaches nDCG@10 of 0.5102, hit@10 of 0.9835, and recall@100 of 0.5326. BM25 performs well because medical terminology, procedure names, anatomical terms, and disease names often appear in both the query and relevant passages.

The limitation is ranking among many positives and near-positives. A passage can share terms with the question but discuss a different clinical relation, study endpoint, or patient setting. BM25 is good at finding at least one relevant passage, but not sufficient for ordering the best evidence.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses top-500 candidates and reaches nDCG@10 of 0.5479, hit@10 of 0.9615, and recall@100 of 0.5838. Dense retrieval improves top-rank relevance and coverage, although BM25 has a slightly higher hit@10.

This suggests that embedding similarity helps connect short clinical questions to explanatory passages when exact wording differs. Dense retrieval can also group evidence by medical relation, not just shared terminology.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates, with 1 row receiving the optional rank-101 safeguard. It reaches nDCG@10 of 0.5688, hit@10 of 0.9890, and recall@100 of 0.6122. Hybrid retrieval is the strongest reported profile on all broad evidence-access metrics.

The result matches biomedical retrieval behavior. Sparse retrieval anchors rare clinical terms, while dense retrieval captures paraphrase and evidence relation. The combined pool is the best first-stage candidate source for reranking.

### Metric Interpretation for Model Researchers

Because most queries have many positives, nDCG@10 is more informative than hit@10. Hit@10 is nearly saturated for BM25 and hybrid retrieval, while recall@100 measures how much of the broad evidence set is available.

For `NanoCUREv1`, a strong model should retrieve several clinically relevant passages early, not just one passage containing the right terminology. Ranking quality matters because clinicians need high-quality evidence quickly.

### Query and Relevance Type Tendencies

Queries are concise clinical questions. Relevant documents are biomedical passages, often including study titles, clinical observations, or review-like evidence. Many positives can answer or support the same information need from different sources.

Relevance is evidence usefulness for the clinical question. A passage can share terminology and still be non-relevant if it addresses a different clinical outcome or context.

### Representative Failure Modes

Common failures include overranking passages with matching procedure names but wrong outcomes, missing paraphrased clinical evidence, confusing anatomical or dental terms, and retrieving broad background passages instead of answer-supporting evidence. BM25 is vulnerable to term overlap; dense retrieval can underweight rare medical terms.

### Training Data That May Help

Useful training data includes clinical passage retrieval, biomedical evidence retrieval, medical QA with cited passages, PubMed-style search logs, and hard negatives from the same disease, procedure, or specialty. Evaluation queries, passages, and qrels should be excluded.

### Model Improvement Notes

Models should preserve rare biomedical terminology while learning question-to-evidence relations. Hard negatives should share the main diagnosis, procedure, or anatomy but answer a different clinical relation. Hybrid retrieval is especially appropriate because both exact terms and semantic evidence matching are important.

## Example Data

| Query | Positive document |
| --- | --- |
| What are self/cutting or self-drilling screws? [46 chars] | The Use of MMF Screws: Surgical Technique, Indications, Contraindications, and Common Problems in Review of the Literature Self-cutting or self-drilling screws have a drill-shaped point to penetrate t... [200 / 231 chars] |
| Where is the bad split in sagittal split osteotomies of the mandible usually located during orthogna... [100 / 113 chars] | Dal Pont vs Hunsuck: Which Technique Can Lead to a Lower Incidence of Bad Split during Bilateral Sagittal Split Osteotomy? A Triple-blind Randomized Clinical Trial Older age is definitely correlated t... [200 / 1,064 chars] |
| Which are the advantages of endoscopic approach to treat massive arterial epistaxis? [84 chars] | Success Rate of Endoscopic Sphenopalatine Artery Ligation for the Management of Refractory Posterior Epistaxis Patients in a Tertiary Care Hospital: A Descriptive Cross-sectional Study The findings of... [200 / 613 chars] |
| How do fixed orthodontic appliances contribute to the development of white spot lesions? [88 chars] | In-vivo durability of a fluoride-releasing sealant (OpalSeal) for protection against white-spot lesion formation in orthodontic patients The results of this study provide some evidence on the abatemen... [200 / 1,370 chars] |
| What is the most frequent type of dental injury when anterior and buccal teeth are associated with f... [100 / 116 chars] | Traumatic Dental Injury—An Enigma for Adolescents: A Series of Case Reports Coronal fractures of permanent dentition are the most frequent type of dental injury. Fractured anterior teeth are usually t... [200 / 733 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| CURE: A Dataset for Clinical Understanding & Retrieval Evaluation | 2024 | task paper | [https://arxiv.org/abs/2412.06954](https://arxiv.org/abs/2412.06954) |
| CURE ACM proceedings record | 2025 | proceedings record | [https://doi.org/10.1145/3711896.3737435](https://doi.org/10.1145/3711896.3737435) |
| clinia/CUREv1 | 2025 | dataset card | [https://huggingface.co/datasets/clinia/CUREv1](https://huggingface.co/datasets/clinia/CUREv1) |
| Introducing RTEB: A New Standard for Retrieval Evaluation | 2025 | benchmark article | [https://huggingface.co/blog/rteb](https://huggingface.co/blog/rteb) |

### Representative Snippets

| Query | Relevant document excerpt |
| --- | --- |
| What are self-cutting or self-drilling screws? | A passage explains that these screws use a drill-shaped point to penetrate bone. |
| Where is the bad split in sagittal split osteotomies usually located? | A passage discusses bad split risk during bilateral sagittal split osteotomy. |
| What are advantages of endoscopic treatment for massive arterial epistaxis? | A passage describes endoscopic sphenopalatine artery ligation outcomes. |
| How do fixed orthodontic appliances contribute to white spot lesions? | A passage discusses sealants and protection against white spot lesion formation. |
| What is the most frequent dental injury with facial fractures? | A passage identifies coronal fractures of permanent dentition as frequent. |
