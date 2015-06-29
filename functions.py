#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import gps
import numpy

def contrario(estado):
	contr="ninguno"
	if(estado=="RED"):
		contr="GREEN"
	elif(estado=="GREEN"):
		contr="RED"
	return contr

def aceleration(v1,t1,v2,t2):
	print 'Your aceleration is (m/s2): '+ str((v2-v1)/(t2-t1))

def ms_to_kmh(distance_metres, time_seconds):
	return (distance_metres*3600)/(time_seconds*1000)


def guilty_speed(speed_kmh,upper,lower): 
	g = "none"
	if(speed_kmh>upper):
		g = "up"
	elif(speed_kmh<lower):
		g = "down"
	return g

def speed_limits(speed_kmh,upper,lower): 
	response = True
	if(speed_kmh>upper or speed_kmh<lower):
		response= False
	return response

def init_speeds(speeds):
	pos_v=0
	for i in range(len(speeds)):
		speeds[i-1] = 0
	return speeds, pos_v

def media_speeds(speeds,long_speeds): #calcula la media en funcion de los elementos de la ventana rellenos	
	try:
		media = (sum(speeds))/(int(long_speeds)-speeds.count(0))
	except ZeroDivisionError:
		media = 0.0000001

	return media

def init_pos_v(pos_v,long_speeds):
	if(pos_v==long_speeds):
		pos_v=0
	return pos_v

def aumenta_speeds(speeds,pos_v,previous_state,actual_state, v_llegar,long_speeds):
	if not(previous_state):
		previous_state = actual_state #Entra con False el previous
	elif(previous_state==actual_state):
		pass
	else:
		previous_state = False 
		speeds , pos_v = init_speeds(speeds)

	#print str(pos_v) + " posicion guardada"
	speeds[pos_v]=v_llegar
	pos_v = pos_v + 1
	#print speeds
	pos_v = init_pos_v(pos_v,long_speeds)

	return speeds, pos_v, previous_state

def data_extractor(data):
	actual_state = data.split(' ')[0]
	last_seconds = float(data.split(' ')[1]); #ultimos segundos recibidos para el cambio
	return actual_state, last_seconds


