# try to build a graph s.t I can assign arbitrary coordinate labels to it
# like for now, I can just have a grid -n to n, or 0,n or something.

#building queue class from http://www.redblobgames.com/pathfinding/a-star/implementation.html
import time
import collections
import datetime
import heapq
import numpy as np
import spacepy.coordinates
import spacepy.time
import matplotlib.pyplot as plt
# from implementation import *
import timeit as ti
class PriorityQueue:
    def __init__(self):
        self.elements = []
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self):
        return heapq.heappop(self.elements)[1]

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
    def __init__(self,width=10,height=10):
        self.all_nodes = []

        # define total area
        self.width = width
        self.height = height
        
        # this also works with range argument (-maxx, maxx), (-maxy,maxy) etc.
        for x in range(self.width):
            for y in range(self.height):
                self.all_nodes.append((x,y))
        self.all_nodes = tuple(self.all_nodes)
        # define obstacles
        # self.obstacles = [(2,0), (3,0),(4,0),(2,1),(3,1),(4,1),(2,2),(3,2),(4,2),(14,11)]
        self.obstacles = []
        self.obstacles = self.getObstacles()
        print("self.obstacles", self.obstacles)
        
        # trying to apply uniform cost 1 to the grid
        # self.weights = {w: 1 for w in self.all_nodes}
        # self.weights = {w: 50 for w in self.obstacles}
    def in_bounds(self, id):
        (x,y) = id
        return 0<=x < self.width and 0 <= y < self.height

    def passable(self, id):
        # true if the id isn't an obstacle
        return id not in self.obstacles

    def neighbors2(self, id, connectivity, reverse):
        # the main difference between this one and the original one is that
        # the configuration space coordinates are immutable this way
        (x,y) = id

        # different forms of connectivity 8
        # results = [(x+1, y),(x+1, y+1), (x, y+1),(x-1, y), (x-1, y+1), (x-1, y-1), (x, y-1), (x+1,y-1)]
        # results = [(x+1,y), (x+1,y+1), (x,y+1), (x-1,y+1), (x-1,y),(x-1,y-1), (x,y-1), (x+1,y-1)]

        # very important to search the cardinal directionsi first

        if connectivity == 8:
            results = [(x+1,y), (x-1,y), (x,y+1), (x,y-1), (x+1,y+1), (x-1,y+1), (x-1,y-1), (x+1,y-1)]
        # different forms of connectivity 4        
        elif connectivity == 4:
            results = [(x+1,y), (x-1,y), (x,y+1),(x,y-1)]
        else:
            print("invalid connectivity")

        if reverse==1:
            if (x+y) % 2 == 0: 
                results.reverse()
        elif reverse ==0:
            pass
        else:
            print("invalid reversal state")
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
        print("current", current)
        path = [current]
        print("path", current)
        while current != start:
            current = came_from[current]
            #print("current", current)
            path.append(current)
        path.append(start) # optional
        path.reverse() # optional
        return path

    def breadth_first_search(self, start, goal,connectivity=4, reverse=0):
        frontier = Queue()
        frontier.put(start)
        came_from = {}
        came_from[start] = None

        while not frontier.empty():
            current = frontier.get()
            # print("current",current)
            if current == goal:
                break

            for next in self.neighbors2(current,connectivity, reverse):
                if next not in came_from:
                    frontier.put(next)
                    came_from[next] = current

        return came_from
    def dijkstras_search(self,start,goal,connectivity=8,reverse=0):
        frontier = PriorityQueue()
        frontier.put(start, 0)
        came_from = {}
        came_from[start] = None

        while not frontier.empty():
           current = frontier.get()

           if current == goal:
              break
           
           for next in self.neighbors2(current, connectivity, reverse):
              if next not in came_from:
                 priority = self.heuristic(goal, next)
                 frontier.put(next, priority)
                 came_from[next] = current
        return came_from
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

        # the sun is always on the x axis
        startPoint = (self.width/2,self.height/2)
        print("self.width/2", self.width/2)
        print("self.height/2", self.height/2)
        start_x = startPoint[0]
        start_y = startPoint[1]
        # print("startx", start_x)
        # print("starty", start_y)
        # make a 10x10 grid
        length_x = 10 
        length_y = 10
        for x in range(-length_x,length_x):
            for y in range(-length_y,length_y):
                obstacles.append((start_x+x, start_y+y))
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


        # accounting for GMAT offset
        # time = [t + 29999.5 for t in time]
        print("new time vector")
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

        # alternate form due to "handwriting"
        # den = np.sqrt(r + 1/np.arcsin(phi_1)**2 - 1)
        den = np.sqrt(r + 1/np.arcsin(phi_1)**2 - 1)
        # print num/den
        t = spacepy.time.Ticktock(time,'MJD')
        # print("time object,", t.UTC)
        # print("TIME original input", time)


        ### SOMETHING IS WRONG IN TSYGANENKO
        # phi_c gets made into a vector here
        # phi_c is in the solar magnetic coordinates
        # phi_c = np.arcsin(num/den) #+ self.tilt(t)*np.pi/180
        phi_c = np.arcsin(num/den) + 0*self.tilt(t)*np.pi/180
        phi_cdeg = 180*phi_c/np.pi # + self.tilt(time)
        # phi_c = phi_c[0]
        print("PHI_C", phi_c)
        print("phi_cdeg", phi_cdeg)

        # verify these coordinates with the tsyganenko paper
        #Zsm = np.cos(phi_c)
        Zsm = np.sin(phi_c)
        #Xsm = np.sin(phi_c)
        Xsm = np.cos(phi_c)
        Ysm = [0]*len(Xsm) 
        print("zsm", Zsm)
        # change the dimensions of the coordinate vector
        # there's probably a nice way to do that with .shape
        print("about to try coordinate dimension change")
        coordinates_sm = [[i,j,k] for i,j,k in zip(Xsm, Ysm, Zsm)]
        # print("final coordinates", coordinates_sm)
        # c_sm = spacepy.coordinates.Coords([[Xsm, 0, Zsm]], 'SM', 'car', ticks=t)
        # c_gsm = spacepy.coordinates.Coords([[Xsm, 0, Zsm]], 'GSM', 'car', ticks=t)
        c_gse = spacepy.coordinates.Coords(coordinates_sm, 'SM', 'car', ticks=t)
        # print("END FOR NOW", [[Xsm, [0 for elements in t], Zsm]])
        c_gse = c_gse.convert('GSE', 'car')
        c_gsm = c_gse.convert('GSM', 'car')
        c_sm = c_gse.convert('SM', 'car')

        # print("shape of xgse", c_gse.x.shape)
        # print("shape of zgse", c_gse.z.shape)
        xgse = np.asarray(c_gse.x).tolist()
        ygse = np.asarray(c_gse.y).tolist()
        zgse = np.asarray(c_gse.z).tolist()

        xgsm = np.asarray(c_gse.x).tolist()
        ygsm = np.asarray(c_gse.y).tolist()
        zgsm = np.asarray(c_gse.z).tolist()

        xsm = np.asarray(c_sm.x).tolist()
        ysm = np.asarray(c_sm.y).tolist()
        zsm = np.asarray(c_sm.z).tolist()
        # print("type of gse coordinate vector", type(c_gse.x))
        # print("gse coordinate vector", xgse)
    
        print('gsex', c_gse.x.shape)
        print('gsey', c_gse.y.shape)
        print('gsez', c_gse.z.shape)
        print('time', len(time))

        # originally i used only a single x and z value here but now
        # i'll try the vector version
        phi = np.arctan2(xsm, zsm) 
        phigsm = np.arctan2(xgsm, zgsm)
        
        theta = np.arctan2(ygse,xgse)
        plt.plot(t.UTC,phi)
        # plt.plot(c_gsm.z, c_gsm.x)
        # plt.show()
        
        print("i'm done plotting!")
        
        # need  a way to implement t with this coordinate transform

        # the fact that I'm using [0] here means we aren't using the dinural change
        # this needs to change the boundary every time step and it's not
        # newPhi_c = np.array(np.arctan2(c_gse.x, c_gse.z))
        newPhi_c = np.array(np.arctan2(c_sm.z, c_sm.x))
        # latVector = np.array(np.arctan2(c_gse.y, c_gse.x))
        latVector = np.array(np.arctan2(c_sm.x, c_sm.y))
        print("type of phi_c", type(np.array(newPhi_c)))
        print("type of latevector", type(latVector))
        # possible dimensions problem here
        # print("newPhi_c", newPhi_c)
        lowBound = newPhi_c - thresh
        highBound = newPhi_c + thresh
        # lowbound = phi - thresh
        # highbound = phi + thresh
        # lowLateralBound = theta - thresh
        # highLateralBound = theta + thresh
        lowLateralBound = latVector - thresh
        highLateralBound = latVector + thresh
 
        # plt.plot(r,phi)
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

    def simpleGoalRegion(self):
        # return theta = 0, phi = 78 degrees latitude
        # need to include offsets because the coordinate system here is only
        # positive integers
        theta =0
        phi = 78
        return (self.width/2,phi)
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
        return np.arctan2(c_sm.x, c_sm.z)
 

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
    
    def draw_graph(self):
        # trying to draw the grid
        for y in range(self.max_y):
            for x in range(self.max_x):
                print("#")
            print("\n")
    
    def heuristic(self,a, b):
        # implements the manhattan distance
        (x1, y1) = a
        (x2, y2) = b
        return abs(x1 - x2) + abs(y1 - y2)

