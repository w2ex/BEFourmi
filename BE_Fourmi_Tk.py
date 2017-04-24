# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 13:59:19 2017

@author: Thomas
"""

from Tkinter import *
import random

NB_FOURMIS = IntVar(Mafenetre)


LISTE_COORDS_ANTS = []

NB_ITERATIONS = IntVar(Mafenetre)


CITY1 = 0
CITY2 = 0

DEBUT_LIGNE = (0,0)
FIN_LIGNE = (0,0)

RIGHT_CLICKED1 = False
RIGHT_CLICKED2 = False

DETECTION_CLIC_SUR_OBJET = False

LISTE_VILLES = []

LISTE_COORDS_VILLES = []
LISTE_ROUTES = []

NB_VILLES = 0


def Go():
    global LISTE_ROUTES
    global LISTE_COORDS_VILLES
    global NB_FOURMIS
    global NB_ITERATIONS
    global LISTE_COORDS_ANTS
    
    print(NB_FOURMIS)
    print(NB_ITERATIONS)
    # on retire les routes doublons et les routes de X à X
    processing()
    print("processing done")
    print(LISTE_ROUTES)
    # fourmilière
    r = 7
    home = LISTE_COORDS_VILLES[0]
    Canevas.create_rectangle(home[0]-r, home[1]-r, home[0]+r, home[1]+r, outline='black', fill='blue')
    # source de nourriture
    food = LISTE_COORDS_VILLES[-1]
    Canevas.create_rectangle(food[0]-r, food[1]-r, food[0]+r, food[1]+r, outline='black', fill='blue')
    print("rectanges created")
    civ = Civilisation(LISTE_ROUTES, LISTE_COORDS_VILLES, NB_FOURMIS)
    for i in range(NB_ITERATIONS):
        civ.tourSuivant()
        LISTE_COORDS_ANTS = civ.get_ants_position()
    
def processing():
    global LISTE_ROUTES
    list(set(LISTE_ROUTES))
    for i in xrange(len(LISTE_ROUTES)):
        if LISTE_ROUTES[i][0] == LISTE_ROUTES[i][1]:
            LISTE_ROUTES.remove(LISTE_ROUTES[i])
    
def impr(x):
    print(x)

def Clic_ville(event):
    """ Gestion de l'événement Clic gauche sur la zone graphique """
    global NB_VILLES
    global LISTE_VILLES
    global LISTE_COORDS_VILLES
    
    # position du pointeur de la souris
    X = event.x
    Y = event.y
    # on dessine un carré
    r = 5
    outline_color = 'black'
    fill_color = 'green'
    LISTE_VILLES.append(Canevas.create_rectangle(X-r, Y-r, X+r, Y+r, outline=outline_color,fill=fill_color))
    LISTE_COORDS_VILLES.append((X,Y))
    NB_VILLES += 1
    
    print("La liste des villes : " + str(LISTE_VILLES))
    print("La liste des coordonnées : " + str(LISTE_COORDS_VILLES))

def Clic_route(event):
    """ Gestion de l'événement Clic gauche """
    global DETECTION_CLIC_SUR_OBJET
    global RIGHT_CLICKED1
    global RIGHT_CLICKED2
    global DEBUT_LIGNE
    global FIN_LIGNE
    global LISTE_ROUTES
    global CITY1
    global CITY2

    # position du pointeur de la souris
    X = event.x
    Y = event.y
    print("Position du clic -> ",X,Y)

    if not(RIGHT_CLICKED1):
        # coordonnées des villes
        for i in xrange(len(LISTE_VILLES)):
            city = LISTE_VILLES[i]
            [xmin,ymin,xmax,ymax] = Canevas.coords(city)
            print("Position objet -> ",xmin,ymin,xmax,ymax)
            if xmin<=X<=xmax and ymin<=Y<=ymax: 
                DETECTION_CLIC_SUR_OBJET = True
                DEBUT_LIGNE = (xmin+xmax)/2, (ymin+ymax)/2
                RIGHT_CLICKED1 = True
                CITY1 = i
            else: 
                DETECTION_CLIC_SUR_OBJET = False
                #print("DETECTION CLIC SUR OBJET -> ",DETECTION_CLIC_SUR_OBJET)
    else:
        for i in xrange(len(LISTE_VILLES)):
            city = LISTE_VILLES[i]
            [xmin,ymin,xmax,ymax] = Canevas.coords(city)
            print("Position objet -> ",xmin,ymin,xmax,ymax)
            if xmin<=X<=xmax and ymin<=Y<=ymax: 
                DETECTION_CLIC_SUR_OBJET = True
                FIN_LIGNE = (xmin+xmax)/2, (ymin+ymax)/2
                RIGHT_CLICKED2 = True
                CITY2 = i
                LISTE_ROUTES.append((CITY1,CITY2))
            else: 
                DETECTION_CLIC_SUR_OBJET = False
                #print("DETECTION CLIC SUR OBJET -> ",DETECTION_CLIC_SUR_OBJET)
    
    if RIGHT_CLICKED1 and RIGHT_CLICKED2:
        x0 = DEBUT_LIGNE[0]
        y0 = DEBUT_LIGNE[1]
        x1 = FIN_LIGNE[0]
        y1 = FIN_LIGNE[1]
        fill_color = 'blue'
        Canevas.create_line(x0,y0,x1,y1,fill=fill_color)
        RIGHT_CLICKED1 = False
        RIGHT_CLICKED2 = False
        CITY1 = 0
        CITY2 = 0
        print("La liste des routes : " + str(LISTE_ROUTES))

