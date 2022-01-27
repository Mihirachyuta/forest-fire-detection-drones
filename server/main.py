import numpy as np
import threading
import time
import requests

#forest array
fire = np.zeros((256,2))
assignd=np.zeros((256,3))
reference_arr=np.zeros((16,16))
forest=np.zeros((16,16))

fa=0
fb=0
a=0

def searchdup(x,y):
    for i in range(256):
        if fire[i][0]==x and fire[i][1] ==y:
          return 1

def newpoint(a,b):
    global fire
    global assignd
    global fa
    global fb
    fire[fa][0]=a
    fire[fa][1]=b
    fa+=1
    assignd[fb][0]=a
    assignd[fb][1]=b-1
    assignd[fb][2]=1
    #print("new assigned point x",assignd[fb][0],"y",assignd[fb][1])
    fb+=1
    assignd[fb][0]=a+1
    assignd[fb][1]=b-1
    assignd[fb][2]=2
    fb+=1
    assignd[fb][0]=a-1
    assignd[fb][1]=b
    assignd[fb][2]=3
    fb+=1
    assignd[fb][0]=a+1
    assignd[fb][1]=b+1
    assignd[fb][2]=4
    fb+=1
    assignd[fb][0]=a
    assignd[fb][1]=b+1
    assignd[fb][2]=5
    fb+=1
    assignd[fb][0]=a-1
    assignd[fb][1]=b+1
    assignd[fb][2]=6
    fb+=1
    assignd[fb][0]=a-1
    assignd[fb][1]=b
    assignd[fb][2]=7
    fb+=1
    assignd[fb][0]=a-1
    assignd[fb][1]=b-1
    assignd[fb][2]=8
    fb+=1


def generateMappedlocation(x,y):
    lat=-1.976375-0.05*x 
    lon=-63.278451+0.05*y
    return lat,lon



class Drones:
    x=0
    y=0
    dir=1
    status=0
    id=0

    def __init__(self) -> None:
        pass

    def assign(self,a,b,c):
        self.x=a
        self.y=b
        self.dir=c
        #print(self.x,self.y,self.dir)

    def sendCoordinates(self):
        location=generateMappedlocation(self.x,self.y)
        r=requests.post("http://127.0.0.1:5000/location",json={'id':self.id,'x':location[0],'y':location[1],'fire':True})
        print(r.text,location,self.id,self.x,self.y)

    def sendFireCoordinates(self):
        location=generateMappedlocation(self.x,self.y)
        r=requests.post("http://127.0.0.1:5000/fire",json={'x':location[0],'y':location[1]})
        print(r.text,location,self.id,self.x,self.y)

    def check(self):
        global forest
        global fire
        self.sendCoordinates()
        self.status=reference_arr[int(self.x)][int(self.y)]
        if(self.status==1):
            if searchdup(self.x,self.y)!=1:
                newpoint(self.x,self.y)
                self.sendFireCoordinates()

        time.sleep(5)
            #forest[self.x][self.y]
            #fire[self.x][self.y]

    def initmove(self):
        if(self.dir==1):
            while True:
                self.check()
                self.y-=1
                # self.check()
                if(self.x<=0 or self.x>=15 or self.y<=0 or self.y>=15):
                    break
        if(self.dir==2):    
            while True:
                self.check()
                self.x+=1
                self.y-=1
                if(self.x<=0 or self.x>=15 or self.y<=0 or self.y>=15):
                    break
        if(self.dir==3):    
            while True:
                self.check()
                self.x-=1
                # self.check()
                if(self.x<=0 or self.x>=15 or self.y<=0 or self.y>=15):
                    break
        
        if(self.dir==4):
            while True:
                self.check()
                self.x+=1
                self.y+=1
                # self.check()
                if(self.x<=0 or self.x>=15 or self.y<=0 or self.y>=15):
                    break
        if(self.dir==5):
            while True:
                self.check()
                self.y+=1
                # self.check()
                if(self.x<=0 or self.x>=15 or self.y<=0 or self.y>=15):
                    break
        if(self.dir==6):
            while True:
                self.check()
                self.x-=1
                self.y+=1
                # self.check()
                if(self.x<=0 or self.x>=15 or self.y<=0 or self.y>=15):
                    break
            
        if(self.dir==7):
            while True:
                self.check()
                self.x-=1
                # self.check()
                if(self.x<=0 or self.x>=15 or self.y<=0 or self.y>=15):
                    break

        if(self.dir==8): 
            while True:
                self.check()
                self.x-=1
                self.y-=1
                #print(self.x,self.y)
                if(self.x<=0 or self.x>=15 or self.y<=0 or self.y>=15):
                    break
                
        
    def dronemove(self):
        global a
        global assignd
        #for i in range (0,4):
        self.initmove()
        a+=1
        self.assign(assignd[a][0],assignd[a][1],assignd[a][2])

    def setid(self,id):
        self.id=id
            
            

drone_arr=[]
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




for i in range(0,4):
    drone_arr.append(Drones())
    drone_arr[i].setid(i)

drone_arr[0].assign(8,8,8)
drone_arr[1].assign(8,9,4)
drone_arr[2].assign(9,8,2)
drone_arr[3].assign(9,9,6)

drone_arr[1].sendCoordinates()
drone_arr[2].sendCoordinates()
drone_arr[3].sendCoordinates()
drone_arr[0].sendCoordinates()
time.sleep(5)


drone_arr[0].initmove()
drone_arr[1].initmove()
drone_arr[2].initmove()
drone_arr[3].initmove()

#print("hi")

drone_arr[0].assign(assignd[a][0],assignd[a][1],assignd[a][2])
a+=1
drone_arr[1].assign(assignd[a][0],assignd[a][1],assignd[a][2])
a+=1
drone_arr[2].assign(assignd[a][0],assignd[a][1],assignd[a][2])
a+=1
drone_arr[3].assign(assignd[a][0],assignd[a][1],assignd[a][2])

# t1 = threading.Thread(target=drone_arr[0].dronemove(), args=())
# t2 = threading.Thread(target=drone_arr[1].dronemove(), args=())
# t3 = threading.Thread(target=drone_arr[2].dronemove(), args=())
# t4 = threading.Thread(target=drone_arr[3].dronemove(), args=())

# t1.start()
# t2.start()
# t3.start()
# t4.start()


for i in range(0,7):
    drone_arr[0].dronemove()
    drone_arr[1].dronemove()
    drone_arr[2].dronemove()
    drone_arr[3].dronemove()


print(fire)
