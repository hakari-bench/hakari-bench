# MNanoBEIR / NanoBEIR-fr / NanoNFCorpus

## Overview

This task is the French NanoBEIR version of NFCorpus, a medical information retrieval benchmark built from consumer health and nutrition information needs linked to biomedical articles. The original NFCorpus collection was designed to expose the vocabulary gap between lay health topics and medical literature. In this NanoBEIR slice, short French translated health queries must retrieve French translated medical or biomedical documents from 2,953 candidates. The task contains 50 queries and 1,651 positive relevance judgments, with an average of 33.02 positives per query. It is a many-positive biomedical retrieval benchmark where models must recover a set of relevant evidence documents, not just one answer passage.

## Details

### What the Original Data Measures

NFCorpus measures medical and nutrition retrieval where lay queries are linked to scientific evidence. Queries may be short food, diet, disease, supplement, or health-topic labels, while relevant documents are long biomedical abstracts or summaries. The task rewards models that bridge consumer wording to technical terminology, interventions, mechanisms, outcomes, and study contexts.

### Observed Data Profile

The French Nano task has 50 queries, 2,953 documents, and 1,651 positives. Positives per query average 33.02, with a median of 23.5 and a maximum of 100. Forty-seven queries are multi-positive. Queries are very short, averaging about 29 characters, while documents are long, averaging about 1,811 characters. Examples include healthy chocolate milkshakes, medical ethics, fava beans, chicken nuggets, and saturated fats. Documents are translated biomedical abstracts or scientific summaries.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.303, Hit@10 of 0.640, and Recall@100 of 0.167. Sparse retrieval often finds at least one relevant document when a query term directly appears in a medical abstract. However, recall is low because each query has many positives and because lay wording does not always match biomedical vocabulary. BM25 can also over-rank documents that share a food or disease term while studying a different outcome.

### Dense Evaluation Profile

The dense harrier-oss-270m baseline is slightly stronger in recall, with nDCG@10 of 0.305, Hit@10 of 0.620, and Recall@100 of 0.196. Dense retrieval helps bridge lay French health terms to scientific concepts, but the gains are modest. The task remains difficult because generic semantic similarity does not fully capture medical relevance, intervention-outcome specificity, or the diversity of the positive evidence set.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid profile reaches nDCG@10 of 0.310, Hit@10 of 0.580, and Recall@100 of 0.203, with eight safeguard rows at 101 candidates. It gives the best nDCG@10 and Recall@100 but the lowest Hit@10 among the three profiles. This suggests that hybrid search improves evidence-set coverage and graded ranking, while sometimes failing to place at least one positive in the top 10 for queries where BM25's direct term match works. For biomedical retrieval, both exact terminology and semantic expansion are necessary but insufficient.

### Metric Interpretation for Model Researchers

Hit@10 is not enough for NFCorpus because every query can have many relevant documents. A model can hit one abstract while missing most of the evidence set. Recall@100 is especially important and remains low across all methods. nDCG@10 measures whether the first page contains relevant medical evidence, but researchers should also inspect coverage across different evidence clusters for the same health topic.

### Query and Relevance Type Tendencies

Queries are short French health topics or lay questions. Relevant documents are long biomedical abstracts, clinical summaries, or article descriptions. A single query can map to studies about different populations, mechanisms, interventions, and outcomes. Hard negatives often share a disease or diet word but do not address the same medical relevance relation.

### Representative Failure Modes

BM25 can miss positives that use technical terminology instead of lay wording. Dense retrieval can retrieve medically adjacent abstracts that are not relevant to the specific topic. Hybrid retrieval improves coverage but still misses most positives for many queries. Failure analysis should focus on missing evidence clusters, not only the first retrieved document.

### Training and Leakage Considerations

Training should exclude NFCorpus, BEIR, NanoBEIR, and translated NutritionFacts records likely to overlap with these queries or linked medical documents. Useful non-overlapping data includes biomedical IR datasets, consumer-health question to abstract pairs, PubMed relevance ranking data, and French or multilingual medical retrieval supervision. Multi-positive training is recommended because most queries require multiple valid evidence documents.

### Model Improvement Signals

