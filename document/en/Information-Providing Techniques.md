---
title: "Information-Providing Techniques"
slug: "info-providing-techniques"
order: 3
---

## Techniques in Prompt Engineering

In practice, prompt engineering is not a one-way command but a methodology to improve efficiency by continuously "aligning" requirements. The following are several common and efficient strategies along with negative examples:

### 1. Define Task and Goal Clearly

Specific instructions can guide the model to produce more reliable results. When writing a prompt, it is recommended to clarify the subject, audience, and expected effect.

**Comparison of Examples:**

*   **[Good]:** "Please write a popular science short article about 'quantum entanglement' for middle school students. The word count should be around 500 words. The language should be vivid and humorous, aiming to stimulate the reader's curiosity."

*   **[Bad]:** "Write an article about quantum entanglement." (The information is too vague, making it difficult for the model to grasp the appropriate audience depth and style.)


### 2. Providing Contextual Background

Supplementing necessary information (such as scene descriptions and constraints) is crucial. The model has no way of knowing your environment. The clearer the background, the more useful the suggestions.

**Comparison of Examples:**

*   **[Good]:** "I am developing an open-source project based on Django, and I encountered a 500 error during file uploads in a Docker environment. The server uses Nginx and the system is Ubuntu. Please help me analyze the cause and provide troubleshooting steps."

*   **[Bad]:** "My project's file upload keeps erroring with a 500. How do I fix it?" (Lacking information about the tech stack and deployment environment, which can easily lead the troubleshooting in the wrong direction.)


### 3. Using Examples for Guidance (Few-shot)

By providing reference examples, you intuitively tell the model "what a good result is." This is particularly effective for tasks involving specific formats or linguistic styles.

**Comparison of Examples:**

*   **[Good]:** "Please convert informal tone into formal business tone. Example: 'Hey, how's that thing going?' ➔ 'Hello, could you please provide an update on the progress of the matter we discussed?' To be converted: 'Send me that file.'"

*   **[Bad]:** "Help me rewrite 'Send me that file' into a formal tone." (Lacking specific demonstrations of 'formality' levels, the output may deviate from your actual needs.)

### 4. Instruct the Model to Answer from Multiple Perspectives

Some questions do not have clear answers, or involve comparing different schemes. This is common for many questions in the humanities or controversial topics. In such cases, to obtain a more objective answer, we should explicitly instruct the large language model to analyze the problem from multiple perspectives.

**Comparison of Examples:**

*   **[Good]:** "Please analyze Obama's performance from economic, diplomatic, and social perspectives, respectively."

*   **[Bad]:** "Was Obama a good president?" (The information is too vague; the model might only analyze from a single angle or provide an extreme answer.)

Of course, most current language models know that there are no black-and-white answers in the world, and their responses are relatively objective. This technique is more applicable to complex problems where you yourself may not know which perspectives to consider.

**Comparison of Examples:**

**[Good]:**

```
Currently, three economists are observing a nearly closed independent economy. They observed that:

1. This economy is located on a medium-sized island.
2. The variety of agricultural products in this market is limited, and supply is less than demand.
3. The supply in this labor market is less than demand.

The three economists expressed different views on the current state of the economy on this island.
From the perspective of modern economics, what did each of the three economists say?
```

**[Bad]:** 

```
There is an economy, and:

1. This economy is located on a medium-sized island.
2. The variety of agricultural products in this market is limited, and supply is less than demand.
3. The supply in this labor market is less than demand.

From the perspective of modern economics, how should we analyze the economy on this island?
```
