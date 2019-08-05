def valid_actions(grid):
        #List of tuples
        actions = []
        for i in range(10):
            for j in range(10):
                if grid[i][j] == 0 or grid[i][j] == 1:
                    actions.append((i,j))
        return actions