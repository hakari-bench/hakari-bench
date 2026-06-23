# NanoBRIGHT / NanoBrightEconomics

## Overview

NanoBrightEconomics is the Economics StackExchange slice of NanoBRIGHT. Queries are long user posts about economic theory, finance, markets, public policy, macroeconomic mechanisms, or requests for supporting literature. Relevant documents are source passages from papers, reports, reference pages, or cited web material. The task is useful for measuring whether retrieval systems can connect a detailed economic question to evidence that supports the requested mechanism, model, empirical claim, or institutional explanation.

## Details

### What the Original Data Measures

BRIGHT frames StackExchange retrieval as source-support search rather than direct answer retrieval. A query combines the question title and body, and positives are cited or validated documents that help answer the post. In Economics, those positives can be academic passages, explanatory pages, market infrastructure descriptions, policy discussions, or empirical evidence.

This task therefore measures reasoning-oriented retrieval in a domain where the query may be phrased as a puzzle, a policy objection, a mathematical derivation, or a request for papers. Relevance depends on whether the document supports the exact economic concept at issue, not merely whether it shares words like tax, GDP, interest, trade, or market.

### Observed Data Profile

The task contains 103 queries, 10,000 documents, and 800 relevance judgments. It is multi-positive but highly uneven: there are 7.77 positives per query on average, a minimum of 1, a median of 3.0, a maximum of 85, and 68 multi-positive queries, or 66.02% of the set.

Queries average 739.57 characters, making them much longer than ordinary keyword-style search queries. They often include assumptions, formulas, quoted claims, and motivating examples. Documents average 532.57 characters and tend to be compact passage chunks, so the main challenge is matching the economic relation rather than scanning long documents.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.3029, hit@10 of 0.5340, and recall@100 of 0.4888 using the top-500 BM25 candidate subset. This is a modest lexical baseline. It can retrieve documents for named concepts, formulas, stock-market mechanics, taxes, GDP components, or recognizable economic terminology.

The limitation is that many Economics queries are conceptual. A question may ask why a model derivative is valid, whether taxes matter under central-bank financing, or when equity and efficiency conflict. The supporting document may use different vocabulary, cite a formal model, or discuss the same mechanism at a different level of abstraction. BM25 therefore misses many positives and is not enough as the sole candidate source.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.4095, hit@10 of 0.6311, and recall@100 of 0.5950. Dense retrieval improves substantially over BM25 on all reported metrics. This shows that embedding similarity captures conceptual economic support better than term frequency alone.

Dense retrieval is especially helpful when the query describes a scenario or asks for an explanation rather than naming the exact source concept. It can connect questions about deficit spending, welfare tradeoffs, market clearing, production functions, or policy incentives to passages that discuss the underlying theory or evidence with different wording.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.3875, hit@10 of 0.6408, and recall@100 of 0.6262. It uses a top-100 candidate range with an optional rank-101 safeguard; this task has 19 safeguard rows, candidate counts from 100 to 101, and a mean of 100.18 candidates.

The hybrid profile has the best hit@10 and recall@100, while dense retrieval has the best nDCG@10. This means the hybrid pool is better at exposing at least one positive and covering more relevant documents, but its fused ordering does not place positives as high as dense retrieval in every case. It is a strong input pool for reranking.

### Metric Interpretation for Model Researchers

This task separates semantic ranking from candidate coverage. BM25 underperforms because exact words are not enough for many economics questions. Dense retrieval gives the best top-rank ordering by nDCG@10, suggesting that semantic matching is central. Reranking_hybrid gives the best hit@10 and recall@100, suggesting that sparse terms still add useful coverage for named mechanisms, formulas, and institutional phrases.

Researchers should read the scores as evidence that Economics retrieval benefits from hybrid systems, but also needs a reranker that can decide whether a passage supports the exact model or empirical claim. A same-topic passage can be misleading if it discusses a nearby but different economic issue.

### Query and Relevance Type Tendencies

Queries include questions about GDP accounting, derivatives in RBC models, taxes and central-bank deficit financing, efficiency-equity tradeoffs, stock price determination, market order matching, and requests for economic papers. Positives may come from formal definitions, textbook-style explanations, finance reference pages, policy papers, or empirical research.

The relevance relation is often explanatory. The desired passage may justify a step in a model, define a concept such as elasticity of substitution, explain an institutional process such as order matching, or provide evidence for a welfare or policy claim.

### Representative Failure Modes

Likely failures include retrieving passages with the right economic keywords but the wrong causal mechanism, confusing finance infrastructure with macroeconomic theory, matching a formula name without explaining the step asked in the query, and over-ranking broad policy discussion when the query asks for a specific empirical claim.

BM25 is vulnerable to lexical distraction from long, detailed queries. Dense retrieval is vulnerable to plausible same-topic passages that do not support the exact reasoning step. Hybrid retrieval improves coverage but still requires careful reranking to avoid broad topical matches.

### Training Data That May Help

Useful training data includes non-overlapping Economics StackExchange posts with cited sources, economics paper recommendation pairs, policy-report and finance QA retrieval data, textbook-style economic concept retrieval, and hard negatives from nearby economic topics.

Synthetic data should pair realistic economics questions with passages that support a specific mechanism, model, or empirical claim. Negative passages should share terms and topic but fail to answer the precise question, such as a tax passage that does not address monetary financing or a market passage that does not explain order matching.

