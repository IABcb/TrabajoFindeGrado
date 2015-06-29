#!/usr/bin/python
# -*- coding: utf-8 -*-
import map_converter
import deg2utm
import numpy
import functions
import math
import time
import gps

def dist_coords(coord_x1, coord_y1, coord_x2, coord_y2):
	coord_x1=float(coord_x1)
	coord_x2=float(coord_x2)
	coord_y1=float(coord_y1)
	coord_y2=float(coord_y2)
	return numpy.sqrt(((coord_x2-coord_x1)**2)+((coord_y2-coord_y1)**2))

def th_cos(d1_c,d2_a,d_entre_coords_b):	#devuelve distancia a d1_c th.cos => u = (c**2-a**2+b**2)/(2*b)
	return abs(((d1_c**2)-(d2_a**2)+(d_entre_coords_b**2))/(2*(d_entre_coords_b)))

def basedatos_distancias():
	print "Creando base de datos..."
	cx,cy,ux,uy = map_converter.coordenadas()
	to=len(ux)-1
	base_d=[]
	for i in range(to+1): #10 coords, 10 distancias entre ellas porque es cíclico
		j=i+1
		if(i==to):
			j=0
		base_d.append(dist_coords(ux[i],uy[i],ux[j],uy[j]))
	distancia_total = numpy.sum(base_d) #Suma de distancias es la distancia total
	print "Nº de coords: " + str(i+1) 
	return base_d, distancia_total, cx, cy, ux, uy, to


def lectura(session):
	c = True
	while(c):
		try:			
			#gpsp.run()
			#gpsp.lectura()
			lo = session.fix.longitude #gpsp.lo
			la = session.fix.latitude #gpsp.la
			v_actual = session.fix.speed * 3.6 #gpsp.v*3.6 #convertido a km/h
			hora = time.time()#session.utc #session.fix.time
			lo_isnan = math.isnan(float(lo))
			la_isnan = math.isnan(float(la))
			v_actual_isnan = math.isnan(float(v_actual))			
			if ((lo != 0.0 and la != 0.0) and ((lo_isnan==False and la_isnan==False) and(v_actual_isnan ==False))):
				c = False
    		except KeyError:
			pass
    		except KeyboardInterrupt:
			quit()
		except StopIteration:
			gpsp = None
			print "GPSD has finished"
	return float(lo), float(la), float(v_actual), hora


def correccion_iden(iden,iden_2,to,sig):
	#sig=1:siguiente coord, empieza de nuevo el ciclo xq tengo última coordenada
	#sig=0:anterior coord, cojo última coordenada
	iden_c=iden_2
	if((iden==to) and (sig==1)): 
		iden_c=0
	#	print "Corregido a 0"
	elif((iden==0) and (sig==0)):
		iden_c=to
	#	print "Corregido a ultimo"
	return iden_c

def correccion_sig_coord(iden, iden_2, d1_r, d2_r, base_d, to):
	#Corrige cuando el iden_2 elegido no es el que cierra el rango. A lo mejor por distancia está más cerca, pero no es el correcto
	iden_c = iden_2
	if((iden_2 == iden -1 or (iden_2 == to and iden == 0)) and d1_r > base_d[iden_2]):
		iden_c = iden + 1
		iden_c = correccion_iden(iden,iden_c,to,1)
	elif((iden_2 == iden + 1 or (iden_2 == 0 and iden == to)) and d2_r > base_d[iden]):
		iden_c = iden - 1
		iden_c = correccion_iden(iden,iden_c,to,0)		
	return iden_c
	

def eleccion_sig_coord(x_m,y_m,ux,uy,iden,to,d,base_d): ############
	#Coordenadas siempre en sentido horario
	iden_2=999999999
	id1=iden-1
	id2=iden+1
	id1 = correccion_iden(iden,id1,to,0)
	id2 = correccion_iden(iden,id2,to,1)
	d1 = dist_coords(x_m,y_m,ux[id1],uy[id1]) 
	d2 = dist_coords(x_m,y_m,ux[id2],uy[id2])
	d1_r = th_cos(d1,d,base_d[id1])
	d2_r = th_cos(d2,d,base_d[iden])
	if(d2_r <= d1_r):
		iden_2 = id2
	elif(d2_r > d1_r):               
		iden_2 = id1
	iden_2 = correccion_sig_coord(iden, iden_2, d1_r, d2_r, base_d, to)
	return iden_2

def caza_iden(x_m,y_m,ux,uy,to):
	d=9999999999
	iden = 99999
	for i in range(to+1):
		d2 = dist_coords(x_m,y_m,ux[i],uy[i])
		if(d2<d):			
			iden=i
			d=d2
	return d, iden

