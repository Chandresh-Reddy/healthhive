from myapp import views
from django.urls import path,include

urlpatterns = [
    path("",views.index,name = "index"),
    path("dhtreading",views.dhtreading,name= "dhtreading"),
    path("loadlocation",views.loadlocation,name = "loadlocation"),
    path("maps",views.maps,name = "maps"),
    path("distance",views.distance,name = "distance")
    ]