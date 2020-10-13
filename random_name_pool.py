#!/usr/bin/env python3

import random

FAMILY_NAMES_FILE_PATH="./family_names.txt"
GIVEN_NAMES_FILE_PATH="./given_names.txt"

class RandomNamePool:
    def __init__(self):
        self.used_names=[]

        family_names_file=open(FAMILY_NAMES_FILE_PATH,'r')
        self.family_name_list=[name.split('\n')[0] for name in family_names_file.readlines()]
        given_names_file=open(GIVEN_NAMES_FILE_PATH,'r')
        self.given_name_list=[name.split('\n')[0] for name in given_names_file.readlines()]
        family_names_file.close()
        given_names_file.close()

        self.capacity=len(self.family_name_list)*len(self.given_name_list)

    def generate_name(self):
        if len(self.used_names)>=self.capacity:
            return False

        while(True):
            name={
                "family_name":self.family_name_list[random.randint(0,len(self.family_name_list)-1)],
                "given_name":self.given_name_list[random.randint(0,len(self.given_name_list)-1)]
            }

            if name not in self.used_names:
                self.used_names.append(name)
                return name

if __name__=="__main__":
    random_name_pool=RandomNamePool()

    cnt=0
    while(True):
        name=random_name_pool.generate_name()
        cnt+=1
        if not name:
            break
        else:
            print(name["given_name"],name["family_name"],cnt)