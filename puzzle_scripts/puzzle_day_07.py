# Processing input
def process_input():
    input_file = open("inputs/input_day_07.txt", "r")
    bridges = []
    for line in input_file:
        line = line.replace("\n", "")
        bridge_test_value = int(line.split(":")[0])
        bridge_numbers = line.split(":")[1].split()
        bridge_numbers = [int(num) for num in bridge_numbers]
        bridge = (bridge_test_value, bridge_numbers)
        bridges.append(bridge)
    input_file.close()
    return bridges

# Get sum of all test values where the bridge was completable with operations
def get_total_calibration_results(bridges, binary=True):
    total_sum = 0
    for bridge in bridges:
        if can_be_completed_with_operators(bridge[0], bridge[1], binary):
            total_sum += bridge[0]
    return total_sum

# Tests for a bridge of numbers if it can be completed with operations to match the test_value
def can_be_completed_with_operators(test_value, numbers, binary=True):
    num_operators = len(numbers) - 1
    num_combinations = 2**num_operators
    if not binary:
        num_combinations = 3 ** num_operators
    current_comb = [0 for i in range(num_operators)]
    if test_operation_combination(test_value, numbers, current_comb):
        return True
    for i in range(num_combinations):
        for x in range(num_operators-1, -1, -1):
            if binary:
                if current_comb[x] == 0:
                    current_comb[x] = 1
                    break
                else:
                    current_comb[x] = 0
            else:
                if current_comb[x] == 0 or current_comb[x] == 1:
                    current_comb[x] += 1
                    break
                else:
                    current_comb[x] = 0
        if test_operation_combination(test_value, numbers, current_comb, binary):
            return True
    return False

# Tests a combination of operations
def test_operation_combination(test_value, numbers, combination, binary=True):
    operational_result = numbers[0]
    for i in range(1, len(numbers)):
        if combination[i-1] == 0:
            operational_result += numbers[i]
        elif combination[i-1] == 1:
            operational_result *= numbers[i]
        elif not binary and combination[i-1] == 2:
            operational_result = concatenate_numbers(operational_result, numbers[i])
        else:
            raise ValueError("Invalid combination.")
        if operational_result > test_value:
            return False
    if operational_result == test_value:
        return True
    return False

# Concatenate two numbers without using strings
def concatenate_numbers(a, b):
    digits = len(str(b))
    return a * (10 ** digits) + b

total_bridges = process_input()
calibration_results = get_total_calibration_results(total_bridges)
print("Result for Part A:", calibration_results)

calibration_results = get_total_calibration_results(total_bridges, binary=False)
print("Result for Part B:", calibration_results)