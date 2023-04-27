import logic.utils.fileUtils as fileUtils

from logic.world.world import World
from logic.world.blockType import BlockType

def load_world_file(path:str) -> World:
    """
    Charge une world depuis un fichier
    """
    if not fileUtils.file_exist(path):
        print(f"The file with the path \"{path}\" was not found")
        exit()

    world_matrix = []

    file_world = open(path, "r")
    file_lines = file_world.readlines()
    # For each line of file
    for file_line in file_lines:
        line_matrix = []
        # Remove the char '\n'
        file_line = file_line.rstrip()
        # For each character of the line (each char represent a bloc)
        for bloc_character in file_line:
            line_matrix.append(BlockType.get_block_type_from_char(bloc_character))
        world_matrix.append(line_matrix)
    world = World(world_matrix)

    return world
