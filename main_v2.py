import numpy as np

#array for forest grid
forest=np.zeros((16,16))
reference_arr=np.zeros((16,16))
drone_arr=[]
fire=[]

#array for probable locations of fire
fire_prob=np.array((256,2))

#array that shows the current locations of free drones
free_Drone_local=[]

#Array for locations checked
#array for fire found


#define drone class
class Drone:
    #variables
    #current location
    x=0
    y=0
    #id
    id=0
    #destination location
    dest_x=0
    dest_y=0
    #route array
    dest_route=np.zeros((20,2))
    route_path_point=0

    def __init__(self) -> None:
        pass


    #Move function - move one cell at a time
    def move(self):
        self.x=self.dest_route[self.route_path_point][0]
        self.y=self.dest_route[self.route_path_point][1]
        self.route_path_point+=1

    #Assign location
    def assign(self,a,b):
        self.x=a
        self.y=b
    #set id
    def setid(self,id):
        self.id=id
    #checkFire
    def check(self):
        global reference_arr
        global fire
        global forest
        status=reference_arr[int(self.x)][int(self.y)]
        if(status==1):
            fire.append([int(self.x),int(self.y)])
            forest[int(self.x)][int(self.y)]=1
            newpoint(self.x,self.y)

#Add probable locations of fire
def newpoint(a,b):
    global fire
    global assignd
    global fa
    global fb
    pass
    

#function for map routing to move from source to destination


#Calculate distance function
def findDistance(source_x,source_y,dest_x,dest_y):
    pass
    

#main
for i in range(0,9):
    drone_arr.append(Drone())
    drone_arr[i].setid(i)

fire.append([7,5])
newpoint(7,5)

#Cycle start
#drones check existing location
for i in range(0,9):
    drone_arr[i].move()
    drone_arr[i].check()