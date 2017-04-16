import random as rand
import numpy as np
import matplotlib.pyplot as plt


class Route :
    
    def __init__(self, ville1, ville2) :
        self.pheromone = 0
        self.villes = [ville1, ville2]
        self.distance = float(np.sqrt((ville1.X -ville2.X)**2+(ville1.Y-ville2.Y)**2))
        self.route_dir = (float(ville2.Y-ville1.Y))/(ville2.X-ville1.X)
        
    def evaporer_Pheromone(self) :
        self.pheromone = 0.7*self.pheromone
    
    def get_villes(self):
        return self.villes
    
    def get_distance(self) :
        return self.distance
    
    def qte_pheromones(self) :
        return self.pheromone
        
    def augmente_pheromone(self, pheromone):
        self.pheromone += pheromone
    
    def route_dir(self):
        return self.route_dir


class Ville :
    
    def __init__(self, nom, X, Y):
        self.nom = nom
        self.X = X
        self.Y = Y
     
    def get_position(self):
        return np.array([self.X, self.Y])


class Fourmi :
    
    def __init__(self, alpha, beta, gamma, position, last_ville, current_route, step):
        self.alpha = alpha # alpha sur [0, 1] 0 : exploration, 1 : tendance à suivre 
        self.beta = beta # capacité à déposer de la phéromone
        self.gamma = gamma # remplacer step par gamma pour jouer sur la vitesse de déplacement de la fourmi ?
        self.porte_nourriture = False
        self.nourriture_collectee = 0
        self.memoire_routes = []
        self.nb_fois_meme_route = 0
        self.position = position
        self.last_ville = last_ville
        self.current_route = current_route
        self.step = step

    def prendre_nourriture(self):
        self.porte_nourriture = True
        self.nourriture_collectee += 1
    
    def laisser_nourriture(self):
        self.porte_nourriture = False
    
    def deposer_pheromone(self):
        self.route.augmente_pheromone()
        
    def marcher(self, routes):
        if self.current_route.get_villes()[0] != self.last_ville :
            next_ville = self.current_route.get_villes()[0]
        else :
            next_ville = self.current_route.get_villes()[1]
        if np.linalg.norm(self.position - next_ville.get_position()) <=10 :
            self.position = next_ville.get_position()
            self.last_ville = next_ville
            self.current_route = self.choix_chemin(routes)
            self.memoire_routes.append(self.current_route)
        #self.position = self.position + np.array([sens*self.step, sens*self.current_route.route_dir*self.step])
        else :
            self.position = self.position + (next_ville.get_position() - self.position)*self.step/np.linalg.norm(self.position - next_ville.get_position())
        #print self.position
        self.current_route.augmente_pheromone(self.beta) # un truc à voir ici parce que plus la route est longue, plus il y aura de pheromone
        

    def choix_chemin(self, routes):
        routes_dispo = []
        liste_choix =[]
        liste2 = []
        for r in routes :
            if r.get_villes()[0] == self.last_ville or r.get_villes()[1] == self.last_ville :
                routes_dispo.append(r)
        for e in routes_dispo:
            qte_pheromones = int(100*e.qte_pheromones()/e.get_distance())
            liste_choix.append(e)
            liste2.append(e) # liste avec une fois chaque chemin dispo
            for i in range(qte_pheromones):
                liste_choix.append(e) # liste avec phéromone fois chaque chemin dispo
        epsilon = rand.random()
        if epsilon > self.alpha :
            route_choisie = rand.choice(liste2) # exploration favorisée
        else :
            route_choisie = rand.choice(liste_choix) # suit les hauts taux de phéromone (mais toujours exploration)
        return route_choisie
    
    def getpos(self) :
        return self.position


class Civilisation :
    
    def __init__(self, routes = [(0,1), (1,2), (1,3), (2,3), (3,4)], villes=[('nid', 0,0), ('ville1', 20, 20), ('ville2', 70, 30), ('ville3', 50, 80), ('food', 100, 50)]):
        self.villes = [Ville(v[0], v[1], v[2]) for v in villes]
        self.ville_nid = self.villes[0]
        self.ville_food = self.villes[-1]
        self.routes = [Route(self.villes[r[0]], self.villes[r[1]]) for r in routes]
        self.fourmis = [Fourmi(rand.random(), 5*rand.random(), 5*rand.random(), self.ville_nid.get_position(),  self.ville_nid, self.routes[0], 5*rand.random()) for i in range(20)]
        self.fourmideter =Fourmi(1, 0, rand.random(), self.ville_nid.get_position(),  self.ville_nid, self.routes[0], 5)
    
    def tourSuivant(self) :
        for fourmi in self.fourmis :
            if np.linalg.norm(fourmi.getpos() - self.ville_food.get_position())==0 and fourmi.porte_nourriture==False :
                fourmi.prendre_nourriture()
            elif np.linalg.norm(fourmi.getpos() - self.ville_nid.get_position())==0 and fourmi.porte_nourriture == True :
                fourmi.laisser_nourriture()
            else :
                fourmi.marcher(self.routes)
                
    def pos_fourmi(self):
        X = []
        Y = []
        for f in self.fourmis :
            pos = f.getpos()
            X.append(pos[0])
            Y.append(pos[1])
        return (X,Y)
        
    def fin(self):
        X = []
        Y = []
        for i in range (2000):
            self.tourSuivant()
        while np.linalg.norm(self.fourmideter.getpos() - self.ville_food.get_position()) !=0  :
            self.fourmideter.marcher(self.routes)
            pos = self.fourmideter.getpos()
            X.append(pos[0])
            Y.append(pos[1])
        plt.plot(X,Y, '.')
        plt.show()
            
                
def traitement():
    
    civ = Civilisation()
    X = []
    Y = []
    plt.plot([0,20,70,50,100], [0,20,30,80,50], '+')
    for i in range(1000):
        civ.tourSuivant()
        pos = civ.pos_fourmi()
        X.append(pos[0])
        Y.append(pos[1])
    for r in civ.routes :
        print r.qte_pheromones()
    plt.plot(X,Y,'.')
    plt.show()
    '''
    civ = Civilisation()
    civ.fin()'''