
import numpy as np
import math

#array for forest grid
forest=np.zeros((16,16))
reference_arr=np.zeros((16,16))
drone_arr=[]
fire=[]

#array for probable locations of fire
fire_prob=[]
free_Drone_local=[]
drone_locations=[]
checked_points=[]


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
    global checked_points
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
                    if [tmp_x,tmp_y] in checked_points :
                        y=False
                    if y:
                        fire_prob.append([tmp_x,tmp_y,dir])
                        # fp_p+=1


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

def assign():
    global drone_arr
    global fire_prob
    
    for i in range(0,len(drone_arr)):
        print(i,drone_arr[i].is_assigned)
        if(drone_arr[i].is_assigned==False):
            #print(i)
            min_dist=100
            for j in range(0,len(fire_prob)):
                d=findDistance(drone_arr[i].x,drone_arr[i].y,fire_prob[j][0],fire_prob[j][1])
                #print(d,i)
                if(d<min_dist):
                    min_dist=d
                    #print(min_dist)
                    drone_arr[i].dest_x=fire_prob[j][0]
                    drone_arr[i].dest_y=fire_prob[j][1]
                    drone_arr[i].dir=fire_prob[j][2]
                    drone_arr[i].is_assigned=True
                    drone_arr[i].is_goal_reached=False
                    tmp=j
            print(fire_prob)
            print("drone",i,"assigned to",fire_prob[tmp][0]," ",fire_prob[tmp][1])
            # try:
            #     fire_prob.remove(fire_prob[tmp])
            # except:
            #     pass
            # tp=[]
            # tp.append(fire_prob[tmp])        
            # fire_prob.remove(tp[0])
            

#drone class
class Drone():
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
    #For whether the drones needs to be assigned again
    is_assigned= False
    is_goal_reached=False

    def assign(self,a,b,c):
        self.x=a
        self.y=b
        self.dir=c
        self.is_assigned=True
        self.is_goal_reached=True
        self.check()

    def setid(self,i):
        self.id=i

    def check(self):
        global reference_arr
        global checked_points
        global fire_prob
        global fire
        global forest
        
        status=reference_arr[int(self.x)][int(self.y)]
        checked_points.append([self.x,self.y])

        if(status==1):
            fire.append([int(self.x),int(self.y)])  #Appending to fire array
            forest[int(self.x)][int(self.y)]=1  #changing the status to 1 to compare with ref_arr
            newpoint(self.x,self.y)  #Adding probable fire locations
        for j in range(0,len(fire_prob)):
            if(self.x==fire_prob[j][0] and self.y==fire_prob[j][1]):
                try:
                    fire_prob.remove(fire_prob[j])
                    break #remove from the fire_prob array
                except Exception as e:
                    print(e)

        else:
            self.is_assigned=False 
            self.is_goal_reached=False
    
    def path_plan_move(self):
        global drone_locations
        if not self.is_assigned:
            return
        points,distances=path_plan(self.x,self.y,self.dest_x,self.dest_y)

        for x in range(0,len(points)):
            if points[x] not in drone_locations:
                break

        #Changing location to move
        self.x=points[x][0]
        self.y=points[x][1]

        #Changing Drone location
        drone_locations[self.id][0]=self.x
        drone_locations[self.id][1]=self.x

        #Checking if the goal is reached 
        if(self.x==self.dest_x and self.y==self.dest_y):
            self.is_goal_reached=True
            self.check()

    def ripple_move(self):
        tmp_x=self.x
        tmp_y=self.y
        if self.is_assigned:
            if(self.dir==0 or self.dir==7 or self.dir==6):
                tmp_x-=1
            if(self.dir==2 or self.dir==3 or self.dir==4):
                tmp_x+=1
            if(self.dir==0 or self.dir==1 or self.dir==2):
                tmp_y-=1
            if(self.dir==4 or self.dir==5 or self.dir==6):
                tmp_y+=1
            if(tmp_x<16 and tmp_y<16 and tmp_y>-1 and tmp_x>-1):
                self.x=tmp_x
                self.y=tmp_y
            else:
                self.is_assigned=False

    def move(self):
        if self.is_goal_reached :
            self.ripple_move()
            self.check()
        else:
            self.path_plan_move()
        
        




#test

# reference_arr[5][5]=0
# reference_arr[8][8]=1
# reference_arr[8][8]=1

# drone=Drone()
# newpoint(7,8)
# drone.assign(5,5)

# for i in range(10):
#     pass



# print("Fire_prob: ",fire_prob)
# print("Fire :", fire)
# print("Checked: ", checked_points)
# print("is goal reached:",drone.is_goal_reached,"is assigned",drone.is_assigned)


### Main
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

forest[3][2]=1
fire.append([3,2])
checked_points.append([3,2])
newpoint(3,2)

for i in range(0,9):
    drone_arr.append(Drone())
    drone_arr[i].setid=i
    drone_arr[i].assign(fire_prob[i][0],fire_prob[i][1],fire_prob[i][2])
    drone_locations.append([fire_prob[i][0],fire_prob[i][1]])


i=0
while i<10:
    try:
        for j in range(0,9):
            drone_arr[j].move()
        assign()
    except KeyboardInterrupt:
        break
    i+=1

print("Reference arr: ",reference_arr)
print("Forest arr: ",forest)
print("checked points",checked_points)
print("fire prob",fire_prob)