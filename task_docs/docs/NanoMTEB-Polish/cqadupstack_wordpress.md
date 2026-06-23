# NanoMTEB-Polish / cqadupstack_wordpress

## Overview

`cqadupstack_wordpress` is the Polish NanoMTEB version of the WordPress subset from CQADupStack. The task evaluates duplicate-question retrieval for WordPress development and site administration. Queries ask about shortcodes, post content, taxonomies, hooks, media libraries, excerpts, categories, comments, templates, and admin notices. Relevant documents are posts that ask the same WordPress behavior or development problem, not merely posts that mention the same function or plugin area.

The Nano split contains 200 queries, 10,000 documents, and 344 positive relevance judgments. Queries average about 56 characters, while documents average about 1,041 characters. The average number of positives per query is 1.72, with 47 multi-positive queries and a largest cluster of 62 positives. This means the task contains many narrow WordPress issues, plus some repeated problems that form larger duplicate clusters.

## Details

### What the Original Data Measures

CQADupStack measures duplicate-question retrieval in community QA forums. In the WordPress subset, relevance depends on the same WordPress behavior: a taxonomy insertion issue, excerpt-length change, media-manager performance problem, category preselection workflow, comment disabling behavior, or hook-based admin notice. A shared function name is not enough if the user is trying to change a different behavior.

This is a technical retrieval task where PHP snippets, WordPress hooks, template concepts, admin workflows, and user-facing symptoms are all relevant. Models must understand both code-like tokens and the broader site behavior being requested.

### Observed Data Profile

The documents are long because WordPress questions often include PHP snippets, theme or plugin context, version details, and attempted fixes. The Polish translation covers explanatory prose, while code identifiers such as `wp_query`, `$post->post_content`, `transition_post_status`, taxonomy names, and shortcode-related terms remain visible.

The task has fewer positives than several other CQADupStack splits, making precise top-rank retrieval important. However, the maximum cluster size of 62 shows that some WordPress problems are repeated frequently. A model must handle both exact development questions and common site-administration issues.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.3139, hit@10 of 0.4250, and recall@100 of 0.4651. Lexical matching is relatively useful because WordPress development has distinctive function names, hooks, variables, and admin terms. When a query contains a specific hook or API name, BM25 can preserve relevant candidates.

The limitation is that the same function or hook can appear in different tasks. A post mentioning `wp_query` may concern ordering, filtering, pagination, or custom post types. A taxonomy post may concern insertion, querying, display, or assignment. BM25 can identify the broad implementation area, but it often needs semantic help to identify the exact behavior.

### Dense Evaluation Profile

The dense `harrier-oss-270m` run reports nDCG@10 of 0.2951, hit@10 of 0.4500, and recall@100 of 0.5349. Dense retrieval improves recall and hit rate, meaning it finds more relevant WordPress posts somewhere in the candidate set. It can connect descriptions of the same user-facing behavior even when exact function names differ.

However, dense nDCG@10 is lower than BM25. This suggests that embeddings may retrieve semantically related WordPress questions but not order true duplicates as precisely at the top. Code identifiers and hook names are important ranking cues, and dense retrieval can underweight them relative to broad behavior similarity.

### Reranking Hybrid Evaluation Profile

`reranking_hybrid` is strongest, with nDCG@10 of 0.3289, hit@10 of 0.4850, and recall@100 of 0.6017. Candidate lists contain 100 to 101 items, and 50 rows use the positive safeguard. The hybrid profile combines BM25's precise WordPress tokens with dense retrieval's semantic recovery of equivalent behaviors.

This is an ideal example of why hybrid search matters for code-adjacent support tasks. BM25 alone ranks exact API matches well but misses paraphrased behavior. Dense retrieval finds more positives but can blur implementation details. Hybrid retrieval recovers the most positives and places more of them in the top 10.

### Metric Interpretation for Model Researchers

This split is strongly hybrid-favorable. BM25 is better than dense on nDCG@10, dense is better than BM25 on recall@100 and hit@10, and `reranking_hybrid` improves over both. That pattern indicates complementary retrieval signals: exact code tokens and semantic behavior descriptions both matter.

Researchers should treat this task as a useful diagnostic for WordPress-style support retrieval. A model that ignores function names will struggle with top-rank precision; a model that ignores semantic behavior will lose recall. The best systems should preserve both.

### Query and Relevance Type Tendencies

Representative queries ask about programmatically inserting hierarchical taxonomy terms, increasing WordPress excerpt length, speeding a slow media-library page that loads full-quality images, predefining categories through GET parameters, and disabling comments on pages. These are concrete development or administration problems.

Relevant documents often include PHP snippets or admin workflows that differ from the query wording. The model must identify whether the same WordPress state and desired behavior are involved. It should also distinguish core WordPress behavior from plugin-specific or theme-specific details.

