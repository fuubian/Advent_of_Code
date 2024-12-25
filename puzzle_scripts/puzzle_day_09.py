# Processing input
def process_input():
    input_file = open("inputs/input_day_09.txt", "r")
    disk_map = input_file.read().replace("\n", "")
    input_file.close()
    return disk_map

def process_disk_map(disk_map):
    converted_disk_map = []
    current_id = 0
    for i in range(0, len(disk_map), 2):
        # File layout
        file_length = int(disk_map[i])
        for x in range(file_length):
            converted_disk_map.append(current_id)
        current_id += 1

        # End of string reached?
        if i+1 >= len(disk_map):
            break

        # Free space
        free_space = int(disk_map[i + 1])
        for x in range(free_space):
            converted_disk_map.append('.')

    return converted_disk_map

def move_file_blocks_partial(disk_map):
    index_start = 0
    index_end = len(disk_map)-1

    while index_start < index_end:
        if disk_map[index_start] == '.':
            if disk_map[index_end] != '.':
                file_id = disk_map[index_end]
                disk_map[index_start] = file_id
                disk_map[index_end] = '.'
            index_end -= 1
            continue
        index_start += 1

    return disk_map

def locate_empty_blocks(disk_map, end_index):
    empty_blocks = []
    found_block = False
    index_start = None
    for i in range(end_index):
        if not found_block and disk_map[i] == '.':
            index_start = i
            found_block = True
        elif found_block and disk_map[i] != '.':
            end_index = i
            found_block = False
            empty_blocks.append((index_start, end_index))
    return empty_blocks

def update_empty_blocks(empty_blocks, file_size, changed_block_index, file_pos):
    empty_blocks[changed_block_index] = (empty_blocks[changed_block_index][0] + file_size, empty_blocks[changed_block_index][1])
    new_empty_block = (file_pos, file_pos + file_size)

    # Binary search to locate insertion point
    left, right = 0, len(empty_blocks)
    while left < right:
        mid = (left + right) // 2
        if empty_blocks[mid][0] < file_pos:
            left = mid + 1
        else:
            right = mid
    insertion_index = left

    # Check for merging with adjacent blocks
    if insertion_index > 0 and empty_blocks[insertion_index - 1][1] == file_pos:
        # Merge with previous block
        new_empty_block = (empty_blocks[insertion_index - 1][0], new_empty_block[1])
        empty_blocks[insertion_index - 1] = new_empty_block
        insertion_index -= 1
    else:
        empty_blocks.insert(insertion_index, new_empty_block)
    if insertion_index + 1 < len(empty_blocks) and empty_blocks[insertion_index + 1][1] == new_empty_block[1]:
        # Merge with the next block
        new_empty_block = (new_empty_block[0], empty_blocks[insertion_index + 1][1])
        empty_blocks[insertion_index] = new_empty_block
        del empty_blocks[insertion_index + 1]

    return empty_blocks

def move_file_blocks_complete(disk_map):
    # Locate empty blocks
    empty_blocks = locate_empty_blocks(disk_map, len(disk_map))

    index_end = len(disk_map)-1
    while index_end > 0:
        # Locate next file
        while disk_map[index_end] == '.' and index_end > 0:
            index_end -= 1

        # Get file size and update index pointer
        file_id = disk_map[index_end]
        file_size = 0
        while disk_map[index_end] == file_id and index_end > 0:
            file_size += 1
            index_end -= 1
        file_start_index = index_end + 1

        # Find first block of empty space
        for i in range(len(empty_blocks)):
            block_size = empty_blocks[i][1] - empty_blocks[i][0]
            if file_start_index < empty_blocks[i][0]:
                break
            if block_size >= file_size:
                block_start_index = empty_blocks[i][0]
                for x in range(file_size):
                    disk_map[block_start_index + x] = file_id
                    disk_map[file_start_index + x] = '.'
                empty_blocks = update_empty_blocks(empty_blocks, file_size, i, file_start_index)
                #print(empty_blocks)
                #result = ""
                #for element in disk_map:
                #    result += str(element)
                #print(result)
                break

    return disk_map

def calculate_checksum(disk_map):
    checksum = 0
    for i in range(len(disk_map)):
        if disk_map[i] == '.':
            continue
        checksum += disk_map[i] * i
    return checksum

def fragment_disk(disk_map, complete=False):
    converted_disk_map = process_disk_map(disk_map)
    if complete:
        converted_disk_map = move_file_blocks_complete(converted_disk_map)
    else:
        converted_disk_map = move_file_blocks_partial(converted_disk_map)
    return calculate_checksum(converted_disk_map)

input_map = process_input()
checksum_result1 = fragment_disk(input_map)
print("Result for Part A:", checksum_result1)

checksum_result2 = fragment_disk(input_map, complete=True)
print("Result for Part B:", checksum_result2)