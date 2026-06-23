# NanoMTEB-Polish / cqadupstack_android

## Overview

`cqadupstack_android` is the Polish NanoMTEB version of the Android forum from CQADupStack, a benchmark derived from duplicate-question links in Stack Exchange communities. The source task asks a retrieval system to find questions that describe the same Android problem as the query, even when the wording, device model, application context, or proposed workaround differs. In this Polish version, the benchmark preserves the duplicate-question structure while presenting the task through translated Polish text. This makes it useful for studying whether a retrieval model can combine lexical technical matching with semantic recognition of equivalent troubleshooting situations.

The Nano task contains 200 queries, 10,000 candidate documents, and 809 positive relevance judgments. The average query is about 59 characters, while the average document is about 627 characters, so the task is mostly short technical questions matched against longer forum-style posts. Relevance is often one-to-many: 88 of the 200 queries have more than one positive document, and some queries have many duplicates. The task therefore rewards models that can recover a cluster of related Android questions, not only a single nearest paraphrase.

## Details

### What the Original Data Measures

CQADupStack was introduced to evaluate duplicate-question retrieval in community question answering forums. In the Android subset, relevance means that two posts ask substantially the same question, not merely that they mention the same phone, operating-system feature, or application. A relevant item may use different surface wording, a different device name, or a different description of the same user intent.

For model researchers, this task is especially informative because Android support questions mix several matching signals. Some queries are dominated by fixed technical names such as Google Play, ROM, emulator, home button, audio file, or screen capture. Others depend on a more abstract interpretation of user intent, such as saving instead of opening a file, displaying a phone screen during a presentation, or making headset controls perform track-skipping actions. The benchmark therefore exposes the difference between exact-term retrieval, dense semantic retrieval, and hybrid candidate construction.

### Observed Data Profile

The documents are longer than the queries and often contain explanatory context, attempted solutions, or environment details. Query-document matching is not simply title-to-title matching: a query may be terse, while a relevant document can include the fuller forum description. Because the corpus is translated into Polish, the task also tests robustness to Polish morphology, inflection, and translated technical phrases. English product names and Android-specific identifiers remain visible, creating a mixed-language technical vocabulary.

The relevance distribution is skewed. The median number of positives per query is 1, but the maximum is 100, and 44.0% of queries have multiple positives. This means aggregate metrics reflect both isolated duplicate pairs and broad duplicate clusters. A system that retrieves only one good match can perform acceptably on single-positive queries but lose recall on the clustered cases.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.3379, hit@10 of 0.5100, and recall@100 of 0.4030. This is a solid lexical baseline for a technical forum task, because Android questions often contain distinctive repeated terms. When the query includes names such as Google Play, emulator, ROM, or Bluetooth-style hardware controls, term frequency and exact overlap can place relevant documents near the top.

The limitation is that duplicate questions are not always lexical duplicates. A user may describe the same action through different verbs, mention the symptom rather than the feature, or include a device-specific story that hides the shared intent. Polish inflection also makes exact token overlap less reliable unless tokenization and normalization happen to align well. As a result, BM25 is useful for anchoring obvious technical terms, but it misses a meaningful portion of semantic duplicates.

### Dense Evaluation Profile

The dense `harrier-oss-270m` run is stronger on this task, with nDCG@10 of 0.4139, hit@10 of 0.6400, and recall@100 of 0.5006. The gain suggests that many Android duplicates are recoverable through embedding similarity rather than direct word overlap. Dense retrieval can connect questions about equivalent user goals, such as capturing a phone screen, changing download behavior, or controlling media playback, even when the wording is not identical.

This profile is typical of translated duplicate-question retrieval: semantic similarity is often more important than a single shared token. The model still benefits from technical anchors, but its advantage comes from grouping related troubleshooting intents. The higher hit@10 indicates that dense retrieval is better at placing at least one relevant duplicate in the first page of results.

### Reranking Hybrid Evaluation Profile

`reranking_hybrid` combines the BM25 and dense candidate behavior and reports nDCG@10 of 0.4121, hit@10 of 0.6250, and recall@100 of 0.5105. Its top-10 precision is almost tied with dense retrieval, while its recall@100 is the best of the three profiles. The candidate lists contain 100 to 101 items, and 25 rows required the relevance safeguard that keeps positives available for reranking diagnostics.

This pattern is useful: dense retrieval appears to rank the very top slightly better, but the hybrid candidate pool recovers more relevant material overall. For reranking experiments, this task benefits from using hybrid candidates because they include both lexical Android terminology and semantically similar duplicate formulations. A reranker evaluated only on one candidate source would miss part of the task's intended difficulty.

### Metric Interpretation for Model Researchers

The main lesson is that this Android subset favors dense retrieval for top-ranked answers, while hybrid retrieval is preferable when broad candidate coverage matters. BM25 remains competitive enough to expose lexical dependence, but it is not the best single method. If a new retrieval model improves only over BM25, that may indicate better semantic matching rather than full duplicate-question competence. If it improves over dense and `reranking_hybrid`, it is likely handling both technical terminology and paraphrased troubleshooting intent.

Because the task has many single-positive queries and several high-positive clusters, nDCG@10 and recall@100 should be read together. nDCG@10 reflects whether the most useful duplicates are ranked early; recall@100 reflects whether the model can preserve enough positives for downstream reranking. A model with high nDCG but lower recall may be good for direct search, while a model with stronger recall may be better as the first stage of a reranking pipeline.

### Query and Relevance Type Tendencies

