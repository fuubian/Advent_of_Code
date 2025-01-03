import regex as re
from math import gcd

# Processing input
def process_input():
    input_file = open("inputs/input_day_13.txt", "r")
    machines = []
    button_regex = r"X\+(\d+), Y\+(\d+)"
    price_regex = r"X=(\d+), Y=(\d+)"
    while True:
        button_a_line = input_file.readline()
        if button_a_line:
            if button_a_line == "\n":
                continue
            button_b_line = input_file.readline()
            price_line = input_file.readline()

            button_a_match = re.findall(button_regex, button_a_line)[0]
            button_b_match = re.findall(button_regex, button_b_line)[0]
            price_match = re.findall(price_regex, price_line)[0]

            button_a = (int(button_a_match[0]), int(button_a_match[1]))
            button_b = (int(button_b_match[0]), int(button_b_match[1]))
            price = (int(price_match[0]), int(price_match[1]))

            machines.append([button_a, button_b, price])
        else:
            break

    return machines

# Extended Euclidean algorithm
def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return g, x, y

# Find the lowest token number for one machine
def find_lowest_token_number(machine):
    # I solved it for one equation on paper and transformed it into general code here
    # Sorry for the variable mess, I'm not able to eloquently explain my calculations
    A_X, A_Y = machine[0]
    B_X, B_Y = machine[1]
    X, Y = machine[2]

    multi1_A_X, multi1_B_X, multi1_X = A_X * A_Y, B_X * A_Y, X * A_Y
    multi2_A_Y, multi2_B_Y, multi2_Y = A_Y * A_X, B_Y * A_X, Y * A_X
    sub_B, sub_XY = multi1_B_X - multi2_B_Y, multi1_X - multi2_Y

    # Check if number of button B pressed is a natural number
    B_number = sub_XY / sub_B
    if B_number % 1 != 0:
        return 0

    # Check if number of button A pressed is a natural number
    A_number = (X - B_X * B_number) / A_X
    if A_number % 1 != 0:
        return 0

    # Return number of tokens
    return int(A_number * 3 + B_number * 1)


# Find the lowest token number for a complete list of machines
def find_lowest_token_number_overall(machine_list):
    token_number = 0
    for machine in machine_list:
        token_number += find_lowest_token_number(machine)
    return token_number

# Modify machine list by adding 10000000000000 to the price coordinates
def modify_price_numbers(machine_list):
    modified_machine_list = []
    for machine in machine_list:
        modified_machine = [machine[0], machine[1], (machine[2][0] + 10000000000000, machine[2][1] + 10000000000000)]
        modified_machine_list.append(modified_machine)

    return modified_machine_list

input_machines = process_input()
result1 = find_lowest_token_number_overall(input_machines)
print("Result for Part A:", result1)

modified_machines = modify_price_numbers(input_machines)
result2 = find_lowest_token_number_overall(modified_machines)
print("Result for Part B:", result2)