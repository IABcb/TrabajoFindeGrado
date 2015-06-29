#!/usr/bin/python
# -*- coding: utf-8 -*-
#import os

def coordenadas(ruta):
	#os.system(ruta) #Doy todos los permisos para no tener problemas al trabajar con fichero
	latitudesY = []
	longitudesX = []
	f = open(ruta,"r")
	for lat_long in f:
     		latitudesY.append(float(lat_long.split('@')[0]))
		longitudesX.append(float(lat_long.split('@')[1]))		
	f.close()  
	return longitudesX, latitudesY
