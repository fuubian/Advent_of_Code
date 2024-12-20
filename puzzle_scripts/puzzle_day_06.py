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
        self.seen_states = set() # consisting of tuples (pos, direction)
        self.loop_flag = False

    # add obstacles to the field
    def add_obstacle(self, x, y):
        self.obstacles.add((x, y))

    # check if agent is outside the field
    def check_out_field(self, pos):
        return not (0 <= pos[0] < self.width and 0 <= pos[1] < self.height)

    # check if a collision with an obstacle occurred
    def check_collision(self, pos):
        return pos in self.obstacles

    # Make a step and check if collision or out of box occurs
    def update_step(self):
        while True:
            new_pos = self.guard.make_move()
            if self.check_out_field(new_pos):
                return True
            if self.check_collision(new_pos):
                self.guard.register_collision()
            else:
                break
        current_state = (new_pos, self.guard.direction)
        if current_state in self.seen_states:
            self.loop_flag = True
            return True
        self.seen_states.add((new_pos, self.guard.direction))
        self.guard_positions.add(new_pos)
        return False

    # Reset the object state for a fresh simulation
    def reset_area_state(self):
        self.guard.reset_position(self.guard_start_pos, self.guard_start_dir)
        self.guard_positions = set()
        self.seen_states = set()
        self.loop_flag = False

    # Run default simulation of the guard walking around until she walks out of the area
    def run_simulation(self):
        while not self.update_step():
            pass
        if self.loop_flag:
            return None
        return len(self.guard_positions)

    # Check if loop occurs when an additional object was in the default path of the guard
    def run_loop_simulation(self):
        counter_loops = 0
        counter_pos = 0
        original_guard_positions = self.guard_positions.copy()
        for g_pos in original_guard_positions:
            counter_pos += 1
            if g_pos == self.guard_start_pos:
                continue

            # Modify itself with additional object and run simulation to check for loops
            self.reset_area_state()
            self.obstacles.add((g_pos[0], g_pos[1]))
            if self.run_simulation() is None:
                counter_loops += 1
            self.obstacles.remove((g_pos[0], g_pos[1]))
            print(counter_pos, counter_loops)
        return counter_loops

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

    def reset_position(self, new_pos, new_dir):
        self.pos = new_pos
        self.direction = new_dir

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