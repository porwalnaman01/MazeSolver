class QueueFrontier():

    def __init__(self):
        self.frontier = []

    def add(self, data):
        self.frontier.append(data)

    def isEmpty(self):
        return len(self.frontier) == 0

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def remove(self):
        try:
            if self.isEmpty() == False:
                node = self.frontier[0]
                self.frontier = self.frontier[1:]
                return node
        except IndexError:
            raise Exception('Error')


class Node():

    def __init__(self, parent, state, action):
        self.parent = parent
        self.action = action
        self.state = state


class Maze():
    def __init__(self, filename):
        with open(filename) as f:
            contents = f.read()

            # we check validity of our maze object

        if contents.count('A') != 1:
            raise Exception(' The maze can have only 1 starting point')

        if contents.count('B') != 1:
            raise Exception('The maze can have only 1 ending point')

            # calculate length and width of the maze
        contents = contents.splitlines()
        self.length = len(contents)
        self.breadth = max(len(line) for line in contents)

        self.walls = []

        for i in range(self.length):
            row = []
            for j in range(self.breadth):
                try:
                    if contents[i][j] == 'A':
                        row.append(False)
                        self.start = (i, j)
                    elif contents[i][j] == 'B':
                        row.append(False)
                        self.goal = (i, j)
                    elif contents[i][j] == ' ':
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)
            self.walls.append(row)
        self.solution = None

    def neighbours(self, state):
        row, col = state
        candidates = [
            ('up', (row - 1, col)),
            ('down', (row + 1, col)),
            ('left', (row, col - 1)),
            ('right', (row, col + 1))
        ]
        results = []
        for actions, (r, c) in candidates:
            if 0 <= r < self.length and 0 <= c < self.breadth and not self.walls[r][c]:
                results.append((actions, (r, c)))
        return results

    def solve(self):
        self.state_explored = 0
        start = Node(parent=None, state=self.start, action=None)
        frontier = QueueFrontier()
        frontier.add(start)

        self.explored = set()
        while True:
            if frontier.isEmpty() == True:
                raise Exception('no solution')
            node = frontier.remove()
            self.state_explored += 1
            if node.state == self.goal:
                actions = []
                cells = []
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions)
                return self.solution
            self.explored.add(node.state)

            for action, state in self.neighbours(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(parent=node, state=state, action=action)
                    frontier.add(child)

m = Maze('a.txt')
print(m.solve())

