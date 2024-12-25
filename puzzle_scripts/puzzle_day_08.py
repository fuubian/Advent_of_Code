# Processing input
def process_input():
    input_file = open("inputs/input_day_08.txt", "r")
    city_map = []
    for line in input_file:
        line = line.replace("\n", "")
        input_line = [symbol for symbol in line]
        city_map.append(input_line)
    input_file.close()
    return city_map

def get_antenna_positions(city_map):
    # Create dictionary of all antenna positions
    antenna_positions = {}
    for line in range(len(city_map)):
        for point in range(len(city_map[line])):
            if city_map[line][point] != '.':
                antenna_type = city_map[line][point]
                if antenna_type not in antenna_positions:
                    positions = [(line, point)]
                    antenna_positions[antenna_type] = positions
                else:
                    antenna_positions[antenna_type].append((line, point))
    return antenna_positions

def find_unique_nodes(city_map):
    antenna_positions = get_antenna_positions(city_map)

    # Find unique nodes
    unique_nodes = set()
    for antenna in antenna_positions:
        positions = antenna_positions[antenna]
        for i in range(len(positions)):
            for j in range(i+1, len(positions)):
                pos1 = positions[i]
                pos2 = positions[j]
                distance = (pos1[0] - pos2[0], pos1[1] - pos2[1])
                new_pos1 = (pos1[0] + distance[0], pos1[1] + distance[1])
                new_pos2 = (pos2[0] - distance[0], pos2[1] - distance[1])

                if 0 <= new_pos1[0] < len(city_map) and 0 <= new_pos1[1] < len(city_map[0]):
                    unique_nodes.add(new_pos1)
                if 0 <= new_pos2[0] < len(city_map) and 0 <= new_pos2[1] < len(city_map[0]):
                    unique_nodes.add(new_pos2)

    return len(unique_nodes)

def find_unique_nodes_resonant_harmonics(city_map):
    antenna_positions = get_antenna_positions(city_map)

    # Find unique nodes
    unique_nodes = set()
    for antenna in antenna_positions:
        positions = antenna_positions[antenna]
        for i in range(len(positions)):
            for j in range(i + 1, len(positions)):
                pos1 = positions[i]
                pos2 = positions[j]
                distance = (pos1[0] - pos2[0], pos1[1] - pos2[1])

                counter = 0
                while True:
                    new_pos1 = (pos1[0] + counter * distance[0], pos1[1] + counter * distance[1])
                    if 0 <= new_pos1[0] < len(city_map) and 0 <= new_pos1[1] < len(city_map[0]):
                        unique_nodes.add(new_pos1)
                        counter += 1
                    else:
                        break
                counter = 0
                while True:
                    new_pos2 = (pos2[0] - counter * distance[0], pos2[1] - counter * distance[1])
                    if 0 <= new_pos2[0] < len(city_map) and 0 <= new_pos2[1] < len(city_map[0]):
                        unique_nodes.add(new_pos2)
                        counter += 1
                    else:
                        break

    return len(unique_nodes)

city_map = process_input()
num_unique_nodes = find_unique_nodes(city_map)
num_unique_nodes_rh = find_unique_nodes_resonant_harmonics(city_map)

print("Result for Part A:", num_unique_nodes)
print("Result for Part B:", num_unique_nodes_rh)