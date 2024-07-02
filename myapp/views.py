from django.shortcuts import render
from django.http import JsonResponse
from myapp.models import *
import json
import random
from faker import Faker
from geopy.distance import geodesic
fake = Faker()

def index(request):
    exportdata = []

    data = Soldiersdata.objects.filter(Humidity__gt=60)

    
    for row in data:
        
        if int(row.Temperature) > int(row.Humidity):
            indicator = "/static/images/humidity.gif"
            abn = "Abnormal Humidity Signals"
        else:
            indicator = "/static/images/temp.gif" 
            abn = "Abnormal Temperature Signals"
    
        exportdata.append({"ip": row.Soldierip.Soldierip,"Name":row.Soldierip.Name,"Rank":row.Soldierip.Rank,"Alive":row.Soldierip.Alive,"Humidity":row.Humidity,"Temperature":row.Temperature,"Indicator" : indicator,"Abn":abn,"Heartbeat":row.HeartBeat})
    return render(request, "index.html", {"Data": exportdata[:20]})

def dhtreading(request):
    distances = []
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            print(data)
        except json.JSONDecodeError as e:
            print("Error decoding JSON:", e)
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        
       
        try:
            print("Ip Address",data["IPAddress"])
            my = Soldiersdata.objects.filter(Soldierip = Soldier.objects.get(Soldierip = "192.168.43.236"))
            print("Issue at lvl1")
            my2 = Locationdetails.objects.filter(Soldierip = Soldier.objects.get(Soldierip = "192.168.43.236"))
            print("Issue at lvl2")
            if "N" and "E" in data["Location"]:
                print("True")
                locdetails = data["Location"]
                if locdetails[0] == "$GPRMC" :
                    mapslatti = int(locdetails[3][:2]) + float(locdetails[3][2:])/60
                    if locdetails[4] == 'S':
                        mapslatti *= -1
                    mapslongi = int(locdetails[5][:3]) + float(locdetails[5][3:])/60
                    if locdetails[6] == 'W':
                        mapslongi *= -1
                    print("GPRMC :- " , mapslatti)
                elif locdetails[0] == "$GPGGA":
                    mapslatti = int(locdetails[2][:2]) + float(locdetails[2][2:])/60
                    if locdetails[3] == 'S':
                        mapslatti *= -1
                    mapslongi = int(locdetails[4][:3]) + float(locdetails[4][3:])/60
                    if locdetails[5] == 'W':
                        mapslongi *= -1
                    print("GPGGA :- " , mapslatti)
                elif locdetails[0] == "$GPGLL":
                    mapslatti = int(locdetails[1][:2]) + float(locdetails[1][2:])/60
                    if locdetails[2] == 'S':
                        mapslatti *= -1
                    mapslongi = int(locdetails[3][:3]) + float(locdetails[3][3:])/60
                    if locdetails[4] == 'W':
                        mapslongi *= -1
                    print("GPGLL :- " , mapslatti)

                
                

                
                # print(mapslatti,mapslongi)
                    
            else:
                print("False")
            for row2 in my2:
                row2.lattitude  = mapslatti
                row2.longitude =  mapslongi
                row2.save()
            for row in my:
                print(mapslatti,mapslongi)
                print(row)
                row.Temperature = data["Temperature"]
                row.Humidity = data["humidity"]
                row.HeartBeat = data["heartbeat"]
            
                row.save()
                # row.update(Humidity = data["humidity"],Temperature = data["Temperature"])
        except:
            print("Data Doesnot Exist")
       
        data = Soldiersdata.objects.filter(Needhelp = True)
        for row in data:
            for row1 in Locationdetails.objects.filter(Soldierip = Soldier.objects.get(Soldierip = row.Soldierip.Soldierip)): 
                for row2 in Locationdetails.objects.all()[:20]:
                    distances.append(direction(row1.Soldierip.Soldierip,row2.Soldierip.Soldierip,float(row1.lattitude),float(row1.longitude),float(row2.lattitude),float(row2.longitude)))
        distances = sorted(distances,key=lambda x : x[3])
        for entry in distances[1:5]:
            my = Soldiersdata.objects.filter(Soldierip = Soldier.objects.get(Soldierip = entry[1]) )
            updatedata = {entry[2] : True}
            for obj in my:
                for key,value in updatedata.items():
                    setattr(obj,key,value)
                obj.save()
        
        led  = Soldiersdata.objects.filter(Soldierip = Soldier.objects.get(Soldierip = "192.168.43.236"))
        # led.update(North = False,East  = False,South  = False,West = False)
        for row in led:
            print([row.North,row.East,row.South,row.West])
            return JsonResponse({"LED": [row.North,row.West,row.South,row.East]})
    

def loadlocation(request):
    return JsonResponse({"Message" : "Coordinates Recieved"})
def maps(request):
    locations = []
    distances= []
    
    

    for row in Locationdetails.objects.all():
        soldierinfo = {}
        per = Soldier.objects.filter(Soldierip = row.Soldierip.Soldierip)
        for row1 in per:
            soldierinfo["Name"]  = row1.Name
            soldierinfo["Rank"]  = row1.Rank
        locations.append({
            "ip":row.Soldierip.Soldierip,
            "lattiude":row.lattitude,
            "longitude":row.longitude,
            "Personnel" : soldierinfo
            
            
            
        })
    
    return render(request,"maps.html",{"Location":locations[:20]})
def distance(request):
    locations = {}
    
    if request.method == "GET":
        latitude = request.GET.get('lattitude', '')
        longitude = request.GET.get('longitude', '')
        for row in Locationdetails.objects.all()[:20]:
            locations[row.Soldierip.Soldierip]  = round(geodesic((latitude,longitude),(row.lattitude,row.longitude)).kilometers,2)
        locations  = {key:value for key,value in sorted(locations.items(),key=lambda item:item[1])}    
            
            
        
    return JsonResponse({"Data" : locations})
from math import atan2, degrees

def direction(ip1,ip2,a, b, c, d):
    bearing = atan2(d - b, c - a)
    bearing = (degrees(bearing) + 360) % 360
    if 45 <= bearing < 135:
        return [ip1,ip2,"East",geodesic((a, b), (c, d)).meters]
    elif 135 <= bearing < 225:
        return [ip1,ip2,"South",geodesic((a, b), (c, d)).meters]
    elif 225 <= bearing < 315:
        return [ip1,ip2,"West",geodesic((a, b), (c, d)).meters]
    else:
        return [ip1,ip2,"North",geodesic((a, b), (c, d)).meters]

