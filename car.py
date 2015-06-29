#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket 
import os
from gps import *
from time import *
import sys
import time
import threading
import functions
import distance_converter
import deg2utm
import data_car
import data_semaphore
import controller
import interfaz


#############################
#SENTIDO HORARIO SIEMPRE#
#############################

####################
#VARIABLES GLOBALES#
####################
session = None              #sesion del GPS
data = ""                   #datos recibidos
yes_conexion = False        #conexion de socket
time_waiting_conexion = 0.3 #tiempo espera a recibir (no puede ser menor que el tiempo entre balizas)
mensajes_recibidos = 0

os.system('clear') 
class GpsPoller(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)		
		global session 
		session = gps(mode=WATCH_ENABLE) 
		self.current_value = None
		self.running = True 	
 
	def run(self):
		global session
		while gpsp.running:
			session.next() #Esto continuara el loop y recojera todos los datos para limpiar el buffer

if __name__ == '__main__':
	def killall_process():	
		b_off=""
		while(b_off!="x" and b_off!="X"):
			b_off = raw_input()
		os.system("sudo pkill python")

	def conexion():
		global data
		global yes_conexion
		global time_waiting_conexion
		global mensajes_recibidos
		UDP_IP,	UDP_PORT, buffer_size, conexion = data_car.datos_socket()
		# CONEXION A SOCKET
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)		
		while conexion: 
			try:
				sock.bind((UDP_IP, UDP_PORT))
				print "Connection established"
				conexion = False
			except socket.error:
				print 'Failed to bind socket'
				sys.exit()

		while(True):
			try:
				sock.settimeout(time_waiting_conexion)
				data, addr = sock.recvfrom(buffer_size)
				mensajes_recibidos +=1
				yes_conexion = True
			except socket.error:
				yes_conexion = False
				data=""
			except KeyboardInterrupt:
				"Closing communications.."
				break
		sock.close()
		quit() 

	def run(master,base_d,distancia_total,cx,cy,ux,uy,to,iden_s,iden_s2,d_s,gpsp,upper_v,lower_v,sentido,last_seconds,v_llegar,actual_state,previous_state,light,speeds,long_speeds,pos_v,carril,s_max,s_n,d_z1,d_z2,	red_duration_time,green_duration_time,decision_ant,z_ant,interfaz_time_refresh,vv_llegar_med_ant,diccionario):
		global data
		global yes_conexion
		global time_waiting_conexion
		global mensajes_recibidos
		n_escritura=20


		lo_coche, la_coche,v_coche,hora= distance_converter.lectura(session)
		lo_m_coche,la_m_coche = deg2utm.grados2UTM(lo_coche,la_coche)		
		iden, iden_2, d = distance_converter.franja_coords(lo_m_coche,la_m_coche,ux,uy,base_d,to)

		# IN ROAD
		inroad = distance_converter.in_road(d,carril)
		#time.sleep(0.3)
		recibiendo ="NO_OK"
		inroad = True ######################################
		sentido = "horario" ########################################
		if not(inroad): 
			decision = "Te faltan " + str(int(d)) + " metros para llegar al carril"
			vv_llegar_med="--"
			interfaz.imprime_interfaz(info,v_llegar_med,distance,v_act,decision,decision_ant,vv_llegar_med,v_coche,d,d_z1,d_z2,z_ant,sentido,actual_state,vv_llegar_med_ant,lo_coche,la_coche,hora,recibiendo,diccionario,escribe,mensajes_recibidos)

		else:
			
			if(s_n%100==0):
				pass
				#sentido = distance_converter.sentido(session,ux,uy,to) 		

			dist = distance_converter.distancia_restante(base_d,ux,uy,lo_m_coche,la_m_coche,iden,iden_2,lo_m_semaforo,la_m_semaforo,iden_s,iden_s2,sentido,d,d_s,to)
			if(yes_conexion):	
				s_n+=1
				recibiendo = "OK"
				escribe=False
				if(s_n%n_escritura==0):
					escribe=True

				actual_state, last_seconds = functions.data_extractor(data)			
				v_llegar = functions.ms_to_kmh(dist, last_seconds)
				decision , previous_state , pos_v,vv_llegar_med= controller.controlador(v_llegar,v_coche,last_seconds,upper_v,lower_v,dist,d_z1,d_z2,actual_state,previous_state,pos_v,speeds,long_speeds,	red_duration_time,green_duration_time)				

				light = True #Inicio maquina estados (True = recibiendo señal)
				z_ant, decision_ant,vv_llegar_med_ant,diccionario = interfaz.imprime_interfaz(info,v_llegar_med,distance,v_act,decision,decision_ant,vv_llegar_med,v_coche,dist,d_z1,d_z2,z_ant,sentido,actual_state,vv_llegar_med_ant,lo_coche,la_coche,hora,recibiendo,diccionario,escribe,mensajes_recibidos)

			else:
				if(data !="" and light==True): #Se mete aquí cuando ha recibido algo y ya no recibe
					last_seconds = float(last_seconds) - time_waiting_conexion
					if (last_seconds<=0.0):
						decision = "Conexion failed: El semaforo cambió a " + str(functions.contrario(actual_state))
						vv_llegar_med = "--"
						escribe=False
						if(s_n%n_escritura==0):
							escribe=True
						z_ant, decision_ant,vv_llegar_med_ant,diccionario = interfaz.imprime_interfaz(info,v_llegar_med,distance,v_act,decision,decision_ant,vv_llegar_med,v_coche,dist,d_z1,d_z2,z_ant,sentido,actual_state,vv_llegar_med_ant,lo_coche,la_coche,hora,recibiendo,diccionario,escribe,mensajes_recibidos)
