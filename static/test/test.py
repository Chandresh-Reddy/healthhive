import random
from faker import Faker
from myapp.models import *

fake = Faker()
def fakedata():
    part1 = random.randint(1, 255)
    part2 = random.randint(0, 255)
    part3 = random.randint(0, 255)
    part4 = random.randint(1, 255)
    fakeip = f"{part1}.{part2}.{part3}.{part4}"
    humidity = random.randint(50,100)
    return {"ip":fakeip,"Name":fake.name(),"Rank":random.choice([1,2,3,4,5,6,7]),"Alive":random.choice([True,False])}
for row in range(10):
    print(fakedata())
    