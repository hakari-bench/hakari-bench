# NanoRTEB / NanoFreshStack

## Overview

`NanoFreshStack` is an English technical-document retrieval task from NanoRTEB. The query is a realistic developer question, often from recent or niche software contexts, and relevant documents are technical documentation, release notes, tests, or code-adjacent text that support the answer. Most queries have multiple positives. BM25 is useful for exact API names and error messages, dense retrieval improves semantic matching, and `reranking_hybrid` is the strongest overall profile by combining exact technical anchors with broader documentation relevance.

## Details

### What the Original Data Measures

FreshStack was introduced to build realistic retrieval benchmarks for technical documents. It focuses on practical developer information needs, recent domains, documentation corpora, community questions, and nugget-level support labels.

RTEB includes FreshStack as an English technical retrieval task. The Nano split asks whether a retriever can connect long developer questions to the documentation or code-adjacent files that support an answer.

### Observed Data Profile

The Nano split contains 200 queries, 3,770 documents, and 1,522 positive qrel rows. Queries average 1,660.21 characters, while documents average 4,983.03 characters. Positives per query average 7.61, with a minimum of 1, a median of 7, and a maximum of 21. There are 189 multi-positive queries, 94.5% of the split.

Example queries involve Godot input behavior, Angular template binding errors, Angular signals without zone.js, Godot Android export cache directories, and Angular server-side rendering with ngrx state.

### BM25 Evaluation Profile

The BM25 candidate subset uses top-500 candidates and reaches nDCG@10 of 0.2768, hit@10 of 0.6850, and recall@100 of 0.6196. BM25 can match exact framework names, API symbols, error strings, class names, and version-specific terminology.

Its limitation is that technical questions are long and often include code blocks, logs, and narrative debugging context. The relevant document may describe the underlying behavior without repeating the exact phrasing from the question.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses top-500 candidates and reaches nDCG@10 of 0.3396, hit@10 of 0.7750, and recall@100 of 0.7523. Dense retrieval improves both top-rank quality and broad coverage over BM25.

This indicates that semantic matching helps map developer problems to relevant documentation sections, especially when the question describes symptoms rather than naming the exact concept.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates, with 4 rows receiving the optional rank-101 safeguard. It reaches nDCG@10 of 0.3482, hit@10 of 0.7600, and recall@100 of 0.7674. Hybrid retrieval is the strongest profile for nDCG@10 and recall@100, while dense retrieval has slightly higher hit@10.

This tradeoff is typical for technical documentation search. Sparse retrieval protects exact API and error-token matches, while dense retrieval recovers conceptually relevant docs. The combined pool is especially useful when a query has several supporting documents.

### Metric Interpretation for Model Researchers

Because most queries have multiple positives, nDCG@10 measures whether several supporting documents are ranked early, hit@10 measures whether at least one support appears in the first ten, and recall@100 measures how much support is available for reranking.

For `NanoFreshStack`, hit@10 alone can hide weak coverage. A good retriever should find multiple supporting documents across docs, release notes, and related source text.

### Query and Relevance Type Tendencies

Queries are long developer questions with error messages, code snippets, framework versions, and expected-versus-observed behavior. Relevant documents are technical pages or code-adjacent files that explain the behavior or support an answer.

Relevance is support for the information need. A document can mention the same framework or API and still be wrong if it addresses a different lifecycle hook, version, component, or runtime behavior.

### Representative Failure Modes

Common failures include overmatching API names while missing the relevant behavior, retrieving documentation for the wrong framework version, ranking generic guides above specific troubleshooting sections, and missing support documents when the query uses symptom descriptions. BM25 overweights exact tokens; dense retrieval can blur nearby technical concepts.

### Training Data That May Help

Useful training data includes technical-document retrieval, StackOverflow-to-doc linking, issue-to-doc search, API documentation examples, and hard negatives from the same framework version or symbol family. Evaluation queries, documents, and qrels should be excluded.

### Model Improvement Notes

Models should preserve exact API names, error strings, and versions while learning symptom-to-document semantic matching. Hard negatives should share the same framework, API, or error family but differ in lifecycle, version, or behavior. Hybrid retrieval is the best first-stage profile for broad candidate generation.

## Example Data

