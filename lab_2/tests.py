import json
import logging
import os

from math import erfc, fabs, pow, sqrt

logging.basicConfig(level=logging.INFO)

SEQUENCE_LENGTH = 128
BLOCK_SIZE = 6


def frequency_test(bitstring:str) -> float:
    """
    Calculates the p-value of the frequency (monobit) test for a given bit sequence.

    This test evaluates whether the number of ones and zeros in the sequence is approximately equal,
    indicating uniform distribution.

    Parameters:
    bitstring (str): The binary sequence to be tested.
    """
    try:
        N = len(bitstring)
        sum_values = fabs(sum(1 if bit == '1' else -1 for bit in bitstring))
        p_value = erfc((sum_values) / sqrt(2*N))
        return p_value
    except Exception as ex:
        logging.error(f"Error occurred during the test execution: {ex}\n")



def runs_test(sequence):
    """
    Performs the runs test for the given binary sequence.

    This test checks for the presence of runs in the sequence, where a run is defined as consecutive
    bits of the same value.

    Parameters:
    sequence (str): The binary sequence to be tested.

    Returns:
    float: The p-value indicating the randomness of the runs in the sequence.
    """
    try:
        n = len(sequence)
        runs = [sequence[0]]
        for bit in sequence:
            if bit != runs[-1]:
                runs.append(bit)
        k = len(runs)
        pi = sequence.count('1') / n
        tau = 2 / (pi * (1 - pi)) ** 0.5
        vobs = sum([1 for i in range(1, k - 1) if runs[i - 1] != runs[i + 1]]) + 1
        p_value = erfc(abs(vobs - 2 * n * pi * (1 - pi)) / (2 * pi * (1 - pi) * (2 * n) ** 0.5))
        return p_value
    except Exception as ex:
        logging.error(f"Error occurred during the test execution: {ex}\n")


def longest_run_test(sequence):
    """
    Longest Run Test: This test identifies the longest run of ones in the sequence.

    Parameters:
    sequence (str): The binary sequence to be tested.

    Returns:
    float: The p-value for the longest run test.
    """
    try:
        blocks = [sequence[i:i+BLOCK_SIZE] for i in range(0, len(sequence), BLOCK_SIZE)]
        lengths = [block.count('1') for block in blocks]
        m = max(lengths)
        n = len(sequence)
        nu = (n - BLOCK_SIZE + 3) / 2 ** BLOCK_SIZE
        sigma = (16 * 105 + 16 * 2 ** 4) / 2 ** 9
        p_value = erfc(abs(m - nu) / (2 ** 0.5 * sigma))
        return p_value
    except Exception as ex:
        logging.error(f"Error occurred during the test execution: {ex}\n")



def read_sequence_from_file(file_name):

    with open(file_name, 'r') as file:
        sequence = file.read().strip()
    return sequence

def save_results(results, output_path):
    with open(output_path, "w") as results_file:
        json.dump(results, results_file, indent=4)


if __name__ == "__main__":
    try:
        with open(os.path.join("lab_2", "settings.json"), "r") as paths_file:
            paths = json.load(paths_file)
        
        cpp_sequence = read_sequence_from_file(paths["cpp_path"])
        java_sequence = read_sequence_from_file(paths["java_path"])

        p_value_frequency_cpp = frequency_test(cpp_sequence)
        p_value_runs_cpp = runs_test(cpp_sequence)
        p_value_longest_run_cpp = longest_run_test(cpp_sequence)

        p_value_frequency_java = frequency_test(java_sequence)
        p_value_runs_java = runs_test(java_sequence)
        p_value_longest_run_java = longest_run_test(java_sequence)

        results = {
            "cpp": {
                "frequency_test": p_value_frequency_cpp,
                "runs_test": p_value_runs_cpp,
                "longest_run_test": p_value_longest_run_cpp
            },
            "java": {
                "frequency_test": p_value_frequency_java,
                "runs_test": p_value_runs_java,
                "longest_run_test": p_value_longest_run_java
            }
        }
        save_results(results, paths["output_path"])
    
    except FileNotFoundError as e:
        logging.error(f"File not found: {e.filename}")
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON: {e}")
    except KeyError as e:
        logging.error(f"KeyError: {e}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")