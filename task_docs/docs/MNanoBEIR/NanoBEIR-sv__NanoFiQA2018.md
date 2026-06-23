# MNanoBEIR / NanoBEIR-sv / NanoFiQA2018

## Overview

NanoFiQA2018 in the Swedish NanoBEIR slice is a financial question-answer retrieval task derived from FiQA. The queries are Swedish translated finance questions, and the corpus contains Swedish translated answer passages. The retrieval goal is to find passages that answer practical financial questions about taxes, investment returns, trading volume, credit card rewards, and related personal-finance issues. This makes the task a compact but difficult diagnostic for domain-specific retrieval and answer matching in Swedish.

## Details

### What the Original Data Measures

FiQA was introduced for financial opinion mining and question answering. In retrieval form, it tests whether a model can connect a finance question to answer passages that resolve the user's need. The task often involves practical financial reasoning, terminology, regulations, and contextual advice rather than a single named entity.

The Swedish translated version adds multilingual challenges around finance vocabulary, tax terminology, investment concepts, and informal answer style. A relevant answer may not repeat the query wording. Instead, it may explain a concept, cite a rule, or give a practical recommendation. This makes semantic answer matching more important than simple keyword overlap.

### Observed Data Profile

The task contains 50 queries, 4,598 documents, and 123 relevance judgments. There are multiple positives for 28 queries, or 56.0% of the query set. The average number of positives is 2.46, with a minimum of 1, a median of 2.0, and a maximum of 15. The task therefore mixes single-answer lookup with broader answer-set retrieval.

Queries average 62.24 characters, while documents average 925.72 characters. The queries are short finance questions, and the documents are longer answer passages that may include explanation, examples, or caveats. The model must identify answer usefulness, not just topic similarity.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.1159, hit@10 of 0.2800, and recall@100 of 0.3984 using the top-500 BM25 candidate subset. This is a difficult lexical retrieval profile. The median first positive in the old diagnostic was far down the ranking, and the current candidate metrics show that exact term matching misses many useful answers.

The weakness is understandable for finance QA. A question may ask "what type of return" while the answer discusses CAGR; a tax question may be answered by a passage using different legal or accounting wording. BM25 can retrieve passages with shared finance terms, but those terms are often too broad to identify the actual answer.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.3435, hit@10 of 0.6000, and recall@100 of 0.6748. Dense retrieval is much stronger than BM25 across all metrics. This indicates that embedding similarity is better aligned with answer intent and can connect financial questions to explanatory passages even when the wording differs.

The dense gains are especially important for top-10 usability. A finance QA system needs the answer passage near the top, and lexical retrieval often fails to surface it. Dense retrieval still leaves substantial room for improvement, likely because finance answers can be nuanced, jurisdiction-specific, or dependent on details that generic semantic similarity does not fully capture.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.2256, hit@10 of 0.4600, and recall@100 of 0.6911. It uses a top-100 candidate range with an optional rank-101 safeguard; the observed candidate count ranges from 100 to 101, with 8 safeguard rows and a mean of 100.16 candidates. The hybrid profile has the highest recall@100 but weaker top-10 ranking than dense retrieval.

This means hybrid search is useful as a candidate pool but not as the best first-stage ordering for NanoFiQA2018-sv. Combining BM25 and dense candidates recovers slightly more positives by rank 100, but the lexical component can pull less useful term-overlap passages upward. A downstream reranker could benefit from the hybrid pool, while dense retrieval alone is the stronger direct ranking baseline.

### Metric Interpretation for Model Researchers

nDCG@10 is the most important metric for user-facing finance QA retrieval because the answer must appear high enough to be read or used by a downstream system. hit@10 measures whether at least one answer appears in the first page, and recall@100 measures whether a reranker can recover answer passages from the candidate set. Here, the difference between dense nDCG@10 and hybrid recall@100 is particularly informative.

The task shows a clear semantic-retrieval advantage. BM25 is weak because finance questions and answers often differ in wording. Dense retrieval is strongest at the top ranks. reranking_hybrid improves candidate coverage, but its first-stage ordering is less aligned with answer usefulness. Researchers should use this task to test answer-intent matching and finance-domain hard negatives.

### Query and Relevance Type Tendencies

Queries ask practical financial questions such as what kind of return Vanguard reports, tax consequences of freelance work, what counts as high or low trading volume, whether credit card points can pay tax-deductible business expenses, and how a contractor should file taxes. Relevant documents are explanatory answers, often with examples or assumptions.

