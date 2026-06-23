# NanoCoIR / NanoCodeFeedbackST

## Overview

NanoCodeFeedbackST is an English single-turn code-assistant retrieval task in NanoCoIR. It is based on CoIR's CodeFeedback-ST setting, where a user programming instruction is the query and the intended assistant response is the document to retrieve. The response may contain code, explanatory prose, formatting guidance, or a combination of all three.

Compared with the multi-turn feedback task, the difficulty is concentrated in one dense user request. The model must identify the answer that directly satisfies the requested operation, language, library, or implementation constraint. This makes the task useful for evaluating instruction-to-answer retrieval in code assistants, especially when many candidate answers share programming vocabulary.

## Details

### What the Original Data Measures

CoIR describes CodeFeedback-ST as a hybrid code QA retrieval task built from CodeFeedback-Filtered-Instruction. The user instruction becomes the query, and assistant answers become retrieval documents. The original data therefore measures whether a model can match a specific programming request to the response that implements or explains it.

Unlike dialogue retrieval, there is no need to track turn order. The challenge is to understand the full instruction and distinguish answers that are topically similar but operationally different. A relevant answer must satisfy the requested language, task, data structure, framework, or algorithm.

### Observed Data Profile

This Nano split contains 200 queries, 10,000 documents, and 200 positive qrels. Each query has exactly one positive response. Queries average 730.52 characters, while documents average 1,538.73 characters. The documents are often longer than the queries because they include implementation details, explanation, and formatted code blocks.

Observed queries include factorial functions, PHP conversion of Python Unicode-processing code, TensorFlow Iris classification, connected-component detection in NumPy arrays, and class-design modifications. These examples span SQL, Python, PHP, Linux-style tasks, data processing, and general programming explanation.

### BM25 Evaluation Profile

BM25 is very strong on NanoCodeFeedbackST. It reaches nDCG@10 of 0.8722, hit@10 of 0.9250, and recall@100 of 0.9650 with a top-500 candidate pool. The high lexical score reflects substantial overlap between instructions and answers: programming-language names, APIs, libraries, class names, table names, function names, and task-specific terms often reappear in the response.

The BM25 result shows that term frequency is genuinely useful here. A request for TensorFlow, PHP, Django, SQL, NumPy, or a named function often gives lexical retrieval clear anchors. However, lexical matching alone is not perfect. Candidate answers can share the same language or API but solve a different operation, and some relevant answers paraphrase the instruction rather than repeating it exactly.

### Dense Evaluation Profile

The dense harrier-oss-270m profile is the strongest top-rank result, with nDCG@10 of 0.9532, hit@10 of 0.9800, and recall@100 of 0.9800. Dense retrieval improves over already-strong BM25, suggesting that semantic matching helps distinguish the exact requested operation among answers with similar vocabulary.

Dense similarity is especially useful when the instruction describes behavior and the answer expresses the solution through code. A model can connect "replace spaces after punctuation-ending words" to the implementation structure even when the response uses different wording. Remaining dense errors are likely near-miss answers in the same programming language or library family.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate subset reaches nDCG@10 of 0.9115, hit@10 of 0.9650, and recall@100 of 1.0000. It uses exactly 100 candidates per query, with no safeguard-positive rows and no 101-candidate cases. This is the strongest coverage result, although its top-rank ordering is below dense retrieval.

The hybrid pattern is useful for downstream reranking. BM25 contributes exact API and identifier matches, while dense retrieval contributes semantic instruction matching. Together they recover every positive by rank 100. The lower nDCG@10 compared with dense means that the candidate mixture still needs a strong final ranker to choose the answer that directly satisfies the instruction.

### Metric Interpretation for Model Researchers

NanoCodeFeedbackST is a high-performing code instruction retrieval task where all three retrieval modes are informative. BM25 shows that exact programming terms are strong signals. Dense retrieval shows that semantic understanding of the requested operation improves top placement. Reranking_hybrid shows that combined candidates can provide complete top-100 positive coverage.

