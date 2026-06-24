# NanoIFIR / NanoIFIRFire

## Overview

`NanoIFIRFire` is an English legal precedent retrieval task in NanoIFIR derived from IFIR's FIRE legal subset. The queries are long case summaries or citation-context instructions, and the documents are prior Indian Supreme Court case documents.

This task evaluates retrieval of citable prior cases. The relevant relation is legal reasoning support: a positive document should help support the current case's legal issue, holding, or precedent need, not merely share broad legal vocabulary.

## Details

### What the Original Data Measures

IFIR describes its FIRE2017 legal subset as retrieving prior cases that support the reasoning process for the current case. It also notes that legal instructions can be very long because they include lengthy case descriptions, creating a long-instruction stress test for retrieval models.

The FIRE 2017 IRLeD Precedence Retrieval task asks systems to retrieve relevant or citable prior case documents for Indian Supreme Court cases. Legal texts are long and structurally complex, and legal practitioners often care about recall over multiple relevant authorities.

### Observed Data Profile

This Nano split contains 167 queries, 1,739 documents, and 563 positive qrels. Queries have 3.37 positives on average, with a minimum of 1, a median of 3.0, and a maximum of 5. There are 156 multi-positive queries, or 93.41% of the split. Queries average 3,283.81 characters, and documents average 27,167.67 characters.

Observed queries describe appeals involving murder convictions, sexual assault acquittals, charges under sections of the Indian Penal Code, service suspension, customs valuation, and other long legal disputes. Documents are Supreme Court judgments with citations, procedural history, legal principles, and holdings.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.3566, hit@10 of 0.7006, and recall@100 of 0.7567 with a top-500 candidate pool. BM25 is stronger here than in `NanoIFIRAila`, likely because many queries and precedents share statutory sections, citation language, offense labels, and legal phrases.

Even so, lexical retrieval is incomplete. Similar words can appear in cases with different facts or holdings, and relevant precedent may depend on reasoning role rather than repeated terms.

### Dense Evaluation Profile

The dense harrier-oss-270m profile reaches nDCG@10 of 0.3421, hit@10 of 0.6946, and recall@100 of 0.7105. Dense retrieval is slightly weaker than BM25 across the main metrics.

This suggests that general dense embeddings do not fully capture long legal precedent relations in this split. They may find broadly related legal disputes, but exact statutes, procedural context, and citation-style lexical anchors remain important.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate subset reaches nDCG@10 of 0.3996, hit@10 of 0.7904, and recall@100 of 0.7904. It uses 100 candidates per query, with 12 rank-101 safeguard positives.

Hybrid retrieval is strongest across the profile. It combines BM25's legal-term precision with dense semantic coverage, giving the best top-10 ranking and the best relevant coverage. This is a good candidate pool for legal reranking experiments.

### Metric Interpretation for Model Researchers

`NanoIFIRFire` is a legal retrieval task where hybrid search is clearly helpful. BM25 is a competitive baseline because legal documents reuse statutes, offenses, and citation formulas. Dense-only retrieval is not enough, but it contributes when combined with lexical matching.

Because most queries have multiple positives, recall@100 is important. nDCG@10 measures whether citable prior cases are surfaced early enough for legal research. A model that improves this task likely handles both exact legal signals and precedent-level similarity.

### Query and Relevance Type Tendencies

Queries are long current-case summaries with facts, statutes, procedural posture, and legal issues. Documents are long prior judgments from Indian Supreme Court material.

The relevance relation is citable prior-case relevance. Positives may share a statute, offense, issue, legal standard, or reasoning pattern with the current case.

### Representative Failure Modes

BM25 may retrieve cases with the same statutory section but different legal questions. Dense retrieval may retrieve cases with similar fact narratives but different holdings. Hybrid retrieval improves both, but still needs reranking to identify whether a case is actually citable for the issue.

Long documents also create dilution: a relevant holding or cited principle may be a small part of a lengthy judgment.

### Training Data That May Help

Useful training data includes non-overlapping FIRE IRLeD precedence retrieval pairs, Indian Supreme Court citation-prediction data, legal case similarity datasets, long-context legal retrieval data, and same-issue hard negatives.

Training should exclude `NanoIFIRFire` queries, qrels, and positive cited prior-case documents.

### Model Improvement Notes

Improving this task requires legal-domain matching over long contexts. Models should represent statutes, offenses, procedural posture, holdings, and citation role separately.

For reranking, the key signal is whether the prior judgment would support the current case's reasoning. Citation-aware objectives and issue-level segmentation may be more useful than generic document embeddings.

## Example Data

