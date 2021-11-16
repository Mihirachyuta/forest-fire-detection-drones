import flask
from flask import request
from flask_cors import CORS

app=flask.Flask(__name__)
CORS(app, support_credentials=True)


drones={}
fire_location=[]

drones[1]=[-2.104332, -62.639214,True]
drones[2]=[-2.258833, -62.441400,True]
drones[3]=[-2.373951, -62.738817,True]
#drones[3]=[-2.104332, -62.738817,True]


@app.route('/')
def hello_world():
    return "Hello World"


@app.route('/location',methods = ['POST'])
def sendLocation():
    if request.method == 'POST':
        global drones
        global fire_location
        result = request.get_json()
        device_id=result['id']
        x=result['x']
        y=result['y']
        fire=result['fire']
        drones[device_id]=[x,y,fire]
        if(fire):
            fire_location.append([x,y])
        print(drones,fire_location)
        return "sent"

@app.route('/drones',methods = ['GET'])
def getDrones():
    if request.method== 'GET':
        global drones
        id=[]
        lat=[]
        lon=[]
        for drone in drones.keys():
            id.append(str(drone))
            temp=drones.get(drone)
            lat.append(str(temp[0]))
            lon.append(str(temp[1]))
        drone_logs={"id":id,"lat":lat,"long":lon}
        return drone_logs

if __name__ == '__main__':
    app.run(debug=True)