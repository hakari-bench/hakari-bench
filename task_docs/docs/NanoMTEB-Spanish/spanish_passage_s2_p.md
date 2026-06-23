# NanoMTEB-Spanish / spanish_passage_s2_p

## Overview

`spanish_passage_s2_p` is the document-level version of the Spanish Passage Retrieval health dataset. The source test collection was created for Spanish-speaking users with consumer health information needs, especially baby care, vaccination, and low back pain. In this S2P variant, a Spanish health question is the query and the relevant documents are full Spanish health-related web pages that contain answer-bearing passages. The task therefore evaluates whether a retriever can find the right page, even when the answer is only one part of a long document.

The Nano split contains 167 queries, 7,501 documents, and 996 positive relevance judgments. Queries average about 68 characters, while documents average about 2,711 characters. Almost every query has multiple positives: 165 of 167 queries have more than one relevant page, with an average of 5.96 positives and a maximum of 19. This is a multi-positive consumer-health retrieval task, where broad candidate coverage and careful top-rank ordering both matter.

## Details

### What the Original Data Measures

The Spanish Passage Retrieval collection was designed to evaluate retrieval for Spanish health-related resources. Its topics are expressed as natural-language questions and relevance was assessed at passage level, with links back to the source documents. The S2P task retrieves the source web page rather than only the extracted answer passage.

This distinction is important. A full page can contain a relevant answer passage alongside unrelated sections, navigation text, headings, or broader medical background. A model must connect the user's health question to a page that contains the answer, not necessarily to a page whose whole text is about the exact query.

### Observed Data Profile

Documents are long consumer-health web pages. They may include headings, educational explanations, procedural advice, and multiple subtopics. Queries ask about breastfeeding benefits, introducing complementary foods, feeding on demand, free vaccines, vaccination for infectious disease prevention, emergency contacts, pediatric checkups, newborn weight, and baby care in hot weather.

The high multi-positive rate means that many questions have several useful pages. Some pages may answer the question directly; others may contain the answer passage in a broader article. Evaluation therefore rewards models that retrieve several relevant pages, not only a single best page.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.5129, hit@10 of 0.9162, and recall@100 of 0.8855. This is a strong lexical profile. Spanish health questions often share important words with the relevant pages, such as `vacunas`, `bebé`, `lactancia`, `amamantar`, `espalda`, and related terms. BM25 can usually find at least one relevant page quickly.

Its limitation is long-document noise and consumer-health paraphrase. A page may use formal medical wording while the query is phrased as a layperson question. Conversely, a long page can mention many medical terms and still not answer the specific question. BM25 is useful but not sufficient for ranking all relevant pages optimally.

### Dense Evaluation Profile

The dense `harrier-oss-270m` run reports nDCG@10 of 0.4719, hit@10 of 0.9281, and recall@100 of 0.8363. Dense retrieval slightly improves hit@10 over BM25 but loses nDCG and recall. This suggests that dense similarity can identify some answerable pages, but it is less reliable at covering the full set of relevant long documents.

The pattern is understandable for S2P. Full pages are long and may contain multiple topics, which can dilute the embedding signal. Dense retrieval may prefer semantically coherent pages that match the query globally, while missing pages where the relevant answer is a smaller passage inside a broader article.

### Reranking Hybrid Evaluation Profile

`reranking_hybrid` is strongest, with nDCG@10 of 0.6220, hit@10 of 0.9880, and recall@100 of 0.9488. Candidate lists contain 100 to 101 items, and 1 row uses the positive safeguard. The hybrid profile combines BM25's strong health-term coverage with dense semantic matching of consumer questions.

This is the most appropriate first-stage profile for S2P. The task needs lexical preservation of medical and childcare terms, but it also benefits from semantic matching across layperson paraphrases. Hybrid retrieval improves both top-rank quality and candidate coverage.

### Metric Interpretation for Model Researchers

This split is hybrid-favorable. BM25 is strong because health pages and questions share domain vocabulary, dense retrieval helps some query-to-page semantic matches, and the hybrid combination is best across all reported metrics. The long-document setting makes pure dense retrieval less dominant than in short answer-passage retrieval.

Because almost all queries have multiple positives, hit@10 should not be read alone. A model can find one relevant page while missing many other useful pages. nDCG@10 and recall@100 are more informative for judging how well the system ranks and preserves the relevant page set.

### Query and Relevance Type Tendencies

Representative queries ask about the benefits of breast milk, when to introduce foods beyond breastfeeding, whether to breastfeed whenever the baby asks, which vaccines are free, and how vaccination prevents infectious disease. Relevant documents are full web pages containing answer passages, sometimes embedded inside broader health education content.

The task is layperson-oriented. Queries use everyday phrasing, while documents may use medical, institutional, or pediatric vocabulary. Good retrieval requires mapping between those styles.

### Representative Failure Modes

BM25 may over-rank long pages that mention the same medical term but do not answer the exact question. Dense retrieval may retrieve pages that are broadly about breastfeeding or vaccination but lack the specific answer passage. Hybrid retrieval reduces both risks but can still struggle when many pages cover the same broad health topic.

Another failure mode is page-level dilution. The correct answer may be only one paragraph in a long page. Models that embed or score the whole page as a single unit may under-rank it if the rest of the page is off-topic.

