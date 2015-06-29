#!/usr/bin/python
# -*- coding: utf-8 -*-
from Tkinter import *
import Tkinter as tk
import controller
import sys
import os, time
def graficos():
	#PARAMETROS VENTANA
	bg_w="black"
	fg_l0="orange"
	fg_l1="orange"
	fg_l2="orange"
	fg_l3="orange"
	fg_l4="orange"
	fg_l5="orange"
	fg_l6="orange"
	bg_l0="black"
	bg_l1="black"
	bg_l2="black"
	bg_l3="black"
	bg_l4="black"
	bg_l5="black"
	bg_l6="black"
	############################### VENTANA #############################################################
	root = tk.Tk()
	#root.withdraw()
	ox,oy=root.winfo_screenwidth()/2,root.winfo_screenheight()/2
	root.geometry("=320x240+%d+%d" % (ox-160,oy-120) )
	root.title("Coche fantástico")
	root.config(bg=str(bg_w))
	############################### INFO ################################################################
	info = StringVar()
	label0 = Label(root, textvar=info)
	label0.config(fg = str(fg_l0), bg = str(bg_l0))
	label0.config(font = ("Helvetica", 12, "bold italic"))
	label0.place(x=5,y=20)
	############################### V LLEGAR ############################################################
	v_llegar_med= StringVar()
	label1 = Label(root, textvar=v_llegar_med,height=1,width=3)
	label1.config(fg = str(fg_l1), bg = str(bg_l1))
	label1.config(font = ("Helvetica", 64, "bold italic"))
	label1.place(x=50,y=50)
	label2 = tk.Label(root, text= "km/h")
	label2.config(fg = str(fg_l2), bg = str(bg_l2))
	label2.config(font = ("Helvetica", 24, "bold italic"))
	label2.place(x=180,y=90)
	############################### DISTANCIA POR RECORRER ##############################################
	distance =StringVar()
	label3 = tk.Label(root, textvar=distance)
	label3.config(fg = str(fg_l3), bg = str(bg_l3))
	label3.config(font = ("Helvetica", 12, "bold italic"))
	label3.place(x=5,y=180)#210)
	label4 = tk.Label(root, text="km to semaphore")
	label4.config(fg = str(fg_l4), bg = str(bg_l4))
	label4.config(font = ("Helvetica", 12, "bold italic"))
	label4.place(x=50,y=180)#210)
	############################### V ACTUAL ############################################################
	v_act =StringVar()
	label5 = tk.Label(root, textvar=v_act)
	label5.config(fg = str(fg_l5), bg = str(bg_l5))
	label5.config(font = ("Helvetica", 24, "bold italic"))
	label5.place(x=230,y=170)#200)
	label6 = tk.Label(root, text= "km/h")
	label6.config(fg = str(fg_l6), bg = str(bg_l6))
	label6.config(font = ("Helvetica", 12, "bold italic"))
	label6.place(x=270,y=180)#210)
	return root,info,v_llegar_med,distance,v_act

def imprime_interfaz(info,v_llegar_med,distance,v_act,decision,decision_ant,vv_llegar_med,v_coche,dist,d_z1,d_z2,z_ant,sentido,actual_state,vv_llegar_med_ant,lo,la,hora,recibiendo,diccionario,escribe,mensajes_recibidos):
	z = controller.zona(dist,d_z1,d_z2)
	os.system('clear')
	print "ZONA: "+ str(z)
	print "##################################"
	print "Sentido: " + str(sentido)
	print "Distancia a semaforo: " + str(dist)
	if((z=!z_ant) or z ==2):
		print decision
		info.set(str(decision))
		if(vv_llegar_med=="--"):
			print "--"
			v_llegar_med.set(vv_llegar_med)
		else:
			print str(int(vv_llegar_med))+ " km/h"
			v_llegar_med.set(str(int(vv_llegar_med)))
		z_ant = z
		decision_ant = decision
		vv_llegar_med_ant = vv_llegar_med
	else:
		print decision_ant
		info.set(str(decision_ant))
		if(vv_llegar_med_ant=="--"):
			print "--"
			v_llegar_med.set(vv_llegar_med_ant)
		else:
			print str(int(vv_llegar_med_ant))+ " km/h"
			v_llegar_med.set(str(int(vv_llegar_med_ant)))
	v_act.set(str(int(v_coche)))
	print actual_state
	print "##################################"
	distance.set(str(round((dist/1000),3)))

	if(escribe):
		#LOG FILE
		version = sys.argv[1] 	
		outfile = open('logfile_car_v' + str(version) +'.txt', 'a') 
		s=0
		for linea in diccionario:
			outfile.write((str(diccionario[s])))
			s+=1
		outfile.close()
		diccionario=[]
	else:
		diccionario.append(str(z)+","+str(lo)+","+str(la)+","+str(hora)+","+str(dist)+","+str(v_coche)+","+str(recibiendo)+","+str(vv_llegar_med_ant)+","+str(decision_ant)+","+str(actual_state) + "," + str(mensajes_recibidos) + '\n')

	print str(z)+","+str(lo)+","+str(la)+","+str(hora)+","+str(dist)+","+str(v_coche)+","+str(recibiendo)+","+str(vv_llegar_med_ant)+","+str(decision_ant)+","+str(actual_state)+"," + str(mensajes_recibidos) 
	return z_ant, decision_ant,vv_llegar_med_ant,diccionario

