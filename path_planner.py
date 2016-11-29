# try to build a graph s.t I can assign arbitrary coordinate labels to it
# like for now, I can just have a grid -n to n, or 0,n or something.

#building queue class from http://www.redblobgames.com/pathfinding/a-star/implementation.html
import collections
import datetime

import numpy
import spacepy.coordinates
import spacepy.time


class Queue:
    def __init__(self):
        self.elements = collections.deque()
    def empty(self):
        # returns true if the set is empty, false otherwise
        return len(self.elements) == 0
    def put(self,x):
        self.elements.append(x)
    def get(self):
        return self.elements.popleft()

# building the simple graph from http://www.redblobgames.com/pathfinding/grids/graphs.html
class GridGraph:
    # builds a graph of a rectangular grid
    # later i'll worry about labeling the coordinates
    def __init__(self,max_x,max_y):
        self.all_nodes = []

        # define total area
        self.max_x = max_x
        self.max_y = max_y
        for x in range(self.max_x):
            for y in range(self.max_y):
                self.all_nodes.append((x,y))
        self.all_nodes = tuple(self.all_nodes)
        # define obstacles
        self.obstacles = []
        # self.obstacles = getObstacles()
    def in_bounds(self, id):
        (x,y) = id
        return 0<=x < self.max_x and 0 <= y < self.max_y

    def passable(self, id):
        # true if the id isn't an obstacle
        return id not in self.obstacles

    def neighbors2(self, id):
        # the main difference between this one and the original one is that
        # the configuration space coordinates are immutable this way
        (x,y) = id
        results = [(x+1, y),(x+1, y+1), (x, y+1),(x-1, y), (x-1, y+1), (x-1, y-1), (x, y-1), (x+1,y-1)]
        results = filter(self.in_bounds,results)
        results = filter(self.passable, results)
        return results
    def neighbors(self,node):
        # i need to make this compatible with the immutable "tuple" type
        # connectivity 8
        dirs = [[1,0],[1,1],[0,1],[-1,1],[-1,0],[-1,-1],[0,-1],[1,-1]]
        result = []
        for dir in dirs:
            # results vector is the list of neighbors
            # so add the dirs to each x,y coordinate
            neighbor = [node[0] + dir[0], node[1] + dir[1]]
            if neighbor in self.all_nodes:
                result.append(neighbor)
        return result

    def reconstruct_path(self, came_from, start, goal):
        current = goal
        path = [current]
        while current != start:
            current = came_from[current]
            path.append(current)
        path.append(start) # optional
        path.reverse() # optional
        return path

    def breadth_first_search(self, start, goal):
        frontier = Queue()
        frontier.put(start)
        came_from = {}
        came_from[start] = None

        while not frontier.empty():
            current = frontier.get()
            # print("current",current)
            if current == goal:
                break

            for next in self.neighbors2(current):
                if next not in came_from:
                    frontier.put(next)
                    came_from[next] = current

        return came_from
    def dijkstras_search(self,start,goal):
        # placeholder function for dijkstras_search
        pass
    def a_star_search(self, start, goal):
        # i'll add this in later if needed
        pass

    def getObstacles(self, model="circle"):
        # this function has the purpose of automating the different obstacles
        # this corresponds to the location of the sun.
        pass

    def getGoalRegion(self,model="tsyganenko"):
        # this function will return the goal location, based on the cusp location from the tsyganenko model
        # also i guess i'd incorporate that guys rotating dipole model here.
        # the coordinates are cylindrical but you can convert to GSM
        pass
    def tilt(self,t):
        """Get dipole tilt for time or range of times

        :param t: time or times to calculate tilt
        :type t: list or datetime
        :returns: positive sunward dipole tilt, in degrees, for each time
        :rtype: list
        """
        t = spacepy.time.Ticktock(t)
        c_sm = spacepy.coordinates.Coords([[0, 0, 1.0]] * len(t), 'SM', 'car',
                                          ticks=t)
        c_gsm = c_sm.convert('GSM', 'car')
        return numpy.rad2deg(numpy.arctan2(c_gsm.x, c_gsm.z))

        # print(tilt(spacepy.time.tickrange('2008-03-08T10:00:00', '2008-03-08T22:00:00', datetime.timedelta(hours=1))))
        # print(tilt(datetime.datetime(2016, 3, 3)))
        # print(tilt([datetime.datetime(2016, 3, 1) + datetime.timedelta(days=i) for i in range(7)]))
    def testTilt(self):
        GridGraph.tilt(self, [datetime.datetime(2016, 3, 1) + datetime.timedelta(days=i)
            for i in range(7)])
    def simpleTest(self):
        # utility test function
        # print("sampleGrid", self.all_nodes)
        node1 = self.all_nodes[0]
        # print("node", node1)
        # print("neighbors", self.neighbors(node1))
        parents = self.breadth_first_search((0,0),(1999,125))
        # print("parents", parents)

        # note depending on how big the grid is, using bfs is very slow
        path = self.reconstruct_path(parents,(0,0),(1999,125))
        print("path",path)


if __name__ == "__main__":
    # GridGraph(2000,1000).simpleTest()
    GridGraph(2000,1000).testTilt()

    # some of the unanswered questions here are how do we relate translation in (x,y,z)_GSE
    # to motion on the map? The baseline attitude track is determined by the normal vector on the ellipse
    # that defines the orbit.
