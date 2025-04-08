class Block:
    """
    Base class for blocks in the Lazor game.
    Determines how lasers interact with blocks.
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def properties(self, meshgrid):
        """
        Get the reflect and transmit behavior at (x, y) in the meshgrid.

        Returns:
            tuple[bool, bool]: (reflect, transmit)
        """
        try:
            cell = meshgrid[self.y][self.x]
        except IndexError:
            return False, False  # Out of bounds — safe default

        if cell == 'A':      # Reflect only
            return True, False
        elif cell == 'B':    # Opaque
            return False, False
        elif cell == 'C':    # Refract
            return True, True
        else:                # Empty or anything else
            return False, True


class Add(Block):
    """
    Simple wrapper class to access block behavior using a meshgrid.
    Inherits from Block.
    """

    def __init__(self, x, y):
        super().__init__(x, y)

    def prop(self, meshgrid):
        return self.properties(meshgrid)
