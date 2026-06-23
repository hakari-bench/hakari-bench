# MNanoBEIR / NanoBEIR-de / NanoClimateFEVER

## Overview

NanoBEIR-de / NanoClimateFEVER is the German NanoBEIR version of
Climate-FEVER, a climate claim verification retrieval task introduced in
[CLIMATE-FEVER: A Dataset for Verification of Real-World Climate
Claims](https://arxiv.org/abs/2012.00614). Each query is a German translated
climate-related claim, and the retrieval target is a German translated
Wikipedia evidence passage that supports, refutes, or qualifies the claim. The
Nano task contains 50 claims, 3,408 evidence candidates, and 148 positive
qrels. Most claims have multiple positives. The task tests whether a retriever
can find claim-specific climate evidence involving quantities, time periods,
causal statements, and skeptical or misinformation-style wording. The strongest
candidate view is `reranking_hybrid`, which improves both top-rank quality and
top-100 evidence coverage.

## Details

### What the Original Data Measures

Climate-FEVER adapts FEVER-style verification to real-world climate claims.
Instead of synthetic claims written from Wikipedia sentences, the source claims
come from public climate discourse and can be subtle, partial, or misleading.
Evidence may support only part of a claim, refute a causal interpretation, or
require attention to numbers and time ranges.

The German NanoBEIR version keeps this claim-to-evidence retrieval objective in
translated form. The task is not label classification. A retriever must surface
the evidence passages that a verifier would need before deciding whether the
claim is supported or refuted.

### Observed Data Profile

The metadata records 50 queries, 3,408 documents, and 148 positive qrels.
Queries have 2.96 positives on average, 44 queries are multi-positive, and the
maximum is 5 positives. Query text averages 149.10 characters, while evidence
documents average 1,767.31 characters. Examples include claims about warming
from 1970 to 1998, statistically insignificant trends, local sea-level
variation, Hurricane Harvey, and the CERN CLOUD experiment.

The documents are long German translated Wikipedia-style evidence passages.
They may discuss geological eras, solar cycles, mean sea level, climate change
impacts, attribution of recent climate change, greenhouse gases, or public
climate discourse. Evidence can be indirect, so topic matching alone is not
enough.

### BM25 Evaluation Profile

The BM25 candidate subset reaches nDCG@10 = 0.2481, hit@10 = 0.6200, and
Recall@100 = 0.5270. BM25 is useful when claims contain exact climate terms,
named projects, quantities, places, or event names that appear in evidence
passages. German translated claims often include distinctive technical phrases
that sparse retrieval can preserve.

BM25's weakness is evidence specificity. A passage can share words like
climate, warming, sea level, or carbon dioxide without addressing the claim's
specific time range, causal relation, or measurement. Long German documents
also contain many general climate terms, making lexical overlap an imperfect
ranking signal.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` reaches nDCG@10 =
0.2625, hit@10 = 0.6800, and Recall@100 = 0.5878. Dense retrieval improves over
BM25 on all visible metrics, suggesting that embedding similarity helps connect
declarative climate claims to evidence passages that use different wording.

Dense retrieval is especially useful when the evidence explains a phenomenon
rather than repeating the claim. Its risk is broad climate-topic drift: a
passage may be semantically related to climate change but fail to verify the
particular claim.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset reaches nDCG@10 = 0.3310, hit@10 =
0.7400, and Recall@100 = 0.6216. It is the strongest candidate view on all
visible metrics. The metadata records 3 rows with the optional rank-101
safeguard, meaning a few positives needed explicit preservation near the
candidate boundary.

For reranker experiments, hybrid is the best pool because it keeps BM25's exact
scientific and climate terms while adding dense semantic evidence matches. The
reranker can focus on whether the passage actually supports, refutes, or
qualifies the claim.

### Metric Interpretation for Model Researchers

NanoClimateFEVER-de is a multi-positive claim-evidence task. BM25 captures
lexical anchors but has limited coverage. Dense retrieval improves both ranking
and coverage, and hybrid improves again. This is a clear case where lexical and
semantic retrieval are complementary.

Because each query often has several positives, Recall@100 should be read as
evidence-pool coverage. A downstream verifier benefits from multiple evidence
passages because one passage may address only one facet of a climate claim.

### Query and Relevance Type Tendencies

Queries are German declarative climate claims. They include quantities,
temperature trends, time windows, sea-level variation, named experiments,
extreme weather events, and attribution language. Relevant documents are long
evidence passages that address the claim's factual content.

Lexical-heavy cases involve named projects, events, or climate terms. Dense
cases involve explanatory evidence phrased differently from the claim. Hybrid
retrieval is strongest when a claim contains exact technical anchors but
requires semantic matching to find the correct evidence facet.

### Representative Failure Modes

BM25 can retrieve a passage that repeats climate vocabulary but does not verify
the claim. Dense retrieval can retrieve a general climate-change passage that
misses the claim's quantity, time period, or causal relation. Both methods can
confuse evidence about a related phenomenon with evidence for the specific
statement. Good hard negatives are same-topic climate passages with different
measurements, mechanisms, or time ranges.

### German-Specific Notes

German climate retrieval involves long translated claims, compound terms,
technical vocabulary, numbers, units, and named scientific projects. Sparse
retrieval needs to preserve compounds, names, and numeric expressions. Dense
retrieval needs climate-domain semantics and sensitivity to causal and temporal
phrasing. Translation variation can affect terms such as greenhouse gases,
global warming, sea level, and attribution.

### Training and Leakage Notes

Training should exclude Climate-FEVER, BEIR, or NanoBEIR records likely to
overlap with these evaluation claims or evidence passages. Useful
non-overlapping data includes Climate-FEVER claim-evidence pairs, FEVER-style
retrieval data, German or multilingual scientific claim verification, and
climate-domain claim-to-evidence pairs.

### Model Improvement Hints

The main improvement target is claim-specific evidence coverage. First-stage
retrievers should preserve climate entities, numbers, and technical terms while
using dense matching to find indirect evidence. Rerankers should distinguish
generic climate passages from evidence that addresses the claim's quantity,
time span, or causal assertion.

### Training Data That May Help

Useful training data includes non-overlapping climate claim/evidence pairs,
German fact-checking retrieval, scientific claim verification data, climate
science QA, and hard negatives from the same climate topic with different
evidence relations.

### Synthetic Data Guidance

Generate German climate and environmental evidence passages with entities,
dates, quantities, causal statements, and scientific mechanisms. Then generate
declarative climate claims that can be supported, refuted, or qualified by the
passages. Positives should contain evidence addressing the claim, not merely the
same climate topic.

## Example Data

| Query | Positive document |
| --- | --- |
| Von 1970 bis 1998 gab es eine Erwärmungsperiode, die die Temperaturen um etwa 0,4 Grad Celsius erhöhte und die globale Erwärmungs-Alarmisten-Bewegung ins Leben gerufen hat. [172 chars] | Das Paläozän (ausgesprochen: /paleoˈtseːn/ oder /ˈpaleoˌtseːn/), auch Paläozän genannt, das „alte Neue“, ist eine geologische Epoche, die etwa von 66 bis 56 Millionen Jahren dauerte. Es ist die erste Epoche des Paläogens in der modernen Kainozoischen Ära. Wie bei vielen geologischen Perioden sind die Schichten, die den Beginn und das Ende der Epoche definieren, gut identifiziert, aber die genauen Altersangaben bleiben ungewiss. Die Epoche des Paläozäns umfasst zwei bedeutende Ereignisse in der Erdgeschichte. Sie begann mit dem Massenaussterbeereignis am Ende der Kreidezeit, bekannt als die Kreide-Paläogen-Grenze (K-Pg-Grenze). Dies war eine Zeit, die durch das Aussterben der nicht-vogelartigen Dinosaurier, riesiger Meeresreptilien und vieler anderer Fauna und Flora gekennzeichnet war. Das Aussterben der Dinosaurier hinterließ weltweit unbesetzte ökologische Nischen. Das Paläozän endete mit dem Paläozän-Eozän-Thermischen Maximum, einem geologisch kurzen (ca. 0,2 Millionen Jahre) Interva... [1,000 / 1,266 chars] |
| Tatsächlich zeigt der Trend, wenn auch statistisch nicht signifikant, nach unten. [81 chars] | Der Sonnenzyklus oder Sonnenfleckenzyklus ist ein fast periodischer 11-Jahres-Zyklus, der die Aktivität der Sonne (einschließlich Veränderungen in der Sonnenstrahlung und dem Ausstoß von Sonnenmaterial) und ihr Erscheinungsbild (Veränderungen in der Anzahl und Größe von Sonnenflecken, Flares und anderen Erscheinungen) beschreibt. Diese Veränderungen wurden über Jahrhunderte hinweg beobachtet, sowohl durch Veränderungen im Aussehen der Sonne als auch durch auf der Erde beobachtete Phänomene wie Polarlichter. Die Veränderungen auf der Sonne haben Auswirkungen im Weltraum, in der Atmosphäre und auf der Erdoberfläche. Obwohl es die Hauptkomponente der Sonnenaktivität ist, treten auch unregelmäßige Schwankungen auf. [720 chars] |
| Lokale und regionale Meeresspiegel zeigen weiterhin typische natürliche Schwankungen, an einigen Orten steigen sie, an anderen sinken sie. [138 chars] | Der mittlere Meeresspiegel (MSL) (abgekürzt einfach Meeresspiegel) ist ein Durchschnittswert der Oberfläche eines oder mehrerer Ozeane der Erde, von dem Höhen wie Höhenlagen gemessen werden können. MSL ist eine Art vertikaler Datumsbezug, ein standardisierter geodätischer Referenzpunkt, der beispielsweise in der Kartografie und der Schifffahrtsnavigation als Kartenbezugspunkt oder in der Luftfahrt als Referenz für den Meeresspiegel verwendet wird, bei dem der Luftdruck gemessen wird, um die Flughöhe und damit die Flugflughöhen zu kalibrieren. Ein gängiger und relativ einfacher Standard für den mittleren Meeresspiegel ist der Mittelpunkt zwischen mittlerer Niedrig- und mittlerer Hochwasserlinie an einem bestimmten Ort. Meeresspiegel können von vielen Faktoren beeinflusst werden und haben sich über geologische Zeiträume hinweg stark verändert. Die genaue Messung von Veränderungen des MSL kann Einblicke in den fortschreitenden Klimawandel bieten, und der Anstieg des Meeresspiegels wird hä... [1,000 / 1,164 chars] |

### Public Sources

- [CLIMATE-FEVER: A Dataset for Verification of Real-World Climate Claims](https://arxiv.org/abs/2012.00614), 2020.
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663), 2021.
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595), 2025.
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-de](https://huggingface.co/datasets/hakari-bench/NanoBEIR-de)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| CLIMATE-FEVER: A Dataset for Verification of Real-World Climate Claims | 2020 | task paper | [https://arxiv.org/abs/2012.00614](https://arxiv.org/abs/2012.00614) |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | [https://arxiv.org/abs/2104.08663](https://arxiv.org/abs/2104.08663) |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | [https://arxiv.org/abs/2502.13595](https://arxiv.org/abs/2502.13595) |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | [https://huggingface.co/collections/zeta-alpha-ai/nanobeir](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
