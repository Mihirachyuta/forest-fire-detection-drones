

class drones:
    x=0
    y=0

    def __init__(self) -> None:
        pass

    def assign(self,a,b):
        self.x=a
        self.y=b
        print(a,b)

    def disp(self):
        print(self.x,self.y)

y=drones()

y.assign(1,2)