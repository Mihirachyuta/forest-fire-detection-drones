import numpy as np
import math

#array for forest grid
forest=np.zeros((16,16))
reference_arr=np.zeros((16,16))
drone_arr=[]
fire=np.zeros((256,2))

#array for probable locations of fire
fire_prob=np.zeros((256,2))
fp_p=0

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
    global fire_prob
    global fp_p
    for i in range(-1,2):
        for j in range(-1,2):
            tmp_x=a+i
            tmp_y=b+j
            if(tmp_x!=a or tmp_y!=b):
                if(tmp_x<16 and tmp_y<16 and tmp_y>-1 and tmp_x>-1):
                    fire_prob[fp_p][0]=tmp_x
                    fire_prob[fp_p][1]=tmp_y
                    fp_p+=1
    

#function for map routing to move from source to destination


#Calculate distance function
def findDistance(source_x,source_y,dest_x,dest_y):
    return math.sqrt((source_x-dest_x)**2+(source_y-dest_y)**2)
    

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