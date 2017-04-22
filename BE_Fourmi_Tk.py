# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 13:59:19 2017

@author: Thomas
"""

from Tkinter import *
import random

def Cercle():
    """ Dessine un cercle de centre (x,y) et de rayon r """
    x = random.randint(0,Largeur)
    y = random.randint(0,Hauteur)
    r = 20
    Canevas.create_oval(x-r, y-r, x+r, y+r, outline='blue', fill='blue')

def Clic_ville(event):
    """ Gestion de l'événement Clic gauche sur la zone graphique """
    global NB_VILLES
    global LISTE_VILLES
    
    # position du pointeur de la souris
    X = event.x
    Y = event.y
    # on dessine un carré
    r = 5
    outline_color = 'black'
    fill_color = 'green'
    LISTE_VILLES.append(Canevas.create_rectangle(X-r, Y-r, X+r, Y+r, outline=outline_color,fill=fill_color))
    NB_VILLES += 1
    
    print(LISTE_VILLES)
    print(NB_VILLES)


def Clic_route(event):
    """ Gestion de l'événement Clic gauche """
    global DETECTION_CLIC_SUR_OBJET
    global RIGHT_CLICKED1
    global RIGHT_CLICKED2
    global DEBUT_LIGNE
    global FIN_LIGNE

    # position du pointeur de la souris
    X = event.x
    Y = event.y
    print("Position du clic -> ",X,Y)

    if not(RIGHT_CLICKED1):
        # coordonnées des villes
        for city in LISTE_VILLES:
            [xmin,ymin,xmax,ymax] = Canevas.coords(city)
            print("Position objet -> ",xmin,ymin,xmax,ymax)
            if xmin<=X<=xmax and ymin<=Y<=ymax: 
                DETECTION_CLIC_SUR_OBJET = True
                DEBUT_LIGNE = (xmin+xmax)/2, (ymin+ymax)/2
                RIGHT_CLICKED1 = True
            else: 
                DETECTION_CLIC_SUR_OBJET = False
                print("DETECTION CLIC SUR OBJET -> ",DETECTION_CLIC_SUR_OBJET)
    else:
        for city in LISTE_VILLES:
            [xmin,ymin,xmax,ymax] = Canevas.coords(city)
            print("Position objet -> ",xmin,ymin,xmax,ymax)
            if xmin<=X<=xmax and ymin<=Y<=ymax: 
                DETECTION_CLIC_SUR_OBJET = True
                FIN_LIGNE = (xmin+xmax)/2, (ymin+ymax)/2
                RIGHT_CLICKED2 = True
            else: 
                DETECTION_CLIC_SUR_OBJET = False
                print("DETECTION CLIC SUR OBJET -> ",DETECTION_CLIC_SUR_OBJET)
      
    if RIGHT_CLICKED1 and RIGHT_CLICKED2:
        x0 = DEBUT_LIGNE[0]
        y0 = DEBUT_LIGNE[1]
        x1 = FIN_LIGNE[0]
        y1 = FIN_LIGNE[1]
        fill_color = 'blue'
        Canevas.create_line(x0,y0,x1,y1,fill=fill_color)
        RIGHT_CLICKED1 = False
        RIGHT_CLICKED2 = False



DEBUT_LIGNE = (0,0)
FIN_LIGNE = (0,0)


RIGHT_CLICKED1 = False
RIGHT_CLICKED2 = False


DETECTION_CLIC_SUR_OBJET = False

LISTE_VILLES = []

NB_VILLES = 0

def Effacer():
    """ Efface la zone graphique """
    Canevas.delete(ALL)




# Création de la fenêtre principale (main window)
Mafenetre = Tk()
Mafenetre.title('Colonie de fourmis & Problème du plus court chemin')

# Création d'un widget Canvas (zone graphique)
Largeur = 480
Hauteur = 320
Canevas = Canvas(Mafenetre, width = Largeur, height =Hauteur, bg ='white')
# La méthode bind() permet de lier un événement avec une fonction :
# un clic gauche sur la zone graphique provoquera l'appel de la fonction utilisateur Clic_xxxx()
Canevas.bind('<Button-1>', Clic_ville)
Canevas.bind('<Button-3>', Clic_route)

Canevas.focus_set()
Canevas.pack(padx=10,pady=10)



# Création d'un widget Scale
echelle = Scale(Mafenetre,from_=1,to=100,resolution=1,orient=HORIZONTAL,\
length=300,width=20,label="Nombre de fourmis",tickinterval=99)
echelle.pack(padx=10,pady=10)


# Création d'un widget Button (bouton Go)
BoutonGo = Button(Mafenetre, text ='Go', command = Cercle)
BoutonGo.pack(side = LEFT, padx = 10, pady = 10)

# Création d'un widget Button (bouton Effacer)
BoutonEffacer = Button(Mafenetre, text ='Effacer', command = Effacer)
BoutonEffacer.pack(side = LEFT, padx = 5, pady = 5)

# Création d'un widget Button (bouton Quitter)
BoutonQuitter = Button(Mafenetre, text ='Quitter', command = Mafenetre.destroy)
BoutonQuitter.pack(side = LEFT, padx = 5, pady = 5)

Mafenetre.mainloop()