### Representative Failure Modes

BM25 may over-rank documents that share a function name or hook but ask a different behavior. Dense retrieval may retrieve posts that describe similar user-facing outcomes but require a different WordPress mechanism. Both systems can be confused by long documents that contain multiple snippets or background mentions.

Another failure mode is losing the distinction between theme, plugin, and admin contexts. The same term can appear in a front-end template question, an admin-screen workflow, or a plugin-development hook. True duplicate relevance depends on which context is central.

### Training Data That May Help

Useful training data includes WordPress Stack Exchange duplicate pairs, Polish WordPress support QA, plugin and theme development questions, and hard negatives sharing hooks or function names but differing in behavior. Short-title to long-post pairs are particularly valuable.

Hard negatives should include multiple taxonomy questions with different operations, multiple media-library performance or image-size questions with different causes, and multiple comment-setting questions involving different post types or admin settings.

### Model Improvement Notes

Dense models can improve by jointly representing code identifiers and user-facing site behavior. Sparse systems can improve through tokenization of PHP variables, hooks, and WordPress function names, but lexical retrieval alone misses behavior paraphrases. Hybrid retrieval is the strongest first-stage approach for this split.

For reranking, the task rewards models that can compare a short query with a long PHP-heavy post and determine whether the same WordPress behavior is being requested. Improvements should be checked against both top-10 ranking and recall@100.

## Example Data

| Query | Positive document |
| --- | --- |
| Programowe wstawianie terminów hierarchicznych i ustalanie terminów dla postów powoduje usterkę? [96 chars] | Wstawianie terminów w taksonomii hierarchicznej Naprawdę mam kilka problemów z wstawianiem terminów. Oto mój scenariusz: mam taksonomię o nazwie veda_release_type: //Release Type and Region $labels = array( 'name'=> _x('Release Types/Regions', 'Taxonomy general name' ), 'singular_name' => _x ('Typ/region wydania', 'taksonomia pojedyncza nazwa'), 'search_items' => __('Wyszukaj typy/regiony wydań'), 'popular_items' => __('Popularne typy/regiony wydań'), 'all_items' => __('Wszystkie typy/regiony wydania'), 'edit_item' => __('Edytuj typ/regiony wydania'), 'edit_item' => __('Edytuj typ/region wydania'), 'update_item' => __('Typ/region aktualizacji'), 'add_new_item' => __('Dodaj typ/region nowej wersji'), 'new_item_name' => __('Typ/nazwa nowego wydania'), 'separate_items_with_commas' => __('Oddziel typy wydań/regiony przecinkami'), 'add_or_remove_items' => __('Dodaj lub usuń R zwolnij typy/regiony'), 'choose_from_most_used' => __('Wybierz z najczęściej używanych typów/regionów wydań') ); $ar... [1,000 / 3,822 chars] |
| Jak zwiększyć długość fragmentu w wordpressie? [46 chars] | fragment w postaciach Mam kod w functions.php: function string_limit_words($string, $word_limit) { $words = explode(' ', $string, ($word_limit + 1)); if(count($słowa) > $word_limit) array_pop($słowa); return implode(' ', $słowa); } ale muszę ograniczyć fragment w liczbie znaków, czy możesz mi w tym pomóc? [306 chars] |
| Strona biblioteki multimediów bardzo wolno, ładuje obrazy w pełnej jakości [74 chars] | Wordpress 3.5 Media Manager - Zmień rozmiar załadowanego obrazu Nowy menedżer mediów ładuje obrazy w PEŁNYM rozmiarze, co jest NAPRAWDĘ nieefektywne dla miniatury. Chciałbym go zastąpić miniaturą o innym rozmiarze, która jest również przechowywana dla każdego obrazu źródłowego. Nie mogę też znaleźć na to sposobu. Czy ktoś ma jakieś wskazówki? [344 chars] |

### Source Reference Table

| Source | What it contributes |
| --- | --- |
| CQADupStack paper | Original duplicate-question retrieval construction. |
| MTEB paper | Benchmark framing for retrieval tasks. |
| CLARIN-KNEXT dataset card | Polish translated WordPress subset. |
| MTEB task card | Task packaging and retrieval interface. |

### Representative Snippets

- A query asks about programmatically inserting hierarchical taxonomy terms; relevant posts discuss inserting terms into hierarchical taxonomies.
- A query asks how to increase WordPress excerpt length; relevant documents describe functions that limit excerpt text.
- A query asks why the media library is slow and loads full-quality images; relevant posts discuss changing image size in the WordPress media manager.
- A query asks about predefined categories through GET parameters; relevant documents discuss adding a category to the new-post admin URL.
- A query asks how to disable comments on a page; relevant posts describe removing commenting or posting ability for pages.
