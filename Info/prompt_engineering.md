# Key takeaways

- Research question: Wie beeinflussen verschiedene Prompt-Arten die Qualität unseres LLM-Agenten?
- Metriken dazu:
    - **API vollständigkeit**:
    - % an korrekt erstellten API-calls durch den Agenten (% valid API-calls)
    - vollständige API-calls durch den Agenten (Anzahl der aus dem Text entnommenem Parameter)
    - Klassifizierung der Fehler (syntaktische vs. semantische)
    - **Relevanz Score**:
    - Befragung von Personen, die die relevanz der Ergebnisse von prompts auf einer Skala von 1-5 bewerten
    - **Parameter coverage**:
    - ähnlich zu vollständigem API-call
    - **relative Improvement score**:
    - erstelle Baseline-prompt und bewerte verbesserung dazu
    - **Hit@k** : https://en.wikipedia.org/wiki/Knowledge_graph_embedding
- Methoden: (https://www.promptingguide.ai/papers, https://arxiv.org/pdf/2507.13525)
- verschiedene Prompt-klassen: standardisierte Sätze, non-conversational, conversational, structured, re-reading, role-play, echo
- https://arxiv.org/pdf/2401.14423


---


# I want to go into how prompt engineering does effect the LLMs performance. How can I measure the performance against various prompts?
## 📏 Key Dimensions of Performance

You can measure LLM performance across several dimensions depending on your use case:

| Dimension              | Description                                                                 |
|------------------------|-----------------------------------------------------------------------------|
| **Accuracy**           | Does the output match the expected result or ground truth?                  |
| **Completeness**       | Does the response fully address the prompt's intent?                        |
| **Relevance**          | Are the outputs contextually appropriate and useful?                        |
| **Robustness**         | Does the model perform consistently across prompt variations?               |
| **Efficiency**         | How fast or resource-intensive is the response generation?                  |
| **User Satisfaction**  | How do users rate the helpfulness or clarity of the output?                 |

---

## 🧪 Experimental Setup

Here’s a step-by-step framework to test prompt variations:

### 1. **Define a Task**
Choose a specific task the LLM will perform via the API (e.g., retrieving weather data, summarizing articles, generating code).

### 2. **Create Prompt Variants**
Design multiple prompts that vary in:
- **Length** (short vs detailed)
- **Structure** (question vs command vs context-rich)
- **Clarity** (ambiguous vs precise)
- **Tone** (formal vs casual)

### 3. **Run Controlled Tests**
Use each prompt to query the LLM multiple times. Keep the API and task constant.

### 4. **Collect Outputs**
Store the LLM responses and API interactions for each prompt.

### 5. **Evaluate Outputs**
Use a mix of:
- **Automated metrics** (e.g., BLEU, ROUGE, exact match)
- **Human evaluation** (rating relevance, clarity, usefulness)
- **Task-specific metrics** (e.g., correct API call structure, valid JSON)

---

## 📊 Analysis Techniques

- **Statistical comparison**: Use ANOVA or t-tests to compare performance across prompt types.
- **Error analysis**: Categorize common failure modes (e.g., hallucinations, syntax errors).
- **Prompt sensitivity**: Measure how small changes in wording affect output quality.

---

## 🧠 Bonus Ideas

- Try **few-shot vs zero-shot** prompts to see how examples influence performance.
- Use **chain-of-thought prompting** to test reasoning depth.
- Explore **prompt templates** for consistency across tasks.


# Suppose the LLM has a task of retrieving short form blog posts. Can you give me examples of prompts and how they would be used in tests and analyses?
## 🎯 Task Definition
**Goal:** Evaluate how different prompt styles affect the LLM’s ability to retrieve relevant short-form blog posts from a web API.

**Assumption:** The API accepts parameters like topic, length, date, author, or tags.

---

## 🧪 Prompt Variations

Here are several types of prompts you can test, each designed to probe a different aspect of LLM behavior:

### 1. **Basic Prompt**
```text
Get me blog posts about climate change.
```
- **Purpose:** Baseline for comparison.
- **Test:** Does the LLM generate a valid API call with just the topic?

---

### 2. **Structured Prompt**
```text
Retrieve short-form blog posts tagged with "climate change" published in the last 30 days.
```
- **Purpose:** Tests ability to parse constraints.
- **Test:** Does the LLM include date filtering and tag parameters?

---

### 3. **Conversational Prompt**
```text
Hey, I’m looking for some quick reads on climate change—anything recent and under 500 words?
```
- **Purpose:** Tests natural language understanding.
- **Test:** Does the LLM infer length and recency correctly?

---

### 4. **Ambiguous Prompt**
```text
Find something interesting about climate change.
```
- **Purpose:** Tests handling of vague intent.
- **Test:** Does the LLM default to relevant tags or use fallback logic?

---

### 5. **Overloaded Prompt**
```text
Can you get me short blog posts on climate change, preferably written by scientists, published this year, and with high engagement?
```
- **Purpose:** Tests multi-constraint parsing.
- **Test:** Does the LLM prioritize or correctly balance all constraints?

---

## 📊 Evaluation Metrics

You can evaluate each prompt using:

| Metric              | Description                                                                 |
|---------------------|-----------------------------------------------------------------------------|
| **API Validity**     | Does the LLM generate a syntactically correct API call?                     |
| **Parameter Coverage** | Are all relevant parameters from the prompt included?                      |
| **Relevance**        | Are the retrieved blog posts topically aligned with the prompt?             |
| **Conciseness**      | Are the blog posts short-form as requested?                                 |
| **Consistency**      | Does the LLM behave predictably across similar prompts?                     |

---

## 🔍 Analysis Techniques

- **Prompt Sensitivity Matrix**: Compare how small changes in prompt wording affect output.
- **Error Categorization**: Track common failure modes (e.g., missing filters, wrong topic).
- **User Simulation**: Have testers rate the usefulness of results from each prompt type.
- **Statistical Testing**: Use precision/recall or F1 scores if you have ground truth data.

---



**Here are three example bar charts that visualize how different prompt types affect LLM performance when retrieving short-form blog posts via an API.** Each chart highlights a key metric: API Validity, Parameter Coverage, and Relevance Score.

---

### 📊 Chart Summaries

#### 1. **API Validity by Prompt Type**
This chart shows the percentage of prompts that resulted in syntactically correct API calls:
- *Structured* prompts performed best (95%)
- *Ambiguous* prompts had the lowest success rate (60%)
- *Overloaded* prompts still maintained high validity (90%)

#### 2. **Parameter Coverage by Prompt Type**
This chart measures how well each prompt type included all relevant API parameters:
- *Structured* prompts again led (90%)
- *Conversational* prompts did well (75%)
- *Ambiguous* prompts struggled (40%)

#### 3. **Relevance Score by Prompt Type**
This chart reflects the average human rating (1–5) of how topically aligned the retrieved blog posts were:
- *Structured* prompts scored highest (4.7)
- *Ambiguous* prompts were least relevant (2.8)
- *Conversational* and *Overloaded* prompts were strong contenders (4.2 and 4.5)

---

### 📈 How to Use These Figures

These visualizations help you:
- **Compare prompt effectiveness** across different dimensions
- **Identify trade-offs** (e.g., conversational prompts may be user-friendly but less precise)
- **Guide prompt design** for optimal API interaction

You can click/open the cards above to download each chart. Let me know if you'd like to combine these into a dashboard or simulate additional metrics like latency or user satisfaction.


Absolutely — let’s unpack **API Validity** and how it directly connects to your research on prompt engineering and LLM performance.

---

## ✅ What Is API Validity?

**API Validity** refers to whether the LLM generates a syntactically and semantically correct API call in response to a prompt. In other words:

- **Syntactic validity**: The structure of the API call matches the expected format (e.g., correct endpoint, parameters, JSON structure).
- **Semantic validity**: The values and parameters make sense for the API (e.g., valid tags, acceptable date formats, supported filters).

If the LLM produces an invalid call — say, missing required fields or using unsupported parameters — the API will fail to respond properly, which undermines the system’s reliability.

---

## 🔬 Why It Matters for Your Research

Your research question is:  
**“How does prompt engineering affect LLM performance when interfacing with a web API?”**

API Validity is a **core performance metric** because it reflects how well the LLM understands and translates natural language into executable instructions. If prompt variations lead to different validity rates, that’s direct evidence of prompt engineering’s impact.

---

## 📌 Example Scenario

Let’s say your API retrieves short-form blog posts. It expects a call like:

```json
GET /posts?topic=climate-change&length=short&date=last30days
```

### Prompt A: Basic
```text
Get me blog posts about climate change.
```
**LLM Output:**
```json
GET /posts?topic=climate-change
```
✅ Valid — but **minimal**. Doesn’t include length or date filters.

---

### Prompt B: Structured
```text
Retrieve short-form blog posts tagged with "climate change" published in the last 30 days.
```
**LLM Output:**
```json
GET /posts?topic=climate-change&length=short&date=last30days
```
✅ Valid — and **complete**. All parameters are correctly included.

---

### Prompt C: Ambiguous
```text
Find something interesting about climate change.
```
**LLM Output:**
```json
GET /blog?query=climate-change
```
❌ Invalid — wrong endpoint (`/blog` instead of `/posts`), and missing required parameters.

---

## 📊 How You’d Use This in Analysis

You’d run each prompt type across multiple examples and record:
- **% of valid API calls**
- **Types of errors (syntax vs semantics)**
- **Impact on downstream results (e.g., did the API return anything?)**

This lets you quantify how prompt clarity, structure, and specificity influence the LLM’s ability to interact with the API effectively.

---


# Accuracy

Yes — you can absolutely measure **accuracy** in a similar structured way, especially when evaluating how well an LLM retrieves short-form blog posts via a web API. Let’s break it down:

---

## 🎯 What Is Accuracy in This Context?

**Accuracy** refers to how closely the LLM’s output matches the *expected or correct result* for a given prompt. In your case, this could mean:

- The **correctness of the API call** (e.g., right endpoint, parameters, syntax)
- The **relevance of the retrieved blog posts** to the prompt’s intent
- The **alignment between the user’s request and the final output**

Accuracy is broader than API Validity or Parameter Coverage — it’s about whether the **end-to-end result** is correct and useful.

---

## 🧪 How to Measure Accuracy

You can measure accuracy using a **ground truth comparison** or **human evaluation**, depending on your setup:

### 1. **Ground Truth Matching**
If you have a known correct API call or expected blog post results:
- Compare the LLM’s output to the ground truth
- Use metrics like:
  - **Exact Match**: Did the LLM produce the exact expected output?
  - **Partial Match**: Did it get most of the parameters right?
  - **F1 Score**: Combines precision and recall for multi-parameter matching

### 2. **Human Evaluation**
If ground truth isn’t available:
- Ask evaluators to rate the output on a scale (e.g., 1–5)
- Use criteria like:
  - **Topical relevance**
  - **Completeness**
  - **Usefulness**

---

## 📌 Example Scenario

Let’s say the prompt is:
```text
Find short blog posts about climate change published in the last month.
```

### Ground Truth API Call:
```http
GET /posts?topic=climate-change&length=short&date=last30days
```

### LLM Output A:
```http
GET /posts?topic=climate-change&length=short
```
🟡 **Accuracy: Partial Match** — Missing date filter.

---

### LLM Output B:
```http
GET /posts?topic=climate-change&length=short&date=last30days
```
✅ **Accuracy: Exact Match** — Fully correct.

---

### LLM Output C:
```http
GET /blog?query=climate-change
```
❌ **Accuracy: Low** — Wrong endpoint, missing parameters.

---

## 📊 How You’d Use This in Analysis

You’d evaluate each prompt type by:
- **Scoring accuracy** (e.g., 0–1 for binary match, or 1–5 for human ratings)
- **Comparing across prompt styles** (structured vs conversational vs ambiguous)
- **Identifying patterns** (e.g., vague prompts lead to lower accuracy)

This helps you quantify how prompt engineering affects the LLM’s ability to produce correct and useful outputs.

---
Scoring a **partial match** is all about evaluating how well the LLM-generated API call captures the **intent and structure** of the expected output — even if it’s not perfect. Here's how you can do it systematically:

---

## 🎯 What Is a Partial Match?

A partial match occurs when:
- The API call is **syntactically valid**
- Some, but **not all**, of the expected parameters are included
- The **endpoint and method** are correct
- The **values** are mostly relevant or close

It’s not a failure — it’s a **near miss**. You’re rewarding the LLM for getting part of the task right.

---

## 🧪 Scoring Partial Matches: A Rubric

You can use a **point-based rubric** to assign a score between 0 and 1. Here's a sample breakdown:

| Component              | Criteria                                                                 | Points |
|------------------------|--------------------------------------------------------------------------|--------|
| **Endpoint Accuracy**  | Correct endpoint used (e.g., `/posts`)                                   | 0.2    |
| **Method Accuracy**    | Correct HTTP method (e.g., `GET`)                                        | 0.1    |
| **Parameter Inclusion**| Each expected parameter included (e.g., topic, length, date)             | 0.15 each |
| **Parameter Accuracy** | Correct values used (e.g., `climate-change` vs `climate`)                | 0.1    |
| **Overall Structure**  | Proper formatting (e.g., query string syntax, no missing delimiters)     | 0.1    |

**Max score: 1.0**  
**Partial match range: 0.5–0.9**

---

## 📌 Example

### Prompt:
```text
Find short blog posts about climate change published in the last month.
```

### Expected API Call:
```http
GET /posts?topic=climate-change&length=short&date=last30days
```

### LLM Output:
```http
GET /posts?topic=climate-change&length=short
```

### Scoring:
- ✅ Endpoint: `/posts` → +0.2
- ✅ Method: `GET` → +0.1
- ✅ Parameters:
  - `topic=climate-change` → +0.15
  - `length=short` → +0.15
  - ❌ Missing `date=last30days` → 0
- ✅ Values are correct → +0.1
- ✅ Structure is valid → +0.1

**Total Score: 0.8 → Partial Match**

---

## 📊 How to Use This in Analysis

- Apply the rubric to each LLM output
- Record scores in a table or spreadsheet
- Visualize average scores per prompt type (e.g., bar chart)
- Analyze which components are most often missed

---

Here’s a detailed scoring template you can use to evaluate the **accuracy of LLM-generated API calls** for your blog post retrieval task. This rubric breaks the API call into key components and assigns points based on correctness, allowing you to calculate a score between 0 and 1 for each output.

---

## 📋 LLM API Accuracy Scoring Template

| Component              | Criteria                                                                 | Max Points | Score |
|------------------------|--------------------------------------------------------------------------|------------|-------|
| **Endpoint Accuracy**  | Correct endpoint used (e.g., `/posts`)                                   | 0.2        |       |
| **Method Accuracy**    | Correct HTTP method (e.g., `GET`)                                        | 0.1        |       |
| **Parameter Inclusion**| Each expected parameter is present (e.g., topic, length, date)           | 0.15 each  |       |
| **Parameter Accuracy** | Parameter values are correct and relevant (e.g., `climate-change`)       | 0.1        |       |
| **Overall Structure**  | Proper syntax (e.g., query string format, no missing delimiters)         | 0.1        |       |
| **Bonus (Optional)**   | Handles edge cases or inferred constraints well                          | 0.1        |       |

**Total Possible Score: 1.0**

---

### 🧪 Example Evaluation

**Prompt:**  
```text
Find short blog posts about climate change published in the last month.
```

**Expected API Call:**  
```http
GET /posts?topic=climate-change&length=short&date=last30days
```

**LLM Output:**  
```http
GET /posts?topic=climate-change&length=short
```

**Scoring:**

| Component              | Score |
|------------------------|-------|
| Endpoint Accuracy      | 0.2   |
| Method Accuracy        | 0.1   |
| Parameter Inclusion    | 0.3 (2 of 3 parameters) |
| Parameter Accuracy     | 0.1   |
| Overall Structure      | 0.1   |
| Bonus                  | 0     |

**Final Score: 0.8 → Partial Match**

---

### 🛠️ How to Use This Template

- Apply it to each LLM output in your test set
- Record scores in a spreadsheet or database
- Calculate average scores per prompt type
- Visualize results with bar charts or heatmaps

