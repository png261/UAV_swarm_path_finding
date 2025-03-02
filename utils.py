from collections import deque
import heapq

class Point:
    """
        Point class to represent a point in the map
        Attributes:
            x: x-coordinate of the point in pixel
            y: y-coordinate of the point in pixel
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Vector:
    """
        Vector class to represent a vector in the map
        Attributes:
            x: x-coordinate of the vector in pixel
            y: y-coordinate of the vector in pixel
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def normalize(self):
        """
            Normalize the vector
            Returns:
                Vector object representing the normalized vector
        """
        magnitude = (self.x ** 2 + self.y ** 2) ** 0.5
        if magnitude == 0:
            return Vector(0, 0)
        return Vector(self.x / magnitude, self.y / magnitude)



def is_point_in_polygon(x, y, polygon):
    """Check if a point (x, y) is inside a polygon."""
    n = len(polygon)
    inside = False

    p1x, p1y = polygon[0]
    for i in range(n + 1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside

def bfs(valid_cells, start):
    # Tạo dictionary lưu trạng thái bản đồ
    map_dict = {(x, y): v for x, y, v in valid_cells}
    
    if start not in map_dict or map_dict[start] == -1:
        return None  # Điểm bắt đầu không hợp lệ

    # Khởi tạo ma trận khoảng cách (bắt đầu từ điểm start)
    distances = {pos: float('inf') for pos in map_dict if map_dict[pos] == 1}
    distances[start] = 0  # Khoảng cách đến chính nó là 0

    # Hàng đợi BFS, bắt đầu từ điểm start
    queue = deque([start])
    directions = [(0, 30), (0, -30), (30, 0), (-30, 0)]  # Lên, xuống, phải, trái
    
    while queue:
        x, y = queue.popleft()

        for dx, dy in directions:
            next_pos = (x + dx, y + dy)
            if next_pos in distances and distances[next_pos] == float('inf'):  # Chưa đi qua
                distances[next_pos] = distances[(x, y)] + 1
                queue.append(next_pos)
    return distances  # Trả về toàn bộ khoảng cách

### Tsunami algo ###

def wavefront(goal, map):
    temp = (goal[0] // Parameters.cell_size, goal[1] // Parameters.cell_size)
    goal = temp;
    map_width = int(Parameters.map_width // Parameters.cell_size) + 1
    map_height = int(Parameters.map_height // Parameters.cell_size) + 1
    wavefront_matrix = [[-1 for j in range(map_height)] for i in range(map_width)];
    state_table = [[-1 for j in range(map_height)] for i in range(map_width)]
    value_table = [[-1 for j in range(map_height)] for i in range(map_width)]
    horizontal = 0;
    for x in range(0, Parameters.map_width, Parameters.cell_size):
        vertical = 0;
        for y in range(0, Parameters.map_height, Parameters.cell_size):                
            center_x = x + Parameters.cell_size // 2;
            center_y = y + Parameters.cell_size // 2;
            state_table[horizontal][vertical] = map.cells[(center_x, center_y)].state;
            value_table[horizontal][vertical] = map.cells[(center_x, center_y)].value;
            vertical += 1;
        horizontal += 1;

    def bfs_condition(state_table, result, position):
        if (state_table[position[0]][position[1]] != CellState.UNREACHABLE and state_table[position[0]][position[1]] != CellState.NO_INTEREST) and result[position[0]][position[1]] == -1:
            return True;
        return False

    rows, cols = len(state_table), len(state_table[0])
    
    # Initialize the result matrix with -1 (unreachable) values
    result = [[-1 for _ in range(cols)] for _ in range(rows)]
    
    # Directions for moving in the grid (up, down, left, right)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    # Priority queue initialization: (distance, x, y)
    pq = []
    heapq.heappush(pq, (0, goal[0], goal[1]))  # Start from the goal with distance 0
    result[goal[0]][goal[1]] = 0  # Distance from goal to goal is 0

    while pq:
        dist, x, y = heapq.heappop(pq)  # Pop the node with the smallest distance
        
        # Explore all possible neighbors
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            
            # Check if the neighbor is within bounds, not an obstacle, and not visited
            if 0 <= nx < rows and 0 <= ny < cols and bfs_condition(state_table, result, (nx, ny)):
                # Set the distance to the neighbor
                result[nx][ny] = dist + 1
                # Push the neighbor into the priority queue with updated distance
                heapq.heappush(pq, (dist + 1, nx, ny))
    
    return result

#def tsunami_next_position((recent_uav.cell_x, recent_uav.cell_y), map0, wavefront_map):
    
    