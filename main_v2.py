

import numpy as np
import math




#array for forest grid
forest=np.zeros((16,16))
reference_arr=np.zeros((16,16))
drone_arr=[]
fire=[]

#array for probable locations of fire
fire_prob=np.zeros((256,2))
fp_p=0

#array that shows the current locations of free drones
free_Drone_local=[]
no_free_drones=8
drone_locations=[]
drone_next_locations=[]
#Array for locations checked
#array for fire found

#Calculate distance function
def findDistance(source_x,source_y,dest_x,dest_y):
    return math.sqrt((source_x-dest_x)**2+(source_y-dest_y)**2)
    


#Add probable locations of fire
def newpoint(a,b):
    global fire_prob
    global fp_p
    for i in range(-1,2):
        for j in range(-1,2):
            y=True
            tmp_x=a+i
            tmp_y=b+j
            #print(tmp_x,tmp_y)
            if(tmp_x!=a or tmp_y!=b):
                if(tmp_x<16 and tmp_y<16 and tmp_y>-1 and tmp_x>-1):
                    #print(fp_p,tmp_x,tmp_y)
                    for z in range(0,256):
                        if fire_prob[z][0]==tmp_x and fire_prob[z][1]==tmp_y:
                            y=False
                    if y:
                        fire_prob[fp_p][0]=tmp_x
                        fire_prob[fp_p][1]=tmp_y
                        fp_p+=1

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
    #For whether the drones needs to be assigned again
    is_assigned= False
    def __init__(self) -> None:
        pass


    #Move function - move one cell at a time
    # def move(self):
    #     self.x=self.dest_route[self.route_path_point][0]
    #     self.y=self.dest_route[self.route_path_point][1]
    #     self.route_path_point+=1

    def move(self):
        global drone_locations
        global drone_next_locations
        if self.x==self.dest_x and self.y==self.dest_y:
            return
        points,distances=path_plan(self.x,self.y,self.dest_x,self.dest_y)
        #print(points)
        for x in range(0,len(points)):
            if points[x] not in drone_locations and points[x] not in drone_next_locations:
                break
        self.x=points[x][0]
        self.y=points[x][1]

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
        global no_free_drones
        status=reference_arr[int(self.x)][int(self.y)]
        if(status==1):
            fire.append([int(self.x),int(self.y)])
            forest[int(self.x)][int(self.y)]=1
            self.is_assigned=False
            no_free_drones+=1
            newpoint(self.x,self.y)
            for j in range(0,fp_p):
                if(self.x==fire_prob[j][0] and self.y==fire_prob[j][1]):
                    pass #remove from the array

#Assignment of probable location
def assign():
    global no_free_drones
    global drone_arr
    global fire_prob
    while(no_free_drones>0):
        for i in range(0,9):
            if(drone_arr[i].is_assigned==False):
                #print(i)
                min_dist=100
                for j in range(0,fp_p):
                    d=findDistance(drone_arr[i].x,drone_arr[i].y,fire_prob[j][0],fire_prob[j][1])
                    #print(d,i)
                    if(d<min_dist):
                        min_dist=d
                        drone_arr[i].dest_x=fire_prob[j][0]
                        drone_arr[i].dest_y=fire_prob[j][1]
                drone_arr[i].is_assigned=True
                no_free_drones-=1
                print("Num free drones: ",no_free_drones)
                



    

#function for map routing to move from source to destination
def path_plan(source_x,source_y, dest_x,dest_y):
    tmp_points=[]
    tmp_distances=[]
    points=[]
    distances=[]
    for i in range(-1,2):
        for j in range (-1,2):
            tmp_x=source_x+i
            tmp_y=source_y+j
            if(tmp_x<16 and tmp_y<16 and tmp_y>-1 and tmp_x>-1):
                continue
            if(tmp_x==source_x and tmp_y==source_y):
                continue
            dist=findDistance(tmp_x,tmp_y,dest_x,dest_y)
            tmp_points.append([tmp_x,tmp_y])
            tmp_distances.append(dist)
    for i in range(0,len(tmp_points)):
        indexed=tmp_distances.index(min(tmp_distances))
        points.append(tmp_points[indexed])
        distances.append(tmp_distances[indexed])
        tmp_distances.remove(distances[i])
        tmp_points.remove(points[i])
    return points, distances
            


reference_arr[4][4]=1
reference_arr[4][3]=1
reference_arr[4][2]=1
reference_arr[3][3]=1
reference_arr[3][2]=1
reference_arr[3][1]=1
reference_arr[2][3]=1
reference_arr[2][2]=1
reference_arr[1][2]=1

reference_arr[3][10]=1
reference_arr[3][11]=1
reference_arr[3][12]=1
reference_arr[4][11]=1
reference_arr[4][12]=1
reference_arr[5][12]=1

print(reference_arr)
#main
for i in range(0,9):
    drone_arr.append(Drone())
    drone_arr[i].setid(i)
print(no_free_drones)
fire.append([3,2])
newpoint(3,2)
#print(fire_prob)
for i in range(0,8):
    drone_arr[i].assign(fire_prob[i][0],fire_prob[i][1])
    no_free_drones-=1
    drone_arr[i].is_assigned=True
    #print(drone_arr[i].x,drone_arr[i].y)
    drone_arr[i].check()

print(no_free_drones)

#print("fire_prob",fire_prob)

#Cycle start
#drones check existing location
# for i in range(0,9):
#     drone_arr[i].assign()
#     drone_arr[i].move()
#     drone_arr[i].check()
x=0
while x<50:
    assign()
    for i in range(0,9):
        #print(drone_arr[i].dest_x,drone_arr[i].dest_y)
            drone_arr[i].assign(drone_arr[i].dest_x,drone_arr[i].dest_y)
            #print(drone_arr[i].x,drone_arr[i].y)
            drone_arr[i].check()
    x+=1

    # for i in range(0,9):
    #     if(drone_arr[i].is_assigned==False):
    #         print(i)
# x=0
# while x<50:
#     assign()
#     #print(x," ",end='')
#     for i in range(0,9):
#         drone_arr[i].move()
#         drone_arr[i].check()
#     x+=1

print("reference:")
print(reference_arr)
print()
print("Forest")
print(forest)

# print("Fire")
# print(fire_prob)
