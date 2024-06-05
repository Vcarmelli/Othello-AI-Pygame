import threading
import time

def task(name, delay):
    print(f'Thread {name} starting')
    time.sleep(delay)
    print(f'Thread {name} finished after {delay} seconds')

if __name__ == "__main__":
    # List of tasks with thread names and delays
    tasks = [
        ("A", 2),
        ("B", 3),
        ("C", 1),
        ("D", 4),
    ]
    
    threads = []
    
    # Create and start threads
    for name, delay in tasks:
        thread = threading.Thread(target=task, args=(name, delay))
        thread.start()
        threads.append(thread)
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    print('All threads have finished')
