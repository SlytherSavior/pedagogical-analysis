import json
#let's try to analyze what the inital json extracted from the scraper looks like and count the number of examples, images, equations ... anything imp for pedagogical analysis purposes .. :)

def count_items(filename="categorical_analysis2.json"):
    save_file_name = "content_analysis2.json"
    paragraph = 0 
    equations = 0 
    images = 0 
    examples = 0
    example_content = 0
    solution_content = 0

    with open(filename, "r", encoding="utf-8") as file1:
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
    with open(save_file_name, "w", encoding="utf-8") as file:
        json.dump(final_output, file, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    count_items()