Typical queries involve Android device behavior, file handling, emulator performance, localization, ROM-specific behavior, Google Play installation issues, screen mirroring, and media-control shortcuts. Relevant documents usually ask the same practical question from a different angle. The connection may be explicit through shared nouns, or implicit through a shared action such as "save instead of open" or "show the phone display on another screen."

The Polish translation makes grammatical variation important. A system should handle inflected nouns and verbs, borrowed English technical terms, and short queries that omit context. Good retrieval requires both recognizing stable Android vocabulary and abstracting from the exact wording of the forum post.

### Representative Failure Modes

Weak lexical systems may over-rank documents that share an Android term but ask a different question. For example, posts about Google Play can involve installation, authentication, application publishing, or account behavior; only some are duplicates. Dense systems may make the opposite mistake by retrieving conceptually adjacent troubleshooting posts that solve a similar kind of problem but do not ask the same duplicate question.

Hybrid candidate construction reduces these risks but does not remove them. If BM25 contributes many near-keyword false positives and dense retrieval contributes broad topical neighbors, the reranker still needs to decide whether the underlying user intent is identical. This task therefore remains useful for evaluating cross-encoder rerankers and late-stage duplicate detection.

### Training Data That May Help

Training data with duplicate questions, paraphrased troubleshooting queries, Stack Exchange style posts, and Polish technical text should help. Particularly relevant examples include pairs where one post is short and another contains longer context, pairs with translated English product names, and pairs where the same Android action is described through different verbs or symptoms.

Hard negatives are also important. The most valuable negatives are Android posts with strong term overlap but different intent, such as multiple Google Play questions that concern different failure modes. These negatives teach the model not to confuse topical similarity with duplicate-question relevance.

### Model Improvement Notes

For dense models, improvements should target Polish morphology, mixed Polish-English technical vocabulary, and short-to-long duplicate matching. For sparse or lexical systems, better tokenization and normalization can raise recall, but exact matching alone is unlikely to close the dense gap. For hybrid systems, the task suggests that candidate fusion is valuable because lexical and semantic retrieval recover complementary positives.

Researchers should pay attention to whether a model improves nDCG@10, recall@100, or both. A model that only improves top-10 ranking may be attractive for direct search. A model that improves hybrid recall is more useful for reranking pipelines, where the first-stage candidate pool must preserve as many relevant duplicates as possible.

## Example Data

| Query | Positive document |
| --- | --- |
| Dlaczego urządzenie z Androidem ROM jest specyficzne? [53 chars] | Dlaczego nie ma ogólnych instalatorów systemu operacyjnego telefonu? Jestem przyzwyczajony do instalowania i usuwania różnych systemów operacyjnych na moich komputerach, nawet mając kilka naraz. Zazwyczaj instalacja nowego systemu operacyjnego oznacza: 1. Nagranie obrazu ISO na płytę CD/DVD/USB. 2. Włóż go. 3. Uruchom. (Może najpierw musisz trochę poprawić BIOS). Jedyną różnicą między komputerami jest architektura procesora: x86, x86_64, ramię itp. W zależności od tego musisz pobrać jedno lub drugie ISO. Ale nigdy nie muszę się martwić, jaką ma kartę graficzną, mysz, klawiaturę, ekran, kartę sieciową itp. Kreator instalacji automatycznie to wykryje i zainstaluje odpowiednie sterowniki. Czasami, jeśli nie są dołączone, instalator również je pobiera. W każdym razie kluczową kwestią jest to, że **ISO jest zawsze takie samo**. Teraz pojawia się wiele mobilnych systemów operacyjnych: Ubuntu, Tizen, Firefox OS, wszechobecny Android i dlaczego nie ma żadnej dystrybucji Linuksa ARM!. Niestety... [1,000 / 1,811 chars] |
| Jak mogę zapisać plik, zamiast go otwierać? [43 chars] | Jak pobrać plik audio ze strony internetowej? Czy istnieje sposób na pobranie pliku audio, takiego jak plik mp3 z przeglądarki systemu Android na urządzenie, aby móc go później słuchać, gdy będę offline? Czy jest sposób na zaprogramowanie strony internetowej, aby było to możliwe? _Nie_ szukam dodatkowej aplikacji, która pomogłaby mi to osiągnąć. [347 chars] |
| Jak przechwycić strumień wideo z ekranu telefonu z systemem Android i wyświetlić go na laptopie? [96 chars] | Jak wyświetlić ekran mojego telefonu z systemem Android do prezentacji? Jak wyświetlić ekran mojego Droid Incredible, aby móc zademonstrować smartfon w pokoju pełnym ludzi? Czy ktoś wie, jak mogę połączyć telefon z komputerem? Do telewizora? [241 chars] |

### Source Reference Table

| Source | What it contributes |
| --- | --- |
| CQADupStack paper | Original duplicate-question retrieval task design and Stack Exchange construction method. |
| MTEB paper | Benchmark framing for embedding evaluation across retrieval tasks. |
| CLARIN-KNEXT dataset card | Polish translated Android subset used as the source for the task. |
| MTEB task card | Task-level dataset packaging and retrieval interface. |

### Representative Snippets

- A query asks why Android ROM behavior is device-specific; relevant posts discuss installing or adapting phone operating-system images.
- A query asks how to save a file instead of opening it; relevant documents describe Android download behavior for media files.
- A query asks how to capture and display a phone video stream on a laptop; relevant posts frame the same need as screen sharing or presentation display.
- A query about Google Play shared user IDs maps to documents about installation incompatibility and package-signing behavior.
- A query about headset controls maps to posts about changing volume buttons or headphone controls for music navigation.