def franja_coords(x_m,y_m,ux,uy,base_d,to):
	d, iden = caza_iden(x_m,y_m,ux,uy,to)
	iden_2 = eleccion_sig_coord(x_m,y_m,ux,uy,iden,to,d,base_d)
	#print "iden: " + str(iden)
	#print "iden 2: " + str(iden_2)
	#print "distancia a iden:  " + str(d) + "m"
	#print "distancia a iden 2: " + str(dist_coords(x_m,y_m,ux[iden_2],uy[iden_2])) + "m"
	return iden, iden_2, d

def suma_distancias(id_inf,id_top,dc_p,ds_p,base,sentido,to):
	#id_inf: id del punto inferior de la base_d
	#id_top: id del punto superior de la base_d
	#dc_p: distancia coche punto siguiente
	#ds_p: distancia semaforo punto anterior
	if(sentido=="horario"):
		if(id_inf<id_top):
			dist = base[id_inf:id_top]
			distancia_medio = numpy.sum(dist)
		elif(id_inf>id_top):
			dist_fin = numpy.sum(base[id_inf:to+1])#]) + base[to] #base[to] es distancia de ultima coord a la primera
			if(id_top==0):
				dist_init = 0
			else:
				dist_init = numpy.sum(base[0:id_top])
			distancia_medio = dist_fin + dist_init
		else:
			distancia_medio=0
	elif(sentido=="antihorario"):
		if(id_inf<id_top):
			if(id_inf==0):
				dist_init = 0
			else:				
				dist_init = numpy.sum(base[0:id_inf])
			dist_fin = numpy.sum(base[id_top:to+1])#]) + base[to] le sumo uno, en vez de sumar base[to], parece lo mismo
			distancia_medio = dist_fin + dist_init
		elif(id_inf>id_top):
			dist = base[id_top:id_inf]
			distancia_medio = numpy.sum(dist)
		else:
			distancia_medio =0
	#print "Distancia proyectada coche-iden: " + str(dc_p) + "m"
	#print "Distancia proyectada semaforo-iden_s: " + str(ds_p) + "m"
	#print "Distancia medio iden inf y top: " + str(distancia_medio) + "m"
	return dc_p+ds_p+distancia_medio

def semaforo_justo_atras(x_m,y_m,xs_m,ys_m,ux,uy,iden,iden_2,iden_s,iden_s2,sentido,to,d,d_s,base_d): 
	#Valido en mismo rango de iden
	atras=False
	if((iden_s == iden_s2-1) or (iden_s == to and iden_s2 == 0)):
		ds_u = th_cos(d_s,dist_coords(xs_m,ys_m,ux[iden_s2],uy[iden_s2]),base_d[iden_s])
		if(iden == iden_s):
			dc_u = th_cos(d,dist_coords(x_m,y_m,ux[iden_2],uy[iden_2]),base_d[iden])
		else:
			dc_u = th_cos(dist_coords(x_m,y_m,ux[iden_2],uy[iden_2]),d,base_d[iden_2])
	elif((iden_s2 == iden_s-1) or (iden_s2 == to and iden_s == 0)):
		ds_u = th_cos(dist_coords(xs_m,ys_m,ux[iden_s2],uy[iden_s2]),d_s,base_d[iden_s2])
		if(iden == iden_s2):
			dc_u = th_cos(d,dist_coords(x_m,y_m,ux[iden_2],uy[iden_2]),base_d[iden])
		else:
			dc_u = th_cos(dist_coords(x_m,y_m,ux[iden_2],uy[iden_2]),d,base_d[iden_2])
	if((sentido == "horario" and dc_u >= ds_u) or (sentido == "antihorario" and dc_u <= ds_u)):	
		atras = True
	return atras

def mismo_rango_iden(id1,id2,ids,ids2):
	igual = False
	if((id1 == ids and id2 == ids2) or (id1 == ids2 and ids == id2)):
		igual = True
	return igual

def mismo_iden_4(id1,id2,ids,ids2):
	igual = False
	if((id1 == id2 and ids == ids2) and id1 == ids):
		igual = True
	return igual