| Query | Positive document |
| --- | --- |
| The legal case at hand involves an appeal challenging the order of the Calcutta High Court that upheld the conviction and life imprisonment sentence of the appellant under Section 302 of the Indian Penal Code, 1860. The prosecution's case revolved around an incident where the appellant shot the deceased, who later succumbed to his injuries. The prosecution presented witnesses, including the FIR maker, the deceased's wife, and individuals who heard the deceased identify the appellant as his assai... [500 / 2,854 chars] | 416; 1985 (2) SCR 621; 1985 (1) SCC 552; 1985 (1) SCALE 108 (18 January 1985) CHANDRACHUD, Y.V. ((CJ) CHANDRACHUD, Y.V. ((CJ) SEN, AMARENDRA NATH (J) CITATION: 1985 AIR 416 1985 SCR (2) 621 1985 SCC (1) 552 1985 SCALE (1)108 CITATOR INFO : R 1992 SC1817 (17) Indian Penal Code. ss. 300 302 and 304-Murder and culpable homicide not amounting to murder-Distinction between. Indian Evidence Act-Evidence-Appreciation of-Dying declaration-If true, whether corroboration necessary-Death caused and/or atrocities perpetrated while in police custody-Burden of proof-Need for re-examination by legislature. Criminal Law-Petty details and minor contradictions in evidence-Whether can tilt the scale of justice. Respondent 1 was the Station House Officer and Respondents 2 to 4 were attached as constables to the Police Station. The prosecution alleged that a complaint was filed against the deceased for cattle trespass. The Respondent pursuant to the said complaint sought to extort illegal gratification fro... [1,000 / 27,331 chars] |
| The legal case in question involves an appeal filed by the State of Rajasthan against the acquittal of the accused-respondent by the High Court of Rajasthan in a case of sexual assault under Section 376 of the Indian Penal Code. The prosecution's case revolved around the testimony of the prosecutrix, a 15-year-old girl who was allegedly raped by the accused in a secluded area near her home. The prosecutrix narrated the incident to her father and another woman immediately after it occurred, and a... [500 / 3,018 chars] | (5) SCC 518; 1995 (6) JT 437; 1995 (4) SCALE 752 (11 August 1995) AHMADI A.M. (CJ) AHMADI A.M. (CJ) SEN, S.C. (J) CITATION: 1995 AIR 2472 1995 SCC (5) [518 JT 1995] (6) 437 1995 SCALE (4)752 Ahmadi, CJI Special leave granted. The appellant challenges his conviction under Section 376, IPC, and the sentence and fine imposed on him. The facts leading to the conviction, briefly stated, are that the prosecutrix (PW 1) Panchbai, was working at a factory where she had reported for duty on the morning of 28.8.1987 around 8.00 a.m. Her job was to lift boulders and place them within the factory premises. While she was working inside the factory, another labourer by the name Charan was also present. The appellant and his companion Pyaru came to the factory premises, asked Charan to fetch tea and on his departure the appellant lifted her bodily and took her inside the machine room, placed her on the ground, undressed her from below the waist and had sexual intercourse with her. Pyaru, since acquit... [1,000 / 12,815 chars] |
| The legal case involves an appeal against the judgment of acquittal recorded by a Trial Court in a case where the appellants were charged with offences under Section 307 and 307 read with Section 109 of the Indian Penal Code. The incident took place in a village where the accused allegedly attacked the victim with a weapon, resulting in severe injuries. The trial court acquitted the accused based on various grounds including doubts regarding the evidence of witnesses and inconsistencies in their... [500 / 3,651 chars] | 1988 (2) Suppl.SCR 391; 1988 (4) SCC 302; 1988 (3) JT 544; 1988 (2) SCALE 632 (12 August 1988) VENKATACHALLIAH, M.N. (J) VENKATACHALLIAH, M.N. (J) SEN, A.P. (J) CITATION: 1988 AIR 2154 1988 SCR Supl. (2) 391 1988 SCC (4) [302 JT 1988 ] (3) 544 1988 SCALE (2)632 Constitution of lndia 1950: Article 136-Supreme Court does not interfere with findings of fact reached by High Court unless vitiated by serious errors. The respondents were put on trial for offences under section 302 read with section 34, IPC. At the trial the prosecution mainly relied on the eye- witnesses and the statement of the deceased recorded by the Investigating Officer, which was sought to be used as a dying declaration. The defence assailed the credibility of the eye-witnesses as well as the authenticity of the dying declaration. The Sessions Judge accepted the prosecution case that notwithstanding the somewhat serious injuries inflicted on him, the deceased was in a position to instant the preparation of the First Inf... [1,000 / 33,988 chars] |

### Source Reference Table

| Source | Role |
| --- | --- |
| [IFIR: A Comprehensive Benchmark for Evaluating Instruction-Following in Expert-Domain Information Retrieval](https://arxiv.org/abs/2503.04644) | Expert-domain instruction-following IR benchmark paper. |
| [Overview of the FIRE 2017 IRLeD Track: Information Retrieval from Legal Documents](https://ceur-ws.org/Vol-2036/T3-1.pdf) | Original legal precedence retrieval overview. |
| [hakari-bench/NanoIFIR](https://huggingface.co/datasets/hakari-bench/NanoIFIR) | Nano benchmark dataset containing this split. |

### Representative Snippets

| Query Pattern | Positive Document Pattern |
| --- | --- |
| A case summary challenging a murder conviction and life sentence under Section 302 of the Indian Penal Code. | A prior Supreme Court judgment involving criminal conviction reasoning and cited precedent. |
| A state appeal against acquittal in a sexual assault case under Section 376. | A prior judgment discussing standards for evaluating sexual assault evidence and acquittal review. |
| A case involving charges under Section 307 and Section 109 of the Indian Penal Code. | A judgment about attempted murder, abetment, acquittal, or appellate review principles. |
| A service-law dispute involving suspension of a State Bank of India employee. | A prior judgment about disciplinary proceedings, service law, or procedural fairness. |
| A customs valuation dispute involving imported iron ore pellets. | A prior judgment about customs valuation, tribunal review, or statutory interpretation. |
