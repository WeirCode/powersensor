#include <iostream>
#include <vector>
#include <chrono>
#include <cmath>
#include <thread>

// Matrix multiplication for floating-point stress
void matrix_multiply(int size) {
    std::vector<std::vector<double>> A(size, std::vector<double>(size, 1.5));
    std::vector<std::vector<double>> B(size, std::vector<double>(size, 2.5));
    std::vector<std::vector<double>> C(size, std::vector<double>(size, 0.0));

    for (int i = 0; i < size; ++i)
        for (int k = 0; k < size; ++k)
            for (int j = 0; j < size; ++j)
                C[i][j] += A[i][k] * B[k][j];
}

// Prime number check for integer workload
bool is_prime(int n) {
    if (n <= 1) return false;
    if (n == 2) return true;
    if (n % 2 == 0) return false;
    for (int i = 3; i <= std::sqrt(n); i += 2)
        if (n % i == 0)
            return false;
    return true;
}

// Count number of primes in a range
int count_primes(int start, int end) {
    int count = 0;
    for (int i = start; i <= end; ++i)
        if (is_prime(i)) ++count;
    return count;
}

int main() {
    std::cout << "Starting test workload..." << std::endl;

    auto start_time = std::chrono::high_resolution_clock::now();

    // Loop to simulate periodic load
    for (int i = 0; i < 5; ++i) {
        std::cout << "Iteration " << i + 1 << ": Matrix multiplication..." << std::endl;
        matrix_multiply(600);  // Tune size for load
        
        std::cout << "Iteration " << i + 1 << ": Prime calculation..." << std::endl;
        int primes = count_primes(1000000, 1001000);
        std::cout << "Found " << primes << " primes." << std::endl;

        std::this_thread::sleep_for(std::chrono::milliseconds(500));  // Brief pause
    }

    auto end_time = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration<double>(end_time - start_time).count();

    std::cout << "Finished in " << duration << " seconds." << std::endl;
    return 0;
}

