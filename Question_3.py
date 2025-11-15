import threading
import time

# Constants for better readability
NUMBER_OF_TEST_ROUNDS = 10  # How many times to repeat the experiment
FACTORIAL_NUMBERS = [50, 100, 200]  # The factorial values to calculate


# QUESTION 3.2: Factorial Function with Big-O Analysis
def calculate_factorial(n):
    # Calculate factorial: n! = n × (n-1) × (n-2) × ... × 2 × 1
    # Example: 5! = 5 × 4 × 3 × 2 × 1 = 120

    result = 1  # Start with 1 (identity for multiplication)

    # Multiply all numbers from 1 to n
    for i in range(1, n + 1):
        result *= i

    return result


# QUESTION 3.3: Multithreading Implementation
class FactorialThread(threading.Thread):
    # Custom thread class for calculating factorials

    def __init__(self, n, thread_name):
        # Initialize the thread
        threading.Thread.__init__(self)
        self.n = n  # The number to calculate factorial for
        self.thread_name = thread_name
        self.result = None  # Will store the factorial result
        self.start_time = None  # When this thread started
        self.end_time = None  # When this thread finished

    def run(self):
        # This method executes when thread.start() is called

        # Record start time in nanoseconds
        self.start_time = time.perf_counter_ns()

        # Perform the calculation
        self.result = calculate_factorial(self.n)

        # Record end time in nanoseconds
        self.end_time = time.perf_counter_ns()


def multithreading_test(rounds=NUMBER_OF_TEST_ROUNDS):
    # Test factorial calculation using multithreading (Question 3.3)

    print("\n" + "=" * 70)
    print("MULTITHREADING TEST")
    print("=" * 70)
    print("Calculating: 50!, 100!, and 200! using separate threads")
    print("=" * 70)

    numbers = FACTORIAL_NUMBERS
    all_times = []  # Store time for each round

    # Run the experiment multiple times
    for round_num in range(1, rounds + 1):
        # Step 1: Create one thread for each factorial calculation
        threads = []
        for num in numbers:
            thread = FactorialThread(num, f"Thread-{num}")
            threads.append(thread)

        # Step 2: Record when we start ALL threads
        overall_start = time.perf_counter_ns()

        # Step 3: Start all threads simultaneously
        for thread in threads:
            thread.start()  # Each thread begins running

        # Step 4: Wait for ALL threads to complete
        for thread in threads:
            thread.join()  # Block until this thread finishes

        # Step 5: Record when ALL threads are done
        overall_end = time.perf_counter_ns()

        # Step 6: Calculate total time for this round
        total_time = overall_end - overall_start
        all_times.append(total_time)

        # Display results for this round
        print(f"\nRound {round_num}:")
        print(f"  Total Time: {total_time:,} nanoseconds ({total_time / 1_000_000:.4f} ms)")

        # Show individual thread times
        for i, thread in enumerate(threads):
            thread_time = thread.end_time - thread.start_time
            print(f"  Thread {numbers[i]}!: {thread_time:,} nanoseconds")

    # Calculate and display average across all rounds
    average_time = sum(all_times) / len(all_times)

    print("\n" + "=" * 70)
    print("MULTITHREADING SUMMARY")
    print("=" * 70)
    print(f"Total Rounds: {rounds}")
    print(f"Average Time: {average_time:,.2f} nanoseconds ({average_time / 1_000_000:.4f} ms)")
    print("=" * 70)

    return all_times, average_time


# QUESTION 3.4: Sequential Execution (Without Multithreading)
def sequential_test(rounds=NUMBER_OF_TEST_ROUNDS):
    # Test factorial calculation WITHOUT multithreading (Question 3.4)

    print("\n" + "=" * 70)
    print("SEQUENTIAL TEST (No Multithreading)")
    print("=" * 70)
    print("Calculating: 50!, 100!, and 200! sequentially")
    print("=" * 70)

    numbers = FACTORIAL_NUMBERS
    all_times = []

    # Run the experiment multiple times
    for round_num in range(1, rounds + 1):
        # Record start time
        start_time = time.perf_counter_ns()

        # Calculate factorials one after another (not simultaneously)
        results = []
        individual_times = []

        for num in numbers:
            # Time each individual calculation
            individual_start = time.perf_counter_ns()
            result = calculate_factorial(num)
            individual_end = time.perf_counter_ns()

            results.append(result)
            individual_times.append(individual_end - individual_start)

        # Record end time
        end_time = time.perf_counter_ns()

        # Calculate total time for this round
        total_time = end_time - start_time
        all_times.append(total_time)

        # Display results for this round
        print(f"\nRound {round_num}:")
        print(f"  Total Time: {total_time:,} nanoseconds ({total_time / 1_000_000:.4f} ms)")

        for i, num in enumerate(numbers):
            print(f"  Factorial {num}!: {individual_times[i]:,} nanoseconds")

    # Calculate and display average
    average_time = sum(all_times) / len(all_times)

    print("\n" + "=" * 70)
    print("SEQUENTIAL SUMMARY")
    print("=" * 70)
    print(f"Total Rounds: {rounds}")
    print(f"Average Time: {average_time:,.2f} nanoseconds ({average_time / 1_000_000:.4f} ms)")
    print("=" * 70)

    return all_times, average_time


# QUESTION 3.5: Performance Comparison and Analysis
def compare_performance():
    # Compare multithreading vs sequential performance

    rounds = NUMBER_OF_TEST_ROUNDS

    # Run both experiments
    multi_times, multi_avg = multithreading_test(rounds)
    seq_times, seq_avg = sequential_test(rounds)

    # Display comparison
    print("\n" + "=" * 70)
    print("PERFORMANCE COMPARISON")
    print("=" * 70)
    print(f"Multithreading Average:  {multi_avg:,.2f} ns ({multi_avg / 1_000_000:.4f} ms)")
    print(f"Sequential Average:      {seq_avg:,.2f} ns ({seq_avg / 1_000_000:.4f} ms)")
    print("-" * 70)

    # Determine which is faster
    if multi_avg < seq_avg:
        # Multithreading won
        speedup = seq_avg / multi_avg
        time_saved = seq_avg - multi_avg
        print(f"✓ Multithreading is FASTER by {speedup:.2f}x")
        print(f"  Time saved: {time_saved:,.2f} ns ({time_saved / 1_000_000:.4f} ms)")
    elif multi_avg > seq_avg:
        # Sequential won
        slowdown = multi_avg / seq_avg
        time_lost = multi_avg - seq_avg
        print(f"✗ Sequential is FASTER by {slowdown:.2f}x")
        print(f"  Time lost with multithreading: {time_lost:,.2f} ns ({time_lost / 1_000_000:.4f} ms)")
        print("\nWhy? Python's Global Interpreter Lock (GIL) prevents true parallel")
        print("execution for CPU-bound tasks like factorial calculation.")
    else:
        print("→ Both methods have similar performance")

    print("=" * 70)


# Main execution
if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("QUESTION 3: CONCURRENT PROCESSING")
    print("=" * 70)

    # Run performance comparison
    compare_performance()

    print("\n✓ Program completed!")