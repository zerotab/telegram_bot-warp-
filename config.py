import urllib.request
import json
import datetime
import random
import string
import time
import os
import sys
import logging
import telebot
from telebot.types import ForceReply
import os
import admins
from admins import *



TOKEN = "6519161930:AAFlBrAw8A2d87r4ujIGbWvJkISRZAIeJg8"
planes = [0,1,5,10,20,50,100]



# PARA VERIFICAR SI EXISTE UN VALOR EN UN ARRAY
def existe(array, valor):
    return valor in array