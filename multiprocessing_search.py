import concurrent.futures
import time


def search_in_file_multiprocess(file, keywords):
    results = {kw: [] for kw in keywords}
    try:
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()
            for keyword in keywords:
                if keyword in content:
                    results[keyword].append(file)
    except Exception as e:
        print(f"Error reading {file}: {e}")
    return results


def multi_process_search(files, keywords):
    start_time = time.time()
    combined_results = {kw: [] for kw in keywords}

    # Використовуємо ProcessPoolExecutor для розподілу файлів між процесами
    with concurrent.futures.ProcessPoolExecutor() as executor:
        future_to_file = {
            executor.submit(search_in_file_multiprocess, file, keywords): file
            for file in files
        }
        for future in concurrent.futures.as_completed(future_to_file):
            result = future.result()
            for key, value in result.items():
                combined_results[key].extend(value)

    end_time = time.time()
    execution_time = end_time - start_time
    return combined_results, execution_time
