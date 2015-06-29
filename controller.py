#!/usr/bin/python
# -*- coding: utf-8 -*-
import functions
import os
def decisor_priori(v_llegar,upper,lower,actual_state,previous_state,pos_v,speeds,long_speeds):
	speeds, pos_v , previous_state= functions.aumenta_speeds(speeds,pos_v,previous_state,actual_state,v_llegar,long_speeds)
	decision = ""
	guilty_v = "none"
	#print str(speeds)
	speed_media=functions.media_speeds(speeds,long_speeds)
	if(functions.speed_limits(speed_media,upper,lower)):
		decision= "OK"
	else:
		guilty_v = functions.guilty_speed(speed_media,upper,lower)
		decision= "NO_OK"
	return decision , previous_state , pos_v, speed_media, 	guilty_v

def zona(d,d_z1,d_z2):
	z=0
	if(d <= d_z1 and d > d_z2):
		z = 1
	elif(d <= d_z2):
		z = 2
	else:
		z = 3
	return z

def movimiento(v_act):
	return v_act>=1.5 #km/h


def bajar_velocidad(t_var,v): #posibles mejoras: meter v_up2 y v_down2 para que el cambio sea mas drastico si se puede por limites
	v_h_km = 1.0/v
	v_s_m = v_h_km*3600/1000
	v_down = 1/((v_s_m + t_var)*1000/3600)
	return v_down

def subir_velocidad(t_var,v):
	v_h_km = 1.0/v
	v_s_m = v_h_km*3600/1000
	v_up = 1/((v_s_m - t_var)*1000/3600)
	return v_up

def controlador(v_llegar,v_coche,last_seconds,upper_v,lower_v,dist,d_z1,d_z2,actual_state,previous_state,pos_v,speeds,long_speeds,	red_duration_time,green_duration_time):
	z = zona(dist,d_z1,d_z2)
