
'''
assumptions:
- the 2d array is balanced (all subarrays are of same length)
- can not travel diagonally, only up, down, left or right
'''

'''
example 2d array
[
    [0,0,1],
    [0,0,0],
    [1,1,0]
]

example path

[
    [Y,Y,1],
    [0,Y,Y],
    [1,1,Y]
]

'''
def maze_solver(maze, x, y):
    if len(maze) == 0:
        return False #or return True / is lack of a maze, means its solved?

    # out of bounds in maze
    if x < 0 or x >= len(maze) or y < 0 or y >= len(maze[0]):
        return False

    # if wall or already visited
    if maze[x][y] == 1 or maze[x][y] == 'Y':
        return False

    '''
    If we have reached the tile in the maze designated as the end, we have entered
    our base case and may exit. We have our recursive function return true in order to
    communicate that it has reached the base case
    '''
    last_cell_x = len(maze) - 1
    last_cell_y = len(maze[0]) - 1
    if x == last_cell_x and y == last_cell_y:
        maze[x][y] = 'Y'
        return True
    
    maze[x][y] = 'Y'

    '''
    In our recursive step we should begin by marking the current tile as part of the
    solution path, then search in all possible directions that are not already part of the
    solution path. If this does not find us our exit, we should backtrack and unmark the
    current tile from the path.
    '''
  
    #down
    if maze_solver(maze, x+1, y):
        return True
    #up
    if maze_solver(maze, x-1, y): 
        return True
    #left
    if maze_solver(maze, x, y-1):
        return True
    #right
    if maze_solver(maze, x, y+1):
        return True

    #returned false in that path, so put it back to 0
    maze[x][y] = 0
    return False

maze = [
    [0, 0, 1],
    [0, 0, 0],
    [1, 1, 0]
]

maze_solver(maze, 0, 0)
print(maze)