################################INICIALIZO TODo DE NUEVO					
						light=False	
						sentido,last_seconds,v_llegar,actual_state,previous_state,light,speeds,	long_speeds,pos_v,s_max,s_n,z_ant,decision_ant,vv_llegar_med_ant,diccionario= data_car.datos_init()	

############
		
					elif(last_seconds<=time_waiting_conexion): 	
						v_llegar = functions.ms_to_kmh(dist, last_seconds)	
						decision , previous_state , pos_v,vv_llegar_med= controller.controlador(v_llegar,v_coche,last_seconds,upper_v,lower_v,dist,d_z1,d_z2,actual_state,previous_state,pos_v,speeds,long_speeds,red_duration_time,green_duration_time)
						escribe=False
						if(s_n%n_escritura==0):
							escribe=True
						z_ant, decision_ant,vv_llegar_med_ant,diccionario = interfaz.imprime_interfaz(info,v_llegar_med,distance,v_act,decision,decision_ant,vv_llegar_med,v_coche,dist,d_z1,d_z2,z_ant,sentido,actual_state,vv_llegar_med_ant,lo_coche,la_coche,hora,recibiendo,diccionario,escribe,mensajes_recibidos)
						time.sleep(last_seconds)
################################INICIALIZO TODO DE NUEVO									
						light=False
						sentido,last_seconds,v_llegar,actual_state,previous_state,light,speeds,	long_speeds,pos_v,s_max,s_n,z_ant,decision_ant,vv_llegar_med_ant,diccionario= data_car.datos_init()

