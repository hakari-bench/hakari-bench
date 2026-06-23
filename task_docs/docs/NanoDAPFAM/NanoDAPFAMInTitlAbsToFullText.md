# NanoDAPFAM / NanoDAPFAMInTitlAbsToFullText

## Overview

NanoDAPFAMInTitlAbsToFullText is an English patent-family retrieval task. The query contains a source patent family's title and abstract, and the target document contains the full text of a candidate patent family. Relevance is restricted to DAPFAM IN-domain positives, so target families are citation-related and share IPC3 technical class with the query family.

This split tests compact summary-to-full-text retrieval inside a shared patent domain. The query gives only summary-level invention information, while targets are very long patent records. The model must expand from a title and abstract to same-domain prior-art families whose relevant evidence may appear anywhere in full text.

## Details

### What the Original Data Measures

DAPFAM is a domain-aware patent-family retrieval benchmark that uses citation links as relevance labels. IN-domain positives are citation-related families sharing IPC3 domain with the source. This split uses short source fields and long target fields to test in-domain prior-art retrieval from concise search input.

### Observed Data Profile

This Nano split contains 200 queries, 10,000 documents, and 3,072 positive qrels. There are 194 multi-positive queries, with an average of 15.36 positives per query, a minimum of 1, median of 18.0, and maximum of 20. Queries average 771.27 characters, while full-text targets average 68,924.25 characters.

The query side resembles a patent search summary. The target side contains claims, descriptions, and background material, so ranking must tolerate substantial full-text noise.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.3490, hit@10 of 0.8200, and recall@100 of 0.5677 with a top-500 candidate pool. Title and abstract terms remain useful because in-domain patents often reuse technical vocabulary. BM25 can often find at least one positive.

The limitation is full-text length and same-domain ambiguity. Many target documents share the same vocabulary, and long descriptions can contain query terms incidentally. BM25 therefore trails dense and hybrid methods in recall.

### Dense Evaluation Profile

The dense harrier-oss-270m profile reaches nDCG@10 of 0.4255, hit@10 of 0.8750, and recall@100 of 0.6729. Dense retrieval improves over BM25 by matching the summary-level invention concept to longer target-family content.

Dense retrieval is useful when target patents describe the same technical contribution with different phrasing. It is still limited by long-document representation and multi-positive coverage.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate subset reaches nDCG@10 of 0.4228, hit@10 of 0.8900, and recall@100 of 0.6803. It uses top-100 candidates with optional rank-101 safeguards; five rows contain 101 candidates and five safeguard-positive rows are recorded. Hybrid retrieval gives the best hit@10 and recall@100, while dense retrieval has slightly higher nDCG@10.

This means exact summary terms and semantic similarity are complementary. Hybrid is the better candidate pool for downstream reranking, while dense ranking remains very competitive at the top.

### Metric Interpretation for Model Researchers

This is an in-domain summary-to-full-text task. High hit@10 does not imply complete retrieval because each query has many positives. Recall@100 shows that dense and hybrid methods recover substantially more cited families than BM25.

The split is useful for evaluating long patent target handling from short user-facing patent summaries.

### Query and Relevance Type Tendencies

Queries are titles and abstracts. Documents are full patent texts. Positives are same-domain cited families. Since the domain is shared, broad topic classification is not enough; models must rank citation-relevant families within a technical class.

### Representative Failure Modes

BM25 may retrieve full texts with incidental term overlap. Dense retrieval may rank semantically related but non-cited same-domain families. Hybrid retrieval can still be distracted by long target documents whose background sections match the query.

### Training Data That May Help

Useful training data includes same-domain title-abstract patent retrieval, full-text patent prior-art search, and family-level citation retrieval. Training should exclude NanoDAPFAM evaluation family IDs and citation labels.

Synthetic data should pair title-abstract summaries with full-text same-domain patent family records, using cited families as positives and same-IPC non-cited families as hard negatives.

### Model Improvement Notes

Improving this task requires summary-to-long-document matching inside the same patent domain. Models should identify the main inventive concept from title and abstract, then locate related evidence in very long target records.

For reranking, passage-level evidence aggregation and citation-likelihood signals may improve positive coverage.

## Example Data

