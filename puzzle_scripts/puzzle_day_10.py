def process_input():
    input_file = open("inputs/input_day_10.txt", "r")
    hiking_map = []
    for line in input_file:
        line = line.replace("\n", "")
        input_line = [int(s) for s in line]
        hiking_map.append(input_line)
    input_file.close()
    return hiking_map

def get_trail_heads(hiking_map):
    trail_heads = set()
    for i in range(len(hiking_map)):
        for j in range(len(hiking_map[i])):
            if hiking_map[i][j] == 0:
                trail_heads.add((i, j))
    return trail_heads

def calculate_trailhead_scores(hiking_map):
    trail_heads = get_trail_heads(hiking_map)
    total_trailhead_scores = 0
    for head in trail_heads:
        pos_y = head[0]
        pos_x = head[1]
        next_reachable_positions = find_next_position(hiking_map, pos_x, pos_y)

        for i in range(8):
            tmp_position_set = set()
            for pos in next_reachable_positions:
                position_tree = find_next_position(hiking_map, pos[1], pos[0])
                tmp_position_set = tmp_position_set.union(position_tree)
            next_reachable_positions = tmp_position_set
            if len(next_reachable_positions) == 0:
                break

        total_trailhead_scores += len(next_reachable_positions)

    return total_trailhead_scores

def calculate_distinct_trailhead_scores(hiking_map):
    trail_heads = get_trail_heads(hiking_map)
    total_trailhead_scores = 0
    for head in trail_heads:
        pos_y = head[0]
        pos_x = head[1]
        distinct_trails = [[(pos_y, pos_x)]]

        for i in range(9):
            added_trails = []
            for trail_index in range(len(distinct_trails)):
                if distinct_trails[trail_index]:
                    last_pos_y = distinct_trails[trail_index][-1][0]
                    last_pos_x = distinct_trails[trail_index][-1][1]
                    position_tree = find_next_position(hiking_map, last_pos_x, last_pos_y)
                    if len(position_tree) == 1:
                        new_pos = position_tree.pop()
                        distinct_trails[trail_index].append(new_pos)
                    elif len(position_tree) > 1:
                        new_pos = position_tree.pop()
                        for pos in position_tree:
                            new_trail = distinct_trails[trail_index] + [pos]
                            added_trails.append(new_trail)
                        distinct_trails[trail_index].append(new_pos)
                    else:
                        distinct_trails[trail_index] = None
            distinct_trails = distinct_trails + added_trails

        trail_score = 0
        for trail in distinct_trails:
            if trail is not None:
                trail_score += 1
        total_trailhead_scores += trail_score

    return total_trailhead_scores

def find_next_position(hiking_map, pos_x, pos_y):
    next_reachable_positions = set()
    next_level = hiking_map[pos_y][pos_x] + 1

    for i in range(-1, 2, 2):
        if 0 <= pos_x+i < len(hiking_map[pos_y]) and hiking_map[pos_y][pos_x+i] == next_level:
            next_reachable_positions.add((pos_y, pos_x+i))
        if 0 <= pos_y+i < len(hiking_map) and hiking_map[pos_y+i][pos_x] == next_level:
            next_reachable_positions.add((pos_y+i, pos_x))

    return next_reachable_positions

input_map = process_input()
result_score1 = calculate_trailhead_scores(input_map)
result_score2 = calculate_distinct_trailhead_scores(input_map)

print("Result for Part A:", result_score1)
print("Result for Part B:", result_score2)