def distancias_pasado_sem(x_m,y_m,iden,iden_2,iden_s,iden_s2,sentido,to,base_d,d,d_s,ux,uy):
	dc_p = 0
	ds_p = 0
	iden_inf = 0
	iden_top = 0
	if(sentido == "horario"):
		if(iden == iden_s):
			if((iden - 1  == iden_s2) or (iden -1 == -1 and iden_s2 == to)):
				dc_p = th_cos(d,dist_coords(x_m,y_m,ux[iden_2],uy[iden_2]),base_d[iden_2])
				ds_p = th_cos(dist_coords(x_m,y_m,ux[iden_s2],uy[iden_s]),d_s,base_d[iden_s2])
				iden_inf = iden
				iden_top = iden_s2
			else:
				dc_p = th_cos(dist_coords(x_m,y_m,ux[iden_2],uy[iden_2]),d,base_d[iden])
				ds_p = th_cos(d_s,dist_coords(x_m,y_m,ux[iden_s2],uy[iden_s]),base_d[iden_s])
				iden_inf = iden_2
				iden_top = iden_s
		elif(iden == iden_s2):		
				dc_p = th_cos(d,dist_coords(x_m,y_m,ux[iden_2],uy[iden_2]),base_d[iden_2])
				ds_p = th_cos(d_s,dist_coords(x_m,y_m,ux[iden_s2],uy[iden_s]),base_d[iden_s])
				iden_inf = iden
				iden_top = iden_s
	elif(sentido == "antihorario"):
		if(iden == iden_s):
			if((iden + 1  == iden_s2) or (iden + 1 == to+1 and iden_s2 == 0)):
				dc_p = th_cos(d,dist_coords(x_m,y_m,ux[iden_2],uy[iden_2]),base_d[iden])
				ds_p = th_cos(dist_coords(x_m,y_m,ux[iden_s2],uy[iden_s2]),d_s,base_d[iden_s])
				iden_inf = iden
				iden_top = iden_s2
			else:
				dc_p = th_cos(dist_coords(x_m,y_m,ux[iden_2],uy[iden_2]),d,base_d[iden_2])
				ds_p = th_cos(d_s,dist_coords(x_m,y_m,ux[iden_s2],uy[iden_s2]),base_d[iden_s2])
				iden_inf = iden_2
				iden_top = iden_s
		elif(iden == iden_s2):		
				dc_p = th_cos(d,dist_coords(x_m,y_m,ux[iden_2],uy[iden_2]),base_d[iden])
				ds_p = th_cos(d_s,dist_coords(x_m,y_m,ux[iden_s2],uy[iden_s2]),base_d[iden_s2])
				iden_inf = iden
				iden_top = iden_s
	return dc_p, ds_p, iden_inf, iden_top