# def timing(f):
#     print("used timing function")
#     def wrap(*args):
#         time1 = time.time()
#         ret = f(*args)
#         time2 = time.time()
#         print('%s function took %0.3f ms' % (f.__name__, (time2-time1)*1000.0))
#         return ret
#     return wrap
class GridWithWeights(GridGraph):
    def __init__(self, width, height):
        super().__init__(width, height)
    
        self.weights = {}
    
    def cost(self, from_node, to_node):
        return self.weights.get(to_node, 1)
    def a_star_search(self, start, goal,connectivity=4, reverse=1):
        # i'll add this in later if needed

        frontier = PriorityQueue()
        frontier.put(start, 0)
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0
        
        while not frontier.empty():
            # print("is frontier empty???,", frontier.empty())
            current = frontier.get()
            # print("current is", current)
            
            if current == goal:
                # print("current == goal", current==goal)
                break
            
            for next in self.neighbors2(current,connectivity,reverse):
                # im hoping to indicate uniform cost 1 by just saying its 1
                new_cost = cost_so_far[current] +  self.cost(current, next)
                # print("next is ,",new_cost)
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    # print("dont give up")
                    cost_so_far[next] = new_cost
                    priority = new_cost + self.heuristic(goal, next)
                    
                    # print("priority",self.heuristic(goal,next))
                    frontier.put(next, priority)
                    came_from[next] = current
            # print("came from ", came_from)
            # print("ccost so far ", cost_so_far)
        # print("frontier", frontier.empty())
        return came_from, cost_so_far

