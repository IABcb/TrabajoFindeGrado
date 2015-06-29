#!/usr/bin/python
# -*- coding: utf-8 -*-	
def data_semaphore_car():
	red_duration_time = 60
	green_duration_time = 20
	lo_semaforo = -3.818465  #URJC RECTA S. HORARIO -3.815588  #URJC CURVA S. ANTIHORARIO  -3.878445 #PARKING#
	la_semaforo =  40.279046 #URJC RECTA S. HORARIO 40.279415  #URJC CURVA S. ANTIHORARIO  40.323873 #PARKING#
	return 	red_duration_time,green_duration_time,lo_semaforo,la_semaforo

def data_semaforo():
					#Tiempos en segundos
	red_message_interval = 0.01     #los intervalos entre balizas no pueden ser menores que el tiempo de espera a conexion del coche 
	green_message_interval = 0.01
	decimal_prec=0.5
	conexion=True
	return 	red_message_interval, green_message_interval, decimal_prec,conexion

def socket():
	#Direcciones
	UDP_IP =    "192.168.1.2"
	UDP_PORT = 5000
	return UDP_IP, UDP_PORT
