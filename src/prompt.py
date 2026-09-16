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

1. CONSTRUCTIVE ALIGNMENT

Definition: The degree to which the intended learning outcomes, the instructional content, and the practice/assessment tasks are in absolute harmony. If a material promises to teach a learner how to "analyze" a system, the practice must require analysis, not merely the recall of definitions.

1 = Severe misalignment: content and practice do not match the stated or implied learning goals.
2 = Weak alignment: practice assesses lower-order skills than the material promises.
3 = Partial alignment: most content aligns with the goals, but notable tangents or missing assessments remain.
4 = Strong alignment: goals, content, and practice clearly correspond, though implicit goals may require slight inference.
5 = Perfect constructive alignment: every section and practice task maps unambiguously to a stated learning outcome.

2. ACTIVATION OF PRIOR KNOWLEDGE

Definition: How effectively the material prepares the learner before introducing new concepts. According to Ausubel's Subsumption Theory, new knowledge must be anchored to existing cognitive schemas through analogies, prerequisite reviews, or recall of past experiences.

1 = No activation: introduces complex new material with no context, analogy, or prerequisite warning.
2 = Superficial activation: mentions a prerequisite without helping the learner recall or visualize it.
3 = Basic anchoring: uses a standard analogy or briefly reviews prior concepts.
4 = Strong activation: explicitly bridges existing knowledge to the new topic and explains the connection.
5 = Expert schema building: prompts recall of a specific mental model or experience and uses it as the foundation for the new concept.

3. PROBLEM-CENTEREDNESS

Definition: The extent to which the learning is anchored in authentic, real-world problems rather than abstract, isolated facts. Learners acquire skills more effectively when they are shown the whole task or problem they will eventually be able to solve.

1 = Pure abstraction: concepts are taught in a vacuum with no real-world use or context.
2 = Fact-centric: focuses mainly on definitions and isolated components; application is an afterthought.
3 = Applied examples: uses hypothetical or generic scenarios, but remains primarily topic-based.
4 = Task-oriented: explicitly frames the material around solving a realistic task or scenario.
5 = Deeply problem-centered: an authentic, complex real-world problem drives the entire lesson.

4. COGNITIVE LOAD MANAGEMENT

Definition: The material's ability to protect working memory through chunking,
signaling, clear sequencing, defined terminology, and removal of irrelevant detail.

1 = Cognitive overload: walls of text, disconnected diagrams, undefined jargon, or excessive tangents.
2 = High friction: poor structure forces the learner to hold too many unconnected pieces in mind.
3 = Adequate processing: reasonably formatted, with some structure but occasional density or minor tangents.
4 = Well-segmented: uses clear signaling and breaks concepts into digestible chunks.
5 = Optimized for working memory: exceptionally clean, sequenced, and signaled presentation with minimal extraneous load.

5. SCAFFOLDING AND FADING

Definition: The temporal progression of learner support. It measures how effectively the material transitions from expert demonstration (fully worked examples) to partial support (completion tasks/faded examples) to independent learner execution.

1 = No support progression: jumps from theory directly to complex independent problem solving.
2 = Static support: provides examples but has a drastic difficulty leap without transitional help.
3 = Basic scaffolding: progresses from simple examples to harder problems but lacks intermediate support.
4 = Clear fading: demonstrates a process fully, then provides hints or partial setups before independent work.
5 = Adaptive scaffolding architecture: smoothly moves from worked examples to faded examples and independent practice.

6. LEARNER ENGAGEMENT (ICAP)

Definition: What the learner is explicitly asked to do, ranging from passive
receiving to active, constructive, and interactive knowledge generation.

1 = Passive: only reading or watching, with no prompts for action.
2 = Active (minimal): pauses for reflection or simple right-or-wrong knowledge checks.
3 = Constructive (basic): asks the learner to summarize, fill gaps, or execute a standard procedure independently.
4 = Constructive (high): applies concepts to novel scenarios, creates original work, or justifies reasoning.
5 = Interactive/generative: modifies models, predicts outcomes before seeing solutions, or synthesizes concepts into a novel creation.

7. FORMATIVE FEEDBACK UTILITY

Definition: When a learner practices, what happens next? This evaluates the depth of the provided solutions or feedback mechanisms. Feedback must move beyond Task-level (right/wrong) to Process-level (how to fix it) and Self-regulatory-level (how to check your own work).

1 = No feedback: practice has no answers or solutions for verification.
2 = Task-level only: provides only the final correct answer.
3 = Process-level (basic): provides a worked solution that shows the correct path.
4 = Corrective: explains the solution and highlights common mistakes or misconceptions.
5 = Self-regulatory: explains the solution, addresses errors, and teaches a method for checking future work.

8. MOTIVATIONAL DESIGN (ARCS)

Definition:  The emotional and motivational engineering of the text. Evaluates how well the material captures Attention (novelty/curiosity), establishes Relevance (personal/career utility), builds Confidence (achievable milestones), and ensures Satisfaction (feeling of accomplishment).

1 = Demotivating: dry, intimidating, or lacking any attempt to build interest.
2 = Neutral: clear presentation without warmth or a reason for the learner to care.
3 = Intermittently engaging: occasional hooks or encouragement without sustained momentum.
4 = Strong motivational design: establishes relevance, uses a supportive tone, and builds confidence through achievable milestones.
5 = Highly inspiring: sustains curiosity, connects skills to learner goals, affirms progress, and ends with empowerment.
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

    "constructive_alignment": {{
      "score": 1,
      "justification": "..."
    }},

    "activation_of_prior_knowledge": {{
      "score": 1,
      "justification": "..."
    }},

    "problem_centeredness": {{
      "score": 1,
      "justification": "..."
    }},

    "cognitive_load_management": {{
      "score": 1,
      "justification": "..."
    }},

    "scaffolding_and_fading": {{
      "score": 1,
      "justification": "..."
    }},

    "learner_engagement": {{
      "score": 1,
      "justification": "..."
    }},

    "formative_feedback_utility": {{
      "score": 1,
      "justification": "..."
    }},

    "motivational_design": {{
      "score": 1,
      "justification": "..."
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