Strong models should improve lay-to-technical medical matching and evidence-set recall. Useful signals include biomedical synonym mapping, consumer health questions paired with abstracts, hard negatives sharing disease or food terms, and cluster-level positives. Hybrid systems should preserve exact medical terms while dense representations expand toward mechanisms, interventions, and outcomes.

## Example Data

| Query | Positive document |
| --- | --- |
| Milkshakes au chocolat santé [28 chars] | Objectif : Étudier la relation entre la consommation de cerises et le risque de crises de goutte récidivantes chez les personnes atteintes de goutte. Méthodes : Nous avons mené une étude cas-témoins appariés pour examiner les associations entre un ensemble de facteurs de risque présumés et les crises de goutte récidivantes. Des individus atteints de goutte ont été recrutés de manière prospective et suivis en ligne pendant un an. Les participants ont été interrogés sur les informations suivantes lors d'une crise de goutte : la date de début de la crise, les symptômes et signes, les médicaments (y compris les médicaments anti-goutte), et les facteurs de risque potentiels (y compris la consommation quotidienne de cerises et d'extrait de cerise) durant les 2 jours précédant la crise. Nous avons évalué les mêmes informations d'exposition sur des périodes de contrôle de 2 jours. Nous avons estimé le risque de crises de goutte récidivantes liées à la consommation de cerises en utilisant une r... [1,000 / 2,038 chars] |
| éthique médicale [16 chars] | CONTEXTE : L'un des principaux défis dans la gestion du cholestérol sérique par l'intervention diététique semble être l'amélioration de l'adhésion des patients. OBJECTIFS : Explorer les nombreuses questions concernant les obstacles et les motivations à l'adhésion à un régime hypocholestérolémiant. MÉTHODES : Nous avons enquêté sur les pratiques diététiques des médecins généralistes français pour les patients atteints d'hypercholestérolémie, et examiné les attitudes de leurs patients envers une telle approche. RÉSULTATS : Nous avons analysé 234 questionnaires personnels de médecins et 356 auto-questionnaires de patients. Les raisons invoquées par les patients pour ne pas suivre le régime prescrit incluaient : « déjà avoir des habitudes alimentaires satisfaisantes » (34,7 %), « refus de subir une privation nutritionnelle » (33,3 %), « difficultés à concilier un régime avec la vie de famille » (27,8 %) et « prise de médicaments hypocholestérolémiants » (22,2 %). Malgré une compréhension g... [1,000 / 2,144 chars] |
| fèves [5 chars] | Au cours des 20 dernières années, l'intérêt croissant pour la biochimie, la nutrition et la pharmacologie de la L-arginine a conduit à des études approfondies visant à explorer ses rôles nutritionnels et thérapeutiques dans le traitement et la prévention des troubles métaboliques humains. Des preuves émergentes montrent que la supplémentation en L-arginine alimentaire réduit l'adiposité chez les rats génétiquement obèses, les rats obèses par le régime alimentaire, les porcs en finition et les sujets humains obèses atteints de diabète de type 2. Les mécanismes responsables des effets bénéfiques de la L-arginine sont probablement complexes, mais impliquent finalement la modification de l'équilibre entre l'apport et la dépense énergétique en faveur de la perte de graisse ou de la réduction de la croissance du tissu adipeux blanc. Des études récentes indiquent que la supplémentation en L-arginine stimule la biogenèse mitochondriale et le développement du tissu adipeux brun, possiblement pa... [1,000 / 1,531 chars] |

## Public Sources

- [NFCorpus paper](https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf)
- [NFCorpus project page](https://www.cl.uni-heidelberg.de/statnlpgroup/nfcorpus/)
- [BEIR benchmark](https://github.com/beir-cellar/beir)
- [MMTEB benchmark](https://arxiv.org/abs/2502.13595)
- [NanoBEIR dataset](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

## Source Reference Table

| Label | URL |
|---|---|
| NFCorpus paper (https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf) |
| NFCorpus project page (https://www.cl.uni-heidelberg.de/statnlpgroup/nfcorpus/) |
| BEIR benchmark (https://github.com/beir-cellar/beir) |
| MMTEB benchmark (https://arxiv.org/abs/2502.13595) |
| NanoBEIR dataset (https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
