# Pedagogical Analysis

This repository extracts instructional content from calculus pages and evaluates
the resulting material against a pedagogical rubric.

## Repository layout

```text
src/
	scraper.py       Fetch and parse an article into structured JSON.
	extract.py       Count content types and write a processed analysis.
	prompt.py        Define the Gemini system prompt and rubric.
	gemini.py        Evaluate processed content with Gemini.
scripts/
	test_scraper.py  Small exploratory scraper test.
data/
	raw/             Scraped article JSON and raw extraction fixtures.
	processed/       Content-count and structure analyses.
	results/         LLM-generated pedagogical analyses.
notebooks/
	pedagogy.ipynb   Workspace for exploratory analysis.
```

## Articles

- Tangent Lines and Rates of Change: <https://tutorial.math.lamar.edu/Classes/CalcI/Tangents_Rates.aspx>
- Taylor Series: <https://tutorial.math.lamar.edu/Classes/CalcII/TaylorSeries.aspx>

## Setup

Install the Python dependencies used by the scripts:

```bash
pip install requests beautifulsoup4 playwright google-genai python-dotenv
playwright install chromium
```

Create a `.env` file in the repository root with the Gemini API key expected by
`src/gemini.py`:

```text
EX_API_KEY=your-api-key
```

## Workflow

Run commands from the repository root:

```bash
python src/scraper.py
python src/extract.py
python src/gemini.py
```

The scripts use repository-relative paths internally, so they can also be
launched from another working directory. The default flow reads
`data/raw/categorical_analysis2.json`, writes
`data/processed/content_analysis2.json`, and saves the latest model response to
`data/results/llm_analysis4.json`.

## Data notes

The JSON files in `data/` are generated artifacts and historical snapshots. The
scraper targets the Taylor Series page by default; edit `URL` in
`src/scraper.py` to collect a different page. The LLM script requires
`EX_API_KEY` and sends the processed article content to Gemini for scoring on
eight criteria from 1 to 5.
