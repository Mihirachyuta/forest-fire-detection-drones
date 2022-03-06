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
no_free_drones=10


#Calculate distance function
def findDistance(source_x,source_y,dest_x,dest_y):
    return math.sqrt((source_x-dest_x)**2+(source_y-dest_y)**2)
    


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



#Assignment of probable location
def assign():
    global no_free_drones
    global drone_arr
    global fire_prob
    while(no_free_drones!=0):
            i=0
            if(drone_arr[i].is_assigned==False):
                min_dist=100
                for j in range(0,fp_p):
                    d=findDistance(drone_arr[i].x,drone_arr[i].y,fire_prob[j][0],fire_prob[j][1])
                    if(d<min_dist):
                        min_dist=d
                        drone_arr[i].dest_x=fire_prob[j][0]
                        drone_arr[i].dest_y=fire_prob[j][1]
                print(min_dist)
                drone_arr[i].is_assigned=True
            no_free_drones=0
                


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
    #For whether the drones needs to be assigned again
    is_assigned= False
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
        global fp_p
        global fire_prob
        status=reference_arr[int(self.x)][int(self.y)]
        if(status==1):
            fire.append([int(self.x),int(self.y)])
            forest[int(self.x)][int(self.y)]=1
            newpoint(self.x,self.y)
            for j in range(0,fp_p):
                if(self.x==fire_prob[j][0] and self.y==fire_prob[j][1]):
                    pass #remove from the array

drone_arr.append(Drone())
drone_arr[0].assign(9,10)
drone_arr[0].setid(0)
fire[0][0]=6
fire[0][1]=8
newpoint(6,8)
for i in range(0,fp_p):
    print(fire_prob[i][:])
assign()
print(drone_arr[0].dest_x,drone_arr[0].dest_y)