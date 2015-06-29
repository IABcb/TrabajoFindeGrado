#!/usr/bin/python
# -*- coding: utf-8 -*-

def datos_socket():
	#Direcciones
	UDP_IP ="192.168.1.2"#
	UDP_PORT = 5000
	buffer_size = 1024              #bytes a recibir
	conexion = True	        	#conexion coche - socket
	return 	UDP_IP,	UDP_PORT,buffer_size, conexion

def datos_limites():
	carril = 30                     #Metros anchura carril
	dmax = 60                    #Distancia zona 1
	dmin = 7 			#Distancia Zona 2
	upper_speed = 50                #Km/h
	lower_speed = 12                #Km/h
	return 	carril,	dmax,upper_speed,lower_speed,dmin

def datos_init():
	sentido =""			#sentido
	last_seconds = 0.0		#ultimos segundos, para maquina de estados sin recibir pero he recibido
	v_llegar = 0     		#velocidad a la que llegar al cambio. Se introduce en ventana
	h=0 				#distancia a carril cuando estoy fuera
	actual_state = False		#incializacion de maquina de estado de verde - rojo
	previous_state = False          #estado anterior al ultimo
	light = False                    #para que una vez que ha cambiado el semaforo y sigo sin recibir datos no diga semaforo cambiado
	speeds = [0.0,0.0,0.0,0.0,0.0]  #ventana velocidades     
	long_speeds = len(speeds)	#longitude de ventana de velocidades		
	pos_v = 0  			#posicion donde voy guardando el tiempo en la ventana
	s_max = 300 			#cada s_max iteraciones calcula el sentido por si he cambiado
	s_n = 0 			#contador de iteraciones de calculo de sentido
	z_ant=False                     #zona anterior a la actual
	decision_ant = False            #decision actual a la actual
	vv_llegar_med_ant = False       #velocidad para llegar anterior a la actual
	diccionario = []		#Para escribir cada 100 mensajes recibidos
	return sentido,last_seconds,v_llegar,actual_state,previous_state,light,speeds,long_speeds,pos_v,s_max,s_n,	z_ant,decision_ant,vv_llegar_med_ant,diccionario

