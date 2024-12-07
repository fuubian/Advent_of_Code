# Processing input
def process_input():
    input_file = open("inputs/input_day_05.txt", "r")
    order_rules = set()
    requested_updates = []
    for line in input_file:
        line = line.replace("\n", "")
        if line != "":
            if line[2] == '|':
                number1 = int(line[0:2])
                number2 = int(line[3:5])
                order_rules.add((number1, number2))
            elif line != "":
                numbers = line.split(",")
                numbers = [int(n) for n in numbers]
                requested_updates.append(numbers)
    input_file.close()
    return order_rules, requested_updates

# Correct an update if it was incorrect
def correct_update(requested_update, order_rules):
    first_loop = True
    change_occurred = False
    while first_loop or change_occurred:
        change_occurred = False
        first_loop = False
        for i in range(len(requested_update)):
            for j in range(i+1, len(requested_update)):
                for rule in order_rules:
                    if rule[0] == requested_update[j] and rule[1] == requested_update[i]:
                        change_occurred = True
                        tmp = requested_update[j]
                        requested_update[j] = requested_update[i]
                        requested_update[i] = tmp
                        break
                if change_occurred:
                    break
            if change_occurred:
                break

    return requested_update

# Check if a requested update is correct
def check_update(requested_update, order_rules):
    for i in range(len(requested_update)):
        for j in range(i+1, len(requested_update)):
            for rule in order_rules:
                if rule[0] == requested_update[j] and rule[1] == requested_update[i]:
                    return False
    return True

# Return middle numbers of all update operations
def return_middle_numbers(requested_updates, order_rules, correction=False):
    m_numbers = []

    for update in requested_updates:
        correctness = check_update(update, order_rules)
        if correctness and not correction:
            m_num = update[int(len(update)/2)]
            m_numbers.append(m_num)
        elif not correctness and correction:
            update = correct_update(update, order_rules)
            m_num = update[int(len(update) / 2)]
            m_numbers.append(m_num)

    return m_numbers

rules, updates = process_input()
middle_numbers1 = return_middle_numbers(updates, rules)
middle_numbers2 = return_middle_numbers(updates, rules, True)
print("Result for Part A:", sum(middle_numbers1))
print("Result for Part B:", sum(middle_numbers2))