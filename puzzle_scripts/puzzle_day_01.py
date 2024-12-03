# Processing input
def process_input():
    input_file = open("inputs/input_day_01.txt", "r")
    list1 = []
    list2 = []
    current_line = input_file.readline()
    while current_line:
        numbers = current_line.replace("\n", "").split()
        list1.append(int(numbers[0]))
        list2.append(int(numbers[1]))
        current_line = input_file.readline()
    input_file.close()
    return list1, list2

# Problem Part A
def calculate_difference(list1, list2):
    list_len = len(list1)
    total_diff = 0
    for i in range(list_len):
        smallest_left = list1[0]
        smallest_right = list2[0]
        index1 = 0
        index2 = 0

        for j in range(1, len(list2)):
            if list1[j] < smallest_left:
                smallest_left = list1[j]
                left_index = j
            if list2[j] < smallest_right:
                smallest_right = list2[j]
                right_index = j

        total_diff += abs(smallest_right - smallest_left)
        list1.pop(index1)
        list2.pop(index2)
    return total_diff

# Problem Part B
def calculate_similarity(list1, list2):
    similarity = 0
    for i in range(len(list1)):
        value = list1[i]
        occurrences = len([x for x in list2 if x == value])
        similarity += value * occurrences
    return similarity

l_1, l_2 = process_input()
result1 = calculate_difference(l_1, l_2)
print("Result for Part A:", result1)

l_1, l_2 = process_input()
result2 = calculate_similarity(l_1, l_2)
print("Result for part B", result2)