| Query | Positive document |
| --- | --- |
| My buttons are displayed (show method) after a short pause, and if I hover the mouse cursor over the position where the button will be and leave it, the button will not realize that it is hovered. This is fixed when moving the mouse, but I really want to fix this little problem. I used base signals mouse_entered() and mouse_exited() After show() buttons must understand is mouse in or not. That's all( [403 chars] | <?xml version="1.0" encoding="UTF-8" ?> <class name="InputEventMouse" inherits="InputEventWithModifiers" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="../class.xsd"> <brief_description> Base input event type for mouse events. </brief_description> <description> Stores general information about mouse events. </description> <tutorials> <link title="Using InputEvent">$DOCS_URL/tutorials/inputs/inputevent.html</link> </tutorials> <members> <member name="button_mask" type="int" setter="set_button_mask" getter="get_button_mask" enum="MouseButtonMask" is_bitfield="true" default="0"> The mouse button mask identifier, one of or a bitwise combination of the [enum MouseButton] button masks. </member> <member name="global_position" type="Vector2" setter="set_global_position" getter="get_global_position" default="Vector2(0, 0)"> When received in [method Node._input] or [method Node._unhandled_input], returns the mouse's position in the root [Viewport] using the... [1,000 / 1,732 chars] |
| Angular is failing to compile because of the following error and I'm really confused as to why. error TS2322: Type 'string' is not assignable to type 'MenuItem'. 4 <menu-item item={{item}}></menu-item> ~~~~ apps/angular-monorepo/src/app/app.component.ts:10:16 10 templateUrl: './app.component.html', ~~~~~~~~~~~~~~~~~~~~~~ Error occurs in the template of component AppComponent. Why is it complaining that item is of type 'string' when I specified that item is of type MenuItem or undefined @Componen... [500 / 1,922 chars] | # Binding dynamic text, properties and attributes In Angular, a **binding** creates a dynamic connection between a component's template and its data. This connection ensures that changes to the component's data automatically update the rendered template. ## Render dynamic text with text interpolation You can bind dynamic text in templates with double curly braces, which tells Angular that it is responsible for the expression inside and ensuring it is updated correctly. This is called **text interpolation**. ```angular-ts @Component({ template: ` <p>Your color preference is {{ theme }}.</p> `, ... }) export class AppComponent { theme = 'dark'; } ``` In this example, when the snippet is rendered to the page, Angular will replace `{{ theme }}` with `dark`. ```angular-html <!-- Rendered Output --> <p>Your color preference is dark.</p> ``` In addition to evaluating the expression at first render, Angular also updates the rendered content when the expression's value changes. Continuing the t... [1,000 / 9,518 chars] |
| I am testing angular 16 signals and per my understanding, when I disable zone.js and call signal.update() the view should be updated with new value. It is not. Please help me to understand why. main.ts platformBrowserDynamic().bootstrapModule(AppModule, { ngZone: 'noop' }) .catch(err => console.error(err)); app.component.ts @Component({ selector: 'app-root', template: ' <h1>{{ title() }}</h1> <button (click)="click()">Change</button> ', }) export class AppComponent { title = signal('Hello'); cli... [500 / 734 chars] | # Resolving zone pollution **Zone.js** is a signaling mechanism that Angular uses to detect when an application state might have changed. It captures asynchronous operations like `setTimeout`, network requests, and event listeners. Angular schedules change detection based on signals from Zone.js. In some cases scheduled [tasks](https://developer.mozilla.org/docs/Web/API/HTML_DOM_API/Microtask_guide#tasks) or [microtasks](https://developer.mozilla.org/docs/Web/API/HTML_DOM_API/Microtask_guide#microtasks) don’t make any changes in the data model, which makes running change detection unnecessary. Common examples are: * `requestAnimationFrame`, `setTimeout` or `setInterval` * Task or microtask scheduling by third-party libraries This section covers how to identify such conditions, and how to run code outside the Angular zone to avoid unnecessary change detection calls. ## Identifying unnecessary change detection calls You can detect unnecessary change detection calls using Angular DevTools... [1,000 / 5,856 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| FreshStack: Building Realistic Benchmarks for Evaluating Retrieval on Technical Documents | 2025 | task paper | [https://arxiv.org/abs/2504.13128](https://arxiv.org/abs/2504.13128) |
| FreshStack project site | 2025 | project page | [https://fresh-stack.github.io/](https://fresh-stack.github.io/) |
| mteb/FreshStackRetrieval |  | dataset card | [https://huggingface.co/datasets/mteb/FreshStackRetrieval](https://huggingface.co/datasets/mteb/FreshStackRetrieval) |
| Introducing RTEB: A New Standard for Retrieval Evaluation | 2025 | benchmark article | [https://huggingface.co/blog/rteb](https://huggingface.co/blog/rteb) |

### Representative Snippets

| Query | Relevant document excerpt |
| --- | --- |
| A Godot user reports delayed button display causing hover state not to update until the mouse moves. | A Godot InputEventMouse class document describes mouse input events. |
| An Angular template fails with a type error involving a `menu-item` binding. | An Angular binding guide explains dynamic text, property, and attribute binding. |
| An Angular 16 signals example does not update after disabling zone.js. | Angular documentation discusses zone pollution and change detection behavior. |
| A Godot Android export creates a `.godot/exported` directory that affects editor behavior. | Godot release-note text discusses export and editor behavior fixes. |
| An Angular SSR application with ngrx has questions about pre-rendered state. | An Angular SSR guide points to the server-side rendering documentation. |
