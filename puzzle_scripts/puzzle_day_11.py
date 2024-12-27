from collections import defaultdict

# Processing input and returning a dictionary that tracks the occurrences for each stone type
def process_input():
    input_file = open("inputs/input_day_11.txt", "r")
    stone_dict = defaultdict(int)
    stone_dict[1] = 0
    stones = input_file.read().split()
    for s in stones:
            stone_dict[int(s)] += 1
    return stone_dict

# Processing a blink, following the given rules, and updating the dictionary
def process_tick(stone_dict):
    # Store changes in di
    changes = defaultdict(int)
    for stone in stone_dict:
        stone_number = stone_dict[stone]
        changes[stone] -= stone_number
        if stone_number >= 1:
            if stone == 0:
                changes[1] += stone_number
            else:
                # Check number of digits
                string_stone = str(stone)
                number_digits = len(string_stone)

                # Check for even digit number
                if number_digits % 2 == 0:
                    half_length = number_digits // 2
                    first_stone_half = int(string_stone[:half_length])
                    second_stone_half = int(string_stone[half_length:])

                    changes[first_stone_half] += stone_number
                    changes[second_stone_half] += stone_number
                else:
                    # Multiplying with 2024
                    new_stone = stone*2024
                    changes[new_stone] += stone_number

    for key, value in changes.items():
        stone_dict[key] += value


# Process n ticks and return the resulting number of stones
def process_n_ticks(tick_number, stone_dict):
    for i in range(tick_number):
        process_tick(stone_dict)

    return sum(stone_dict.values())

input_stone_dict = process_input()
result1 = process_n_ticks(25, input_stone_dict)
print("Result for Part A:", result1)

result2 = process_n_ticks(50, input_stone_dict)
print("Result for Part B:", result2)