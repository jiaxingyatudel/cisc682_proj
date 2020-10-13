#!/usr/bin/env python3

import random

LOREM_IPSUM_FILE_PATH="./lorem_ipsum.txt"

class LoremIpsum:
    def __init__(self):
        self.lorem_ipsum_words=[]

        lorem_ipsum_file=open(LOREM_IPSUM_FILE_PATH,'r')
        lorem_ipsum_str=lorem_ipsum_file.read()

        temp_str=lorem_ipsum_str.lower()
        temp_str=temp_str.replace('\n', '')
        temp_str=temp_str.replace(',', '')
        temp_str=temp_str.replace('.', '')

        self.lorem_ipsum_words=temp_str.split()

    def generate_sentence(self,word_cnt_min=8,word_cnt_max=16,comma_max_density=4):
        sentence=str()

        word_cnt=random.randint(word_cnt_min,word_cnt_max)

        comma_cnt=0
        previous_word=False
        for i in range(word_cnt):
            while(True):
                word=self.lorem_ipsum_words[random.randint(0,len(self.lorem_ipsum_words)-1)]

                if word!=previous_word:
                    previous_word=word
                    sentence+=word

                    if i<word_cnt-1:
                        comma_cnt+=1
                        if comma_cnt>=comma_max_density:
                            r=random.random()
                            if r<0.4:
                                sentence+=","
                                comma_cnt=0

                        sentence+=" "

                    break

        sentence+="."
        sentence=sentence.capitalize()
        return sentence


    def generate_paragraph(self,sentence_cnt_min=4,sentence_cnt_max=8):
        sentence_cnt=random.randint(sentence_cnt_min,sentence_cnt_max)

        paragraph=str()
        for i in range(sentence_cnt):
            paragraph+=self.generate_sentence()

            if i<sentence_cnt-1:
                paragraph+=" "

        return paragraph


if __name__=="__main__":
    lorem_ipsum=LoremIpsum()
    print(lorem_ipsum.generate_paragraph())