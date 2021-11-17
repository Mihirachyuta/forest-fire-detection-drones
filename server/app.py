import flask
from flask import request
from flask_cors import CORS

app=flask.Flask(__name__)
CORS(app, support_credentials=True)


drones={}
fire_location=[]
waypoints=[]

# drones[1]=[-2.104332, -62.639214,True]
# drones[2]=[-2.258833, -62.441400,True]
# drones[3]=[-2.373951, -62.738817,True]
#drones[3]=[-2.104332, -62.738817,True]


@app.route('/')
def hello_world():
    return "Hello World"


@app.route('/location',methods = ['POST'])
def sendLocation():
    if request.method == 'POST':
        global drones
        global fire_location
        global waypoints
        result = request.get_json()
        device_id=result['id']
        x=result['x']
        y=result['y']
        fire=result['fire']
        drones[device_id]=[x,y,fire]
        waypoints.append([x,y])
        return "sent"

@app.route('/fire',methods = ['POST'])
def sendFireLocation():
    if request.method == 'POST':
        global drones
        global fire_location
        result = request.get_json()
        x=result['x']
        y=result['y']
        fire_location.append([x,y])
        return "sent fire"

@app.route('/drones',methods = ['GET'])
def getDrones():
    if request.method== 'GET':
        global drones
        global fire_location
        global waypoints
        id=[]
        lat=[]
        lon=[]
        symbol=[]
        size=[]

        for drone in drones.keys():
            id.append(str(drone))
            temp=drones.get(drone)
            lat.append(str(temp[0]))
            lon.append(str(temp[1]))
            symbol.append("airport")
            size.append("15")
            

        for f in fire_location:
            id.append("fire")
            lat.append(str(f[0]))
            lon.append(str(f[1]))
            symbol.append("fire-station")
            size.append("15")

        for w in waypoints:
            id.append("")
            lat.append(str(w[0]))
            lon.append(str(w[1]))
            symbol.append("circle")
            size.append("1")
        
        drone_logs={"id":id,"lat":lat,"long":lon,"symbol":symbol,"size":size}
        return drone_logs

@app.route('/reset',methods = ['GET'])
def reset():
    if request.method== 'GET':
        global drones
        global fire_location
        global waypoints
        drones={}
        fire_location=[]
        waypoints=[]
        return "Server reset"

if __name__ == '__main__':
    app.run(debug=True)