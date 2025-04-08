from blocks import Add

class Laser:
    """
    The Laser class handles simulating beam movement across a Lazor board.
    It tracks direction, path, and handles behavior with respect to blocks.
    """

    def __init__(self, start_point, path):
        self.source = start_point
        self.direction = path

    def pos_chk(x, y, nBlocks):
        return 0 <= x < nBlocks and 0 <= y < nBlocks

    def laser_strikes(self, path, intercepts, grid, meshgrid, path_1, intercept_new):
        dx, dy = path[-1]
        nx, ny = intercepts[-1]

        n_direct = [(0, 1), (0, -1), (-1, 0), (1, 0)]
        nlist = []
        transmit_list = []

        if (dx, dy) != (0, 0):
            for d in n_direct:
                ex, ey = nx + d[0], ny + d[1]
                if 0 < ex < 2 * len(grid[0]) + 1 and 0 < ey < 2 * len(grid) + 1:
                    delta_x = ex - nx
                    delta_y = ey - ny

                    reflect, transmit = Add(ex, ey).prop(meshgrid)

                    if reflect and not transmit:  # Reflect only
                        new_dx = -dx if delta_x != 0 else dx
                        new_dy = -dy if delta_y != 0 else dy
                        nlist.append((new_dx, new_dy))

                    elif not reflect and not transmit:  # Opaque
                        if delta_x == dx or delta_y == dy:
                            nlist.append((0, 0))
                        else:
                            nlist.append((dx, dy))

                    elif reflect and transmit:  # Refract: split
                        if delta_x == dx or delta_y == dy:
                            new_dx = -dx if delta_x != 0 else dx
                            new_dy = -dy if delta_y != 0 else dy
                            transmit_list.append((dx, dy))
                            nlist.append((new_dx, new_dy))
                        else:
                            nlist.append((dx, dy))

            if nlist:
                path.append(nlist[-1])
            else:
                path.append((dx, dy))

            if transmit_list:
                path_1.append(transmit_list[-1])
                intercept_new.append((nx, ny))

            nx += path[-1][0]
            ny += path[-1][1]
            intercepts.append((nx, ny))

        return path, intercepts, path_1, intercept_new

    def trajectory(self, path, grid, meshgrid):
        intercepts = []
        path_list = []

        for i in range(len(self.source)):
            intercepts.append([self.source[i]])
            path_list.append([self.direction[i]])

        path_1 = []
        intercept_new = []

        for k in range(len(path_list)):
            if len(intercepts[k]) == 1:
                path_list[k], intercepts[k], path_1, intercept_new = self.laser_strikes(
                    path_list[k], intercepts[k], grid, meshgrid, path_1, intercept_new)

            while 0 < intercepts[k][-1][0] < len(meshgrid[0]) - 1 and \
                  0 < intercepts[k][-1][1] < len(meshgrid) - 1:

                if path_list[k][-1] != (0, 0):
                    path_list[k], intercepts[k], path_1, intercept_new = self.laser_strikes(
                        path_list[k], intercepts[k], grid, meshgrid, path_1, intercept_new)
                else:
                    break

            # Handle refracted split laser
            if path_1:
                path_0 = []
                intercept_0 = []
                dx, dy = path_1[-1]
                cx, cy = intercept_new[-1]
                nx, ny = cx + dx, cy + dy

                intercept_new.append((nx, ny))

                while 0 < intercept_new[-1][0] < len(meshgrid[0]) - 1 and \
                      0 < intercept_new[-1][1] < len(meshgrid) - 1:

                    if path_1[-1] != (0, 0):
                        path_1, intercept_new, path_0, intercept_0 = self.laser_strikes(
                            path_1, intercept_new, grid, meshgrid, path_0, intercept_0)
                    else:
                        break

        final_intercept_list = [item for sublist in intercepts for item in sublist]
        return final_intercept_list, path_list, intercept_new