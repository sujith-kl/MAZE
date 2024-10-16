import heapq

# Define the directions for movement (up, down, left, right)
DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

class Node:
    def __init__(self, position, g, h):
        self.position = position  # (row, col)
        self.g = g  # Cost from start to current node
        self.h = h  # Heuristic (estimated cost to goal)
        self.f = g + h  # Total cost (g + h)
    
    def __lt__(self, other):
        return self.f < other.f

def heuristic(a, b):
    # Manhattan distance as the heuristic
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar_search(maze, start, goal):
    # Create a priority queue (min-heap) and add the start node
    open_list = []
    start_node = Node(start, 0, heuristic(start, goal))
    heapq.heappush(open_list, start_node)
    
    # Keep track of visited nodes and the path to reconstruct the solution
    came_from = {}
    g_score = {start: 0}
    
    while open_list:
        current_node = heapq.heappop(open_list)
        current_pos = current_node.position
        
        # Check if we have reached the goal
        if current_pos == goal:
            return reconstruct_path(came_from, current_pos)
        
        # Explore neighbors (up, down, left, right)
        for direction in DIRECTIONS:
            neighbor = (current_pos[0] + direction[0], current_pos[1] + direction[1])
            
            # Check if the neighbor is within the maze bounds and not a wall
            if 0 <= neighbor[0] < len(maze) and 0 <= neighbor[1] < len(maze[0]) and maze[neighbor[0]][neighbor[1]] == 0:
                tentative_g_score = g_score[current_pos] + 1  # Assume each move costs 1
                
                # Only consider this neighbor if it's a better path
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    g_score[neighbor] = tentative_g_score
                    f_score = tentative_g_score + heuristic(neighbor, goal)
                    neighbor_node = Node(neighbor, tentative_g_score, heuristic(neighbor, goal))
                    heapq.heappush(open_list, neighbor_node)
                    came_from[neighbor] = current_pos

    # If we reach this point, no path was found
    return None

def reconstruct_path(came_from, current):
    path = []
    while current in came_from:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path

# Example usage:
if __name__ == "__main__":
    maze = [
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 1, 1, 0],
        [0, 0, 0, 1, 0, 0],
        [1, 1, 0, 1, 0, 1],
        [0, 0, 0, 0, 0, 0]
    ]
    
    start = (0, 0)  # Starting position
    goal = (4, 5)   # Goal position
    
    path = astar_search(maze, start, goal)
    
    if path:
        print("Path found:", path)
    else:
        print("No path found")
