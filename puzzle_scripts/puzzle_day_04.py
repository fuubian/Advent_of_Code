# Processing input
def process_input():
    input_file = open("inputs/input_day_04.txt", "r")
    data = []
    for line in input_file:
        line = line.replace("\n", "")
        data.append(line)
    input_file.close()
    return data

# Check if word in data is target word
def check_word(data, row, col, dr, dc, target, range_value):
    try:
        if all(row + i * dr >= 0 for i in range(range_value)) and all(col + i * dc >= 0 for i in range(range_value)):
            return all(data[row + i * dr][col + i * dc] == target[i] for i in range(range_value))
        return False
    except IndexError:
        return False

# Problem A
def find_word_xmax(data):
    word_counter = 0
    range_value = 4
    target_words = ["XMAS", "SAMX"]
    directions = [
        (1, 0), # Vertical
        (0, 1), # Horizontal
        (1, 1), # Diagonal
        (1, -1) # Diagonal 2
    ]

    for row in range(len(data)):
        for col in range(len(data[row])):
            for dr, dc in directions:
                for word in target_words:
                    if check_word(data, row, col, dr, dc, word, range_value):
                        word_counter += 1

    return word_counter

# Problem B
def find_cross_mas(data):
    word_counter = 0
    range_value = 3
    target_words = ["MAS", "SAM"]

    for row in range(len(data)):
        for col in range(len(data[row])):
            if (check_word(data, row, col, 1, 1, target_words[0], range_value) or check_word(data, row, col, 1, 1, target_words[1], range_value)) \
                and (check_word(data, row, col+2, 1, -1, target_words[0], range_value) or check_word(data, row, col+2, 1, -1, target_words[1], range_value)):
                word_counter += 1

    return word_counter

input_data = process_input()
result1 = find_word_xmax(input_data)
result2 = find_cross_mas(input_data)

print("Result Part A:", result1)
print("Result Part B:", result2)