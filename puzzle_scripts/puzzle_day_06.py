class Area:
    def __init__(self, height, width, guard_pos, guard_dir):
        self.height = height
        self.width = width
        self.obstacles = set()
        self.guard = Guard(guard_pos, guard_dir)
        self.guard_start_pos = guard_pos
        self.guard_start_dir = guard_dir
        self.guard_positions = set()
        self.guard_positions.add(guard_pos)
        self.loop_way = []

    # add obstacles to the field
    def add_obstacle(self, x, y):
        self.obstacles.add((x, y))

    # check if agent is outside the field
    def check_out_field(self, pos):
        if pos[0] < 0 or pos[1] < 0 or pos[0] >= self.width or pos[1] >= self.height:
            return True
        return False

    # check if a collision with an obstacle occurred
    def check_collision(self, pos):
        for obs in self.obstacles:
            if obs[0] == pos[0] and obs[1] == pos[1]:
                return True
        return False

    # Make a step and check if collision or out of box occurs
    def update_step(self):
        new_pos = self.guard.make_move()
        if self.check_out_field(new_pos):
            return True
        if self.check_collision(new_pos):
            self.guard.register_collision()
            return self.update_step()
        if new_pos in self.guard_positions:
            self.loop_way.append(new_pos)
        else:
            self.loop_way = [] # reset loop way
            self.guard_positions.add(new_pos)
        return False

    # Run default simulation of the guard walking around until she walks out of the area
    def run_simulation(self):
        while not self.update_step():
            if self.check_loop():
                return None
        return len(self.guard_positions)

    # Check if loop occurs when an additional object was in the default path of the guard
    def run_loop_simulation(self):
        counter_loops = 0
        counter_pos = 0
        for g_pos in self.guard_positions:
            counter_pos += 1
            if g_pos == self.guard_start_pos:
                continue

            # Create temporary Area object with additional object and run simulation on it to check for loopx
            tmp_area = Area(self.height, self.width, self.guard_start_pos, self.guard_start_dir)
            for obs in self.obstacles:
                tmp_area.add_obstacle(obs[0], obs[1])
            tmp_area.add_obstacle(g_pos[0], g_pos[1])
            if tmp_area.run_simulation() is None:
                counter_loops += 1
            print(counter_pos, counter_loops)
        return counter_loops

    # Check if a loop occurred
    def check_loop(self):
        if len(self.loop_way) < 2:
            return False

        seen_pairs = set()
        for i in range(len(self.loop_way) - 1):
            current_pair = (self.loop_way[i], self.loop_way[i + 1])
            if current_pair in seen_pairs:
                return True
            seen_pairs.add(current_pair)
        return False

    # Resets object after checking for loops
    def reset_area_object(self):
        self.guard_positions = set()
        self.guard_positions.add(self.guard_start_pos)
        self.guard = Guard(self.guard_start_pos, self.guard_start_dir)

    # Check if there is already an object on that position
    def check_for_object(self, x, y):
        if self.guard_start_pos == (x, y):
            return True
        for obs in self.obstacles:
            if obs == (x, y):
                return True
        return False

class Guard:
    def __init__(self, pos, direction):
        self.pos = pos
        self.direction = direction # Directions: (1,0)(-1,0)(0,1)(0,-1)

    def make_move(self):
        self.pos = (self.pos[0] + self.direction[0], self.pos[1] + self.direction[1])
        return self.pos

    def register_collision(self):
        # Return to pos before the collision
        back_movement = (self.direction[0] * -1, self.direction[1] * -1)
        self.pos = (self.pos[0] + back_movement[0], self.pos[1] + back_movement[1])

        # Turn right
        if self.direction == (0,-1):
            self.direction = (1,0)
        elif self.direction == (1,0):
            self.direction = (0,1)
        elif self.direction == (0,1):
            self.direction = (-1,0)
        elif self.direction == (-1,0):
            self.direction = (0,-1)

# Processing input and creation of area object
def process_input():
    input_file = open("inputs/input_day_06.txt", "r")
    obstacles = []
    guard_pos = None
    guard_dir = None
    counter_row = 0
    height = None
    for line in input_file:
        line = line.replace("\n", "")
        counter_column = 0
        for char in line:
            if char == "#":
                obstacles.append((counter_column, counter_row))
            elif char == "^":
                guard_pos = (counter_column, counter_row)
                guard_dir = (0,-1)
            elif char == ">":
                guard_pos = (counter_column, counter_row)
                guard_dir = (1,0)
            elif char == "<":
                guard_pos = (counter_column, counter_row)
                guard_dir = (-1,0)
            elif char == "v":
                guard_pos = (counter_column, counter_row)
                guard_dir = (0,1)
            counter_column += 1
        counter_row += 1
        height = len(line)
    input_file.close()

    # Create area object
    field = Area(height, counter_row, guard_pos, guard_dir)
    for obs in obstacles:
        field.add_obstacle(obs[0], obs[1])

    return field

puzzle_field = process_input()
result1 = puzzle_field.run_simulation()
print("Result for Part A:", result1)

result2 = puzzle_field.run_loop_simulation()
print("Result for Part B:", result2)