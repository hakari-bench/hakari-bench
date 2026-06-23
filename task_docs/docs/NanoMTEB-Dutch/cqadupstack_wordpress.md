# NanoMTEB-Dutch / cqadupstack_wordpress

## Overview

`cqadupstack_wordpress` is the Dutch-translated WordPress subforum split of
CQADupStack. Queries are WordPress development and administration questions,
and relevant documents are older questions marked as duplicates. The Nano split
contains 200 queries, 10,000 documents, and 200 positive qrel rows, with one
positive duplicate per query. It evaluates retrieval over plugins, themes,
hooks, filters, taxonomies, excerpts, media handling, post metadata, comments,
SEO fields, and template logic.

The task is code-adjacent and platform-specific. BM25 benefits from exact
WordPress API names, plugin names, hook names, and option terms, but it often
retrieves same-API posts that are not duplicates. Dense retrieval improves on
BM25, and `reranking_hybrid` is strongest across nDCG@10, hit@10, and
recall@100. This makes the split a useful example of a domain where sparse
technical identifiers and dense implementation intent are complementary.

## Details

### What the Original Data Measures

[CQADupStack](https://doi.org/10.1145/2838931.2838934) provides duplicate-
question retrieval tasks from Stack Exchange duplicate links. In each task, a
newer query question must retrieve an older question that was flagged as a
duplicate. The WordPress subforum focuses on platform implementation and site
administration, with many questions involving function calls, hooks, themes,
plugins, and CMS configuration.

BEIR includes CQADupStack in a standardized zero-shot retrieval benchmark, and
BEIR-NL translates the public BEIR data into Dutch. In this split, surrounding
prose is Dutch-translated, while WordPress identifiers such as `add_action()`,
taxonomy names, plugin names, hooks, and PHP snippets often remain unchanged.
The retrieval task therefore combines Dutch semantic matching with exact API
and code-token evidence.

### Observed Data Profile

The split has 200 queries over 10,000 documents. Queries average 56.55
characters, and documents average 1,183.40 characters. Documents are often long
because they include code snippets, plugin context, administrative settings,
and descriptions of attempted implementations.

Representative questions ask how to insert hierarchical terms and assign them
to posts, how to increase excerpt length, how to load smaller images in the
WordPress media library, how to create a new post link with predefined
categories, and how to disable comments on a page. These examples show that a
true duplicate is usually tied to the same WordPress implementation problem,
not merely the same plugin or feature area.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 = 0.2608, hit@10 = 0.3700, and recall@100 = 0.5950 over
top-500 candidate lists. Sparse retrieval has real value because exact
WordPress terms are highly informative. Function names, hook names, taxonomies,
plugin names, and configuration terms can identify the right API surface.

The weakness is same-API ambiguity. Many WordPress questions mention comments,
excerpts, taxonomies, media, or `add_action()` while asking different
implementation questions. Short translated queries also provide limited
context, and long documents can contain many incidental API names. BM25
therefore recovers useful candidates but does not reliably rank the duplicate
first.

### Dense Evaluation Profile

Dense retrieval with `harrier_oss_v1_270m` reaches nDCG@10 = 0.3057, hit@10 =
0.4250, and recall@100 = 0.6850. Dense retrieval improves over BM25 because it
captures implementation intent and paraphrased troubleshooting descriptions.
It can connect questions that describe the same desired WordPress behavior with
different wording or different amounts of code detail.

Dense retrieval still has difficulty with platform-specific distinctions. Two
posts may both discuss taxonomies, media, excerpts, or comments but require
different hooks or settings. A model that captures only broad WordPress topic
similarity may retrieve plausible non-duplicates.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate column reaches nDCG@10 = 0.3371, hit@10 =
0.4600, and recall@100 = 0.7250, with 100 to 101 candidates per query and 55
rank-101 safeguard rows. This is the strongest profile for the task. Unlike
some other CQADupStack splits where dense has the better initial top order, the
WordPress split benefits from hybrid search at both top-10 and top-100.

The likely reason is that exact API evidence and semantic implementation
evidence are both important. BM25 contributes rare identifiers, while dense
retrieval contributes paraphrase and intent matching. The hybrid pool gives a
reranker a strong starting point, but same-API hard negatives remain common.

### Metric Interpretation for Model Researchers

With one positive duplicate per query, nDCG@10 measures the rank of that
duplicate, hit@10 measures short-list availability, and recall@100 measures
candidate-pool coverage. The metric progression from BM25 to dense to hybrid is
clear: hybrid search is the best first-stage strategy for this split.

This makes the task useful for evaluating code-aware hybrid search. A model
must preserve exact WordPress identifiers while still understanding the user's
implementation goal. Reranking should decide whether the candidate question
asks the same WordPress problem, not simply whether it mentions the same
function or plugin.

### Query and Relevance Type Tendencies

Queries are short Dutch-translated WordPress questions. They often name a
feature area, plugin, hook, function, taxonomy, or desired site behavior.
Relevant documents are longer prior questions that duplicate the implementation
problem, sometimes with code samples or administrative context.

The relevance type is duplicate implementation intent. Two posts about excerpts
or media handling may not be duplicates unless they require the same fix. A
shared API token is important but not sufficient.

### Representative Failure Modes

BM25 can fail by retrieving same-plugin or same-hook documents that address a
different problem. Dense retrieval can fail by grouping semantically related
WordPress features without preserving the exact implementation constraint.
Hybrid retrieval can still rank same-API hard negatives above the positive.

Common errors involve taxonomies, hooks, media handling, comments, and excerpt
logic, where many candidate posts share terminology. Rerankers should compare
the requested behavior and the role of the API call in the candidate.

### Training Data That May Help

Useful training data includes non-overlapping WordPress Stack Exchange
duplicate-question pairs, WordPress support forum QA pairs, and code-aware CMS
duplicate retrieval data. Training should exclude the translated WordPress
test queries and duplicate positives used by this Nano split.

Synthetic data can be generated from WordPress support posts outside the
evaluation set. Preserve function names, hooks, filters, plugin names, and
template terms, then create Dutch paraphrases of the same implementation
problem. Hard negatives should share the same API surface while asking for a
different behavior.

### Model Improvement Notes

Improving this task requires platform-aware semantic retrieval. Dense encoders
should learn from WordPress duplicate pairs and same-API hard negatives. Sparse
features should remain available because exact identifiers often carry the
critical clue.

For rerankers, the central behavior is implementation-equivalence checking:
would the candidate thread solve the same WordPress problem as the query? A
strong model should use code tokens and Dutch prose together rather than
depending on either alone.

## Example Data

| Query | Positive document |
| --- | --- |
| Programmatisch hiërarchische termen invoegen & termen instellen voor berichten veroorzaakt een storing? [103 chars] | Het invoegen van termen in een hiërarchische taxonomie Ik ondervind een paar problemen met het invoegen van termen. Dit is mijn scenario: Ik heb een taxonomie genaamd veda_release_type: //Release Type en Regio $labels = array( 'name'=> _x('Release Types/Regio\'s', 'taxonomy general name' ), 'singular_name' => _x('Release Type/Regio', 'taxonomy singular name'), 'search_items' => __('Zoek Release Types/Regio\'s'), 'popular_items' => __('Populaire Release Types/Regio\'s'), 'all_items' => __('Alle Release Types/Regio\'s'), 'edit_item' => __('Release Type/Regio bewerken'), 'edit_item' => __('Release Type/Regio bewerken'), 'update_item' => __('Release Type/Regio bijwerken'), 'add_new_item' => __('Nieuwe Release Type/Regio toevoegen'), 'new_item_name' => __('Nieuwe Release Type/Regio naam'), 'separate_items_with_commas' => __('Scheid Release Types/Regio\'s met komma\'s'), 'add_or_remove_items' => __('Release Types/Regio\'s toevoegen of verwijderen'), 'choose_from_most_used' => __('Kies uit de... [1,000 / 4,702 chars] |
| Hoe de lengte van een excerpt in WordPress te vergroten? [56 chars] | De korte inhoud per karakter **Mogelijk duplicaat:** > fragment in karakters Op sommige van onze sites tonen we fragmenten van berichten (de beheerders voeren geen fragmenten in). We _kunnen_ de functie `the_excerpt` gebruiken, maar voor zover ik kon zien, kan ik alleen het aantal woorden bepalen dat het extraheert, en dat is iets te algemeen voor ons (een woord kan 2 letters of 10 letters hebben...). Dus we hebben een functie nodig die het aantal karakters neemt en die hoeveelheid uit de inhoud extraheert. Maar we willen ook niet dat de woorden in het midden worden afgebroken. Een laatste vereiste is dat de functie werkt met de multi-byte versie van de stringfuncties van php (bijvoorbeeld: gebruik `mb_substr` in plaats van `substr`). Zijn er ingebouwde WP-functies die dit zouden doen? [800 chars] |
| Media bibliotheek pagina supersnel, laad volle kwaliteit afbeeldingen [69 chars] | Wordpress 3.5 Media Manager - Afbeelding Formaat bij Laden Wijzigen De nieuwe media manager laadt afbeeldingen in VOLLE grootte, wat ECHT inefficiënt is voor een thumbnail. Ik wil dit graag vervangen door een ander formaat thumbnail dat ook voor elke bronafbeelding wordt opgeslagen. Ik kan echter geen manier vinden om dat te doen. Heeft iemand tips? [352 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| CQADupStack: A Benchmark Data Set for Community Question-Answering Research | 2015 | proceedings paper | [https://doi.org/10.1145/2838931.2838934](https://doi.org/10.1145/2838931.2838934) |
| BEIR-NL: Zero-shot Information Retrieval Benchmark for the Dutch Language | 2025 | proceedings paper | [https://aclanthology.org/2025.bucc-1.5/](https://aclanthology.org/2025.bucc-1.5/) |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | arXiv paper | [https://arxiv.org/abs/2104.08663](https://arxiv.org/abs/2104.08663) |
| clips/beir-nl-cqadupstack |  | dataset card | [https://huggingface.co/datasets/clips/beir-nl-cqadupstack](https://huggingface.co/datasets/clips/beir-nl-cqadupstack) |

### Representative Snippets

| Query | Positive passage |
| --- | --- |
| Programmatisch hierarchische termen invoegen en termen instellen voor berichten veroorzaakt een storing? | A translated WordPress question describes inserting terms into a hierarchical taxonomy and assigning them to posts. |
| Hoe de lengte van een excerpt in WordPress te vergroten? | A translated duplicate asks about controlling excerpt length by character count rather than default behavior. |
| Media bibliotheek pagina supersnel, laad volle kwaliteit afbeeldingen | A translated post discusses changing the image size loaded by the WordPress 3.5 media manager. |
| Voorgedefinieerde categorieen in WordPress via GET-parameters | A translated question asks how to create a link for a new post with predefined categories. |
| Hoe schakel ik reacties uit op een pagina? | A translated question asks how to remove the ability for users to post comments on a WordPress page. |
