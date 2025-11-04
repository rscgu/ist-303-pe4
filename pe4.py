import wikipedia
import time
import argparse
import os
import json
from concurrent.futures import ThreadPoolExecutor

def setup_arg_parser():
    """Sets up the command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="Download and save Wikipedia content sequentially or concurrently."
    )
    parser.add_argument(
        "-q", "--query",
        type=str,
        default="generative artificial intelligence",
        help="The search query for Wikipedia topics."
    )
    parser.add_argument(
        "-o", "--output_dir",
        type=str,
        default="wikipedia_references",
        help="The directory to save the output JSON file."
    )
    parser.add_argument(
        "-m", "--mode",
        type=str,
        choices=["sequential", "concurrent", "both"],
        default="both",
        help="Execution mode: 'sequential', 'concurrent', or 'both'."
    )
    parser.add_argument(
        "-w", "--max_workers",
        type=int,
        default=5,
        help="Maximum number of worker threads for concurrent execution."
    )
    return parser

def download_and_save_references(topic, output_dir):
    """
    Retrieves Wikipedia page, extracts title and references, and returns them.
    This function is designed to be used by both sequential and concurrent modes.
    """
    try:
        page = wikipedia.page(topic, auto_suggest=False)
        page_title = page.title
        references = page.references
        return {
            "topic": topic,
            "page_title": page_title,
            "references": references,
            "status": "success"
        }
    except wikipedia.exceptions.PageError:
        return {"topic": topic, "error": "PageError: Could not find page.", "status": "error"}
    except wikipedia.exceptions.DisambiguationError as e:
        return {"topic": topic, "error": f"DisambiguationError: Options are: {e.options}", "status": "error"}
    except Exception as e:
        return {"topic": topic, "error": f"An unexpected error occurred: {str(e)}", "status": "error"}

def run_sequential_download(topics, output_dir):
    """Runs the sequential download process."""
    print("--- Starting Section A: Sequentially download wikipedia content ---")
    start_time = time.perf_counter()
    all_results = []

    for topic in topics:
        result = download_and_save_references(topic, output_dir)
        all_results.append(result)
        if result["status"] == "success":
            print(f"Successfully processed: {result['topic']}")
        else:
            print(f"Failed to process {topic}: {result['error']}")

    end_time = time.perf_counter()
    print(f"Section A execution time: {end_time - start_time:.2f} seconds")
    print("--- Finished Section A ---")
    return all_results, end_time - start_time

def run_concurrent_download(topics, output_dir, max_workers):
    """Runs the concurrent download process."""
    print("\n--- Starting Section B: Concurrently download wikipedia content ---")
    start_time = time.perf_counter()
    all_results = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Map the download function to each topic
        # We need to pass output_dir to the function if it were to save files directly,
        # but here we collect results and save them once at the end.
        future_to_topic = {executor.submit(download_and_save_references, topic, output_dir): topic for topic in topics}
        
        for future in future_to_topic:
            try:
                result = future.result()
                all_results.append(result)
                if result["status"] == "success":
                    print(f"Successfully processed: {result['topic']}")
                else:
                    print(f"Failed to process {result['topic']}: {result['error']}")
            except Exception as exc:
                topic = future_to_topic[future]
                print(f'{topic} generated an exception: {exc}')
                all_results.append({"topic": topic, "error": str(exc), "status": "error"})

    end_time = time.perf_counter()
    print(f"Section B execution time: {end_time - start_time:.2f} seconds")
    print("--- Finished Section B ---")
    return all_results, end_time - start_time

def save_results_to_json(results, output_dir, filename="wikipedia_references.json"):
    """Saves the collected results to a JSON file."""
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, filename)
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=4, ensure_ascii=False)
        print(f"All results saved to {output_path}")
    except IOError as e:
        print(f"Error saving results to {output_path}: {e}")

def main():
    """Main function to orchestrate the download process."""
    parser = setup_arg_parser()
    args = parser.parse_args()

    print(f"Searching Wikipedia for topics related to: '{args.query}'")
    try:
        search_topics = wikipedia.search(args.query)
        if not search_topics:
            print("No topics found for the given query.")
            return
        print(f"Found {len(search_topics)} topics.")
    except Exception as e:
        print(f"Error during Wikipedia search: {e}")
        return

    all_downloaded_data = []
    sequential_time = 0
    concurrent_time = 0

    if args.mode in ["sequential", "both"]:
        sequential_data, sequential_time = run_sequential_download(search_topics, args.output_dir)
        all_downloaded_data.extend(sequential_data)

    if args.mode in ["concurrent", "both"]:
        concurrent_data, concurrent_time = run_concurrent_download(search_topics, args.output_dir, args.max_workers)
        # In 'both' mode, we might want to avoid duplicate entries if the same topics are processed.
        # For simplicity here, we'll just append, but a more robust solution might merge or deduplicate.
        all_downloaded_data.extend(concurrent_data)

    # Save all collected data to a single JSON file
    save_results_to_json(all_downloaded_data, args.output_dir)

    print("\n--- Summary ---")
    print(f"Total execution time (Sequential): {sequential_time:.2f} seconds")
    print(f"Total execution time (Concurrent): {concurrent_time:.2f} seconds")
    print("----------------")

if __name__ == "__main__":
    main()