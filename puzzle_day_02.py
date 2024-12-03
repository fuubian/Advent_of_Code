# Processing input
def process_input():
    input_file = open("inputs/input_day_02.txt", "r")
    levels = []
    current_line = input_file.readline()
    while current_line:
        numbers = current_line.split()
        numbers = [int(n) for n in numbers]
        levels.append(numbers)
        current_line = input_file.readline()
    input_file.close()
    return levels

def check_safe_level(level):
    increasing = level[0] < level[1]
    for i in range(0, len(level)-1):
        if level[i] < level[i+1] and not increasing:
            return False
        elif level[i] > level[i + 1] and increasing:
            return False

        diff = abs(level[i] - level[i+1])
        if diff > 3 or diff == 0:
            return False

    return True

# Problem A
def get_number_of_safe_levels(levels):
    counter = 0
    for i_level in levels:
        if check_safe_level(i_level):
            counter += 1
    return counter

# Problem B
def get_number_of_safe_levels_tolerance(levels):
    counter = 0
    for i_level in levels:
        if check_safe_level(i_level):
            counter += 1
        else:
            for i in range(0, len(i_level)):
                new_list = i_level[:i] + i_level[i+1:]
                if check_safe_level(new_list):
                    counter += 1
                    break
    return counter

input = process_input()
result1 = get_number_of_safe_levels(input)
result2 = get_number_of_safe_levels_tolerance(input)
print("Result Part A:", result1)
print("Result Part B:", result2)