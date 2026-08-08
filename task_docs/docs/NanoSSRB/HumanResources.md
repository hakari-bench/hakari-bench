# NanoSSRB / HumanResources

## Overview

HumanResources evaluates retrieval over employee, organization, role, payroll,
benefit, feedback, policy, and workplace-activity JSON. The task contains 200
English queries, 10,000 documents, and 578 positive qrels. Queries mix exact
employee or department fields, dates, hours, ratings, tenure, and benefit
amounts with semantic conditions such as urgency, collaboration, or key-person
status. Relevant records must satisfy nested policy and employee constraints,
making same-department or same-topic matches insufficient.

## Details

### What the Original Data Measures

SSRB evaluates whether neural retrievers can follow complex natural-language
conditions across varying schemas. HR makes those conditions operational and
often distributes them across nested employee, project, and benefit fields.

### Observed Data Profile

Queries average 321 characters and documents 359 characters, with 2.89
positives per query. Examples target overtime on critical projects, positive
feedback in a date window, or benefits conditioned on tenure and coverage.

### BM25 Evaluation Profile

BM25 reaches 0.1704 nDCG@10, 0.4000 hit@10, and 0.6332 Recall@100. Employee IDs,
departments, and policy terms anchor search, but indirect performance or urgency
conditions are poorly represented by lexical overlap.

### Dense Evaluation Profile

Dense retrieval reaches 0.2451 nDCG@10, 0.5550 hit@10, and 0.7249 Recall@100.
Semantic matching helps with feedback and role intent but may overlook exact
hours, ratings, dates, or eligibility requirements.

### Reranking Hybrid Evaluation Profile

Hybrid is strongest at 0.2776 nDCG@10, 0.5450 hit@10, and 0.7578 Recall@100.
Its higher recall shows complementary lexical and semantic candidates, while
top-ten misses still reveal incomplete constraint checking.

### Metric Interpretation for Model Researchers

Use Recall@100 to assess whether all eligible records reach the reranker and
nDCG@10 to assess final policy compliance. Hybrid gains suggest value from
combining identifiers and semantic descriptions. With multiple positives,
partial coverage may still give useful results but should not be mistaken for
complete employee search.

### Query and Relevance Type Tendencies

Queries combine identity, organization, time, performance, compensation, and
policy conditions. Relevant records can be time entries, feedback, benefits,
employee profiles, or rules, so the model must identify both schema and values.

### Representative Failure Modes

Errors include matching the right employee but wrong period, treating generic
praise as collaboration evidence, ignoring a minimum tenure, or confusing
covered amount with another monetary field. Nested fields make relation errors
especially likely.

### HR-Specific Notes

Identifiers, employment dates, hours, ratings, and organizational roles should
be preserved exactly. Semantic encoders must distinguish evidence about an
employee from eligibility rules or descriptions attached to a benefit.

### Training and Leakage Notes

Exclude benchmark records and disclose SSRB-derived training. Use privacy-safe
synthetic or properly licensed HR data; do not introduce real sensitive
employee information merely to improve benchmark performance.

### Model Improvement Hints

Train schema routing and nested-field alignment together. Use negatives that
share employee, department, or policy vocabulary but violate one date, rating,
tenure, project, or benefit constraint.

### Training Data That May Help

Independent enterprise-search pairs, policy QA, job catalogs, and synthetic HR
record retrieval can help when privacy and overlap are controlled.

### Synthetic Data Guidance

Generate fictional organizations and grounded HR requests across time entries,
feedback, benefits, and roles. Add counterfactual records with one failed
condition; never seed from evaluation objects.

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
| We need to find time entries for employees working on urgent projects during the last week of November 2023. Specifically, I'm looking for records where the employee worked more than 8 hours and the project is considered high priority, meaning it's related to critical system maintenance or resolving major client issues. Please provide time entries for employee with id 'EMP123' who worked on 'critical' projects. [414 chars] | { "time_entry_id": "TE0045", "employee_id": "EMP123", "clock_in_time": "2023-11-27T09:00:00", "clock_out_time": "2023-11-27T17:30:00", "total_hours_worked": 8.5, "overtime_hours": 1.5, "project_code": "CRITICAL-OUTAGE-01" } [251 chars] |
| We are analyzing employee feedback to identify areas for improvement and recognize high performers. I need to find feedback records from the last quarter (October 1, 2023 - December 31, 2023) specifically for employees in the Sales department, with a rating of 4 or higher, and where the feedback highlights positive contributions to team collaboration. I want to focus on feedback that sounds genuinely appreciative. [417 chars] | { "feedback_id": "FB20231115-001", "employee_id": "EMP1234", "feedback_date": "2023-11-15", "feedback_provider": "Jane Doe", "feedback_type": "Peer Review", "comments": "John has been an incredible asset to our team this quarter. He consistently volunteers to help others, shares his knowledge generously, and fosters a very collaborative environment. His positive attitude is infectious, and he always goes the extra mile to ensure everyone feels supported. His contributions were instrumental in the successful completion of the Alpha project.", "rating": 5 } [589 chars] |
| We are reviewing employee benefits to ensure we're offering competitive packages, particularly for long-term employees with significant health needs. I need to find all health insurance benefits that started within the last 5 years, cover over $5000, are associated with employees who have been with the company for at least a decade, and ideally provide comprehensive coverage for chronic conditions. Also, show me benefits for employees who are considered high performers or key personnel. Finally,... [500 / 637 chars] | { "benefit_id": "B-12345", "employee_id": "E-67890", "benefit_type": "Health Insurance", "benefit_details": { "coverage_type": "Comprehensive", "description": "Includes coverage for long-term care, hospitalization, and preventative care. High performance employees are eligible for additional benefits.", "long_term_care_details": "Up to $10,000 per year for qualified long-term care expenses." }, "start_date": "2022-05-15", "end_date": "2024-12-31", "amount_covered": 6500.0 } [534 chars] |