For researchers, the main question is no longer whether the retriever can find broadly relevant programming answers; it often can. The harder question is whether it can rank the one correct answer above near-miss responses that use the same library, language, or concept. nDCG@10 is therefore a better diagnostic than hit@10 alone.

### Query and Relevance Type Tendencies

Queries are single-turn programming instructions. They may request code generation, code conversion, SQL writing, data processing, framework explanation, class modification, or algorithm implementation. Documents are assistant replies, often with both explanation and code.

Relevance is direct instruction satisfaction. The positive document should perform the requested task in the requested language or framework. Similar answers that solve the same broad topic but miss a condition, use a different language, or omit a required modification are non-relevant.

### Representative Failure Modes

BM25 may retrieve an answer that repeats the same language or API terms but addresses a different task. For example, a NumPy answer about array processing may not implement the requested connected-component logic, or a PHP response may not preserve the behavior of the original Python code.

Dense retrieval may over-generalize when several answers share a programming concept. It may retrieve a plausible classifier example that does not match the requested dataset setup, or a class-design answer that modifies the wrong responsibility. Hybrid retrieval usually recovers the positive but may still need reranking to suppress these near misses.

### Training Data That May Help

Useful training data includes single-turn code instruction answering data, SQL and Python assistant-response pairs, and hard negatives that share language and API terms while solving a different operation. Training examples should preserve the full instruction and complete assistant response, including code blocks and explanations.

Leakage control is essential. The metadata records an audit of `m-a-p/CodeFeedback-Filtered-Instruction` in which 156,526 source train rows were scanned. All 200 Nano queries matched normalized source queries, 199 positives matched normalized source answers, all 200 query-positive concatenations matched, 193 high-shingle query matches were found, and 199 high-shingle positive matches were found. Raw public training rows therefore contain direct benchmark leakage and must be filtered before use.

### Model Improvement Notes

The best improvements should target exact instruction satisfaction under near-duplicate programming vocabulary. Models should represent both lexical identifiers and semantic operations. They should know that "use TensorFlow 2 for Iris classification" and "convert this Python Unicode function to PHP" impose concrete implementation constraints.

For reranking research, this split is useful because candidate recall can reach 100% with hybrid retrieval. That makes it possible to study ranking quality without many missing-positive failures. A strong reranker should use code semantics, language constraints, and task requirements to place the single correct assistant response first.

## Example Data

