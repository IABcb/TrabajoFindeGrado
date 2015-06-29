#!/usr/bin/python
# -*- coding: utf-8 -*-
#coordenadas cogidas en sentido horario, sentido del coche antihorario
import proc_data_map
import deg2utm

def coordenadas():
	#PARA PARKING
	#longitudesX, latitudesY = proc_data_map.coordenadas("coords_parking.txt")

	#URJC
	longitudesX, latitudesY = proc_data_map.coordenadas("coords_urjc.txt")

	UTM_X , UTM_Y , zone = deg2utm.conversionCoord(longitudesX,latitudesY)

	return(longitudesX,latitudesY,UTM_X,UTM_Y)

