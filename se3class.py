# construct the se3 group as a class
import numpy as np
class SpecialEuclidean:
    # The SpecialEuclidean class forms the matrix so you can
    # rotate or translate a rigid body
    def __init__(self, tht=0, phi=0, psi=0, x=0, y=0, z=0):
        self.tht = tht
        self.phi = phi
        self.psi = psi
        self.x = x
        self.y = y
        self.z = z
        self.so3 = self.getso3()

    # rotation matrices defined http://mathworld.wolfram.com/RotationMatrix.html
    def R1(self, angle):
        # rotation about x1 axis (typically the x axis)
        return np.matrix([[1, 0, 0],[0, np.cos(angle), np.sin(angle)],[0, -np.sin(angle), np.cos(angle)]])
    def R2(self, angle):
        # rotation about the x2 axis (typically the y axis)
        return np.matrix([[np.cos(angle), 0, -np.sin(angle)],[0,1,0],[np.sin(angle), 0, np.cos(angle)]])
    def R3(self, angle):
        # rotation about the x3 axis (typically the z axis)
        return np.matrix([[np.cos(angle), np.sin(angle), 0],[-np.sin(angle), np.cos(angle), 0],[0, 0,1]])
    def getso3(self, order=(3,1,3)):
        # for now, lets just assume a rotation order
        # classic euler angle is xzx
        print(self.tht)
        thtRot = self.R3(self.tht)
        phiRot = self.R1(self.phi)
        psiRot = self.R3(self.psi)

        # do the matrix multiplication
        so3 = np.dot(thtRot,np.dot(phiRot,psiRot))
        return so3
    def getTranslation(self):
        # builds the translation part of the se3 matrix
        return np.matrix([[self.x],[self.y],[self.z]])

    def getse3(self):
        # combines everything together to get the SE(3) matrix
        # so3 = self.getso3()
        translation = self.getTranslation()
        zeroMatrix = np.matrix([0,0,0])
        oneMatrix = np.matrix([1])
        # print("se3 top shape", self.so3.shape)
        # print("translation shape", translation.shape)
        se3top = np.hstack((self.so3,translation))
        se3bottom = np.hstack((zeroMatrix, oneMatrix))
        se3 = np.vstack((se3top,se3bottom))
        return se3

# lets make a set of points thats a circle
def makeCircle(radius):
    # forms the se3 compatible set of points for buildling a circle
    # in the xy plane
    # the parameterized equation for a circle is
    length = 100
    t = np.linspace(-2*np.pi, 2*np.pi, 100)

    x = radius*np.cos(t)
    y = radius*np.sin(t)
    # make the z dimension
    z = np.zeros(length)
    onesFiller = np.ones(length)
    return np.array([[x],[y],[z],[onesFiller]])

def circleTest():
    points = makeCircle(5)
    print("points dimension", points.shape)
    print("points index", points[0][0].shape)
    rt = SpecialEuclidean(0,np.pi/2,0,2,1,-15).getse3()

    # the "matrix" data type allows you to operate on a ton of elements
    # all at the same time which is why its so dope
    points2 = rt*points

    # array type is way easier to plot than matrix type
    # so just cast it as an ARRAY
    points2 = np.array(points2)
    print("p2", points2)
    print("p2 dimension", points2.shape)
    # points2 = np.dot(rt,points)
    #points2 = np.array([])
    # for i in range(0,len(points[0][0])):
    #    points2.append(points[])

    print("points2", points2)
    # print("points2 dim"points2.shape)
    fig = plt.figure()
    ax = fig.add_subplot(111,projection='3d')
    print("length",len(points))
    for p in range(0,len(points[0])):
        ax.scatter(points[0][p], points[1][p], points[2][p])
    for q in range(0, len(points2[0])):
        ax.scatter(points2[0][q], points2[1][q], points2[2][q])
    plt.show()

def simpleTest():
    rt = SpecialEuclidean(np.pi/2, 0, 0, 1, 0, 0).getse3()
    # print("rt", rt.size)
    # make a sample coordinate
    x1 = np.array([[1],[0],[0],[1]])
    x2 = np.dot(rt,x1)
    print("x1",x1)
    print("x2",x2)
    fig = plt.figure()
    ax = fig.add_subplot(111,projection='3d')
    ax.scatter(x1[0],x1[1],x1[2])
    ax.scatter(x2[0],x2[1],x2[2])
    plt.show()

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    # simpleTest()
    circleTest()


    # yes and from here I think I can just operate on lists of points that
    # define the obstacles as sets of points
    # I can actually use the output of GMAT to animate this thing attitude motion
