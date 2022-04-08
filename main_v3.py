import numpy as np
import math




#array for forest grid
forest=np.zeros((16,16))
reference_arr=np.zeros((16,16))
drone_arr=[]
fire=[]

#array for probable locations of fire
fire_prob=[]
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

#Setting direction
def get_direction(i,j):
    if(i == -1):
        if(j==-1):
            return 0 #NW
        if(j==0):
            return 1 #N
        if(j==1):
            return 2 #NE
    if(i == 0):
        if(j==-1):
            return 3 #E
        if(j==1):
            return 4 #SE
    if(i == 1):
        if(j==-1):
            return 5 #S
        if(j==0):
            return 6 #SW
        if(j==1):
            return 7 #W



#Add probable locations of fire
def newpoint(a,b):
    global fire_prob
    global fp_p
    for i in range(-1,2):
        for j in range(-1,2):
            y=True
            tmp_x=a+i
            tmp_y=b+j
            dir=get_direction(i,j)
            #print(tmp_x,tmp_y)
            if(tmp_x!=a or tmp_y!=b):
                if(tmp_x<16 and tmp_y<16 and tmp_y>-1 and tmp_x>-1):
                    #print(fp_p,tmp_x,tmp_y)
                    for z in range(0,len(fire_prob)):
                        if fire_prob[z][0]==tmp_x and fire_prob[z][1]==tmp_y:
                            y=False
                    if y:
                        fire_prob.append([tmp_x,tmp_y,dir])
                        fp_p+=1

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
            if not (tmp_x<16 and tmp_y<16 and tmp_y>-1 and tmp_x>-1):
                # print("h",tmp_x,tmp_y)
                continue
            if(tmp_x==source_x and tmp_y==source_y):
                continue
            dist=findDistance(tmp_x,tmp_y,dest_x,dest_y)
            tmp_points.append([tmp_x,tmp_y])
            tmp_distances.append(dist)
    # print("tmp_points",tmp_points)
    for i in range(0,len(tmp_points)):
        indexed=tmp_distances.index(min(tmp_distances))
        points.append(tmp_points[indexed])
        distances.append(tmp_distances[indexed])
        tmp_distances.remove(distances[i])
        tmp_points.remove(points[i])
    return points, distances


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
    dir=0
    #route array
    dest_route=np.zeros((20,2))
    route_path_point=0
    #For whether the drones needs to be assigned again
    is_assigned= False
    is_goal_reached=False

    def __init__(self) -> None:
        pass
    
    def move_in_ripple(self):
        tmp_x=self.x
        tmp_y=self.y
        if(self.dir==0 or self.dir==7 or self.dir==6):
            tmp_x-=1
        if(self.dir==2 or self.dir==3 or self.dir==4):
            tmp_x+=1
        if(self.dir==0 or self.dir==1 or self.dir==2):
            tmp_y-=1
        if(self.dir==4 or self.dir==5 or self.dir==6):
            tmp_y+=1
        # print("tmp",tmp_x,tmp_y)
        if(tmp_x<16 and tmp_y<16 and tmp_y>-1 and tmp_x>-1):
            self.x=tmp_x
            self.y=tmp_y
        else:
            self.is_assigned=False
            self.is_goal_reached=False
        
        



    def move(self):
        global drone_locations
        global drone_next_locations
        if self.is_goal_reached:
            self.move_in_ripple()
            return
        # print("dest ",self.dest_x,self.dest_y)
        # if not self.is_assigned:
        #     return
        # if self.x==self.dest_x and self.y==self.dest_y:
        #     return
        points,distances=path_plan(self.x,self.y,self.dest_x,self.dest_y)
        # print(points)

        for x in range(0,len(points)):
            if points[x] not in drone_locations and points[x] not in drone_next_locations:
                break
        self.x=points[x][0]
        self.y=points[x][1]
        if(self.x==self.dest_x and self.y==self.dest_y):
            self.is_goal_reached=True
    
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
            # self.is_assigned=False
            # no_free_drones+=1
            newpoint(self.x,self.y)
            for j in range(0,len(fire_prob)):
                if(self.x==fire_prob[j][0] and self.y==fire_prob[j][1]):
                    fire_prob.remove([self.x,self.y,self.dir]) #remove from the array
        else:
            self.is_assigned=False
            


#Assignment of probable location
def assign():
    global no_free_drones
    global drone_arr
    global fire_prob
    
    for i in range(0,len(drone_arr)):
        if(drone_arr[i].is_assigned==False):
            #print(i)
            min_dist=100
            for j in range(0,fp_p):
                d=findDistance(drone_arr[i].x,drone_arr[i].y,fire_prob[j][0],fire_prob[j][1])
                #print(d,i)
                if(d<min_dist):
                    min_dist=d
                    print(min_dist)
                    drone_arr[i].dest_x=fire_prob[j][0]
                    drone_arr[i].dest_y=fire_prob[j][1]
                    drone_arr[i].dir=fire_prob[j][2]
                    drone_arr[i].is_assigned=True
                    drone_arr[i].is_goal_reached=False

#Main
newpoint(7,8)
reference_arr[6][7]=1
print(fire_prob)

drone_arr.append(Drone())
drone_arr.append(Drone())
drone_arr.append(Drone())
drone_arr.append(Drone())
drone_arr[0].x=1
drone_arr[0].y=2
# drone_arr[0].dest_x=1
# drone_arr[0].dest_y=2
# drone_arr[0].dir=6
# drone_arr[0].is_assigned=False
assign()
print(drone_arr[0].is_assigned)
drone_arr[0].dir=2
for i in range(0,20):
    print(fire_prob)
    if(drone_arr[0].is_assigned):
        drone_arr[0].move()
    # print("dest",)
    if(drone_arr[0].is_goal_reached):
        drone_arr[0].check()
    print(drone_arr[0].x,drone_arr[0].y,drone_arr[0].dest_x,drone_arr[0].dest_y,drone_arr[0].dir,drone_arr[0].is_assigned)





