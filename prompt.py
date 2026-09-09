# llm/prompt.py

import json


SYSTEM_PROMPT = """
You are an expert educational researcher specializing in
pedagogical analysis of instructional material.

Your task is to evaluate an educational text using the
provided pedagogical rubric.

IMPORTANT RULES:

1. Base your evaluation ONLY on the content provided.
2. Do not assume that a pedagogical feature exists if there
   is no evidence for it.
3. Every score must be supported by evidence from the article.
5. Do not evaluate topic relevance or image relevance.
   Those are handled by separate systems.
6. Do not evaluate general writing quality unless it affects
   the learner's ability to understand the material.
7. Return ONLY valid JSON.
"""


RUBRIC = """
Evaluate the article using the following criteria.

All scores must be integers from 1 to 5.

1. EXPLANATION QUALITY

Evaluate how clearly the article explains concepts.

1 = Concepts are poorly explained or mostly presented without explanation.
2 = Limited explanations; important concepts are difficult to follow.
3 = Generally understandable explanations with some gaps.
4 = Clear and well-developed explanations.
5 = Exceptionally clear explanations that make difficult concepts accessible.

2. CONCEPTUAL UNDERSTANDING

Evaluate whether the material helps learners understand underlying
concepts rather than merely perform procedures.

1 = Almost entirely procedural; little conceptual explanation.
2 = Mostly procedural with limited conceptual discussion.
3 = Contains both procedural and conceptual material.
4 = Strong conceptual explanations alongside procedures.
5 = Deeply develops conceptual understanding, intuition, and relationships.

3. SCAFFOLDING

Evaluate how effectively the material supports the learner as concepts
increase in complexity.

Consider:
- prerequisite knowledge
- progression from simple to complex
- intermediate explanations
- step-by-step support
- transitions between concepts

1 = Little or no scaffolding.
2 = Some support but major gaps exist.
3 = Adequate scaffolding.
4 = Strong and consistent scaffolding.
5 = Carefully structured scaffolding that progressively supports independence.

4. WORKED EXAMPLES

Evaluate the pedagogical quality of examples and their solutions.

Consider:
- relevance to concepts
- completeness
- explanation of steps
- reasoning behind steps
- progression in difficulty

1 = Examples are absent or poorly explained.
2 = Examples exist but provide limited instructional value.
3 = Examples adequately demonstrate procedures.
4 = Examples are well explained and support learning.
5 = Examples are exceptionally clear, purposeful, and progressively developed.

5. COGNITIVE DEMAND

Evaluate the level of cognitive processing required from the learner.

Use the revised Bloom's taxonomy:

Remember
Understand
Apply
Analyze
Evaluate
Create

1 = Primarily recall.
2 = Mostly understanding.
3 = Primarily application.
4 = Significant analysis/evaluation.
5 = Strong higher-order thinking involving analysis, evaluation,
    or creation.

IMPORTANT:
This score represents the overall cognitive demand of the material,
not simply the difficulty of the mathematics.

6. PRACTICE OPPORTUNITIES

Evaluate whether learners are given opportunities to actively practice
the concepts.

Consider:
- exercises
- questions
- application problems
- self-check activities
- opportunities to solve independently

1 = No meaningful practice.
2 = Very limited practice.
3 = Some practice opportunities.
4 = Good opportunities for practice.
5 = Extensive and well-designed practice opportunities.

7. FEEDBACK

Evaluate whether learners receive useful feedback about their performance.

Consider:
- worked solutions
- answer explanations
- hints
- common mistakes
- corrective explanations
- self-check mechanisms

1 = No meaningful feedback.
2 = Very limited feedback.
3 = Basic feedback is available.
4 = Good feedback mechanisms.
5 = Detailed, corrective, and instructionally useful feedback.
"""


def build_prompt(article):

    article_json = json.dumps(
        article,
        indent=2,
        ensure_ascii=False
    )

    prompt = f"""
{RUBRIC}

OUTPUT FORMAT

Return JSON with exactly this structure:

{{
  "article_id": "...",

  "pedagogical_analysis": {{

    "explanation_quality": {{
      "score": 1,
      "justification": "...",
    }},

    "conceptual_understanding": {{
      "score": 1,
      "justification": "...",
    }},

    "scaffolding": {{
      "score": 1,
      "justification": "...",
    }},

    "worked_examples": {{
      "score": 1,
      "justification": "...",
    }},

    "cognitive_demand": {{
      "score": 1,
      "justification": "...",
    }},

    "practice_opportunities": {{
      "score": 1,
      "justification": "...",
    }},

    "feedback": {{
      "score": 1,
      "justification": "...",
    }}
  }}
}}

For each criterion:

- Give one integer score from 1 to 5.
- Explain the reasoning.

ARTICLE TO ANALYZE:

{article_json}
"""

    return prompt