### Training Data That May Help

Useful training data includes Spanish consumer-health QA pairs, Spanish medical FAQ retrieval pairs, non-overlapping health web document retrieval data, and multi-positive document-level health retrieval examples. Training should exclude PRES evaluation questions, qrels, and overlapping Spanish health pages.

Hard negatives should be health pages from the same topic area that do not answer the specific question. For example, multiple vaccination pages with different eligibility or cost information are better negatives than unrelated pages.

### Model Improvement Notes

Dense models can improve by using passage-aware representations for long health pages or by aggregating answer-bearing sections rather than treating the whole document uniformly. Sparse systems remain valuable because medical and childcare terms are strong anchors. Hybrid systems are well matched to this task and should be paired with rerankers that can inspect local answer passages inside full pages.

For evaluation, this split is best read as consumer-health document retrieval. The strongest system should find pages that contain the answer, while preserving several relevant pages for users or downstream passage selection.

## Example Data

| Query | Positive document |
| --- | --- |
| ¿Cuáles son los beneficios de la leche materna? [47 chars] | Del 1 al 7 de agosto se celebra la Semana Mundial de la Lactancia Materna en más de 170 países. La Alianza Mundial pro lactancia materna (WABA) coordina las numerosas iniciativas previstas para esta semana, cuyo objetivo es fomentar la lactancia materna o natural y de esta manera mejorar la salud de los bebés en todo el mundo. La Semana Mundial de la Lactancia Materna conmemora una iniciativa, llamada Declaración de Innocenti, formulada por la OMS y UNICEF en agosto de 1990 con el fin de proteger, promover y respaldar la lactancia materna a nivel mundial. En la misma se reconoce que la lactancia materna es el mejor modo de proporcionar al recién nacido los nutrientes que necesita durante los primeros meses de vida. Por ello debería ser posible que todas las mujeres pudieran alimentar al pecho a sus hijos de forma exclusiva hasta los seis meses de edad. Para obtener esta meta hace falta que los países apoyen y refuercen una “cultura de la lactancia materna” en lugar de la “cultura del b... [1,000 / 2,811 chars] |
| ¿Cuándo debo introducir alimentos complementarios aparte de la lactancia materna? [81 chars] | Edad corregida en niños prematuros. El desarrollo de un niño prematuro no puede compararse con el de un bebé nacido a término, al menos hasta los dos años ¿Qué es la edad gestacional? La edad gestacional corresponde al tiempo que ha durado el embarazo y se contabiliza en semanas, desde el primer día de la última regla hasta el día del parto. ¿Qué es la edad cronológica (o edad postnatal)? Es el tiempo transcurrido después del nacimiento. Por lo general, se describe en días, semanas, meses y años. ¿A qué nos referimos con la edad corregida? La edad corregida es la edad que tendría el bebé si hubiera nacido a las 40 semanas, “corrige” o “ajusta” la madurez del bebé, según la intensidad de su prematuridad. La prematuridad, en semanas, se calcula restando a las 40 semanas (fecha teórica prevista del parto) el número de semanas reales de gestación al nacer. Se aconseja que la edad corregida se utilice solo hasta los 2 años de edad (24 meses de edad corregida). Por ejemplo, si el niño nació... [1,000 / 3,006 chars] |
| ¿Tendría que darle el pecho a mi bebé siempre que me lo pida? [61 chars] | ¿Con qué frecuencia debo amamantar al bebé? Durante el primer mes de vida, su recién nacido debería alimentarse entre ocho y 12 veces al día. Si tiene la sensación de que está amamantando a su bebé con más frecuencia que una amiga suya que ha optado por lactancia artificial, es posible que así sea. ¿Por qué? Porque la leche materna se digiere con más facilidad que la leche artificial, lo que significa que avanza más deprisa por el sistema digestivo del bebé y, consecuentemente, tarda menos tiempo en tener hambre. Asimismo, el hecho de amamantar frecuentemente a su bebé favorece su producción de leche durante las primeras semanas. Cuando tienen entre uno o dos meses de vida, la mayoría de los bebés suelen hacer entre siete y nueve tomas diarias. Hasta que se establezca su producción de leche, usted deberá amamantar a su bebé "a demanda" (cuando tenga hambre), lo que suele ser cada hora y media a tres horas. Conforme los recién nacidos crezcan, necesitarán mamar con menos frecuencia y de... [1,000 / 12,558 chars] |

### Source Reference Table

| Source | What it contributes |
| --- | --- |
| ECIR paper | Original Spanish health retrieval test collection. |
| Project page | Topic, document, and relevance-assessment description. |
| Source dataset card | Public dataset packaging. |
| MTEB task card | S2P retrieval formulation. |

### Representative Snippets

- A query asks about the benefits of breast milk; relevant pages discuss World Breastfeeding Week and the value of breastfeeding.
- A query asks when to introduce complementary foods; relevant pages discuss corrected age and early feeding guidance.
- A query asks whether to breastfeed whenever the baby asks; relevant pages describe feeding frequency for newborns.
- A query asks which vaccines are free; relevant pages describe publicly financed vaccines in Spain.
- A query asks about vaccination for preventing infectious diseases; relevant pages describe routine childhood vaccines and protected diseases.