The task rewards models that understand domain concepts and map surface questions to financial explanations. It also requires care with jurisdiction, tax status, account type, and specific financial terms. Broad topical similarity is often insufficient because many passages discuss money, taxes, or investments without answering the specific question.

### Representative Failure Modes

Likely failures include retrieving passages with the same finance term but a different question, missing answers that use technical synonyms, over-ranking broad investment or tax discussions, and confusing personal finance advice across contexts. BM25 may fail when answer wording differs from query wording, while dense models may retrieve semantically related but practically unhelpful answers.

### Training Data That May Help

Useful training data includes financial QA, personal-finance forums, tax and investment answer retrieval, multilingual finance text, and hard negatives that share financial terminology but answer a different need. Swedish financial and regulatory language can help with local terminology, while English finance QA may help if cross-lingual alignment is strong. For rerankers, near-topic wrong answers are the most important negative examples.

### Model Improvement Notes

A model targeting this task should improve domain-specific answer matching. Dense retrievers are the best starting point, but should be trained with finance-specific positives and hard negatives. Sparse systems need query expansion and terminology normalization to bridge question-answer vocabulary gaps. Hybrid systems should be paired with a reranker that can judge whether a passage actually answers the finance question.

## Example Data

| Query | Positive document |
| --- | --- |
| Vilken typ av avkastning anger Vanguard? [40 chars] | På Vanguard-sidan - Detta verkade vara det enklaste eftersom S&P-data är lätt att hitta. Jag använder MoneyChimp för att bekräfta att Vanguards sida erbjuder CAGR, inte aritmetiskt medelvärde. Vanguard anger att 'för amerikanska aktiemarknadens avkastning använder vi Standard & Poor's 90 från 1926 till och med 3 mars 1957,' medan MoneyChimp använder data från Nobelpristagaren Robert Shillers webbplats. [405 chars] |
| Skattekonsekvenser vid frilansarbete [36 chars] | Om du har inkomst i USA, måste du betala amerikansk inkomstskatt på den, om det inte finns ett avtal mellan ditt land och USA som säger annat. [142 chars] |
| Vad betraktas som hög eller låg volym? [38 chars] | Den dagliga volymen jämförs vanligtvis med den genomsnittliga dagliga volymen över de senaste 50 dagarna för en aktie. Hög volym anses vanligtvis vara 2 eller fler gånger den genomsnittliga dagliga volymen över de senaste 50 dagarna för den aktien. Vissa handelsmän kan dock sätta kriteriet till 3x eller 4x den genomsnittliga dagliga volymen (ADV) för att bekräfta ett visst mönster eller en händelse. Volymen jämförs med ADV för aktien själv, eftersom att jämföra den med volymen för andra aktier skulle vara som att jämföra äpplen med päron. Olika företag har olika antal totala aktier tillgängliga, olika nivåer av likviditet och olika nivåer av volatilitet, vilket alla kan påverka de volymer som handlas varje dag. [720 chars] |

### Source Reference Table

| Item | Reference |
| --- | --- |
| Original dataset | [FiQA](https://doi.org/10.1145/3184558.3192301) |
| Retrieval benchmark framing | [BEIR](https://arxiv.org/abs/2104.08663) |
| Multilingual benchmark context | [MMTEB](https://arxiv.org/abs/2502.13595) |
| NanoBEIR collection | [NanoBEIR on Hugging Face](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
| NanoBEIR-sv dataset | [hakari-bench/NanoBEIR-sv](https://huggingface.co/datasets/hakari-bench/NanoBEIR-sv) |

Representative query and positive answer snippets:

| Query | Positive document snippet |
| --- | --- |
| Vilken typ av avkastning anger Vanguard? | På Vanguard-sidan - Detta verkade vara det enklaste eftersom S&P-data är lätt att hitta... |
| Skattekonsekvenser vid frilansarbete | Om du har inkomst i USA, måste du betala amerikansk inkomstskatt på den... |
| Vad betraktas som hög eller låg volym? | Den dagliga volymen jämförs vanligtvis med den genomsnittliga dagliga volymen över de senaste 50 dagarna... |
| Använda kreditkortspoäng för att betala skatteavdragsbara företagsutgifter | För enkelhetens skull, låt oss börja med att bara överväga cashback... |
| Hur ska jag skicka in min deklaration som kontraktör? | För skattemål måste du deklarera som anställd, men också som företagare... |
