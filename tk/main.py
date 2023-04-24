from game.gameFrame import GameFrame
from game.option import Option
from utils.vec2D import Vec2D

if __name__ == "__main__":
    Option(window_dimensions=Vec2D(809, 500), fov=60)

    game_frame = GameFrame()
    game_frame.enable_minimap(Vec2D(600, 10), Vec2D(600 + 200, 10 + 200))
    #game_frame.enable_minimap(Vec2D(50, 10), Vec2D(50 + 500, 10 + 500))
    game_frame.run()