def Effacer():
    """ Efface la zone graphique et reset de variables globales """
    global CITY1
    global CITY2
    global DEBUT_LIGNE
    global FIN_LIGNE
    global RIGHT_CLICKED1
    global RIGHT_CLICKED2
    global DETECTION_CLIC_SUR_OBJET
    global LISTE_VILLES
    global LISTE_COORDS_VILLES
    global LISTE_ROUTES
    global NB_VILLES
    
    Canevas.delete(ALL)
    CITY1 = 0
    CITY2 = 0
    DEBUT_LIGNE = (0,0)
    FIN_LIGNE = (0,0)
    RIGHT_CLICKED1 = False
    RIGHT_CLICKED2 = False
    DETECTION_CLIC_SUR_OBJET = False
    LISTE_VILLES = []
    LISTE_COORDS_VILLES = []
    LISTE_ROUTES = []
    NB_VILLES = 0

## Elements graphiques

# Création de la fenêtre principale (main window)
Mafenetre = Tk()
Mafenetre.title('Colonie de fourmis & Problème du plus court chemin')


# Création d'un widget Frame pour le canvas
Frame0 = Frame(Mafenetre,borderwidth=2,relief=GROOVE)
Frame0.pack(side=RIGHT,padx=10,pady=10)


# Création d'un widget Canvas (zone graphique)
Largeur = 800
Hauteur = 600
Canevas = Canvas(Frame0, width = Largeur, height =Hauteur, bg ='white')
# La méthode bind() permet de lier un événement avec une fonction :
# un clic gauche sur la zone graphique provoquera l'appel de la fonction utilisateur Clic_xxxx()
Canevas.bind('<Button-1>', Clic_ville)
Canevas.bind('<Button-3>', Clic_route)

Canevas.focus_set()
Canevas.pack(padx=10,pady=10)



# Création de la Frame de texte
FrameX = Frame(Mafenetre, borderwidth=2, relief=GROOVE)
FrameX.pack(side=TOP, padx=10, pady=10)

# création d'un widget Frame dans la fenêtre principale, pour les options
Frame1 = Frame(Mafenetre,borderwidth=2,relief=GROOVE)
Frame1.pack(side=TOP,padx=10,pady=10)


# Création d'un widget Label équivalent Readme
Label1 = Label(FrameX, text = 'Clic gauche sur la zone graphique = Ville', fg = 'black')
Label1.pack()
Label2 = Label(FrameX, text='Clic droit sur ville A + clic droit sur ville B = route de A à B', fg='black')
Label2.pack()
Label3 = Label(FrameX, text='/!\ : la première ville = fourmilière, la dernière = la source de nourriture', fg='black')
Label3.pack()
Label4 = Label(FrameX, text='/!\ : ne pas rajouter de villes ou de routes pendant la simulation', fg='black')
Label4.pack()


# Création d'un widget Scale fourmis
echelle = Scale(Frame1,from_=1,to=100,resolution=1,orient=  HORIZONTAL,\
length=300,width=20,label="Nombre de fourmis",tickinterval=99, variable=NB_FOURMIS, command=impr)
echelle.pack(side = TOP, padx=10,pady=10)


# Création d'un widget Scale iterations
echelle = Scale(Frame1,from_=1000,to=20000,resolution=1000,orient=HORIZONTAL,\
length=500,width=20,label="Nombre d'itérations",tickinterval=2000, variable=NB_ITERATIONS, command=impr)
echelle.pack(side = TOP, padx=10,pady=10)

# Création d'un widget Button (bouton Go)
BoutonGo = Button(Frame1, text ='Go', command = Go)
BoutonGo.pack(side = TOP, padx = 10, pady = 10)

# Création d'un widget Button (bouton Effacer)
BoutonEffacer = Button(Frame1, text ='Effacer', command = Effacer)
BoutonEffacer.pack(side = TOP, padx = 5, pady = 5)

# Création d'un widget Button (bouton Quitter)
BoutonQuitter = Button(Frame1, text ='Quitter', command = Mafenetre.destroy)
BoutonQuitter.pack(side = TOP, padx = 5, pady = 5)

Mafenetre.mainloop()