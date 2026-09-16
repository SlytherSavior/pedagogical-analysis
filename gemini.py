
import json
import os
from pathlib import Path

from google import genai
from google.genai import types
from dotenv import load_dotenv

from prompt import SYSTEM_PROMPT, build_prompt




MODEL = "gemini-3.6-flash"

INPUT_FILE = Path("content_analysis2.json")
OUTPUT_FILE = Path("llm_analysis4.json")

load_dotenv(Path(__file__).with_name(".env"))


def load_article(path):

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)



def validate_analysis(result):

    required_criteria = [
        "constructive_alignment",
        "activation_of_prior_knowledge",
        "problem_centeredness",
        "cognitive_load_management",
        "scaffolding_and_fading",
        "learner_engagement",
        "formative_feedback_utility",
        "motivational_design"
    ]

    if "article_id" not in result:
        raise ValueError("Missing article_id")

    if "pedagogical_analysis" not in result:
        raise ValueError("Missing pedagogical_analysis")

    analysis = result["pedagogical_analysis"]

    for criterion in required_criteria:

        if criterion not in analysis:
            raise ValueError(
                f"Missing criterion: {criterion}"
            )

        criterion_data = analysis[criterion]

        if "score" not in criterion_data:
            raise ValueError(
                f"Missing score for {criterion}"
            )

        score = criterion_data["score"]

        if not isinstance(score, int):
            raise ValueError(
                f"Score for {criterion} must be an integer"
            )

        if not 1 <= score <= 5:
            raise ValueError(
                f"Score for {criterion} must be between 1 and 5"
            )

        if "justification" not in criterion_data:
            raise ValueError(
                f"Missing justification for {criterion}"
            )

        

    return True


def save_analysis(result, path):

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(path, "w", encoding="utf-8") as file:

        json.dump(
            result,
            file,
            indent=2,
            ensure_ascii=False
        )



def evaluate_article(article):
    api_key = os.getenv("EX_API_KEY")
    if not api_key:
        raise RuntimeError("EX_API_KEY is not set in the environment or .env file")

    client = genai.Client(api_key=api_key)

    prompt = build_prompt(article)

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            response_mime_type="application/json",
        )
    )

    raw_output = response.text

    try:
        result = json.loads(raw_output)

    except json.JSONDecodeError:

        print("LLM returned invalid JSON:")
        print(raw_output)

        raise ValueError(
            "Could not parse LLM response as JSON."
        )

    validate_analysis(result)

    return result



def main():


    article = load_article(INPUT_FILE)
    print(f"Loaded article from {INPUT_FILE}")

    print("Evaluating article with LLM...")
    result = evaluate_article(article)

    print("LLM analysis completed.")

    save_analysis(
        result,
        OUTPUT_FILE
    )

    print(
        f"Analysis saved to: {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()