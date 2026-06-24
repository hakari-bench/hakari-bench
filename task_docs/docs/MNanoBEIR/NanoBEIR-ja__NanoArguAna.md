# MNanoBEIR / NanoBEIR-ja / NanoArguAna

## Overview

`NanoBEIR-ja__NanoArguAna` is the Japanese NanoBEIR version of ArguAna, an
argument and counterargument retrieval benchmark. The task uses Japanese
translated argumentative passages as queries and asks the retriever to find the
paired Japanese translated counterargument or closely matched argumentative
response. The Nano split contains 50 queries, 3,635 documents, and 50 positive
qrels, with exactly one positive document per query. Queries are long
argumentative passages rather than short keywords, so the task tests whether a
model can identify stance, premise, and argumentative relation across long
translated text.

## Details

### What the Original Data Measures

[ArguAna](https://aclanthology.org/P18-1023/) was introduced for argument
retrieval and argument matching in debate-style text. BEIR includes ArguAna as
an argument retrieval task in which the system must retrieve a corresponding
argumentative text rather than a factual answer passage. In this Japanese
NanoBEIR version, long translated claims and supporting paragraphs are used as
queries, and the relevant document is usually the counterargument or paired
argument that responds to the same issue. The benchmark therefore measures
argument-level semantic matching, not just topic retrieval.

### Observed Data Profile

The task has 50 queries and 3,635 documents. It contains 50 positive qrels, and
every query has exactly one positive. Query length is unusually high, averaging
553.90 characters, while documents average 458.77 characters. The examples are
full debate passages about public indifference to reform, airport expansion,
advertising and happiness, cyber attacks, and religious speech. Long inputs
provide many lexical anchors, but they also contain multiple premises and
supporting details that can distract a retriever from the actual argumentative
relation.

### BM25 Evaluation Profile

The BM25 top-500 subset reaches nDCG@10 = 0.3620, hit@10 = 0.6600, and
Recall@100 = 0.8800. Long queries give BM25 many repeated terms and topical
anchors, so lexical retrieval can often find a relevant candidate within the
top 100. The top-10 score is much weaker, however, because the correct paired
argument is not always the document with the greatest word overlap. Documents
from the same debate topic may share terms while responding to a different
premise or taking a different stance.

### Dense Evaluation Profile

The dense `harrier-oss-270m` top-500 subset reaches nDCG@10 = 0.4239, hit@10 =
0.7800, and Recall@100 = 0.9400. Dense retrieval is the strongest profile for
top-10 ranking on this task. The result indicates that embedding similarity is
better able to connect long argumentative passages by meaning, stance, and
response structure than BM25 alone. This is especially important in translated
Japanese text, where the counterargument may not reuse the same surface forms
as the query but still addresses the same proposition.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses 100 to 101 candidates per query and reaches
nDCG@10 = 0.4022, hit@10 = 0.7600, and Recall@100 = 0.9600. Two queries use the
rank-101 safeguard. Hybrid retrieval has the best top-100 coverage, while dense
retrieval remains better on nDCG@10 and hit@10. This means that combining
lexical and dense search is useful for keeping the single positive in the
candidate set, but the fused order can still rank topical lexical matches above
the best semantic counterargument.

### Metric Interpretation for Model Researchers

This task separates candidate coverage from argumentative ranking. BM25 is not
enough for early precision, even with long text, because word overlap often
tracks topic more than argumentative relation. Dense retrieval is the best
single profile for ranking the positive near the top, suggesting that semantic
representations are essential for counterargument matching. Hybrid retrieval is
best for Recall@100 and is therefore attractive for reranking pipelines. A
strong model should improve dense-like top-rank behavior while preserving the
hybrid candidate coverage.

### Query and Relevance Type Tendencies

The examples involve long policy or social debate passages. The positive
document often challenges a premise, presents a counterexample, or reframes the
claim. Relevance depends on whether the document responds to the same argument,
not simply whether it discusses the same topic. This makes stance, premise
tracking, and discourse relation important features for model analysis.

### Representative Failure Modes

BM25 can retrieve documents that share issue words such as reform, airport
expansion, advertising, cyber attacks, or religion but do not answer the query's
specific claim. Dense retrieval can retrieve semantically related debate text
that is on-topic but not the paired counterargument. Hybrid retrieval can
increase coverage while still placing broad topic matches above the exact
argument pair. Single-positive evaluation makes these rank-order errors costly.

### Training Data That May Help

Useful training data includes non-overlapping argument retrieval,
counterargument pairs, stance-aware retrieval, Japanese debate text, and
multilingual argument mining data. Hard negatives should address the same topic
while responding to a different premise or stance. Training should exclude
ArguAna, BEIR, NanoBEIR, and translated argument records likely to overlap with
this benchmark.

### Model Improvement Notes

Strong systems should encode long argumentative passages without collapsing them
into coarse topic vectors. Useful improvements include stance-aware contrastive
training, hard negatives from the same debate topic, and reranking features that
compare the claim, premise, and response relation. Candidate generation should
retain lexical coverage, but final ranking needs argument-structure awareness.

## Example Data

| Query | Positive document |
| --- | --- |
| 一般大衆は改革に対して無関心である。現在の経済情勢において上院の改革が最優先事項であるべきかどうかは議論の余地があるし、連立政権がそのような措置を開始し、貫徹できるかどうかも疑わしい。上院改革を試みようとする動きは繰り返し遅延しており、下院が変化に対して懐疑的であることを示している。[1] これは、最近の付加投票制（Alternative Vote）の是非を問う国民投票の結果が示すように、英国の世論にも間違いなく反映されている――すなわち、一般大衆は変化に対して否定的か、あるいは無関心なのである。[2] [1] Summers, Deborah, 『Labour's attempts to reform the House of Lords』, The Guardian (2009年1月27日), 2011年6月1日閲覧 [2] BBC News, 『Vote 2011: UK rejects alternative vote』, 2011年5月7日 [435 chars] | AVキャンペーンを貴族院の改革と比較することはできない。さらに、政治的プロパガンダによって誤解している有権者を、無関心と混同してはならない。有権者は、自分たちでは何も変えられない、自分の一票が意味を持たないと感じているために無関心を示すことが多い。国民が直接選挙で国を運営する人々を選べるような改革は、こうした無力感に歯止めをかけるのに役立つだろう。 [175 chars] |
| ヒースロー空港の拡張は経済にとって極めて重要である。ヒースローの拡張により、現在の多くの雇用が守られると同時に、新たな雇用も創出されるだろう。現在、ヒースロー空港は約25万人の雇用を支えている[1]。これに加え、ロンドンの観光産業にも何十万人もの人々が依存しており、その観光産業はヒースローのような良好な交通結節点に頼っている。他の欧州の空港に対して競争力を失うことは、新たな雇用の創出機会を逃すだけでなく、既存の雇用を失う可能性さえある。ヒースローの拡張は、不況の影響で英国のインフラ投資が非常に低い状況にある今、重要なインフラの一部を構築することになり、成長を後押しする助けとなるだろう。良好な航空便の接続は、新たなビジネスを惹きつけ、既存のビジネスを維持するために不可欠である。これは、航空インフラが新たなビジネス機会を発見するために重要だからだ。英国の経済的将来は、ヨーロッパやアメリカといった従来の貿易相手国だけでなく、重慶や成都といった中国やインドの成長著しい都市との貿易にかかっている[2]。こうした都市に拠点を置く企業は、直行便があれば、英国への投資をはるかに積極的に行うだろう[3]... [500 / 651 chars] | ビジネス界は、第3滑走路建設への支持に関して決して一致しているわけではない。調査によれば、多くの有力企業が実際には拡張に賛成していないことが示されている。Sainsbury'sの最高経営責任者ジャスティン・キング氏やBskyBのジェームズ・マーカス氏も含む、懸念を表明する書簡に署名している[1]。したがって、ビジネス界を拡張を一丸となって求める存在として描くのは誤りである。ヒースロー空港の新滑走路以外の選択肢、たとえば他のロンドン近郊の空港に新滑走路を建設する案や、まったく新しい空港を建設する案を検討する際には、それらもヒースロー拡張と同程度の経済的影響をもたらす可能性があることを覚えておくべきである。ビジネスや観光客の誘致において重要なのがアクセスの便であれば、ロンドンとの接続さえ確保されていれば、どの空港から接続しているかは問題ではない。かつてブリティッシュエアウェイズの最高経営責任者を務めたボブ・エイリング氏が指摘したように、ロンドンへの便益を重視するのであれば、空港がハブ空港である必要さえないかもしれない。彼は、ヒースロー空港は乗り継ぎのための拠点ではなく、ロンドンへ来たい旅客に焦点を当てるべきだと述べ、第3滑走路建設は「高価な過ち」になる可能性があると警告した[2]。 [1] オズボーン、アリスター、「Kingfisher最高経営責任者イアン・チェシャー氏、ヒースロー滑走路の成功に疑問を呈す」、ザ・テレグラフ、2009年7月13日、 [2] スチュワート、ジョン、「ヒースローに関するHACANからのブリーフィング：2012年6月」 [685 chars] |
| 人々にはあまりにも多くの選択肢が与えられており、それによって幸福度が低下している。広告は人々の注意を引きつけようとする数え切れない要求を生み出し、その結果、選択の多さに圧倒される状態、いわゆる「選択の専制（チョイス・オーバーロード）」を引き起こす。最近の研究によると、人々は30年前と比べて平均して幸福度が下がっている。これは、経済的に豊かになり、お金の使い道の選択肢がはるかに増えたにもかかわらずである1。広告が繰り広げる宣伝は人々の心に次々と押し寄せ、製品に対する期待を高め、購入後に必ずといってよい失望をもたらす。最近、ある化粧品の広告が、製品の効果を実際以上に宣伝したとして、英国で禁止された2。買い物をする人々は、不満足な購入は自分自身がより賢明に選ばなかったせいだと感じ、他のものを選ばなかったことを後悔する。中にはあまりにも選択肢に圧倒されて、まったく選べない人もいる。 1 Schwartz, The Tyranny of Choice, 2004. 2 Kekeh, Too Beautiful? British MP Draws Line in Sand for Cosmetic... [500 / 515 chars] | 人々が不満を感じているのは、すべてを持てないからであって、選択肢が多すぎてストレスを感じるからではない。実際、広告は人々が持っているお金を使い、自分にとって最も適切な製品を購入するようにする上で極めて重要な役割を果たしている。もし広告が認められなければ、人々は最初に手にした製品に無駄にお金を使ってしまうだろうが、選択肢があれば明らかに他の製品を選ぶはずである。50件の独立した研究を統合したメタアナリシスでは、選択肢の数と不安の間に有意な関連性は見られなかったが、研究間のばらつきから、選択肢の過剰が、特定の非常に限定的で、まだ十分に理解されていない前提条件と関連している可能性は否定できないと推測している1。 1 ^ Scheibehenne, Benjamin; Greifeneder, R. & Todd, P. M. (2010). "Can There Ever be Too Many Options? A Meta-Analytic Review of Choice Overload". Journal of Consumer Research 37: 409-425. [497 chars] |

### Public Sources

- [Argument Mining for Understanding Peer Reviews](https://aclanthology.org/P18-1023/).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).
- [hakari-bench/NanoBEIR-ja](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ja).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Argument Mining for Understanding Peer Reviews | 2018 | task paper | [https://aclanthology.org/P18-1023/](https://aclanthology.org/P18-1023/) |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | [https://arxiv.org/abs/2104.08663](https://arxiv.org/abs/2104.08663) |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | [https://arxiv.org/abs/2502.13595](https://arxiv.org/abs/2502.13595) |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | [https://huggingface.co/collections/zeta-alpha-ai/nanobeir](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
