# MNanoBEIR / NanoBEIR-sv / NanoTouche2020

## Overview

NanoTouche2020 in the Swedish NanoBEIR slice is an argument retrieval task derived from the Touché 2020 shared task. The queries are Swedish translated controversial questions, and the corpus contains Swedish translated argument passages. The retrieval goal is to find passages that contribute relevant arguments to a debate, often across both supporting and opposing perspectives. This makes the task a compact benchmark for argumentative search, stance-aware retrieval, and multi-positive ranking in Swedish.

## Details

### What the Original Data Measures

Touché 2020 evaluates argument retrieval for controversial information needs. A relevant passage is not simply a document that mentions the query topic; it should contain an argument, reason, example, or perspective that helps answer the debate question. Relevance can cover several aspects of the same issue, and a query can have many useful passages.

The Swedish translated version tests this behavior with short debate questions and long argument passages. The model must connect a concise controversial question to passages that may discuss one side, one sub-argument, or one evidential example. Topic matching matters, but stance and argumentative usefulness are central.

### Observed Data Profile

The task contains 49 queries, 5,745 documents, and 932 relevance judgments. Every query is multi-positive, with an average of 19.02 positives per query. The minimum is 6, the median is 19.0, and the maximum is 32. This is a broad relevant-set retrieval task where ranking many useful arguments is more important than finding a single answer.

Queries average 40.96 characters, while documents average 2,158.81 characters. The query-document length gap is large: a short question such as whether homework is good can correspond to many long passages containing reasons, examples, and claims. The model must judge argument relevance inside long text.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.4296, hit@10 of 0.9592, and recall@100 of 0.6320 using the top-500 BM25 candidate subset. Lexical matching is strong for finding at least one relevant argument because debate questions contain clear topic words that often repeat in argument passages.

The lower recall@100 reflects the broader challenge. Each query has many positives, and arguments can use varied wording or focus on different aspects of the same issue. BM25 can identify the obvious topical region, but it may miss arguments that rely on paraphrase, stance framing, or indirect discussion of the topic.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.4427, hit@10 of 0.9184, and recall@100 of 0.7242. Dense retrieval improves nDCG@10 and recall@100 over BM25, while BM25 has the higher hit@10. This suggests that dense similarity is better at retrieving a broader argument set, even if lexical matching is slightly better at finding one immediate hit.

For debate retrieval, the dense advantage in recall is important. Arguments may be semantically relevant without repeating the exact question words. Dense retrieval can connect related claims and reasoning patterns, but it may also retrieve broadly topical passages that are less direct as arguments, explaining the lower hit@10 relative to BM25.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.4707, hit@10 of 0.9796, and recall@100 of 0.7328. It uses exactly 100 candidates per query, with no rank-101 safeguard rows. This is the strongest profile among the three modes across the main top-rank and candidate-coverage measures.

The hybrid result shows that Swedish Touché retrieval benefits from combining lexical topic anchors with dense argumentative similarity. BM25 helps keep the query topic precise, while dense retrieval broadens the relevant argument space. The hybrid ordering improves both first-page relevance and recall, making it the most aligned first-stage profile for this task.

### Metric Interpretation for Model Researchers

Because every query has many positives, hit@10 is not enough. A model can find one relevant argument early and still fail to cover the range of useful arguments. nDCG@10 measures first-page density of relevant passages, while recall@100 measures whether a reranker or user exploration system has a broad candidate set.

The method comparison shows that BM25 is reliable for obvious topic matches, dense retrieval expands coverage, and reranking_hybrid combines both advantages. This makes NanoTouche2020-sv a good benchmark for testing whether hybrid search improves argument discovery rather than merely increasing lexical overlap.

### Query and Relevance Type Tendencies

Queries ask controversial questions such as whether homework is good, whether prescription drugs should be advertised directly to consumers, whether children should need vaccines, whether abortion should be legal, and whether standardized tests improve education. Relevant passages are long arguments with claims, reasons, examples, and sometimes explicit stance.

The task rewards models that understand issue, stance, and aspect. A passage can be relevant even if it argues from a different side than another positive passage. Conversely, a same-topic passage may be weak if it does not address the controversial question in an argumentative way.

