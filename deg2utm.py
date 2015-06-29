#!/usr/bin/python
# -*- coding utf-8 -*-
import numpy
import sys

def conversionCoord(longitudesX,latitudesY):
	n1=len(latitudesY)
	n2=len(longitudesX)
	if(n1!=n2):
		print("Number of coords. does not match")
		sys.exit(1) #Finalizacion del programa si las coordenadas no concuerdan
	else:
		#Creacion matrices
		utmzone = [None] * n1 # n1 son Filas
		UTM_X = [None] * n1
		UTM_Y = [None] * n1
		for j in range(n1):
			UTM_X[j] = [None] * 2 #2 columnas
			UTM_Y[j] = [None] * 2
			utmzone[j] = [None] * 2 
			utmzone[j][1] = '60 X'
		#Conversion coordenadas
		for i in range(n1):
			#la=latitudesY[i-1] ############ASi ESTABA EL MODELO
			#lo=longitudesX[i-1]
			la=latitudesY[i]
			lo=longitudesX[i]
   			sa = 6378137.000000 
			sb = 6356752.314245
			#e = ( ( ( sa ** 2 ) - ( sb ** 2 ) ) ** 0.5 ) / sa???????
     			e2 = ( ( ( sa ** 2 ) - ( sb ** 2 ) ) ** 0.5 ) / sb
			e2cuadrada = e2 ** 2.0
			c = ( sa ** 2.0 ) / sb
		 	#alpha = ( sa - sb ) / sa;             %f??????
			#ablandamiento = 1 / alpha;   % 1/f??????

			lat = la * ( numpy.pi / float(180) )
			lon = lo * ( numpy.pi / float(180) )

			huso = int( ( lo / 6 ) + 31) #parte entera decimal para el huso horario
			S = ( ( huso * 6 ) - 183 )
			deltaS = lon - ( S * ( numpy.pi / float(180) ) )

			if (la<-72): letra='C'
			elif (la<-64):
				letra='D'
			elif (la<-56): 
				letra='E'
			elif (la<-48): 
				letra='F'
			elif (la<-40): 
				letra='G'
			elif (la<-32): 
				letra='H'
			elif (la<-24): 
				letra='J'
			elif (la<-16): 
				letra='K'
			elif (la<-8): 
				letra='L'
			elif (la<0): 
				letra='M'
			elif (la<8): 
				letra='N'
			elif (la<16): 
				letra='P'
			elif (la<24): 
				letra='Q'
			elif (la<32): 
				letra='R'
			elif (la<40): 
				letra='S'
			elif (la<48): 
				letra='T'
			elif (la<56): 
				letra='U'
			elif (la<64): 
				letra='V'
			elif (la<72): 
				letra='W'
			else:
				letra='X'
			

			a = numpy.cos(lat) * numpy.sin(deltaS)
			epsilon = 0.5 * numpy.log( ( 1 +  a) / ( 1 - a ) )
			nu = numpy.arctan( numpy.tan(lat) / numpy.cos(deltaS) ) - lat
			v = ( c / ( ( 1 + ( e2cuadrada * ( numpy.cos(lat) ) ** 2 ) ) ) ** 0.5 ) * 0.9996
			ta = ( e2cuadrada / 2 ) * epsilon ** 2 * ( numpy.cos(lat) ) ** 2
			a1 = numpy.sin( 2 * lat )
			a2 = a1 * ( numpy.cos(lat) ) ** 2
			j2 = lat + ( a1 / 2 )
			j4 = ( ( 3 * j2 ) + a2 ) / 4
			j6 = ( ( 5 * j4 ) + ( a2 * ( numpy.cos(lat) ) ** 2) ) / 3
			alfa = ( 3 / 4 ) * e2cuadrada
			beta = ( 5 / 3 ) * alfa ** 2
			gama = ( 35 / 27 ) * alfa ** 3
			Bm = 0.9996 * c * ( lat - alfa * j2 + beta * j4 - gama * j6 )
			xx = epsilon * v * ( 1 + ( ta / 3 ) ) + 500000
			yy = nu * v * ( 1 + ta ) + Bm

			if (yy<0):
			    yy=9999999+yy
			UTM_X[i]=xx
			UTM_Y[i]=yy
			utmzone[i][0]=str(huso) + ' ' + letra
	return UTM_X , UTM_Y , utmzone


def grados2UTM(lo,la):
	#Conversion coordenadas
	sa = 6378137.000000 
	sb = 6356752.314245
	lo=float(lo)
	la=float(la)
	e2 = ( ( ( sa ** 2 ) - ( sb ** 2 ) ) ** 0.5 ) / sb
	e2cuadrada = e2 ** 2.0
	c = ( sa ** 2.0 ) / sb
	lat = la * ( numpy.pi / float(180) )
	lon = lo * ( numpy.pi / float(180) )
	huso = int( ( lo / 6 ) + 31) #parte entera decimal para el huso horario
	S = ( ( huso * 6 ) - 183 )
	deltaS = lon - ( S * ( numpy.pi / float(180) ) )
	a = numpy.cos(lat) * numpy.sin(deltaS)
	epsilon = 0.5 * numpy.log( ( 1 +  a) / ( 1 - a ) )
	nu = numpy.arctan( numpy.tan(lat) / numpy.cos(deltaS) ) - lat
	v = ( c / ( ( 1 + ( e2cuadrada * ( numpy.cos(lat) ) ** 2 ) ) ) ** 0.5 ) * 0.9996
	ta = ( e2cuadrada / 2 ) * epsilon ** 2 * ( numpy.cos(lat) ) ** 2
	a1 = numpy.sin( 2 * lat )
	a2 = a1 * ( numpy.cos(lat) ) ** 2
	j2 = lat + ( a1 / 2 )
	j4 = ( ( 3 * j2 ) + a2 ) / 4
	j6 = ( ( 5 * j4 ) + ( a2 * ( numpy.cos(lat) ) ** 2) ) / 3
	alfa = ( 3 / 4 ) * e2cuadrada
	beta = ( 5 / 3 ) * alfa ** 2
	gama = ( 35 / 27 ) * alfa ** 3
	Bm = 0.9996 * c * ( lat - alfa * j2 + beta * j4 - gama * j6 )
	xx = epsilon * v * ( 1 + ( ta / 3 ) ) + 500000
	yy = nu * v * ( 1 + ta ) + Bm
	if (yy<0):
	    yy=9999999+yy
	UTM_X=xx
	UTM_Y=yy
	return UTM_X , UTM_Y