| Query | Positive document |
| --- | --- |
| snow removal equipment with automatic walking function the invention relates to snow removal equipment with an automatic walking function. the snow removal equipment comprises a walking module, a working module and a control module, wherein the walking module drives a snow removal machine to move; the working module comprises a working motor and a snow throwing mechanism driven by the working motor, and the snow throwing mechanism collects and throws out snows and occluded foreign substances on... [500 / 988 chars] | multifunctional device for clearing snow an apparatus and method for clearing an accumulation of matter from a surface that includes a blade configured to collect matter upon movement of the apparatus and means to shift the collected matter and distribute it laterally from the apparatus. the apparatus may include a plurality of helically arranged ribbons adjacent the blade formed such that the radial distance from a central axis decreases away from a center portion of the blade. a sealed rotor chamber may also include a rotor with blades that are adjustable in a radial direction or flared in both first and second rotational directions. claims what is claimed is: 1. an apparatus for clearing an accumulation of matter from a surface, including: a blade configured to collect matter upon movement of the apparatus, the blade including a central portion and lateral portions; a first ribbon and a second ribbon located adjacent the blade, the first ribbon and the second ribbon arranged helical... [1,000 / 59,310 chars] |
| waste disposal devices waste disposal device including a housing defining a waste compartment for receiving enclosed waste and arranged to removably receive a cartridge containing a length of flexible tubing which operatively receives waste therein, a retention mechanism for holding a quantity of waste received in the tubing and a rotation mechanism for rotating the retention mechanism when the quantity of waste is held thereby and while the cartridge is stationary in order to twist the tubing a... [500 / 891 chars] | cassette for dispensing pleated tubing a cassette for use in dispensing a pleated tubing. the cassette includes an annular body having a generally u shaped housing with an open central cylindrical core. the annular body includes an inner wall, an angular wall a bottom wall and an outer wall. the annular cover has an outer wall and a ledge that extends radially inward from the outer wall and over the annular body that defines a gap between an inner edge of the ledge and the inner wall of the annular body. an inter-engagement mechanism is provided on the annular body and on opposite edges of the annular cover that cooperates to secure the cover to the body. at least one aperture is provided in the angular wall to enable ventilation of the air. a cassette (10) for use in dispensing a pleated tubing (50), comprising: an annular body (20) having a housing with a generally u-shaped channel cross section, the housing having a central cylindrical core (27); and an annular cover (40) extending... [1,000 / 36,269 chars] |
| an article including identification for use in an electrically heated smoking system. there is provided an electrically heated smoking system (101) for receiving a smoking article (115) or cleaning article (205) configured for use with the smoking system (101). the system comprises a cavity (111) for at least partially receiving the smoking article (115) or cleaning article (205). the smoking article includes identification information printed thereon. the cleaning article includes identificatio... [500 / 1,164 chars] | apparatus for generating aerosol from an aerosolisable medium, an article of aerosolisable medium and a method of determining a parameter of an article to provide an apparatus that heats an aerosolizable medium to volatilize at least one component of the aerosolizable medium, without burning or combusting the aerosolizable medium.solution: an apparatus 100 comprises: a housing; a chamber 112 for receiving an article 102 comprising an aerosolizable medium and including a marker; and a controller 116. the controller is configured to receive: a first input indicative of a rate of movement of the article, received in use, in the chamber; and a second input indicative of a parameter of the article. at least the second input is determined based on the marker.selected drawing: figure 3 claims 1. an apparatus for generating aerosol from an aerosolisable medium, the apparatus comprising: a housing; a chamber for receiving an article comprising aerosolisable medium and including a marker; a cont... [1,000 / 52,756 chars] |

### Source Reference Table

| Source | Role |
| --- | --- |
| [DAPFAM: A Domain-Aware Family-level Dataset to benchmark cross domain patent retrieval](https://arxiv.org/abs/2506.22141) | Source benchmark paper for family-level patent retrieval. |
| [DAPFAM DOI record](https://doi.org/10.1016/j.array.2026.100720) | DOI record for the DAPFAM paper. |
| [datalyes/DAPFAM_patent](https://huggingface.co/datasets/datalyes/DAPFAM_patent) | Public source dataset card. |
| [hakari-bench/NanoDAPFAM](https://huggingface.co/datasets/hakari-bench/NanoDAPFAM) | Nano benchmark dataset containing this split. |

### Representative Snippets

| Query Pattern | Positive Document Pattern |
| --- | --- |
| A title-abstract summary from a source patent family. | A full-text same-domain target family cited by or technically related to the source. |
| A concise apparatus summary. | A long target patent with related apparatus claims and description. |
| A concise process summary. | A full-text target family describing a related same-domain method. |
| A compact material or composition abstract. | A long same-domain target patent with related material details. |
| A vehicle or control-system abstract. | A full-text target family in the same IPC3 domain with related control technology. |
