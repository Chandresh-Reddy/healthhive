from django.db import models
class Soldier(models.Model):
    Soldierip = models.CharField(max_length  = 20)
    Name = models.CharField(max_length  = 50)
    Rank =models.CharField(max_length  = 20)
    Alive = models.BooleanField()
    def __str__(self):
        return self.Name
class Soldiersdata(models.Model):
    Soldierip = models.ForeignKey(Soldier,on_delete = models.CASCADE)
    Humidity = models.CharField(max_length = 15)
    Temperature = models.IntegerField()
    HeartBeat = models.IntegerField(default = 0)
    Needhelp = models.BooleanField()
    North = models.BooleanField()
    South = models.BooleanField()
    East = models.BooleanField()
    West = models.BooleanField()
    def __str__(self):
        return self.Soldierip.Soldierip
class Locationdetails(models.Model):
    Soldierip = models.ForeignKey(Soldier,on_delete  =models.CASCADE)
    lattitude = models.CharField(max_length = 20)
    longitude = models.CharField(max_length = 20)
    def __str__(self):
        return self.Soldierip.Soldierip
class Requests(models.Model):
    Soldierip = models.ForeignKey(Soldier,on_delete = models.CASCADE)
    To = models.CharField(max_length = 20)
    Direction  = models.CharField(max_length = 10)
    def __str__(self):
        return self.Soldierip.Soldierip