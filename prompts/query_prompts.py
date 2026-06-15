"""
MeetAll Query Generation & Evaluation Prompt Templates

Based on: "MeetBench-XL" (arXiv:2602.03285)
Methodology: Enterprise-informed query injection protocol validated by expert review

Usage:
    from prompts.query_prompts import QUERY_GENERATION_PROMPT, ANSWER_GENERATION_PROMPT
    import json
    
    # Format prompt with meeting context and complexity class
    prompt = QUERY_GENERATION_PROMPT.format(
        context=meeting_transcript,
        complexity_class="C02",
        language="en"
    )
"""

# ============================================================================
# 1. QUERY GENERATION PROMPTS (GPT-4o / DeepSeek-R1 style)
# ============================================================================

QUERY_GENERATION_PROMPT_EN = """\
You are an enterprise meeting assistant tasked with generating realistic user queries 
that would naturally arise during or after a business meeting.

## Context: Meeting Transcript
{context}

## Task
Generate {num_queries} natural-language question(s) that a meeting participant might ask,
based on the above transcript. The query must match this complexity class:

**Complexity Class**: {complexity_class}
- Cognitive Load (CL): {cl_desc}
- Context Dependency (CD): {cd_desc}
- Domain Knowledge (DK): {dk_desc}
- Task-Execution Effort (TE): {te_desc}

## Requirements
1. The query MUST be answerable from the provided transcript context
2. The query should sound natural - like something a real person would ask in a meeting
3. Match the cognitive difficulty level specified by CL ({cl_level})
4. Reference the appropriate temporal scope based on CD ({cd_level})
5. Use appropriate domain terminology based on DK ({dk_level})
6. Require the action level specified by TE ({te_level})

## Output Format
Return ONLY the generated query/question text, nothing else.
Do not include explanations, metadata, or formatting markers.

Query:"""

QUERY_GENERATION_PROMPT_ZH = """\
你是一个企业会议助手，负责生成在商务会议中自然出现的用户查询。

## 上下文：会议记录
{context}

## 任务
基于上述会议记录，生成{num_queries}个与会者可能提出的自然语言问题。查询必须符合以下复杂度类别：

**复杂度类别**: {complexity_class}
- 认知负荷 (CL): {cl_desc}
- 上下文依赖 (CD): {cd_desc}
- 领域知识 (DK): {dk_desc}
- 任务执行难度 (TE): {te_desc}

## 要求
1. 查询必须能从提供的会议记录上下文中回答
2. 查询应该听起来自然，像真实的人在会议中会问的问题
3. 符合CL({cl_level})指定的认知难度级别
4. 根据CD({cd_level})引用适当的时间范围
5. 根据DK({dk_level})使用适当的领域术语
6. 要求TE({te_level})指定的行动级别

## 输出格式
只返回生成的查询/问题文本，不要包含解释、元数据或格式标记。

查询："""


ANSWER_GENERATION_PROMPT_EN = """\
You are an expert meeting assistant. Based on the meeting transcript below, provide a 
comprehensive and accurate answer to the user's question.

## Meeting Transcript
{context}

## User Question
{question}

## Requirements
1. Answer the question thoroughly using information from the transcript
2. If the answer requires synthesis across multiple parts of the transcript, include relevant details
3. Cite specific evidence when possible (speaker names, timestamps, key points)
4. If the question cannot be fully answered from the context, state what information is missing
5. Keep the response concise but complete

## Answer:"""

ANSWER_GENERATION_PROMPT_ZH = """\
你是一个专业的会议助手。根据下面的会议记录，为用户提供全面准确的答案。

## 会议记录
{context}

## 用户问题
{question}

## 要求
1. 使用会议记录中的信息全面回答问题
2. 如果需要综合记录的多个部分，请包含相关细节
3. 尽可能引用具体证据（发言人、时间戳、关键点）
4. 如果无法从上下文中完全回答，请说明缺少哪些信息
5. 回答简洁但完整

## 答案："""


# ============================================================================
# 2. EVALUATION PROMPTS (MeetBench-XL / CompassJudger style)
# ============================================================================