#	print
	decision_priori , previous_state , pos_v, v_final, guilty_v= decisor_priori(v_llegar,upper_v,lower_v,actual_state,previous_state,pos_v,speeds,long_speeds)
	
	t_var = 0.015              #tiempo a variar la velocidad
	decision_final = "Fuera de zonas"
	v_down = bajar_velocidad(t_var, v_final)
	v_up = subir_velocidad(t_var,v_final)
	if(z == 1):
		if(actual_state=="GREEN"):
			#print "DECISION PRIORI: " + decision_priori
			if(decision_priori=="OK"):
				decision_final = "MINIMO"
				if(functions.speed_limits(v_up,upper_v,lower_v)):
					v_final=v_up
			elif(decision_priori=="NO_OK"):
				v_pasa_rojo = functions.ms_to_kmh(dist,red_duration_time+last_seconds+1) #velocidad pasar el rojo
				if(guilty_v=="up"):
					if(functions.speed_limits(v_pasa_rojo,upper_v,lower_v)):
						v_final=v_pasa_rojo
						decision_final = "IR A"
					else:
						v_final= "--"
						decision_final = "Vaya frenando para parar"
				elif(guilty_v=="down"):
					v_ok1= False #splitear en poca distancia y mucho tiempo
					while not(v_ok1):
						if(functions.speed_limits(v_up,upper_v,lower_v)):
							v_final=v_up
							decision_final = "MINIMO"
							v_ok1 = True
						else:
							guilty_v = functions.guilty_speed(v_up,upper_v,lower_v)
							if(guilty_v=="up"):###AQUI NO DEBERIA ENTRAR NUNCA
								v_final = v_up 
								decision_final = "NO DEBERIA ENTRAR AQUI 1"
								v_ok1 = True
							elif(guilty_v=="down"):
								v_up =  subir_velocidad(t_var, v_up)
		elif(actual_state=="RED"):
			#print "DECISION PRIORI: " + decision_priori
			if(decision_priori=="OK"):
				decision_final = "MAXIMO"
				if(functions.speed_limits(v_down,upper_v,lower_v)):
					v_final=v_down
			elif(decision_priori=="NO_OK"): 
				if(guilty_v=="up"):
					v_ok2=False					
					while not(v_ok2): ##QUIZA HACE FALTA COMPROBACION DE QUE NO ME PASO AL SIGUIENTE VERDE AL BAJAR V
						if(functions.speed_limits(v_down,upper_v,lower_v)):
							v_final=v_down
							decision_final = "MAXIMO"
							v_ok2 = True
						else: 
							guilty_v = functions.guilty_speed(v_down,upper_v,lower_v)
							if(guilty_v=="up"):
								v_down = bajar_velocidad(t_var, v_down)
							elif(guilty_v=="down"): ########## AQUI NO DEBERIA ENTRAR NUNCA
								v_final= "--"
								decision_final = "NO DEBERIA ENTRAR AQUI 2"
								v_ok2 = True
				elif(guilty_v=="down"):
					decision_final = "Vaya frenando para parar"
					v_final = "--"
	elif(z == 2): #EN MOVIMIENTO, REALIZAR LO MISMO QUE EN Z1	
		if(movimiento(v_coche)):					
			if(actual_state=="GREEN"):
				#print "DECISION PRIORI: " + decision_priori
				if(decision_priori=="OK"):
					decision_final = "MINIMO"
					if(functions.speed_limits(v_up,upper_v,lower_v)):
						v_final=v_up
				elif(decision_priori=="NO_OK"):
					v_pasa_rojo = functions.ms_to_kmh(dist,red_duration_time+last_seconds+1) #velocidad pasar el rojo
					if(guilty_v=="up"):
						if(functions.speed_limits(v_pasa_rojo,upper_v,lower_v)):
							v_final=v_pasa_rojo
							decision_final = "IR A"
						else:
							v_final= "--"
							decision_final = "Vaya frenando para parar"
					elif(guilty_v=="down"):
						v_ok1= False #splitear en poca distancia y mucho tiempo
						while not(v_ok1):
							if(functions.speed_limits(v_up,upper_v,lower_v)):
								v_final=v_up
								decision_final = "MINIMO"
								v_ok1 = True
							else:
								guilty_v = functions.guilty_speed(v_up,upper_v,lower_v)
								if(guilty_v=="up"):###AQUI NO DEBERIA ENTRAR NUNCA
									v_final = v_up 
									decision_final = "NO DEBERIA ENTRAR AQUI 1"
									v_ok1 = True
								elif(guilty_v=="down"):
									v_up =  subir_velocidad(t_var, v_up)
			elif(actual_state=="RED"):
				#print "DECISION PRIORI: " + decision_priori
				if(decision_priori=="OK"):
					decision_final = "MAXIMO"
					if(functions.speed_limits(v_down,upper_v,lower_v)):
						v_final=v_down
				elif(decision_priori=="NO_OK"): 
					if(guilty_v=="up"):
						v_ok2=False					
						while not(v_ok2): 
							if(functions.speed_limits(v_down,upper_v,lower_v)):
								v_final=v_down
								decision_final = "MAXIMO"
								v_ok2 = True
							else: 
								guilty_v = functions.guilty_speed(v_down,upper_v,lower_v)
								if(guilty_v=="up"):
									v_down = bajar_velocidad(t_var, v_down)
								elif(guilty_v=="down"): ########## AQUI NO DEBERIA ENTRAR NUNCA
									v_final= "--"
									decision_final = "NO DEBERIA ENTRAR AQUI 2"
									v_ok2 = True
					elif(guilty_v=="down"):
						decision_final = "Vaya frenando para parar"
						v_final = "--"
		else:
			if(actual_state=="GREEN"):
				#print "GREEN 3"
				#print "DECISION PRIORI" + decision_priori
				v_final=="--"
				decision_final="VAMOOOOOOOOOS!!!!!!!!!!!"
			elif(actual_state=="RED"):
				#print "DECISION PRIORI" + decision_priori
				#print "RED 3"
				v_final="--"
				decision_final="Preparado..." + str(int(last_seconds)) + " s"
	elif(z == 3):
		#print "ZONAAAAAAAAAAAA: "+ str(z)
		v_final="--"
		decision_final="URJC"
	#print "guilty: " + str(guilty_v)
	#print "last_seconds: " + str(last_seconds)
	return decision_final, previous_state, pos_v, v_final