def distancia_restante(base_d,ux,uy,x_m,y_m,iden,iden_2,xs_m,ys_m,iden_s,iden_s2,sentido,d,d_s,to): 
	#la coord del semaforo sera una y fija
	#d es distancia a iden de coche
	#d_s es distancia a iden de semaforo
	distancia = 0
	if(mismo_iden_4(iden,iden_2,iden_s,iden_s2)):
		pass
	elif(mismo_rango_iden(iden,iden_2,iden_s,iden_s2)):
		s_atras = semaforo_justo_atras(x_m,y_m,xs_m,ys_m,ux,uy,iden,iden_2,iden_s,iden_s2,sentido,to,d,d_s,base_d)
		if not(s_atras): 
			#print "Estas frente al semaforo"
			distancia = dist_coords(x_m,y_m,xs_m,ys_m) 
		else:
			dc_p,ds_p,id_inf,id_top = distancias_pasado_sem(x_m,y_m,iden,iden_2,iden_s,iden_s2,sentido,to,base_d,d,d_s,ux,uy)
			#print "Justo acabas de pasar el semaforo"
			distancia = suma_distancias(id_inf,id_top,dc_p,ds_p,base_d,sentido,to)
	else:
		if(sentido=="horario"):
		#Coche-Siguiente Punto
			if(iden_2>iden):
				if(iden==0 and iden_2==to):
					dc_p= th_cos(d,dist_coords(x_m,y_m,ux[iden_2],uy[iden_2]),base_d[iden_2])	
					id_inf = iden
				else:
					dc_p= th_cos(dist_coords(x_m,y_m,ux[iden_2],uy[iden_2]),d,base_d[iden]) #dist coche-punto 
					id_inf=iden_2
			elif(iden_2<iden):
				if(iden==to and iden_2==0):
					dc_p= th_cos(dist_coords(x_m,y_m,ux[iden_2],uy[iden_2]),d,base_d[iden]) #dist coche-punto 
					id_inf=iden_2
				else:
					dc_p= th_cos(d,dist_coords(x_m,y_m,ux[iden_2],uy[iden_2]),base_d[iden_2])
					id_inf=iden
			else: #Cuando los iden son iguales, la distancia es cero al iden
				dc_p=0
				id_inf=iden				
			#Semáforo-Punto Anterior
			if(iden_s2>iden_s):
				if(iden_s == 0 and iden_s2==to): #El iden 2 es mayor, pero es la distancia se coge desde la ultima coord 
					ds_p= th_cos(dist_coords(xs_m,ys_m,ux[iden_s2],uy[iden_s2]),d_s,base_d[iden_s2])	
					id_top=iden_s2
				else:
					ds_p= th_cos(d_s,dist_coords(xs_m,ys_m,ux[iden_s2],uy[iden_s2]),base_d[iden_s]) 
					id_top=iden_s
			elif(iden_s2<iden_s):
				if(iden_s == to and iden_s2 == 0):
					ds_p= th_cos(d_s,dist_coords(xs_m,ys_m,ux[iden_s2],uy[iden_s2]),base_d[iden_s]) 
					id_top=iden_s
				else:
					ds_p= th_cos(dist_coords(xs_m,ys_m,ux[iden_s2],uy[iden_s2]),d_s,base_d[iden_s2])
					id_top=iden_s2		
			else:
				ds_p = 0
				id_top = iden_s
			distancia = suma_distancias(id_inf,id_top,dc_p,ds_p,base_d,sentido,to)
		elif(sentido=="antihorario"):			
			#Coche-Siguiente Punto
			if(iden_2>iden):
				if(iden == 0 and iden_2 == to):
					dc_p= th_cos(dist_coords(x_m,y_m,ux[iden_2],uy[iden_2]),d,base_d[iden_2]) 
					id_inf = iden_2
				else:
					dc_p= th_cos(d,dist_coords(x_m,y_m,ux[iden_2],uy[iden_2]),base_d[iden])
					id_inf = iden 
			elif(iden_2<iden):
				if(iden==to and iden_2==0):
					dc_p= th_cos(d,dist_coords(x_m,y_m,ux[iden_2],uy[iden_2]),base_d[iden])
					id_inf = iden 
				else:
					dc_p= th_cos(dist_coords(x_m,y_m,ux[iden_2],uy[iden_2]),d,base_d[iden_2]) 
					id_inf = iden_2
			else:
				dc_p=0
				id_inf = iden
			#Semáforo-Punto Anterior
			if(iden_s2>iden_s):
				if(iden_s == 0 and iden_s2==to):
					ds_p= th_cos(d_s,dist_coords(xs_m,ys_m,ux[iden_s2],uy[iden_s2]),base_d[iden_s2]) 
					id_top = iden_s
				else:
					ds_p= th_cos(dist_coords(xs_m,ys_m,ux[iden_s2],uy[iden_s2]),d_s,base_d[iden_s])
					id_top = iden_s2
			elif(iden_s2<iden_s):
				if(iden_s== to and iden_s2==0):
					ds_p= th_cos(dist_coords(xs_m,ys_m,ux[iden_s2],uy[iden_s2]),d_s,base_d[iden_s])
					id_top = iden_s2
				else:
					ds_p= th_cos(d_s,dist_coords(xs_m,ys_m,ux[iden_s2],uy[iden_s2]),base_d[iden_s2]) 
					id_top = iden_s
			else:
				ds_p=0
				id_top=iden_s
			distancia = suma_distancias(id_inf,id_top,dc_p,ds_p,base_d,sentido,to)
		else:
			print "No se sabe el sentido"	
	return distancia



def sentido(session,ux,uy,to):
	s=""
	print "Calculando el sentido..."
	p1 = 0
	id_p = 0
	id_p2 = 0
	while(id_p == id_p2):
		lo1, la1,v,hora= lectura(session)
		#time.sleep(0.05)
		if (p1!=0 and (lo1 != lo2 or la1 != la2)):
			calculando = False	
		else:
			lo2, la2, v,hora = lectura(session)
			p1=1		
			#time.sleep(0.05)
			if(lo1 != lo2 or la1 != la2):
				calculando = False
		x1_m, y1_m = deg2utm.grados2UTM(lo1,la2)
		x2_m, y2_m = deg2utm.grados2UTM(lo2,la2)
		d1, id_p = caza_iden(x1_m, y2_m,ux,uy,to)
		d2, id_p2 = caza_iden(x2_m, y2_m,ux,uy,to)
		if((id_p < id_p2) or (id_p==to and id_p2==0)):
			s = "horario"
		elif((id_p > id_p2) or (id_p==0 and id_p2==to)):
			s = "antihorario"
		print "IDENS: " + str(id_p) + " " + str(id_p2)
	return str(s)

def in_road(d,carril):
	return (d<carril)