MEETBENCH_EVALUATION_PROMPT = """\
你是一个擅长评价文本质量的助手。
请你以公正的评判者的身份，评估一个AI助手对于用户提问的回答的质量。

由于您评估的回答类型是会议理解任务，因此你需要从下面的几个维度对回答进行评估：

1. **事实正确性 (Factual Accuracy)**: 回答中提供的信息是否准确无误，是否基于可信的事实和数据。

2. **满足用户需求 (User Need Satisfaction)**: 回答是否满足了用户提出问题的目的和需求，是否对问题进行了全面而恰当的回应。

3. **简洁性 (Conciseness)**: 回答是否简明扼要，没有冗余信息，用最少的文字传达最多的有效内容。

4. **结构清晰性 (Structural Clarity)**: 回答是否结构清晰，逻辑连贯，便于理解和跟随。

5. **完整性 (Completeness)**: 回答是否完整覆盖了问题的所有方面，没有遗漏重要信息。

我们会给您提供：
- 用户的提问 (Question)
- 高质量的标准参考答案 (Reference Answer)
- 需要您评估的AI助手的答案 (Model Response)

## 评估流程
当你开始你的评估时，你需要按照遵守以下的流程：
1. 将AI助手的答案与参考答案进行比较，指出AI助手的答案有哪些不足
2. 从不同维度对AI助手的答案进行评价，在每个维度的评价之后，给每一个维度一个1～10的分数
3. 最后，综合每个维度的评估，对AI助手的回答给出一个1～10的综合分数
4. 你的打分需要尽可能严格

## 评分规则
- **1-2分**: 回答存在与问题不相关的本质性事实错误或有害内容
- **3-4分**: 回答基本无害但质量较低，没有满足用户需求
- **5-6分**: 回答基本满足要求但在部分维度表现较差
- **7-8分**: 回答质量与参考答案相近，在各维度表现良好
- **9-10分**: 回答质量显著超过参考答案，充分解决所有需求

## 输入数据

### 用户提问
{question}

### 标准参考答案
{reference_answer}

### AI助手回答
{model_response}

请按照上述流程进行评估，并在最后按照以下字典格式返回所有打分结果：

{{'事实正确性': 打分, '满足用户需求': 打分, '简洁性': 打分, '结构清晰性': 打分, '完整性': 打分, '综合得分': 打分}}

示例输出格式：
{{'事实正确性': 8, '满足用户需求': 7, '简洁性': 9, '结构清晰性': 8, '完整性': 7, '综合得分': 8}}"""


MEETBENCH_EVALUATION_PROMPT_EN = """\
You are an assistant skilled at evaluating text quality.
Please act as an impartial judge and evaluate the quality of an AI assistant's response to a user's question.

Since the response type you are evaluating is a meeting understanding task, you need to evaluate the response from the following dimensions:

1. **Factual Accuracy**: Whether the information provided in the response is accurate and based on credible facts and data.

2. **User Need Satisfaction**: Whether the response meets the purpose and needs of the user's question, and whether it provides a comprehensive and appropriate answer to the question.

3. **Conciseness**: Whether the response is concise and to-the-point, without redundant information, conveying the most effective content with the least text.

4. **Structural Clarity**: Whether the response has a clear structure and logical coherence, making it easy to understand and follow.

5. **Completeness**: Whether the response completely covers all aspects of the question without omitting important information.

We will provide you with:
- The user's question (Question)
- A high-quality reference answer (Reference Answer)
- The AI assistant's answer to be evaluated (Model Response)

## Evaluation Process
When you begin your evaluation, you must follow this process:
1. Compare the AI assistant's answer with the reference answer, pointing out the shortcomings of the AI assistant's answer
2. Evaluate the AI assistant's answer from different dimensions, giving each dimension a score from 1-10 after each dimension's evaluation
3. Finally, comprehensively assess each dimension's evaluation, and give an overall score from 1-10 for the AI assistant's answer
4. Your scoring should be as strict as possible

## Scoring Rules
- **1-2 points**: The response has essential factual errors unrelated to the question or harmful content
- **3-4 points**: The response is basically harmless but of low quality, failing to meet user needs
- **5-6 points**: The response basically meets requirements but performs poorly in some dimensions
- **7-8 points**: The response quality is close to the reference answer, performing well in all dimensions
- **9-10 points**: The response quality significantly exceeds the reference answer, fully addressing all needs

## Input Data

### User Question
{question}

### Reference Answer
{reference_answer}

### AI Assistant Answer
{model_response}

Please evaluate according to the above process, and return all scoring results in the following dictionary format at the end:

{{'Factual Accuracy': score, 'User Need Satisfaction': score, 'Conciseness': score, 'Structural Clarity': score, 'Completeness': score, 'Overall Score': score}}

Example output format:
{{'Factual Accuracy': 8, 'User Need Satisfaction': 7, 'Conciseness': 9, 'Structural Clarity': 8, 'Completeness': 7, 'Overall Score': 8}}"""


