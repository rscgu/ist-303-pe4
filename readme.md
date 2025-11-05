# Pair Exercise #4: Wikipedia Content Downloader

## Team members: Rachan and Yashas

This exercise involves writing a Python script to download and save Wikipedia content, both sequentially and concurrently. The script has been enhanced with command-line arguments for flexibility and outputs results into a single JSON file.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd ist-303-pe4
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install required Python packages:**
    ```bash
    pip install wikipedia
    ```

## Running the Script

The script `pe4.py` can be executed with various options using command-line arguments.

**Basic Execution (defaults):**
This will search for "generative artificial intelligence", run both sequential and concurrent downloads, and save results to a `wikipedia_references` directory.
```bash
python3 pe4.py
```

**Customizing Execution:**

*   **Specify Search Query:**
    ```bash
    python3 pe4.py --query "artificial intelligence applications"
    ```

*   **Specify Output Directory:**
    ```bash
    python3 pe4.py --output_dir my_ai_references
    ```

*   **Choose Execution Mode:**
    *   Run only sequential:
        ```bash
        python3 pe4.py --mode sequential
        ```
    *   Run only concurrent:
        ```bash
        python3 pe4.py --mode concurrent
        ```

*   **Adjust Concurrency:**
    ```bash
    python3 pe4.py --max_workers 10
    ```

*   **Combine Options:**
    ```bash
    python3 pe4.py --query "machine learning" --output_dir ml_data --mode concurrent --max_workers 8
    ```

## Output

The script will perform the specified download tasks and save all collected data (topic, page title, references, status, and errors) into a single JSON file named `wikipedia_references.json` within the specified output directory (defaults to `wikipedia_references`).

**JSON Output Structure Example:**
```json
[
    {
        "topic": "Generative artificial intelligence",
        "page_title": "Generative artificial intelligence",
        "references": [
            "https://example.com/ref1",
            "https://example.com/ref2"
        ],
        "status": "success"
    },
    {
        "topic": "Non-existent Topic",
        "error": "PageError: Could not find page.",
        "status": "error"
    }
]
```

## Notes

*   The script uses the `wikipedia` Python package. Ensure it is installed.
*   Error handling for `PageError`, `DisambiguationError`, and general exceptions is included.
*   The `auto_suggest=False` parameter is used when fetching Wikipedia pages.
*   For concurrent execution, the `max_workers` argument controls the number of threads used.