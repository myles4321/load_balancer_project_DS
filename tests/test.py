import requests
import concurrent.futures
from collections import Counter
import time

def send_request(session, url, params):
    try:
        response = session.get(url, params=params)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

def load_test(num_requests, num_workers):
    url = 'http://localhost:5000/home'
    results = []
    with requests.Session() as session:
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
            futures = [executor.submit(send_request, session, url, {'id': i}) for i in range(num_requests)]
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                results.append(result)  # Append all results, even None
    return results

if __name__ == '__main__':
    print("Starting load test...")
    num_requests = 10000
    num_workers = 50
    
    start_time = time.time()  # Start the timer
    
    results = load_test(num_requests, num_workers)
    
    end_time = time.time()  # Stop the timer
    elapsed_time = end_time - start_time  # Calculate elapsed time
    
    print(f"Load test completed. Received {len(results)} results.")
    print(f"Total time taken: {elapsed_time:.2f} seconds")
    
    # Print results
    for i, result in enumerate(results):
        if result:
            print(f"Response {i+1}: {result}")
        else:
            print(f"Response {i+1}: No response received")
    
    # Count requests per server
    server_counts = Counter(result['message'].split(': ')[1] for result in results if result)

    print("\nRequests per server:")
    for server, count in server_counts.items():
        print(f"{server}: {count} requests")
    
    print(f"\nTotal successful requests: {sum(1 for r in results if r is not None)}")
    print(f"Total failed requests: {sum(1 for r in results if r is None)}")
    print(f"Average time per request: {(elapsed_time / num_requests):.4f} seconds")