# ============================================================================
# 3. COMPLEXITY CLASS DEFINITIONS (for prompt formatting)
# ============================================================================

COMPLEXITY_CLASSES = {
    "C01": {
        "name": "Simple Fact-Check",
        "cl_level": "low", "cl_desc": "Direct fact extraction (<5s response)",
        "cd_level": "none", "cd_desc": "Self-contained, no context needed",
        "dk_level": "general", "dk_desc": "Common sense only",
        "te_level": "low", "te_desc": "Passive recording",
    },
    "C02": {
        "name": "Recent Summary",
        "cl_level": "medium", "cl_desc": "Synthesis across 2-5 utterances (15-30s)",
        "cd_level": "recent", "cd_desc": "References last 3-5 utterances",
        "dk_level": "general", "dk_desc": "Common sense only",
        "te_level": "medium", "te_desc": "Structured organization",
    },
    "C03": {
        "name": "Long-range Recall",
        "cl_level": "medium", "cl_desc": "Synthesis across 2-5 utterances (15-30s)",
        "cd_level": "long_range", "cd_desc": "References content 15+ min earlier",
        "dk_level": "basic", "dk_desc": "Field-specific terminology",
        "te_level": "medium", "te_desc": "Structured organization",
    },
    "C04": {
        "name": "Domain-Basic Reasoning",
        "cl_level": "medium", "cl_desc": "Synthesis across 2-5 utterances (15-30s)",
        "cd_level": "recent", "cd_desc": "References last 3-5 utterances",
        "dk_level": "basic", "dk_desc": "Field-specific terminology",
        "te_level": "low", "te_desc": "Passive recording",
    },
    "C05": {
        "name": "Expert Domain Inference",
        "cl_level": "high", "cl_desc": "Multi-hop inference (>45s)",
        "cd_level": "long_range", "cd_desc": "References content 15+ min earlier",
        "dk_level": "expert", "dk_desc": "Deep technical/regulatory expertise",
        "te_level": "high", "te_desc": "Strategic planning with tool calls",
    },
    "C06": {
        "name": "Cross-Meeting Tracking",
        "cl_level": "medium", "cl_desc": "Synthesis across 2-5 utterances (15-30s)",
        "cd_level": "cross_meeting", "cd_desc": "References prior sessions",
        "dk_level": "basic", "dk_desc": "Field-specific terminology",
        "te_level": "medium", "te_desc": "Structured organization",
    },
    "C07": {
        "name": "Strategic Decision Support",
        "cl_level": "high", "cl_desc": "Multi-hop inference (>45s)",
        "cd_level": "long_range", "cd_desc": "References content 15+ min earlier",
        "dk_level": "basic", "dk_desc": "Field-specific terminology",
        "te_level": "high", "te_desc": "Strategic planning with tool calls",
    },
    "C08": {
        "name": "Compliance & Risk",
        "cl_level": "high", "cl_desc": "Multi-hop inference (>45s)",
        "cd_level": "cross_meeting", "cd_desc": "References prior sessions",
        "dk_level": "expert", "dk_desc": "Deep technical/regulatory expertise",
        "te_level": "high", "te_desc": "Strategic planning with tool calls",
    },
    "C09": {
        "name": "Technical Deep-Dive",
        "cl_level": "high", "cl_desc": "Multi-hop inference (>45s)",
        "cd_level": "long_range", "cd_desc": "References content 15+ min earlier",
        "dk_level": "expert", "dk_desc": "Deep technical/regulatory expertise",
        "te_level": "medium", "te_desc": "Structured organization",
    },
    "C10": {
        "name": "Project Status Synthesis",
        "cl_level": "medium", "cl_desc": "Synthesis across 2-5 utterances (15-30s)",
        "cd_level": "long_range", "cd_desc": "References content 15+ min earlier",
        "dk_level": "basic", "dk_desc": "Field-specific terminology",
        "te_level": "medium", "te_desc": "Structured organization",
    },
    "C11": {
        "name": "Meeting Facilitation",
        "cl_level": "low", "cl_desc": "Direct fact extraction (<5s)",
        "cd_level": "recent", "cd_desc": "References last 3-5 utterances",
        "dk_level": "general", "dk_desc": "Common sense only",
        "te_level": "medium", "te_desc": "Structured organization",
    },
    "C12": {
        "name": "Resource Coordination",
        "cl_level": "medium", "cl_desc": "Synthesis across 2-5 utterances (15-30s)",
        "cd_level": "recent", "cd_desc": "References last 3-5 utterances",
        "dk_level": "basic", "dk_desc": "Field-specific terminology",
        "te_level": "medium", "te_desc": "Structured organization",
    },
    "C13": {
        "name": "Executive Overview",
        "cl_level": "high", "cl_desc": "Multi-hop inference (>45s)",
        "cd_level": "long_range", "cd_desc": "References content 15+ min earlier",
        "dk_level": "general", "dk_desc": "Common sense only",
        "te_level": "high", "te_desc": "Strategic planning with tool calls",
    },
}


