#/usr/bin/env python
#coding:utf-8

import itertools

def createDeck():
    I=[1,2,3,4,5,6,7,8,9,10]
    J=['spades','hearts','diamonds','clubs']
    return (list(itertools.product(I,J)))


print createDeck()