| Query | Positive document |
| --- | --- |
| Generate the resulting value of the mathematical operation, factorial, when applied to an integer number n. Also, write a function that could compute the factorial of any other integer number m, such that 1<=m<=n. Your function should consider large integers, so avoiding overflow errors is a critical aspect to consider. [321 chars] | Sure, in Python one can use the built-in library `math` for computing the factorial of any integer. However, to understand the concept behind it, you can create your own implementation for factorial calculation. It's also vital to consider that the maximum possible integer depends on Python's environment (for example, Python 2 or Python 3 and is limited to the memory limit). Here is the Python program for this problem: ```python def factorial(n): if not 1 <= n: raise ValueError("Number must be an integer and greater than equal to 1") result = 1 for i in range(2, n+1): result *= i return result print(factorial(5)) # 120 print(factorial(10)) # 3628800 ``` This function accepts an integer number as a parameter and then computes the factorial through a loop, multiplying the `result` value each time. The implementation uses a `for` loop which helps in avoiding stack overflow errors that can occur with recursion when calculating the factorial of large numbers. It has time complexity O(n) as... [1,000 / 1,576 chars] |
| i'd like a php-specific version of this code: import unicodedata def unicode_word_segments(s, n): vowels = ['A', 'E', 'I', 'O', 'U', 'a', 'e', 'i', 'o', 'u'] # unicode vowels s = ''.join(char for char in s if char.isalpha() or char.isspace()) # remove non-alphabetic characters chunks = [] chunk = '' count = 0 for char in s: if unicodedata.normalize("NFKD", char).encode('ASCII', 'ignore').decode() in vowels: # if unicode vowel count += 1 if count == n: # if count reached n chunk += char chunks.ap... [500 / 774 chars] | Sure, here is a PHP-specific version of your code: ```php <?php function unicode_word_segments($s, $n) { $vowels = ['A', 'E', 'I', 'O', 'U', 'a', 'e', 'i', 'o', 'u']; // unicode vowels $s = preg_replace('/[^a-zA-Z\s]/', '',$s); // remove non-alphabetic characters $chunks = []; $chunk = ''; $count = 0; $length = mb_strlen($s, 'UTF-8'); for ($i = 0; $i < $length; $i ++) { $char = mb_substr($s, $i, 1, 'UTF-8'); if (in_array($char, $vowels)) { // if unicode vowel $count += 1; } if ($count == $n) { // if count reached n $chunk .= $char; $chunks[] = $chunk; // add chunk to chunks $chunk = ''; // reset chunk $count = 0; // reset count } else { // if count did not reach n $chunk .= $char; } } return $chunks; } ``` In this PHP version of your code, we're using a regular expression to remove non-alphabetic characters and mb_substr function to properly handle multi-byte unicode characters. Please note that PHP does not provide built-in support for Unicode normalization like Python, so the code ab... [1,000 / 1,476 chars] |
| Implement a neural network classifier in TensorFlow 2 that takes in the Iris dataset and predicts the species of flower. [120 chars] | Here's an example of a simple neural network created in TensorFlow two for the Iris dataset classification problem. Note that this is an example and might not get the highest accuracy possible for the task. ```python import tensorflow as tf from sklearn.datasets import load_iris from sklearn.model_selection import train_test_split from sklearn.preprocessing import OneHotEncoder, StandardScaler iris_data = load_iris() # Preprocess x = iris_data.data y_ = iris_data.target.reshape(-1, 1) # Convert data to a single column # One Hot encode the class labels encoder = OneHotEncoder(sparse=False) y = encoder.fit_transform(y_) # Split the data for training and testing train_x, test_x, train_y, test_y = train_test_split(x, y, test_size=0.20) # Feature Scaling scaler = StandardScaler() scaler.fit(train_x) train_x = scaler.transform(train_x) test_x = scaler.transform(test_x) # Build the model model = tf.keras.models.Sequential([ tf.keras.layers.Dense(10, activation='relu'), tf.keras.layers.Dense(1... [1,000 / 1,790 chars] |

### Source Reference Table

| Source | Role |
| --- | --- |
| [CoIR: A Comprehensive Benchmark for Code Information Retrieval Models](https://arxiv.org/abs/2407.02883) | Benchmark paper defining the retrieval adaptation. |
| [OpenCodeInterpreter: Integrating Code Generation with Execution and Refinement](https://arxiv.org/abs/2402.14658) | Related source paper for code feedback and refinement data. |
| [m-a-p/CodeFeedback-Filtered-Instruction](https://huggingface.co/datasets/m-a-p/CodeFeedback-Filtered-Instruction) | Public source dataset card for single-turn instruction-answer data. |
| [hakari-bench/NanoCoIR](https://huggingface.co/datasets/hakari-bench/NanoCoIR) | Nano benchmark dataset containing this split. |

### Representative Snippets

| Query Pattern | Positive Document Pattern |
| --- | --- |
| Requests factorial computation and a reusable function for bounded integer inputs. | The response explains factorials and provides a Python implementation with appropriate input handling. |
| Requests a PHP-specific version of a Python Unicode word-segmentation function. | The answer rewrites the behavior in PHP and preserves the original vowel and filtering logic. |
| Requests a TensorFlow 2 classifier for the Iris dataset. | The response provides a TensorFlow/Keras example that loads data, defines a model, trains, and predicts classes. |
| Requests connected-cluster handling for a 512-by-512 NumPy array. | The positive answer uses image or array labeling logic to identify connected regions under the requested condition. |
| Requests modifications to ticket and show classes for timing categories. | The response describes class changes and integration steps for adding timing-category arrays. |
