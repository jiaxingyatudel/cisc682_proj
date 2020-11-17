#!/usr/bin/env python3

# names are derived from 1990 Census data

import random

class RandomNamePool:
    def __init__(self):
        self.used_names=[]

        last_names_file=open("./last_names.txt","r")
        self.last_names=[name.split('\n')[0] for name in last_names_file.readlines()]
        last_names_file.close()

        first_names_female_file=open("./first_names_female.txt","r")
        first_names_female=[name.split('\n')[0] for name in first_names_female_file.readlines()]
        first_names_female_file.close()

        first_names_male_file=open("./first_names_male.txt","r")
        first_names_male=[name.split('\n')[0] for name in first_names_male_file.readlines()]
        first_names_male_file.close()

        self.first_names=first_names_female+first_names_male

        self.capacity=len(self.first_names)*len(self.last_names)

    def generate_name(self):
        if len(self.used_names)>=self.capacity:
            return False

        while(True):
            name={
                "first_name":self.first_names[random.randint(0,len(self.first_names)-1)],
                "last_name":self.last_names[random.randint(0,len(self.last_names)-1)]
            }

            if name not in self.used_names:
                self.used_names.append(name)
                return name

    def pick_name(self):
        return {
            "first_name":self.first_names[random.randint(0,len(self.first_names)-1)],
            "last_name":self.last_names[random.randint(0,len(self.last_names)-1)]
        }

if __name__=="__main__":
    random_name_pool=RandomNamePool()

    cnt=0
    while(True):
        name=random_name_pool.generate_name()
        cnt+=1
        if not name:
            break
        else:
            print(name["first_name"],name["last_name"],cnt)