############
					else:				
						v_llegar = functions.ms_to_kmh(dist, last_seconds)	
						decision , previous_state ,pos_v,vv_llegar_med = controller.controlador(v_llegar,v_coche,last_seconds,upper_v,lower_v,dist,d_z1,d_z2,actual_state,previous_state,pos_v,speeds,long_speeds,red_duration_time,green_duration_time)					
						escribe=False
						if(s_n%n_escritura==0):
							escribe=True
						z_ant, decision_ant,vv_llegar_med_ant,diccionario = interfaz.imprime_interfaz(info,v_llegar_med,distance,v_act,decision,decision_ant,vv_llegar_med,v_coche,dist,d_z1,d_z2,z_ant,sentido,actual_state,vv_llegar_med_ant,lo_coche,la_coche,hora,recibiendo,diccionario,escribe,mensajes_recibidos)

				else:
					decision = "URJC" #No he recibido nunca o el semaforo ya cambio sin recibir datos
					vv_llegar_med = "--"
					escribe=False
					if(s_n%n_escritura==0):
						escribe=True
					z_ant, decision_ant,vv_llegar_med_ant,diccionario = interfaz.imprime_interfaz(info,v_llegar_med,distance,v_act,decision,decision_ant,vv_llegar_med,v_coche,dist,d_z1,d_z2,z_ant,sentido,actual_state,vv_llegar_med_ant,lo_coche,la_coche,hora,recibiendo,diccionario,escribe,mensajes_recibidos)
			
		root.after(interfaz_time_refresh,run, master,base_d,distancia_total,cx,cy,ux,uy,to,iden_s,iden_s2,d_s,gpsp,upper_v,lower_v,sentido,last_seconds,v_llegar,actual_state,previous_state,light,speeds,long_speeds,pos_v,carril,s_max,s_n,d_z1,d_z2,	red_duration_time,green_duration_time,decision_ant,z_ant,interfaz_time_refresh,vv_llegar_med_ant,diccionario)

##########################################################################################################################################

	# INTERFAZ GRAFICA 
	root,info,v_llegar_med,distance,v_act = interfaz.graficos()
	# PREPARACION GPS 
	os.system('clear')
	os.system("sudo killall gpsd")
#	os.system("sudo /etc/init.d/gpsd restart")
	os.system("sudo gpsd -n -D 2 /dev/ttyUSB0")	
	gpsp = GpsPoller()
	#gpsp = gps.gps("localhost", "2947")	
	try:
		gpsp.start()
		# PREPARACION DATOS INICIALES
		carril,	d_z1,upper_v, lower_v,d_z2 = data_car.datos_limites()
		sentido,last_seconds,v_llegar,actual_state,previous_state,light,speeds,	long_speeds,pos_v,s_max,s_n,z_ant,decision_ant,vv_llegar_med_ant,diccionario= data_car.datos_init()
		red_duration_time, green_duration_time, lo_semaforo, la_semaforo=data_semaphore.data_semaphore_car()

		# CONEXION A SOCKET
		cnx=threading.Timer(0.1,conexion)
		cnx.start()
		
		# CREACION BASE DE DISTANCIAS SOBRE PUNTOS DE REFERENCIA
		base_d, distancia_total, cx, cy, ux, uy, to= distance_converter.basedatos_distancias()

		# PREPARACION SEMAFORO
		lo_m_semaforo, la_m_semaforo = deg2utm.grados2UTM(lo_semaforo,la_semaforo)
		iden_s, iden_s2, d_s = distance_converter.franja_coords(lo_m_semaforo,la_m_semaforo,ux,uy,base_d,to)

		#DECIDIR DONDE LO PONGOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
		interfaz_time_refresh = 500
		
		#PREPARACION DESTRUCCION
		dstr=threading.Timer(0.1,killall_process)
		dstr.start()
	except(KeyboardInterrupt, SystemExit):
		print 			
		print "\nDesconectando GPS..."
		gpsp.running = False
		os.system("sudo killall gpsd")
		interfaz.close_window(root)
		gpsp.join() # Espera a que el thread finalice
		print "Ok.\nSaliendo..."
		print "Bye Bye!"	 #Al pulsar ctrl+c
		sys.exit()

	# PROGRAMA PRINCIPAL
	run(root,base_d,distancia_total,cx,cy,ux,uy,to,iden_s,iden_s2,d_s,gpsp,upper_v,lower_v,sentido,last_seconds,v_llegar,actual_state,previous_state,light,speeds,long_speeds,pos_v,carril,s_max,s_n,d_z1,d_z2,	red_duration_time,green_duration_time,decision_ant,z_ant,interfaz_time_refresh,vv_llegar_med_ant,diccionario)
	root.mainloop()
quit()
