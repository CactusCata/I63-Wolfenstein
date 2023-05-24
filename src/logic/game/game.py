from __future__ import annotations

from typing import Optional

import logic.world.worldFile as worldFile
from logic.world.world import World

GAME: Optional[Game] = None


class Game:
    """Gère une partie
    """
    def __init__(self, savefile: str = "world"):
        """Constructeur

        Args:
            savefile (str, optional): nom du monde. Defaults to "world".
        """
        global GAME
        GAME = self

        self.world = worldFile.load_world_file(f"../res/worlds/{savefile}.dat")

    def get_world(self) -> World:
        """Renvoie l'instance (unique) du monde

        Returns:
            World: monde actuel
        """
        return self.world
