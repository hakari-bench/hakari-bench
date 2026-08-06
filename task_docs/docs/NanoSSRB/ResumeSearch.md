# NanoSSRB / ResumeSearch

## Overview

ResumeSearch evaluates retrieval over long JSON candidate and resume records.
Its 200 English queries search 10,000 documents with 647 positive qrels. Hiring
requirements combine roles, years of experience, skills, tools, education,
certifications, domain achievements, availability, and explicit exclusions.
Evidence is distributed across nested employment, project, education, and skill
fields, so the task tests both semantic candidate matching and exact
qualification checking. A topically plausible candidate who lacks one mandatory
skill or minimum duration is a hard negative.

## Details

### What the Original Data Measures

The SSRB paper's exact-plus-fuzzy retrieval formulation is especially visible
in hiring search: broad fit and hard qualifications must be evaluated together
across heterogeneous profile schemas.

### Observed Data Profile

ResumeSearch has the longest queries (443 characters on average) and documents
(1,356 characters), with 3.24 positives per query. Examples combine campaign
outcomes and marketing tools, teaching background and exclusions, or degrees,
cloud skills, experience, and start dates.

### BM25 Evaluation Profile

BM25 reaches 0.3297 nDCG@10, 0.6950 hit@10, and 0.8825 Recall@100. Skill names,
degrees, titles, and tools anchor candidates well, but lexical overlap does not
verify duration, achievement, negation, or equivalent experience.

### Dense Evaluation Profile

Dense retrieval reaches 0.3184 nDCG@10, 0.6850 hit@10, and 0.8377 Recall@100.
Semantic role matching helps with paraphrases but loses some exact skill and
credential coverage relative to BM25.

### Reranking Hybrid Evaluation Profile

Hybrid is strongest at 0.3896 nDCG@10, 0.7750 hit@10, and 0.9196 Recall@100.
The substantial gain shows that resume search benefits from retaining exact
skills while adding semantic evidence about duties and achievements.

### Metric Interpretation for Model Researchers

Recall@100 measures whether qualified candidates survive the first stage;
nDCG@10 measures whether the best-qualified profiles rank early. Hybrid gains
should motivate lexical-semantic fusion. With multiple valid candidates,
partial recall can still support screening but does not represent complete
candidate discovery.

### Query and Relevance Type Tendencies

Queries include mandatory skills, minimum years, education, certifications,
tools, industry experience, quantified outcomes, availability, and negative
requirements. Relevant resumes provide evidence for the combined role rather
than merely repeating the job title.

### Representative Failure Modes

Typical errors include counting overlapping jobs twice, matching a skill only
mentioned in passing, confusing education with work experience, ignoring an
exclusion, or overlooking availability. Long profiles can bury disqualifying
details far from strong semantic evidence.

### Resume-Search Notes

Preserve skill and certification names, dates, durations, quantities, and
negation. Models should connect synonymous job duties while keeping claimed
experience distinct from requirements, interests, or unrelated project text.

### Training and Leakage Notes

Exclude NanoSSRB profiles, queries, qrels, and transformed source-test records.
Disclose SSRB exposure and use privacy-safe, licensed, or synthetic resumes;
benchmark improvement does not justify collecting sensitive personal data.

### Model Improvement Hints

Use long-record field pooling, timeline-aware duration features, requirement-to-
evidence alignment, and hard negatives missing one mandatory qualification.
Rerankers should produce constraint-level evidence rather than one global fit
score.

### Training Data That May Help

Independent job-to-resume matching, skill normalization, career taxonomy, and
qualification extraction data can help when privacy and overlap are controlled.

### Synthetic Data Guidance

Generate fictional resumes and grounded job requirements with explicit
timelines, skills, achievements, and exclusions. Create counterfactual profiles
that fail one requirement; never seed from evaluation resumes.

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
| We're looking for a seasoned marketing professional to lead our upcoming product launch. We need someone with a proven track record of exceeding sales targets and deep expertise in digital marketing. Specifically, we're seeking candidates who have managed at least 3 marketing campaigns focused on B2B SaaS products and are proficient in both Salesforce and Marketo. Ideally, we'd like someone with a strong analytical mindset, someone who doesn't just execute but understands *why* campaigns succeed... [500 / 509 chars] | { "sales_targets_met": 12, "marketing_campaign_experience": [ { "objective": "Increase lead generation for B2B SaaS product", "strategies": "SEO, content marketing, PPC", "outcomes": "30% increase in qualified leads" }, { "objective": "Drive product adoption among existing B2B SaaS customers", "strategies": "Email marketing, webinars, in-app messaging", "outcomes": "20% increase in product usage" }, { "objective": "Expand market share in the enterprise B2B SaaS segment", "strategies": "Account-based marketing, thought leadership content", "outcomes": "15% increase in enterprise deals" } ], "customer_relationship_management_tools": [ "Salesforce", "Marketo" ], "branding_experience": "Extensive experience in developing and executing brand strategies.", "digital_marketing_expertise": [ "SEO", "PPC", "Social Media Marketing", "Content Marketing", "Email Marketing" ], "market_research_methods": [ "Surveys", "Focus Groups", "Competitive Analysis" ], "name": "Alice Johnson", "contact_informat... [1,000 / 1,830 chars] |
| We are a private school seeking a highly qualified and experienced high school science teacher to join our team. We need someone with a strong background in biology and chemistry, capable of developing engaging curriculum, and proficient in utilizing modern educational tools. Specifically, we need a teacher with at least 5 years of teaching experience, who has experience with project-based learning, is comfortable teaching AP courses, and doesn’t have administrative experience. We are looking fo... [500 / 787 chars] | { "teaching_subjects": [ "Biology", "Chemistry", "Physics" ], "curriculum_development": "Designed and implemented new curriculum for AP Biology, resulting in a 15% increase in student scores.", "student_engagement_strategies": "Utilized project-based learning and differentiated instruction to cater to diverse learning styles.", "educational_tools": [ "Google Classroom", "Khan Academy", "Interactive Whiteboard" ], "academic_administration_roles": [], "published_works": [], "name": "Jane Doe", "contact_information": { "email": "jane.doe@email.com", "phone_number": "555-123-4567", "address": "123 Main St, Anytown, USA" }, "education": [ { "degree": "Master of Science in Biology", "university": "State University", "graduation_date": "2018" } ], "experience": [ { "role": "High School Science Teacher", "company": "Anytown High School", "duration": "2018 - Present" } ], "skills": [ "Curriculum Development", "Differentiated Instruction", "Classroom Management", "Educational Technology" ], "cer... [1,000 / 1,606 chars] |
| Find a data scientist proficient in Python and SQL, with at least 3 years of experience, who has completed a Master's degree and is available to start within the next month. I am looking for candidates who have experience with AWS cloud services. [[The current time is 2023-12-20]] [282 chars] | { "name": "Alice Johnson", "contact_information": { "email": "alice.johnson@email.com", "phone_number": "555-123-4567" }, "education": [ { "degree": "Master of Science in Data Science", "university": "Stanford University", "graduation_year": "2021" } ], "experience": [ { "title": "Data Scientist", "company": "Tech Solutions Inc.", "start_date": "2021-06-01", "end_date": "2023-12-31", "description": "Developed and deployed machine learning models for time series forecasting using Python and AWS services. Extensive experience with SQL databases." } ], "skills": [ "Python", "SQL", "Machine Learning", "Data Analysis", "Time Series Analysis" ], "cloud_services": [ "AWS", "S3", "EC2" ], "data_analysis_tools": [ "Python", "Pandas", "Scikit-learn" ], "availability": "2024-01-01" } [1,071 chars] |
