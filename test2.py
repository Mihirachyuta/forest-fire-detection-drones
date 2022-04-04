import math
drone_locations=[]
drone_next_locations=[[8,8]]

def move(source_x,source_y, dest_x,dest_y):
    global drone_locations
    global drone_next_locations
    points,distances=path_plan(source_x,source_y,dest_x,dest_y)
    #print(points, distances)
    for x in range(0,8):
        if points[x] not in drone_locations and points[x] not in drone_next_locations:
            break
    x1=points[x][0]
    y1=points[x][1]
    return x1,y1
        
    

#Assign location
def assign(self,a,b):
    self.x=a
    self.y=b

def path_plan(source_x,source_y, dest_x,dest_y):
    tmp_points=[]
    tmp_distances=[]
    points=[]
    distances=[]
    for i in range(-1,2):
        for j in range (-1,2):
            tmp_x=source_x+i
            tmp_y=source_y+j

            if(tmp_x>16 and tmp_y>16 and tmp_y<0 and tmp_x<0):
                continue
            if(tmp_x==source_x and tmp_y==source_y):
                continue
            dist=findDistance(tmp_x,tmp_y,dest_x,dest_y)
            tmp_points.append([tmp_x,tmp_y])
            tmp_distances.append(dist)
    # print(tmp_points)
    for i in range(0,len(tmp_points)):
        indexed=tmp_distances.index(min(tmp_distances))
        points.append(tmp_points[indexed])
        distances.append(tmp_distances[indexed])
        tmp_distances.remove(distances[i])
        tmp_points.remove(points[i])
    return points, distances

def findDistance(source_x,source_y,dest_x,dest_y):
    return math.sqrt((source_x-dest_x)**2+(source_y-dest_y)**2)

x=4
y=4
dest_x=9
dest_y=9
# print(path_plan(x,y,dest_x,dest_y))
a= [5,5] not in [[5,5]]
print(a)

while True:
    x,y=move(x,y,dest_x,dest_y)
    print(x,y)
    if(x==dest_x and y==dest_y):
        break

#a="Hello world!,How are you doing?"
# a=a.split(',')
# a=a[1].split()
# print(a[3:])
# k=1
# w=7
# for i in range(0,9):
#     print("01",end='')
#     #print(1,end='')
# # print()

# for i in range(0,7):
#     for j in range(0,9):
#         if(j==k):
#             print("FF",end='')
#             #print(1,end='')       
#             continue


#         if(j==w):
#             print("FF",end='')
#             #print(1,end='')      
#             continue
#         print("01",end='')
#         #print(1,end='')
#     k+=1
#     w-=1
#     # print()r



# for i in range(0,9):
#     print("01",end='')
#     #print(1,end='')