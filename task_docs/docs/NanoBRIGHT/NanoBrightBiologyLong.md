# NanoBRIGHT / NanoBrightBiologyLong

## Overview

NanoBrightBiologyLong is the compact NanoBRIGHT long-document variant of the Biology StackExchange retrieval task. The queries are detailed biology questions, but the corpus contains full or much longer cited source pages rather than short passage chunks. The retrieval goal is to find the full document that contains the biological mechanism or source evidence needed to answer the question. This makes the task useful for evaluating long-document retrieval, evidence-in-page matching, and biology reasoning support under heavy lexical noise.

## Details

### What the Original Data Measures

BRIGHT's long-document variants test reasoning-intensive retrieval when evidence is embedded in unsplit source pages. For BiologyLong, the question may be answered by one section or concept inside a long reference page. The retriever must rank the whole page, not just the evidence paragraph.

This changes the difficulty from the passage version. The relevant source page can be very long and contain many unrelated sections, so lexical matches can be diluted or swamped by extra terms. A strong system must still connect the user question to the document that contains the needed biological concept.

### Observed Data Profile

The task contains 103 queries, 498 documents, and 134 relevance judgments. The average number of positives is 1.30 per query. The minimum is 1, the median is 1.0, the maximum is 4, and 24 queries are multi-positive, or 23.30% of the set.

Queries average 523.03 characters, while documents average 36,923.73 characters. This is an extreme query-document length mismatch. Queries are detailed Biology StackExchange-style posts, and documents are long encyclopedia or reference pages that may contain the relevant mechanism somewhere inside a much larger page.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.3708, hit@10 of 0.6311, and recall@100 of 0.8731 using the top-500 BM25 candidate subset. Because the corpus has only 498 documents, each candidate list effectively covers the full document pool. Lexical matching can find relevant pages when the question contains distinctive terms such as elastin, chlorophyll, MHC, or phage therapy.

The limitation is long-document noise. A relevant full page may contain many off-topic sections, while an irrelevant page may contain several overlapping biology terms. BM25 can therefore find broad topical pages but rank them behind pages with more concentrated word overlap.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.5779, hit@10 of 0.8835, and recall@100 of 0.9701. Dense retrieval is the strongest direct profile. It improves top-rank quality and candidate coverage substantially over BM25.

This shows that embedding similarity helps bridge long user questions to the right full source page. The model can recognize that a question about long-lived human proteins points to elastin, or that viruses as antibiotics points to phage therapy, even when the page contains much more text than the relevant section.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.4897, hit@10 of 0.7767, and recall@100 of 0.9701. It uses a top-100 candidate range with an optional rank-101 safeguard; this slice has 1 safeguard row, candidate counts from 100 to 101, and a mean of 100.01 candidates. Hybrid matches dense recall@100 but is weaker in top-10 ranking.

This suggests that dense retrieval is better at directly ranking the long source pages, while hybrid retrieval remains useful as a high-recall candidate pool. BM25 contributes exact biological terms, but full-page lexical noise can also reduce top-rank precision.

### Metric Interpretation for Model Researchers

Because positives per query are usually one or a few, hit@10 and nDCG@10 directly reflect whether the correct source page is visible and ranked early. recall@100 is easier than in larger corpora but still useful for checking whether candidate generation misses evidence-bearing pages.

The comparison shows that BM25 is hampered by long-document noise, dense retrieval is strongest for direct ranking, and reranking_hybrid preserves dense-level recall while trading away some rank quality. This task is a good diagnostic for long-document scientific retrieval.

### Query and Relevance Type Tendencies

Queries include questions about the longest-lasting protein in the human body, whether kissing is natural, which light plants can photosynthesize, why tumors evade immune detection, and whether viruses can be used as antibiotics. Positive documents include long pages about elastin, kissing, chlorophyll, major histocompatibility complex, and phage therapy.

The task rewards finding a page that contains the mechanism needed for the answer. The relevant section may be small relative to the full page, so whole-document retrieval must avoid being distracted by unrelated page content.

### Representative Failure Modes

Likely failures include ranking a broad biology page above the precise source page, over-weighting repeated terms from irrelevant sections, missing pages where the key concept is expressed indirectly, and confusing related mechanisms. BM25 may be too sensitive to long-page word counts, while dense retrieval may still blur nearby biological concepts.

### Training Data That May Help

Useful training data includes long biology reference pages aligned to questions, StackExchange posts with full cited sources, passage-to-document distillation, biology QA with citations, and hard negatives from nearby full pages that contain shared terms but not the supporting mechanism.

### Model Improvement Notes

A model targeting this task should learn to retrieve full documents from localized evidence. Sparse systems need field or section-aware indexing. Dense systems are strong and can improve through long-document representation and citation-supervised training. Hybrid systems should account for document length so lexical evidence does not become noisy.

## Example Data