def get_query_generation_prompt(language="en"):
    """
    Get the appropriate query generation prompt template for the given language.
    
    Args:
        language: "en" for English, "zh" for Chinese
        
    Returns:
        Prompt template string
    """
    if language == "zh":
        return QUERY_GENERATION_PROMPT_ZH
    return QUERY_GENERATION_PROMPT_EN


def get_answer_generation_prompt(language="en"):
    """
    Get the appropriate answer generation prompt template for the given language.
    
    Args:
        language: "en" for English, "zh" for Chinese
        
    Returns:
        Prompt template string
    """
    if language == "zh":
        return ANSWER_GENERATION_PROMPT_ZH
    return ANSWER_GENERATION_PROMPT_EN


def format_query_prompt(context, complexity_class, num_queries=1, language="en"):
    """
    Format the query generation prompt with all required parameters.
    
    Args:
        context: Meeting transcript text (max ~5000 tokens recommended)
        complexity_class: One of C01-C13
        num_queries: Number of queries to generate
        language: "en" or "zh"
        
    Returns:
        Formatted prompt string ready for LLM API call
    """
    class_def = COMPLEXITY_CLASSES.get(complexity_class, COMPLEXITY_CLASSES["C01"])
    
    prompt_template = get_query_generation_prompt(language)
    
    return prompt_template.format(
        context=context[:8000],  # Limit context length
        num_queries=num_queries,
        complexity_class=complexity_class,
        cl_level=class_def["cl_level"],
        cl_desc=class_def["cl_desc"],
        cd_level=class_def["cd_level"],
        cd_desc=class_def["cd_desc"],
        dk_level=class_def["dk_level"],
        dk_desc=class_def["dk_desc"],
        te_level=class_def["te_level"],
        te_desc=class_def["te_desc"],
    )


def format_answer_prompt(context, question, language="en"):
    """
    Format the answer generation prompt with all required parameters.
    
    Args:
        context: Meeting transcript text
        question: User's question
        language: "en" or "zh"
        
    Returns:
        Formatted prompt string ready for LLM API call
    """
    prompt_template = get_answer_generation_prompt(language)
    
    return prompt_template.format(
        context=context[:5000],
        question=question,
    )


def format_evaluation_prompt(question, reference_answer, model_response, language="en"):
    """
    Format the MeetBench evaluation prompt.
    
    Args:
        question: Original user question
        reference_answer: Gold/ground truth answer
        model_response: Model's response to evaluate
        language: "en" for English, "zh" for Chinese
        
    Returns:
        Formatted evaluation prompt string
    """
    if language == "zh":
        prompt_template = MEETBENCH_EVALUATION_PROMPT
    else:
        prompt_template = MEETBENCH_EVALUATION_PROMPT_EN
    
    return prompt_template.format(
        question=question,
        reference_answer=reference_answer,
        model_response=model_response,
    )


if __name__ == "__main__":
    # Example usage
    sample_context = """
    [00:01] John: Let's start today's standup. Sarah, can you give us your update?
    [00:05] Sarah: Sure. I finished the API migration we discussed last week. The endpoints are now live.
    [00:12] Mike: Great work! I've been working on the frontend integration. Almost done, just need to fix one bug.
    [00:18] Lisa: Regarding compliance - I need everyone to review the new data handling policy before Friday's deadline.
    [00:25] John: Noted. Any blockers?
    [00:28] Sarah: No blockers from my side.
    [00:31] Mike: Actually, I'm blocked on the database schema changes. Waiting for DB team approval.
    """
    
    # Generate a C02 (Recent Summary) query
    prompt = format_query_prompt(
        context=sample_context,
        complexity_class="C02",
        num_queries=1,
        language="en"
    )
    
    print("=" * 60)
    print("Sample Query Generation Prompt (Class C02)")
    print("=" * 60)
    print(prompt)
