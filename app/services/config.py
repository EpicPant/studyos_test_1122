
CLAUDE_API_KEY = "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"
OPENAI_API_KEY = "sk-rNiuQeFG7pLzTjMKV1snb2jyMm8QA8gE"
DEEPGRAM_API_KEY = "157e7dae07440188ab6eb4c528ce7128594b6a03"

PARTS_PROMT =  """You are tasked with analyzing a lecture text and identifying its main topics and subtopics. Your goal is to create a structured list of the lecture's key points without providing the content of each topic. Here's the lecture text you need to analyze:

<lecture_text>
{lecture_transcribe}
</lecture_text>

Please follow these steps to complete the task:

1. Carefully read and analyze the entire lecture text.

2. Identify the main topics of the lecture. These are typically broad themes or sections that encompass multiple related ideas.

3. For each main topic, determine if it can be further divided into subtopics. If a topic is extensive or covers multiple distinct ideas, it should be broken down into smaller, more specific subtopics.

4. Create a hierarchical list of the main topics and their subtopics. Use Roman numerals (I, II, III, etc.) for main topics and capital letters (A, B, C, etc.) for subtopics.

5. Provide only the titles of the topics and subtopics, not their content or explanations.

6. If there's an overarching title or theme for the entire lecture, include it at the beginning of your list.

Format your response as follows:

<topic_list>
Lecture Title: [Overall title of the lecture, if apparent]

I. [First Main Topic]
   A. [Subtopic A]
   B. [Subtopic B]

II. [Second Main Topic]
    A. [Subtopic A]
    B. [Subtopic B]
    C. [Subtopic C]

[Continue with additional main topics and subtopics as needed]
</topic_list>

Before submitting your final answer, review your list to ensure:
- All major themes from the lecture are represented
- Topics and subtopics are logically organized
- The hierarchy accurately reflects the structure of the lecture
- No content or explanations are included, only titles

Remember, your goal is to provide a clear, concise overview of the lecture's structure without delving into the specific content of each topic."""

BORDERLINES_PROMT = '''
You are tasked with dividing a given text into topics and indicating the boundaries of each topic. Here's how to proceed:

First, you will be provided with a list of topics:
<topics>
{topics}
</topics>

Next, you will be given the full text to analyze:
<text>
{lecture_text}
</text>

Your task is to divide this text into the topics provided earlier. You should indicate where each topic starts and ends within the text.

To indicate the boundaries of each topic:
1. Identify the sentence where a topic begins and the sentence where it ends.
2. Use the format "Topic: [topic name] - Starts: [first few words of starting sentence] ... Ends: [last few words of ending sentence]"

Present your analysis in the following format:
{format}

Ensure that your JSON output follows this structure exactly. Include all topics and subtopics that you identified in the text, with their respective start and end points.

Remember:
- Every sentence in the text should be assigned to a topic.
- Topics should not overlap.
- If a topic is not present in the text, do not include it in your output.
- Be as precise as possible when indicating the start and end of each topic.
- If a topic spans only one sentence, the start and end will be the same sentence.

Provide your analysis of the topic boundaries without any additional commentary or explanation.
'''
CARDS_PROMT2 = """
You are tasked with creating flashcards to check understanding based on a given lecture text. Your goal is to analyze the text and create questions that test comprehension of key concepts and their applications.

First, carefully read the following lecture text:

<lecture_text>
{TOPIC_TEXT}
</lecture_text>

To create effective cards, follow these steps:

1. Identify the main concepts:
   - Focus on the most significant concepts, theories, or principles essential for understanding the material.
   - Formulate a question about the definition, structure, or key components of the concept.
   - Follow up with a question about its application, purpose, or implications.

2. Ensure clarity and relevance:
   - Make sure the questions are clear, concise, and directly related to the lecture content.
   - Avoid using exact phrases from the text to encourage deeper understanding.

3. Create multiple cards based on the lecture text.

4. Format each card as a JSON object with the following structure:
   {format}

Here's an example of a well-formatted card:

{example}

Create multiple cards based on the lecture text, ensuring that each card covers a distinct concept or idea. Present all cards in a single JSON array. Begin your response with the opening bracket of the JSON array and end it with the closing bracket.
"""
CARDS_PROMT = """
You will be creating cards to check understanding based on a given lecture text. Your task is to analyze the text and create questions that test comprehension of key concepts and their applications.


First, carefully read the following lecture text:


<lecture_text> 
{TOPIC_TEXT} 
</lecture_text>


To create effective cards, follow these steps:


Identify the Main Concepts:


Focus on the most significant concepts, theories, or principles essential for understanding the material.


Formulate a question about the definition, structure, or key components of the concept.

Use phrases like:

"What is [concept]?"

"How would you define [concept]?"

"What are the key components of [concept]?" b) Application or Critical Thinking Question:

Ask a follow-up question about its application, purpose, or implications.

Use phrases like:

"Give examples where [concept] is applied."

"What is the purpose of [concept]?"

"How does [concept] relate to [another concept]?"

"What are the potential limitations of [concept]?"

"How would you apply [concept] in a different context?"

Ensure Clarity and Relevance:


Make sure the questions are clear, concise, and directly related to the lecture content.

Avoid using exact phrases from the text to encourage deeper understanding.

Output your cards in the following format:


<card> <question> [First part of the question about the concept's definition or structure] [Second part of the question about the concept's application, purpose, or critical analysis] </question> </card>

Here's an example of a well-formatted card:


<card> <question> What is the law of supply and demand? How is this economic principle applied in real-world markets? </question> </card>
"""

CARDS_CHEKER = """
You are an AI assistant tasked with evaluating answers in a spaced repetition system. Your job is to check the completeness of a user's answer against a provided complete answer. Here's what you need to do:

First, review the following information:

Question:
<question>
{question}
</question>

Complete Answer:
<complete_answer>
{complete_answer}
</complete_answer>

User's Answer:
<user_answer>
{user_answer}
</user_answer>

Your task is to evaluate the user's answer and assign a percentage score from 0 to 100, where:
- 0 means the answer is not complete at all
- 100 means the answer is fully complete and matches the provided complete answer

Guidelines for evaluation:
1. Compare the user's answer to the complete answer, looking for key concepts, facts, and details.
2. Consider partial credit for partially correct or incomplete answers.
3. Do not penalize for minor differences in wording if the core concept is correct.
4. If the user's answer is too general, you should ask them to expand on their answer.
5. Do not provide hints or additional information from the complete answer.

Analyze the user's answer carefully, comparing it to the complete answer. Consider how much of the required information is present and how accurately it is expressed.

Provide a brief explanation of your evaluation, highlighting what was correct, what was missing, or what needs expansion. Then, assign a percentage score based on the completeness of the answer.

Format your response as follows:
<evaluation>
[Your explanation of the evaluation]
</evaluation>

<score>[Percentage score]</score>

If you need to ask the user to expand their answer, use this format instead:
<expand>Please expand on your answer. [Optional: Specific aspect to expand on without giving hints]</expand>

Remember, your goal is to accurately assess the completeness of the user's answer without providing additional information or hints from the complete answer.
"""