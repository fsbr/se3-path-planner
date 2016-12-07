# try to build a graph s.t I can assign arbitrary coordinate labels to it
# like for now, I can just have a grid -n to n, or 0,n or something.

#building queue class from http://www.redblobgames.com/pathfinding/a-star/implementation.html
import collections
import datetime

import numpy as np
import spacepy.coordinates
import spacepy.time
import matplotlib.pyplot as plt


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
    def __init__(self,max_x=10,max_y=10):
        self.all_nodes = []

        # define total area
        self.max_x = max_x
        self.max_y = max_y
        
        # this also works with range argument (-maxx, maxx), (-maxy,maxy) etc.
        for x in range(self.max_x):
            for y in range(self.max_y):
                self.all_nodes.append((x,y))
        self.all_nodes = tuple(self.all_nodes)
        # define obstacles
        self.obstacles = [(2,0), (3,0),(4,0),(2,1),(3,1),(4,1),(2,2),(3,2),(4,2),(14,11)]
        # self.obstacles = []
        # self.obstacles = self.getObstacles()
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
    
    def sunLocation(threshold):
        # the idea is that this defines an angular position of the sun. 
        # what I really want to do is get the sun vector in GSE coordinates

        # the sun center point is on the end of the x unit vector 
        # sunVector np.array([1,0,0])
        pass
          

    def getObstacles(self, model="grid"):
        # this function has the purpose of automating the different obstacles
        # this corresponds to the location of the sun.
        # generates obstacles of a certain shape 
        obstacles = [] 
        startPoint = (2,2)
        start_x = startPoint[0]
        start_y = startPoint[1]
        # print("startx", start_x)
        # print("starty", start_y)
        # make a 10x10 grid
        length_x = 10 
        length_y = 15
        for x in range(0,length_x):
            for y in range(0,length_y):
                obstacles.append([start_x+x, start_y+y])
        obstacles = tuple(obstacles)
        # print("obstacles list,",obstacles)
        return obstacles

    def getGoalRegion(self,time,model="tsyganenko"):
        # input the modified julian time
        # output the lower bound, upper bound, and lateral bounds in radians
        # this function will return the goal location, based on the cusp location from the tsyganenko model
        # also i guess i'd incorporate that guys rotating dipole model here.
        # the coordinates are cylindrical but you can convert to GSM
        
        # eventually needs to take in the time as well

        # legacy "test" outputs use to test function 
        lowBound = 0.2151       # s
        highBound = 0.2849      # s
        
        # threshold 
        thresh = 2*np.pi/180 # two degrees converted to radians
        lateralBound = 2.0*np.pi/180      # s

        

        ### THIS STUFF IS ALL IN THE SOLAR MAGNETIC FRAME
        pi = np.pi              # s
        # its just one equation so i'll try to plot it and see what happens
        re = 6370               # s
        # r = np.linspace(1, 10,1000)     # v 
        r = re+150
        psi = 0#np.linspace(-pi/2,pi/2)#0
        a1 = 0.1287
        a2 = 0.0314
        phi_c0 = 0.24
        phi_1 = phi_c0-(a1*psi + a2*psi**2)  # 75 degrees  
        # print("phi_1",phi_1)
        num = np.sqrt(r)
        # den = np.sqrt(r + 1/np.arcsin(phi_1)**2 - 1)
        den = np.sqrt(r + 1/np.sin(phi_1)**2 - 1)
        # print num/den
        t = spacepy.time.Ticktock(time,'MJD')
        # print("time object,", t)
        # print("TIME original input", time)
        phi_c = np.arcsin(num/den) + self.tilt(t)*np.pi/180
        phi_cdeg = 180*phi_c/np.pi # + self.tilt(time)
        phi_c = phi_c[0]
        # print("PHI_C", phi_c)

        print("about to start plotting!")
        plt.plot(time,phi_cdeg)
        plt.show()

        print("i'm done plotting!")
        # somewhere in here i do the coordinate transformation
        # print("phi_c", phi_c)
        # print("phi_cdeg =,", phi_cdeg)        
        
        # verify these coordinates with the tsyganenko paper
        Zsm = np.cos(phi_c).tolist()
        Xsm = np.sin(phi_c).tolist()

        c_sm = spacepy.coordinates.Coords([[Xsm, 0, Zsm]]*len(t), 'SM', 'car', ticks=t)
        c_gse = c_sm.convert('GSE', 'car')
        
        # need  a way to implement t with this coordinate transform

        # the fact that I'm using [0] here means we aren't using the dinural change
        newPhi_c = np.arctan2(c_gse.x, c_gse.z)[0]
        latVector = np.arctan2(c_gse.y, c_gse.x)[0] 
        # possible dimensions problem here
        # print("newPhi_c", newPhi_c)
        lowbound = newPhi_c - thresh
        highBound = newPhi_c + thresh
        lowLateralBound = latVector - thresh
        highLateralBound = latVector + thresh
 
        # plt.plot(r,phi_c)
        # plt.xlabel('distance (r), earth radii')
        # plt.title('Cusp Geometric Properties')
        # plt.ylabel('zenith angle phi_c')
        # print("phi_c in degrees", phi_cdeg)
        # plt.show()
        #print("phi_c =", 180*phi_c/np.pi)

        # okay I get that the actual value is VERY low
        # that might be good, or maybe its bad i'm not sure exactly how to
        # check but I was expecting a value around 15 deg
        # i get what I think would be the "right" result if I use earth radii
        return lowBound, highBound, lowLateralBound, highLateralBound
    def tilt(self,t):
        # Get dipole tilt for time or range of times
        # :param t: time or times to calculate tilt
        # :type t: list or datetime
        # :returns: positive sunward dipole tilt, in degrees, for each time
        # :rtype: list
        # print("t before,", t)
        t = spacepy.time.Ticktock(t,'MJD')
        # print("important time part", t)
        c_sm = spacepy.coordinates.Coords([[0, 0, 1.0]] * len(t), 'SM', 'car',
                                          ticks=t)
        c_gsm = c_sm.convert('GSM', 'car')
        c_gse = c_sm.convert('GSE', 'car')
        
        # j niehof originally used c_gsm
        return np.arctan2(c_gse.x, c_gse.z)
 

    def testTilt(self):
        GridGraph.tilt(self, [datetime.datetime(2016, 3, 1) + datetime.timedelta(days=i)
            for i in range(7)])
    def simpleTest(self):
        # utility test function
        # print("sampleGrid", self.all_nodes)
        node1 = self.all_nodes[0]
        # print("node", node1)
        # print("neighbors", self.neighbors(node1))
        parents = self.breadth_first_search((0,0),(15,12))
        # print("parents", parents)

        # note depending on how big the grid is, using bfs is very slow
        path = self.reconstruct_path(parents,(0,0),(15,12))
        print("path",path)


if __name__ == "__main__":
    
    # need to specify the UNITS for this thing
    GridGraph(60,40).simpleTest()
    # GridGraph(20,10).testTilt()

    # print(GridGraph().tilt(spacepy.time.tickrange('2008-03-08T10:00:00', '2008-03-08T22:00:00', datetime.timedelta(hours=1))))
    # print(GridGraph().tilt(datetime.datetime(2016, 3, 3)))
    # print(GridGraph().tilt([datetime.datetime(2016, 3, 1) + datetime.timedelta(days=i) for i in range(7)]))


    # YUMMMMM
    # basically to get my code to work, i'll just make it take in a julian time instead of a datetime object




    #GridGraph()
    # some of the unanswered questions here are how do we relate translation in (x,y,z)_GSE
    # to motion on the map? The baseline attitude track is determined by the normal vector on the ellipse
    # that defines the orbit.