| Query | Positive document |
| --- | --- |
| What is the longest-lasting protein in a human body? Protein life times are, on average, not particularly long, on a human life timescale. I was wondering, how old is the oldest protein in a human body? Just to clarify, I mean in terms of seconds/minutes/days passed from the moment that given protein was translated. I am not sure is the same thing as asking which human protein has the longest half-life, as I think there might be "tricks" the cell uses to elongate a given protein's half-life unde... [500 / 1,199 chars] | 2006 Function[edit] The ELN gene encodes a protein that is one of the two components of elastic fibers. The encoded protein is rich in hydrophobic amino acids such as glycine and proline, which form mobile hydrophobic regions bounded by crosslinks between lysine residues. Multiple transcript variants encoding different isoforms have been found for this gene. Elastin's soluble precursor is tropoelastin. The characterization of disorder is consistent with an entropy-driven mechanism of elastic recoil. It is concluded that conformational disorder is a constitutive feature of elastin structure and function. Clinical significance[edit] Deletions and mutations in this gene are associated with supravalvular aortic stenosis (SVAS) and the autosomal dominant cutis laxa. Other associated defects in elastin include Marfan syndrome, emphysema caused by α1-antitrypsin deficiency, atherosclerosis, Buschke-Ollendorff syndrome, Menkes syndrome, pseudoxanthoma elasticum, and Williams syndrome. Elastosi... [1,000 / 6,263 chars] |
| Is kissing a natural human activity? The word natural here is meant in contrast to it being a sociological construct. Is kissing in all its forms something natural for humans? Is it instinctively erotic? Or is it just a conventional form to show trust and intimicy, i.e. the association besically just comes via a social means? Because the only other advantage of this mouth to mouth contact I could see is maybe for the immune system. [435 chars] | A kiss is the touch or pressing of one's lips against another person or an object. Cultural connotations of kissing vary widely. Depending on the culture and context, a kiss can express sentiments of love, passion, romance, sexual attraction, sexual activity, sexual arousal, affection, respect, greeting, peace, and good luck, among many others. In some situations, a kiss is a ritual, formal or symbolic gesture indicating devotion, respect, or a sacramental. The word came from Old English cyssan ("to kiss"), in turn from coss ("a kiss"). History[edit] Anthropologists disagree on whether kissing is an instinctual or learned behaviour. Those who believe kissing to be an instinctual behaviour cite similar behaviours in other animals such as bonobos, which are known to kiss after fighting - possibly to restore peace. Others believe that it is a learned behaviour, having evolved from activities such as suckling or premastication in early human cultures passed on to modern humans. Another the... [1,000 / 40,449 chars] |
| What types of light can't a plant photosynthesize in? I have a plant on my desk, and it got me to wondering: Can my plant use the light from my monitors to photosynthesize? If so, what light (apart from green light, to a degree) can't plants use to perform photosynthesis? I know that plants have the photosynthetic pigments to absorb many different wavelengths of light (primarily red and blue) but would there be certain types of light it can't use? (The specific plant by the way is Schlumbergera... [500 / 509 chars] | Chlorophyll is any of several related green pigments found in cyanobacteria and in the chloroplasts of algae and plants. Its name is derived from the Greek words χλωρός, khloros ("pale green") and φύλλον, phyllon ("leaf"). Chlorophyll allows plants to absorb energy from light. Chlorophylls absorb light most strongly in the blue portion of the electromagnetic spectrum as well as the red portion. Conversely, it is a poor absorber of green and near-green portions of the spectrum. Hence chlorophyll-containing tissues appear green because green light, diffusively reflected by structures like cell walls, is less absorbed. Two types of chlorophyll exist in the photosystems of green plants: chlorophyll a and b. History[edit] Chlorophyll was first isolated and named by Joseph Bienaimé Caventou and Pierre Joseph Pelletier in 1817. The presence of magnesium in chlorophyll was discovered in 1906, and was the first detection of that element in living tissue. After initial work done by German chemis... [1,000 / 14,080 chars] |

### Source Reference Table

| Item | Reference |
| --- | --- |
| Original benchmark paper | [BRIGHT](https://arxiv.org/abs/2407.12883) |
| Project page | [BRIGHT project page](https://brightbenchmark.github.io/) |
| Source dataset | [xlangai/BRIGHT](https://huggingface.co/datasets/xlangai/BRIGHT) |
| NanoBRIGHT dataset | [hakari-bench/NanoBRIGHT](https://huggingface.co/datasets/hakari-bench/NanoBRIGHT) |

Representative query and positive source snippets:

| Query | Positive document snippet |
| --- | --- |
| What is the longest-lasting protein in a human body? | The ELN gene encodes elastin, a component of elastic fibers. |
| Is kissing a natural human activity? | A kiss is the touch or pressing of one's lips against another person or object. |
| What types of light can't a plant photosynthesize in? | Chlorophyll is a green pigment found in cyanobacteria and plant chloroplasts. |
| If tumors have many mutations, why can't the immune system detect them? | The major histocompatibility complex contains genes for cell-surface proteins essential to adaptive immunity. |
| Could viruses be used as antibiotics? | Phage therapy is the therapeutic use of bacteriophages for pathogenic bacterial infections. |
