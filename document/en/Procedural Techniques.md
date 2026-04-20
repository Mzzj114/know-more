---
title: "Procedural Techniques"
slug: "procedure-techniques"
order: 4
---

## Procedural Techniques

### 1. Chain-of-Thought

When facing complex tasks or tasks involving reasoning, decompose the task into multiple intermediate steps and guide the model to think step-by-step. This can significantly improve the accuracy of logical operations.

**Comparison of Examples:**

*   **[Good]:** "Please answer step-by-step: Town A and Town B are 300 km apart. Car A travels at 60 km/h, and Car B travels at 40 km/h. The two cars travel toward each other. Please first calculate the time needed for them to meet, and then calculate the total distance Car A travels at the time of meeting."

*   **[Bad]:** "Two cars are 300 km apart, with speeds of 60 and 40, and they start toward each other. How far did A run?" (Lacks thought chain prompts; for complex calculations, the model occasionally skips steps and reaches incorrect conclusions.)

In addition to specifying decomposed steps directly in the prompt, we can also use the chat history and context features of AI applications to guide the model step-by-step.

**Example:**

* User: Town A and Town B are 300 km apart. Car A travels at 60 km/h, and Car B travels at 40 km/h. The two cars travel toward each other. Please calculate the time needed for them to meet.
* AI: 3 h
* User: Based on this result, find the total distance Car A travels.
* AI： 60 km/h * 3 hours = 180 km

However, for some very complex problems where you don't know how to decompose the task, you can first let the AI decompose the task and create a todo list for the entire task, then guide the AI to act according to the task list it created.

**Comparison of Examples:**

**[Good]:** 

- User: Now you need to write a popular science article about quantum entanglement for high school students. The word count is about 1500 words, and the language should be vivid and humorous to stimulate the reader's curiosity. Based on this requirement, write an outline for the article.
- AI: [Generated Outline]
- User: According to this outline, let's write the first paragraph of the article.
- AI: [Generated First Paragraph]
- User: Please generate the second paragraph.
- ...

**[Bad]:** 

- User: Write a popular science article about quantum entanglement for high school students. The word count is about 1500 words, and the language should be vivid and humorous to stimulate the reader's curiosity.

In this example, the article we want to write is relatively long. Letting the AI generate it all at once may cause the following issues:

- Exceeding the single output limit
- Poor logic and structure in the output
- AI makes independent decisions on certain factors (such as paragraph structure, citation style, etc.), resulting in too many unsatisfactory areas that are difficult to modify.

Conversely, if you first let the AI generate an outline (which is the "task list" in the context of writing) and then guide the AI to generate it section by section, you can gain the following benefits:

- Users can master the overall structure (and can modify the task list themselves)
- Each generation is shorter and more readable
- The output content is easy to change; if a problem arises, the AI can be asked to correct it.

### 2. Precise Control of Output Format

Most of today's large language models have been adjusted to naturally use markdown format for output.

> [What is Markdown?](https://markdown.com.cn/intro.html)

Specifying the required output format can significantly improve the readability and reuse value of the content.

However, language models are "language models" and obviously perform poorly when outputting binary or human-unreadable languages. This poses certain limitations for some office files we commonly use, such as .docx, .pptx, .xlsx, and .pdf. But we still have some ways to solve this problem.

#### 2.1 Various Text-Based Files

You might not know that many types of files have multiple storage methods.
For example, for spreadsheets, the file type we commonly use is xlsx, which is a binary format specified by Microsoft.
But there is something called csv (comma-separated values), which uses comma-separated text to store tables.

Knowing this, we can directly let the AI output in csv format and then use software to convert it to xlsx format.

Other similar alternative file formats include...

**Comparison of Examples:**

*   **[Good]:** "[A lot of data], help me organize this data into a table in csv format. Row and column requirements: ..."

*   **[Bad]:** "[A lot of data], organize this information into a table." (Output format is uncertain and may require secondary manual typesetting.)

The core of these techniques lies in "transparent communication"—clearer expression of requirements means less information loss.

#### 2.2 Let AI Program

AI cannot directly generate human-unreadable files, but AI can write programs and then let the programs generate these files.
Even if you are not familiar with programming, you can use this method because for these simple scripts, as long as your requirements are clear, the AI rarely makes mistakes. Installing a simple programming environment (such as Python) will make your work much easier.

Nowadays, some AI tools (e.g. ChatGPT) have built-in programming sandboxes, which allow them to run code directly online, making the entire process simpler.
However, it should be noted that online sandboxes often do not allow the generation of files, so running scripts locally is still superior.

**Comparison of Examples:**

*   **[Good]:** "[A lot of data], please write a python script that uses appropriate libraries to organize this data and save it in .xlsx format. Tell me how to use this script. Row and column requirements: ..."

*   **[Bad]:** "[A lot of data], organize this information into a table." (Output format is uncertain and may require secondary manual typesetting.)

### 3. Meta Prompts

Meta prompts refer to prompts that let the AI generate prompts. Since AI is powerful, we can also consult the AI about the use of AI itself.

Meta prompt techniques are suitable for cases where the task is complex, the prompt you need is long, or there are many requirements.

When using meta prompt techniques, people generally first point out the task and then explicitly let the AI write a prompt for the AI to execute that task.

This technique is generally used in conjunction with structured prompts.

**Example:**

- User: Please generate a structured prompt template for an AI to write a popular science article. The topic is quantum entanglement, and the audience consists of high school students.
- AI: [The content generated by AI is long, try it yourself!]
- User: [Start a new chat]
- User: [User-modified AI-generated prompt]
- AI: [Article]