if __name__ == "__main__":
    # need to specify the UNITS for this thing
    # g = GridGraph(180,90)
    g = GridWithWeights(180,90)
    g.weights = {loc: 5 for loc in [(3, 4), (3, 5), (4, 1), (4, 2),
                                       (4, 3), (4, 4), (4, 5), (4, 6), 
                                       (4, 7), (4, 8), (5, 1), (5, 2),
                                       (5, 3), (5, 4), (5, 5), (5, 6), 
                                       (5, 7), (5, 8), (6, 2), (6, 3), 
                                       (6, 4), (6, 5), (6, 6), (6, 7), 
                                       (7, 3), (7, 4), (7, 5)]}

    # g.obstacles = [(0,0),(0,1), (1,1), (1,0)]
    # draw_grid(g)
    # s = (173,83)
    # e = (195,95) 
    e = g.simpleGoalRegion()
    print("goal region", e)
    
    # timerVals = []
    # for i in range(0,10):
    #     time1 = time.time()
    #     g.breadth_first_search(s,e)
    #     time2 = time.time()
    #     total_time = time2-time1
    #     print('function took %0.3f ms' % ((time2-time1)*1000.0))
    #     timerVals.append(total_time)
    # print("timer values = ", timervals)
    # print("mean time was", sum(timerVals)/len(timerVals))
    conn = [4,8]
    reverse = [0,1]
    xoff  = [5,45,90,135] 
    endOffs = [-1,1,-5,5, -7,7,-10,10]
    # endOffs = [0]
    # e1 = (90,78)
    # s1 = (90,0)
    # parents, costs = g.a_star_search(e1,s1) 
    for xoffs in endOffs:
        for c in conn:
            for r in reverse:
               
                e = (90, 78+xoffs)
               # hard coding for a*
                # e = (90,78)
                s = (90,0)
                # parents = g.breadth_first_search(s,e,c,r)
                parents, costs = g.a_star_search(s,e,c,r)
                # parents = g.dijkstras_search(s,e,c,r)
                # draw_grid(g, width=3, point_to=parents, start=s, goal=e)
                path = g.reconstruct_path(parents, s, e)
                # draw_grid(g, width=2, path=reconstruct_path(parents, s, e))
                print("paTH", path)

                x= [path[i][0] for i in range(0,len(path))]
                y = [path[i][1] for i in range(0,len(path))]
                
                obs = g.getObstacles()
                xo = [obs[i][0] for i in range(0,len(obs))]
                yo = [obs[i][1] for i in range(0,len(obs))]
                plt.plot(x, y)


    plt.scatter(xo,yo)
    plt.xlabel('Equirectangular longitude (deg)')
    plt.ylabel('Equirectangular latitude (deg)')
    plt.title('A* Paths for Varying Goal Location')
    plt.xlim([-180,180])
    plt.ylim([-90,90])
    plt.show()
    print("lenght of the path", len(path))

    ### the above i need
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