### Model Improvement Notes

Strong models for this task should combine precise economic vocabulary with conceptual semantic matching. Sparse features help with formulas, named models, and institutional terms. Dense representations help map natural-language puzzles to theoretical or empirical support. Rerankers should be trained to distinguish support, background, and merely related discussion.

The observed metrics suggest that a practical system should use reranking_hybrid for candidate generation, then apply a model capable of economic entailment-like judgment. Multi-positive training is useful because some questions have many cited supporting documents, while others depend on a small number of exact sources.

## Example Data

| Query | Positive document |
| --- | --- |
| Would a GDP measure be improved by excluding foreign interest paid? The income method of calculating GDP is as follows: GDP = wages + profits + rents + interest + depreciation + taxes + NFFI. If an economy has high external debt, for instance, because it used external financing to buy machinery and equipment, then foreign interest payments will be high. In that case, wouldn't GDP (per capita) be a poor measure of economic well-being since a significant portion of the generated income is leaving... [500 / 684 chars] | So why in these two sets of countries do economic performance and well-being not go strictly hand in hand? One explanation is that the countries that do better in terms of well-being have made the choice of working less to achieve a better work and life balance. This translates into lower income but also increased leisure time that can be shared with friends and family, or that is used for volunteering and engaging with the community. Another reason is that these countries have better environmental quality, partly because of lower economic production and thus pollution. **Well-being is a matter of democracy and societal choices** , what really matters at the end of the day is whether countries are where their citizens would like them to be. It can be higher economic production or more time for life, longer healthy lives or more connected neighbourhoods. What is important is to collect the relevant set of statistics to judge whether collective objectives are met and ensure that governme... [1,000 / 1,068 chars] |
| Derivative to ln(K(t)) in the RBC model In the calculation of the equation of motion for capital in the RBC model, I came across this equation: d ln K_(t+1) / d ln K_t = (d K_(t+1) / d K_t) * (K_t / K_(t+1)) Can someone explain what are the mathematical steps in between? I don't see how exactly the derivative to ln(K(t)) gets us an almost elasticity-like equation. Would be thankful for any leads. :) [406 chars] | Example [ [ edit ](/w/index.php?title=Elasticity_of_substitution&action=edit&section=3 "Edit section: Example") ] Consider [ Cobb–Douglas production function ](/wiki/Cobb%E2%80%93Douglas_production_function "Cobb–Douglas production function") f ( x 1 , x 2 ) = x 1 a x 2 1 − a {\displaystyle f(x_{1},x_{2})=x_{1}^{a}x_{2}^{1-a}} ![{\\displaystyle f\(x_{1},x_{2}\)=x_{1}^{a}x_{2}^{1-a}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/c1593598228963205f7d1a3be7c9d6e3d69297e7) . The marginal rate of technical substitution is M R T S 21 = 1 − a a x 1 x 2 {\displaystyle MRTS_{21}={\frac {1-a}{a}}{\frac {x_{1}}{x_{2}}}} ![{\\displaystyle MRTS_{21}={\\frac {1-a}{a}}{\\frac {x_{1}}{x_{2}}}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/342b8ef77d0f412260163ac05a1691a5696551a7) It is convenient to change the notations. Denote 1 − a a x 1 x 2 = θ {\displaystyle {\frac {1-a}{a}}{\frac {x_{1}}{x_{2}}}=\theta } ![{\\displaystyle {\\frac {1-a}{a}}{\\frac {x_{1}}{x_{2}}}=\\theta }](h... [1,000 / 2,640 chars] |
| What is the purpose of taxes if central banks can fund deficit spending? Somewhat straight forward. If the federal reserve can print money to buy treasuries to fund deficit spending, what is the purpose of taxes? Sure, taxes reduce the amount of deficit that needs to be picked up by the Fed, but if, as ive seen argued, money “printing” doesn’t necessarily lead to inflation whats the point of levying taxes? Why doesn’t the fed just procure all of the money itself if it could theoretically do so w... [500 / 524 chars] | financial market innovations and shocks, may provide evidence of long-run inconsistencies between policies and targets and give rise to a reassessment of policy. IV CONCLUSIONS This paper has re-examined the correlations between average inflation and average growth rates of various monetary variables. A careful construction of the data set, excluding countries with short data spans, removing documented discontinuities and using appropriate methods of calculating averages confirm the earlier analysis of McCandless and Weber (1995) and question the robustness of some of the results in de Grauwe and Polan (2001). When countries are arranged in order of increasing average inflation recursive regressions indicate that the response may not be constant over countries. In such a case standard OLS produces results that are difficult to interpret and standard regression theory does not apply. For this reason a variable coefficient model is proposed and estimated. There is considerable variabilit... [1,000 / 3,286 chars] |

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
| Would a GDP measure be improved by excluding foreign interest paid? | A source discusses the relation between economic performance, well-being, and choices such as working time. |
| Why does a derivative expression appear in an RBC capital equation? | A reference passage explains elasticity of substitution and related production-function concepts. |
| What is the purpose of taxes if central banks can fund deficit spending? | A policy passage examines long-run consistency between financial conditions, targets, and public policy. |
| Is there always a tradeoff between efficiency and equity? | A source discusses large global distortions and welfare implications of constraints on movement. |
| How are stock prices determined when orders match? | A finance passage explains matching orders between buy and sell requests at the same price. |
