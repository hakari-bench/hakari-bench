# NanoSSRB / Academic

## Overview

Academic evaluates natural-language retrieval over JSON records for grants,
researchers, publications, collaborations, competitions, workshops, and related
academic activities. Its 200 English queries search 10,000 records with 600
positive qrels. A request can combine an exact funder, amount threshold,
institution age, deadline, degree, or research field with a semantic preference
such as innovation, healthcare relevance, or a strong publication record.
Relevant objects must satisfy the combined conditions, so an academically
similar record can still be wrong. BM25 benefits from named institutions and
funding agencies; dense retrieval handles paraphrased expertise and purpose;
hybrid candidates combine both signals.

## Details

### What the Original Data Measures

The [SSRB paper](https://papers.neurips.cc/paper_files/paper/2025/hash/631bbd89466337712564872840a401be-Abstract-Datasets_and_Benchmarks_Track.html)
defines retrieval over heterogeneous semi-structured objects using queries that
mix exact and fuzzy conditions. Academic applies that formulation to multiple
academic schemas rather than treating all records as one fixed table.

### Observed Data Profile

Queries average 298 characters and documents average 900 characters. The three
positives per query often share a schema but vary in field layout. Examples ask
for NIH grants above a threshold, professors with specified expertise and
education, or competitions constrained by audience and deadline.

### BM25 Evaluation Profile

BM25 reaches 0.2975 nDCG@10, 0.6100 hit@10, and 0.8433 Recall@100. Exact agency,
institution, discipline, and award terms provide good anchors, but lexical
matching struggles when suitability is expressed indirectly.

### Dense Evaluation Profile

Dense retrieval reaches 0.4910 nDCG@10, 0.7850 hit@10, and 0.9467 Recall@100.
It connects paraphrased research interests and goals, though a semantic match
may still violate a numeric, date, or exclusion constraint.

### Reranking Hybrid Evaluation Profile

Hybrid reaches 0.4873 nDCG@10, 0.7900 hit@10, and 0.9433 Recall@100. It improves
hit rate slightly over dense while retaining exact anchors, but its top-rank
quality remains close to the dense profile.

### Metric Interpretation for Model Researchers

nDCG@10 measures whether fully qualifying records appear early; Recall@100
shows whether the first stage covers all valid alternatives. Dense gains over
BM25 indicate that academic intent and expertise paraphrases matter. Inspect
constraint failures when recall is high but nDCG is low.

### Query and Relevance Type Tendencies

Queries cover entity lookup, range filtering, temporal conditions, research
topic matching, and multi-field qualification. Relevant records satisfy both
literal fields and the stated academic purpose; topical neighbors that miss one
condition are not interchangeable positives.

### Representative Failure Modes

Typical errors include retrieving the right field but wrong amount, confusing
related research areas, ignoring a negated interest, or ranking an expired
competition. Long nested records can dilute the one field that disqualifies an
otherwise convincing match.

### Academic-Domain Notes

Models should preserve acronyms, institution names, grant identifiers, dates,
and money values while linking broader and narrower research terminology.
Hierarchy-aware encoding helps distinguish a research interest from a degree,
publication title, or project objective.

### Training and Leakage Notes

Exclude NanoSSRB queries, qrels, positives, and source-test objects. Disclose
training on SSRB or `vec-ai/struct-ir`. Near-duplicate synthetic profiles with
changed constraints are particularly important to audit.

### Model Improvement Hints

Use field-aware serialization, numeric/date representations, conjunction-aware
training, and hard negatives that violate exactly one condition. Rerankers
should compare every requested constraint against its corresponding field.

### Training Data That May Help

Independent grant databases, publication search pairs, scholarly profiles, and
academic-event catalogs can help when evaluation records are excluded.

### Synthetic Data Guidance

Generate independent academic schemas and grounded requests with explicit and
semantic constraints. Include near-matches with the wrong funder, date, amount,
topic, or institution; never seed generation from evaluation positives.

### Public Sources

- [SSRB: Direct Natural Language Querying to Massive Heterogeneous Semi-Structured Data](https://papers.neurips.cc/paper_files/paper/2025/hash/631bbd89466337712564872840a401be-Abstract-Datasets_and_Benchmarks_Track.html), 2025.
- [vec-ai/struct-ir](https://huggingface.co/datasets/vec-ai/struct-ir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoSSRB](https://huggingface.co/datasets/hakari-bench/NanoSSRB)
- Source dataset: [vec-ai/struct-ir](https://huggingface.co/datasets/vec-ai/struct-ir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| SSRB: Direct Natural Language Querying to Massive Heterogeneous Semi-Structured Data | 2025 | benchmark paper | [NeurIPS](https://papers.neurips.cc/paper_files/paper/2025/hash/631bbd89466337712564872840a401be-Abstract-Datasets_and_Benchmarks_Track.html) |
| vec-ai/struct-ir | 2025 | source dataset | [Hugging Face](https://huggingface.co/datasets/vec-ai/struct-ir) |

## Example Data

| Query | Positive document |
| --- | --- |
| Find grants funded by the National Institutes of Health (NIH) with an amount greater than $500,000. [99 chars] | { "grant_title": "Advancing Population Health Through Big Data Analytics", "grant_number": "R01MH123456", "principal_investigator": { "name": "Dr. Alice Johnson", "institution": "Harvard University" }, "funding_agency": "NIH", "amount": 750000.0, "start_date": "2023-03-15", "end_date": "2028-03-14", "research_fields": [ "Public Health", "Data Science", "Epidemiology", "Bioinformatics" ], "objectives": [ "Develop novel machine learning models for disease prediction.", "Analyze large-scale health datasets to identify risk factors.", "Improve public health interventions through data-driven insights." ] } [728 chars] |
| I am looking for a professor at a top university who specializes in artificial intelligence and machine learning, particularly those with a focus on applications in healthcare. I'd prefer someone who has a strong publication record and has been awarded a PhD from a highly-regarded institution. Specifically, I need someone affiliated with an institution founded before 1950 and whose research interests include 'deep learning' but *not* 'natural language processing'. Furthermore, I’m interested in... [500 / 737 chars] | { "name": "Andrew Ng", "institution": "Stanford University", "department": "Computer Science", "research_interests": [ "Machine Learning", "Deep Learning", "Artificial Intelligence", "Healthcare AI" ], "publications": [ { "title": "Deep learning for medical image analysis", "year": "2023" }, { "title": "AI-powered diagnosis systems", "year": "2024" } ], "contact_email": "andrew.ng@stanford.edu", "office_location": "Gates Computer Science Building", "profile_url": "https://ai.stanford.edu/~ang/", "education": [ { "degree": "PhD", "institution": "MIT", "field": "Computer Science" } ] } [802 chars] |
| I'm a university student looking for design competitions with good prize money to help fund my final year project. I'd like to find competitions open to undergraduates and graduate students with submission deadlines in the next three months, and I'm particularly interested in competitions that appear challenging or innovative. Can you show me some relevant options? [[The current time is 2024-04-10]] [403 chars] | { "competition_title": "Global Innovation Design Challenge", "organizing_body": "IDEO Futures Foundation", "submission_deadline": "2024-07-15", "competition_date": "2024-08-20", "competition_type": "Design", "eligibility_criteria": "Currently enrolled undergraduate or graduate student at a university.", "prizes": [ { "type": "Cash Prize", "value": "$10,000" }, { "type": "Internship", "value": "Paid internship at IDEO" } ], "registration_url": "https://www.ideofutures.org/designchallenge" } [610 chars] |