### Representative Failure Modes

Likely failures include retrieving generic informational passages instead of arguments, over-ranking passages that repeat the topic but do not give a reason, missing counterarguments framed with different wording, and failing to cover multiple aspects of the debate. BM25 may be too literal, while dense retrieval may be too broad. Hybrid systems reduce these issues when the final ordering preserves both topic precision and argument relevance.

### Training Data That May Help

Useful training data includes argument retrieval, debate passage ranking, stance-aware retrieval, controversial question answering, and hard negatives that share the same topic but do not answer the specific aspect. Swedish argument and opinion data can help with discourse markers and stance phrasing. For rerankers, same-topic weak arguments are particularly useful negatives.

### Model Improvement Notes

A model targeting this task should optimize for broad argument coverage and first-page relevance. Sparse systems need lexical precision but also expansion for paraphrased arguments. Dense systems need stance and aspect sensitivity. Hybrid systems are the strongest baseline here and should be paired with rerankers that can judge whether a passage actually functions as an argument for the query.

## Example Data

| Query | Positive document |
| --- | --- |
| Är läxor bra? [13 chars] | Först och främst finns det tre argument för varför läxor är utmärkta och bör fortsätta i moderna skolor. 1. Läxor hjälper gör-lärarna. Det är allmänt accepterat att det finns tre typer av lärande: de... [200 / 3,658 chars] |
| Bör receptbelagda läkemedel annonseras direkt till konsumenter? [63 chars] | Många annonser innehåller inte tillräckligt med information om hur väl läkemedel fungerar. Till exempel annonseras Lunesta av en fjäril som flyger in genom ett sovrumsfönster, över en person som sover... [200 / 1,768 chars] |
| Skall barn behöva några vacciner? [33 chars] | Det är inte ett fullständigt fall ännu... bara några små punkter jag samlat ihop... Regeringar bör inte ha rätt att ingripa i de hälsoval som föräldrar gör för sina barn. Enligt en undersökning från 2... [200 / 4,244 chars] |
| Bör abort vara lagligt? [23 chars] | Abort ska vara lagligt eftersom personlighet börjar när fostret är livskraftigt eller efter födseln, inte vid befruktningen. Enligt USA:s högsta domstol får en person sin ålder när de är utanför moder... [200 / 286 chars] |
| Förbättrar standardiserade prov utbildningen? [45 chars] | Löst: SAT, ACT och andra standardiserade tester ger mer insikt i en gymnasieelevers beredskap för utbildning på elituniversitet och högskolor än gymnasiebetyget och bör därför spela en större roll i a... [200 / 4,148 chars] |

### Source Reference Table

| Item | Reference |
| --- | --- |
| Original task | [Touché 2020](https://doi.org/10.1007/978-3-030-58219-7_26) |
| Retrieval benchmark framing | [BEIR](https://arxiv.org/abs/2104.08663) |
| Multilingual benchmark context | [MMTEB](https://arxiv.org/abs/2502.13595) |
| NanoBEIR collection | [NanoBEIR on Hugging Face](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
| NanoBEIR-sv dataset | [hakari-bench/NanoBEIR-sv](https://huggingface.co/datasets/hakari-bench/NanoBEIR-sv) |

Representative query and positive argument snippets:

| Query | Positive document snippet |
| --- | --- |
| Är läxor bra? | Först och främst finns det tre argument för varför läxor är utmärkta och bör fortsätta i moderna skolor... |
| Bör receptbelagda läkemedel annonseras direkt till konsumenter? | Många annonser innehåller inte tillräckligt med information om hur väl läkemedel fungerar... |
| Skall barn behöva några vacciner? | Det är inte ett fullständigt fall ännu... Regeringar bör inte ha rätt att ingripa i de hälsoval... |
| Bör abort vara lagligt? | Abort ska vara lagligt eftersom personlighet börjar när fostret är livskraftigt eller efter födseln... |
| Förbättrar standardiserade prov utbildningen? | Löst: SAT, ACT och andra standardiserade tester ger mer insikt i en gymnasieelevers beredskap... |
