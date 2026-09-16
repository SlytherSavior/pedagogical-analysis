import json
from pathlib import Path
#let's try to analyze what the inital json extracted from the scraper looks like and count the number of examples, images, equations ... anything imp for pedagogical analysis purposes .. :)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "data" / "raw" / "categorical_analysis2.json"
DEFAULT_OUTPUT = ROOT / "data" / "processed" / "content_analysis2.json"


def count_items(filename=DEFAULT_INPUT, save_file_name=DEFAULT_OUTPUT):
    paragraph = 0 
    equations = 0 
    images = 0 
    examples = 0
    example_content = 0
    solution_content = 0

    input_path = Path(filename)
    output_path = Path(save_file_name)
    if not input_path.is_absolute():
        input_path = ROOT / input_path
    if not output_path.is_absolute():
        output_path = ROOT / output_path

    with open(input_path, "r", encoding="utf-8") as file1:
        data = json.load(file1)

    items = data.get("content", [])
    for dictonaries in items: 
        block_type = dictonaries.get("type", "")
        if block_type == "paragraph":
            paragraph += 1
        elif block_type == "equations":
            equations += 1
        elif block_type == "image":
            images += 1
        elif block_type == "example":
            examples += 1
        elif block_type == "example-content":
            example_content += 1
        elif block_type == "solution":
            solution_content += 1

    analysis = {
        "paragraphs": paragraph,
        "equations": equations,
        "images": images,
        "examples": examples,
        "example_content": example_content,
        "solution_content": solution_content
    }

    final_output = data.copy()
    final_output["structure"] = analysis

    # Save the original contents together with the analysis.
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(final_output, file, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    count_items()
