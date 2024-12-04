import re

# Processing input
def process_input():
    input_file = open("inputs/input_day_03.txt", "r")
    data = input_file.read()
    input_file.close()
    return data.replace("\n", "")

# Problem Part A
def get_sum_of_mul_operations(data):
    mul_regex = r"mul\(\d{1,3},\d{1,3}\)"
    mul_operations = re.findall(mul_regex, data)
    sum = 0
    for operation in mul_operations:
        value_regex = r"\d{1,3}"
        values = re.findall(value_regex, operation)
        if len(values) == 2:
            sum += int(values[0]) * int(values[1])
        else:
            raise ValueError(f"Unexpected result. {operation} -> {values}")
    return sum

# Problem Part B
def get_sum_with_activations(data):
    activation_regex = r"do\(\).*?(?:don't\(\)|$)"
    activation_regex_beginning = r"/^.*?(?:don't\(\)|do\(\))"

    activated_beginning = re.findall(activation_regex_beginning, data)
    activated_parts = re.findall(activation_regex, data)
    total_sum = 0

    if activated_beginning and len(activated_beginning) == 1:
        total_sum += get_sum_of_mul_operations(activated_beginning[0])
    elif len(activated_beginning) > 1:
        raise ValueError(f"Unexpected regex result. {activated_beginning}")

    for part in activated_parts:
        total_sum += get_sum_of_mul_operations(part)
    return total_sum

input_data = process_input()
result1 = get_sum_of_mul_operations(input_data)
result2 = get_sum_with_activations(input_data)
print("Result Part A:", result1)
print("Result Part B:", result2)