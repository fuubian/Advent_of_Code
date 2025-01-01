from collections import defaultdict

# Processing input
def process_input():
    input_file = open("inputs/input_day_12.txt", "r")
    garden_field = []
    for line in input_file:
        line = [field for field in line.replace("\n", "")]
        garden_field.append(line)
    return garden_field

# Get all needed dictionaries from the grid
def get_area_perimeter(garden_field):
    area_dict = defaultdict(int)
    perimeter_dict = defaultdict(int)
    side_dict = defaultdict(int)
    seen_locations = set()
    for row in range(len(garden_field)):
        for plant in range(len(garden_field[row])):
            if (row, plant) not in seen_locations:
                current_iteration = set()
                overall_iteration = set()
                vertical_brink_locations = set()
                horizontal_brink_locations = set()
                current_plant = garden_field[row][plant]
                current_key = current_plant
                while True:
                    if perimeter_dict[current_key] >= 1:
                        current_key = current_key + '1'
                    else:
                        break

                seen_locations.add((row, plant))
                current_iteration.add((row, plant))
                perimeter_value = 0

                while True:
                    updated_iteration = set()
                    for location in current_iteration:
                        loc1 = (location[0]+1, location[1])
                        loc2 = (location[0], location[1]+1)
                        loc3 = (location[0]-1, location[1])
                        loc4 = (location[0], location[1]-1)
                        if loc1[0] < len(garden_field) and garden_field[loc1[0]][loc1[1]] == current_plant:
                            if loc1 not in overall_iteration:
                                updated_iteration.add(loc1)
                                seen_locations.add(loc1)
                        else:
                            perimeter_value += 1
                            horizontal_brink_locations.add((loc1[0],loc1[1],'up'))
                        if loc2[1] < len(garden_field[row]) and garden_field[loc2[0]][loc2[1]] == current_plant:
                            if loc2 not in overall_iteration:
                                updated_iteration.add(loc2)
                                seen_locations.add(loc2)
                        else:
                            perimeter_value += 1
                            vertical_brink_locations.add((loc2[0], loc2[1], 'left'))
                        if loc3[0] >= 0 and garden_field[loc3[0]][loc3[1]] == current_plant:
                            if loc3 not in overall_iteration:
                                updated_iteration.add(loc3)
                                seen_locations.add(loc3)
                        else:
                            perimeter_value += 1
                            horizontal_brink_locations.add((loc3[0], loc3[1], 'down'))
                        if loc4[1] >= 0 and garden_field[loc4[0]][loc4[1]] == current_plant:
                            if loc4 not in overall_iteration:
                                updated_iteration.add(loc4)
                                seen_locations.add(loc4)
                        else:
                            perimeter_value += 1
                            vertical_brink_locations.add((loc4[0], loc4[1], "right"))

                    #print(f"Plant: {current_plant}; Locations: {current_iteration}; Add-Value: {perimeter_value}\nNew locations:{updated_iteration}")
                    overall_iteration = overall_iteration.union(current_iteration)
                    if len(updated_iteration) == 0:
                        break
                    current_iteration = updated_iteration

                area_dict[current_key] += len(overall_iteration)
                perimeter_dict[current_key] += perimeter_value
                side_dict[current_key] = get_sides(vertical_brink_locations, horizontal_brink_locations, overall_iteration)

    return area_dict, perimeter_dict, side_dict

# Get number of sides via brink locations
def get_sides(vertical_brink_locations, horizontal_brink_locations, overall_iteration):
    vertical_side_value = process_brink_locations(vertical_brink_locations, overall_iteration, axis='vertical')
    horizontal_side_value = process_brink_locations(horizontal_brink_locations, overall_iteration, axis='horizontal')
    return vertical_side_value + horizontal_side_value

# Process either vertical or horizontal brink locations
def process_brink_locations(brink_locations, overall_iteration, axis):
    seen_locations = set()
    side_value = 0

    for location in brink_locations:
        if location not in seen_locations:
            seen_locations.add(location)

            for i in [1, -1]:
                offset = 1
                while True:
                    new_location = (
                        (location[0] + offset * i, location[1], location[2]) if axis == 'vertical'
                        else (location[0], location[1] + offset * i, location[2])
                    )
                    if new_location in brink_locations and new_location not in seen_locations:
                        seen_locations.add(new_location)
                        offset += 1
                    else:
                        break

            side_value += 1
    return side_value

# Get total cost for both parts
def get_total_cost(garden_field):
    total_cost1 = 0
    total_cost2 = 0
    area_dict, perimeter_dict, side_dict = get_area_perimeter(garden_field)

    for key in area_dict:
        total_cost1 += area_dict[key] * perimeter_dict[key]
        total_cost2 += area_dict[key] * side_dict[key]

    return total_cost1, total_cost2

input_field = process_input()
result1, result2 = get_total_cost(input_field)
print("Result Part A:", result1)
print("Result Part B:", result2)