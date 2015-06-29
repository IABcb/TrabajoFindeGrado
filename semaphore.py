#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import socket
import data_semaphore
import sys
import os, time
import threading

boton = ""
def asker():
	global boton
	while(boton!="x" and boton!="X"):
		boton = raw_input("r - g: ")



os.system('clear') #Limpiamos la terminal 

red_duration_time, green_duration_time, lo_semaforo, la_semaforo=data_semaphore.data_semaphore_car()
red_message_interval, green_message_interval, decimal_prec,conexion = data_semaphore.data_semaforo()
UDP_IP, UDP_PORT = data_semaphore.socket()

while conexion:
	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		conexion = False
		print "Connection established"
	except socket.error:
		print 'Failed to create socket'
		

starting_point=time.time() #Comienzo del tiempo                       
version = sys.argv[1] 	
op = sys.argv[2]
outfile = open('logfile_sem_v' + str(version) +'.txt', 'a') 

if(op=="-a"):
	while True:
		t =time.time()
		dif_time = time.time()-starting_point #tiempo que pasa desde el inicio de la vida del semaforo
		if(dif_time<= red_duration_time): #hecho para que vida de semaforo comience en rojo, establecido asi
			#red_message= chr(27)+"[0;41m"+"RED"+chr(27)+"[0m"+" "+	str("%0.5f" % (red_duration_time-dif_time))+ " segundos para el cambio"	
			t_cambio_rojo = red_duration_time-dif_time
			red_message ="RED "+	str("%0.5f" % (t_cambio_rojo))+ " segundos para el cambio"	
			time.sleep(red_message_interval)
			sock.sendto(red_message, (UDP_IP, UDP_PORT))
			#print chr(27)+"[0;41m"+"RED"+chr(27)+"[0m"
			print "RED,"+str(t_cambio_rojo)+","+str(t)
			outfile.write("RED,"+str(t_cambio_rojo)+","+str(t)+'\n')	
		elif(dif_time<= (green_duration_time+red_duration_time)):
			#green_message= chr(27)+"[0;42m"+"GREEN"+chr(27)+"[0m"+" "+ str("%0.5f" % (red_duration_time+green_duration_time-dif_time)) + " segundos para el cambio"
			t_cambio_verde = red_duration_time+green_duration_time-dif_time
			green_message="GREEN " + str("%0.5f" % (t_cambio_verde)) + " segundos para el cambio"
			time.sleep(green_message_interval)
	       		sock.sendto(green_message, (UDP_IP, UDP_PORT))
			#print chr(27)+"[0;42m"+"GREEN"+chr(27)+"[0m"
			print "GREEN,"+str(t_cambio_verde)+","+str(t)	
			outfile.write("GREEN,"+str(t_cambio_verde)+","+str(t)+'\n')
		else:
			starting_point=time.time()


elif(op=="-c"):
	th=threading.Timer(0.1,asker)
	th.start()
	while True:
		#os.system("clear")
		t =time.time()
		if(boton=="r"):
			starting_point = time.time()
		elif(boton=="g"):
			starting_point= time.time()-(red_duration_time+0.1) #Al restar el tiempo de rojo, cuenta como si ese estado ya lo hubieramos pasado
		boton="" #Lo borro para que salga de cada estado
		dif_time = time.time()-starting_point #tiempo que pasa desde el inicio de la vida del semaforo		
		if(dif_time<= red_duration_time): #hecho para que vida de semaforo comience en rojo, establecido asi		
			t_cambio_rojo = red_duration_time-dif_time
			red_message ="RED "+	str("%0.5f" % (t_cambio_rojo))+ " segundos para el cambio"	
			time.sleep(red_message_interval)
			sock.sendto(red_message, (UDP_IP, UDP_PORT))
			
			print "RED,"+str(t_cambio_rojo)+","+str(t)
			outfile.write("RED,"+str(t_cambio_rojo)+","+str(t)+'\n')	
		elif(dif_time<= (green_duration_time+red_duration_time)):
			t_cambio_verde = red_duration_time+green_duration_time-dif_time
			green_message="GREEN " + str("%0.5f" % (t_cambio_verde)) + " segundos para el cambio"
			time.sleep(green_message_interval)
	       		sock.sendto(green_message, (UDP_IP, UDP_PORT))
		
			print "GREEN,"+str(t_cambio_verde)+","+str(t)	
			outfile.write("GREEN,"+str(t_cambio_verde)+","+str(t)+'\n')
		else:
			starting_point=time.time()
else:
	print "Use: python semaphore <logfile_version> <-c or -a>"
print "salio"
outfile.close()
sock.close()

