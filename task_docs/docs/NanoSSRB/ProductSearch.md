# NanoSSRB / ProductSearch

## Overview

ProductSearch evaluates attribute-aware retrieval over JSON records for goods
and services, including vehicles, books, restaurants, electronics, and other
catalog entities. It contains 200 English queries, 10,000 documents, and 600
positive qrels. Requests combine category, brand, price, date, availability,
rating, opening hours, capacity, or technical attributes with softer preferences
such as reliability, popularity, safety, or suitability. A relevant result must
meet the full shopping intent, not merely describe a related product.

## Details

### What the Original Data Measures

SSRB studies direct natural-language querying of semi-structured objects.
ProductSearch is the clearest consumer-search instance: structured filters and
subjective needs appear together in one request.

### Observed Data Profile

Queries average 232 characters and documents 628 characters, with three
positives per query. Examples ask for restaurants open on a day, novels after a
date, or vehicles satisfying price, capacity, safety, fuel, and category rules.

### BM25 Evaluation Profile

BM25 reaches 0.3839 nDCG@10, 0.7250 hit@10, and 0.8783 Recall@100. Brands,
categories, cuisines, and attributes provide strong lexical anchors, but
subjective preferences and numeric filters remain error-prone.

### Dense Evaluation Profile

Dense retrieval is strongest at 0.5305 nDCG@10, 0.8050 hit@10, and 0.9583
Recall@100. It captures suitability and product-intent paraphrases well, though
it may still rank an attractive item that violates one hard filter.

### Reranking Hybrid Evaluation Profile

Hybrid reaches 0.5132 nDCG@10, 0.8200 hit@10, and 0.9633 Recall@100. It gives
the best coverage and hit rate, while dense retains slightly better top-ten
ordering on this candidate profile.

### Metric Interpretation for Model Researchers

Recall@100 measures catalog coverage before reranking; nDCG@10 measures whether
the most compliant items surface first. Dense strength indicates semantic
shopping intent matters. Compare dense and hybrid to determine whether lexical
attributes add useful candidates or introduce near-match noise.

### Query and Relevance Type Tendencies

Queries range from simple category-plus-hours filters to long multi-attribute
requests with exclusions and subjective priorities. Relevant items satisfy all
hard constraints and plausibly meet the semantic preference expressed by the
query.

### Representative Failure Modes

Models may return the right product family at the wrong price, ignore a day or
availability field, treat review praise as proof of a missing attribute, or
overweight one appealing semantic property. Nested attributes and units create
additional relation errors.

### Product-Search Notes

Normalize currencies, dates, units, rating scales, category aliases, and brand
names without erasing distinctions. Reviews can support fuzzy preferences but
should not override authoritative structured fields.

### Training and Leakage Notes

Exclude evaluation catalog objects, queries, and qrels, and disclose SSRB
exposure. Product feeds are duplication-heavy, so audit normalized attributes
and descriptions rather than relying only on IDs.

### Model Improvement Hints

Combine semantic product embeddings with explicit attribute matching and
constraint-aware reranking. Use hard negatives from the same category that
violate exactly one price, date, capacity, availability, or exclusion rule.

### Training Data That May Help

Non-overlapping shopping-query logs, catalog search pairs, product QA, and
attribute extraction data can help when licensing and leakage are controlled.

### Synthetic Data Guidance

Generate independent catalogs and grounded shopping requests with realistic
attributes and preferences. Create single-filter counterfactuals; never use
evaluation products or queries as seeds.

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
| Find restaurants that serve Italian cuisine and are open on Sundays. [68 chars] | { "cuisine_type": "Italian", "menu_items": [ { "name": "Spaghetti Carbonara", "price": 15.99 }, { "name": "Margherita Pizza", "price": 12.5 } ], "opening_hours": { "Monday": "11:00 AM - 10:00 PM", "Tuesday": "11:00 AM - 10:00 PM", "Wednesday": "11:00 AM - 10:00 PM", "Thursday": "11:00 AM - 10:00 PM", "Friday": "11:00 AM - 11:00 PM", "Saturday": "11:00 AM - 11:00 PM", "Sunday": "12:00 PM - 9:00 PM" }, "location": "123 Main Street, Anytown", "product_id": null, "product_name": null, "brand": null, "category": null, "price": null, "availability": null, "rating": 4.5, "reviews": [ { "review_text": "Great Italian food!", "reviewer_name": "John Doe" } ], "release_date": null, "attributes": null } [943 chars] |
| Find me a thriller or mystery novel published after January 1, 2010, and written by a popular author. I'm looking for something really gripping. [144 chars] | { "author": "Gillian Flynn", "publisher": "Crown", "publication_date": "2012-06-05", "genre": [ "thriller", "mystery", "psychological thriller" ], "product_id": "978-0307588371", "product_name": "Gone Girl", "brand": null, "category": "Books", "price": 12.99, "availability": true, "rating": 4.5, "reviews": [ { "review_text": "A truly gripping and suspenseful read!", "reviewer_name": "Jane Doe" } ], "release_date": "2012-06-05", "attributes": null } [580 chars] |
| I'm looking for a reliable family car with good gas mileage and safety features for commuting and weekend trips. I need a vehicle that's a sedan or SUV, with at least 5 seats, a price under $35,000, and a good safety rating. I also prefer something relatively new, released after 2020, and ideally from a well-regarded brand known for longevity. I'm not really interested in electric vehicles at this time. [406 chars] | { "product_id": "FMLY-CR-2024", "product_name": "ComfortRide Family Sedan", "brand": "AutoNova", "category": "Sedan", "engine_type": "Petrol", "vehicle_type": "Sedan", "fuel_efficiency": 32.5, "seat_capacity": 5, "price": 32000.0, "availability": true, "rating": 4.5, "release_date": "2024-03-15", "attributes": { "color": "Silver", "safety_features": [ "ABS", "Airbags", "Lane Departure Warning" ] }, "reviews": [ { "review_text": "Great car for families, very comfortable and fuel efficient!", "reviewer_name": "Jane Doe" } ] } [693 chars] |
