#    ---------------------------------------------------------------------------------------------------------------
#   |                                 PROJET TSP - AI - ALGORITHME GENETIQUE                                        |
#   |    Realisation : TOUATI MOUNIA  N°20225680 (L3CILS)   -    ALKHOURI George  N° 20214191 (L3CILS)              |  
#   |    Année Universitaire : 2023 / 2024                                                                          |
#     --------------------------------------------------------------------------------------------------------------

import numpy as np
import random
from tkinter  import *
import tkinter as tk
#___________________________________METHODES POUR L'ALGORITHMES GENETIQUE_____________________________________________
# Fonction pour calculer la matrice de distance entre villes 
def distances(Coord_Villes):
    tailleV = len(Coord_Villes)
    dist_villes = np.zeros ((tailleV,tailleV))
    for i in range (tailleV):
        for j in range (tailleV):
           dist_villes [i,j] = np.linalg.norm(Coord_Villes[i]-Coord_Villes[j])
    return dist_villes

#                      ----------------------------------------------------------------------------

#Creation d'une population initiale de solutions pour l'algorithme genetique 
def init_population(taillep,Coord_Villes):
    return [np.random.permutation(len(Coord_Villes)) for _ in range (taillep)]

#                      ----------------------------------------------------------------------------

#Calcule la "fitness" d'une solution basée sur la distance totale parcourue pour l'itinéraire donné
def fitness_idv (individu,distance_villes): 
    tailleV = len(distance_villes)
    return 1 / sum (distance_villes[individu[i],individu[(i + 1) % tailleV]] for i in range (tailleV)) #on utilise l'inverse de la distance totale de l'itinéraire comme valeur de fitness

#                      ----------------------------------------------------------------------------

#La selection des parents pour la reproduction en utilisant une méthode de sélection par tournoi.
def tournament_selection(population, fitness,tournament_size,num_parents):
   if tournament_size> len(population):
       raise ValueError ("la taille du tournoi doit etre inferieure ou egale a la taille de la population")
   if num_parents >len(population):
       raise ValueError("Le nombre de parents doit etre inferieur ou egal a la taille de la population")
   parents = []
   for _ in range(num_parents):
        tournament_indices = np.random.choice(len(population), tournament_size, replace=False)
        tournament_fitnesses = [fitness[i] for i in tournament_indices]
        best_index = tournament_indices[np.argmax(tournament_fitnesses)]
        parents.append(population[best_index])
   return parents

#                      ----------------------------------------------------------------------------

#Opération de croisement (dans ce probleme le croisement doit etre ordonné en assurant que la solution enfant herite des génes (indices ville) des deux parents sans répeter aucune ville)
def ox_Croisement(parent1,parent2):
    size = len(parent1) 
    enfant =[None]*size
    debut, fin = sorted(random.sample(range(size),2)) #selection aleatoire deux indices dans l'iteneraire qui erviront de début et de fin pour la section du parent1 à hériter. "sorted" assure que "debut" est avant "fin". 
    enfant[debut:fin+1]= parent1[debut:fin+1]#Copie une séquence continue du parent1 dans l'enfant, de l'indice debut à fin. Cette partie de l'itinéraire de parent1 est directement héritée par l'enfant
    indP2 = 0 #initialisation de l'indice pour commencer a verifier les elemetns de parent2
    for  i in range(size):
         if enfant[i]is None: #Vérifie si la position actuelle dans l'itinéraire de l'enfant est vide
              while parent2[indP2]in enfant : #Tant que l'élément de parent2 à l'indice indP2 est déjà dans l'itinéraire de l'enfant, continue de passer à l'élément suivant de parent2.
                  indP2+=1
              enfant[i]=parent2[indP2]#Ajoute l'élément courant de parent2 à la position actuelle de l'enfant.
              indP2+=1 # on avance pour la prochaine iteration 
    return np.array(enfant)# retourner la tableau numpy d'enfant 

#                        ----------------------------------------------------------------------------

# Mute une solution en échangeant deux villes de l'itinéraire avec un certain taux de mutation
def mutation (individu,mutation_rate):
    tailleV = len(individu)
    for i in range (tailleV):
        if random.random()<mutation_rate : 
            j= random.randint(0,tailleV-1)
            individu[i],individu [j]=individu[j],individu [i]
    return individu
#                        ----------------------------------------------------------------------------
# Fonction algorithme genetique


def algo_Genetique(Coords, taillep, n_generation, mutation_rate, taille_tournament, num_parent):
    distance_m = distances(Coords)  # calculer la matrice des distances entre villes 
    population = init_population(taillep, Coords)  # créer une population initiale de solutions (itinéraires)
    best_overall_individu = None
    best_overall_fitness = float('-inf')  # Initialiser avec l'infini négatif pour s'assurer que toute fitness sera plus grande

    for gen in range(n_generation):  # itérer sur le nombre de générations spécifié par n_generation
        fitness_scores = np.array([fitness_idv(ind, distance_m) for ind in population])  # calculer la fitness pour chaque individu de la population
        new_population = []  # initialisation de la nouvelle population pour stocker la nouvelle génération de solutions

        while len(new_population) < taillep:  # dans cette boucle on génère des enfants pour la nouvelle population
            parents = tournament_selection(population, fitness_scores, taille_tournament, num_parent)  # on sélectionne les parents pour la reproduction
            enfant1 = ox_Croisement(parents[0], parents[1])  # génération d'enfant avec la fonction de croisement 
            enfant2 = ox_Croisement(parents[1], parents[0])
            new_population.append(mutation(enfant1, mutation_rate))  # applique la mutation sur les deux enfants
            new_population.append(mutation(enfant2, mutation_rate))
        population = new_population  # mise à jour de la population

        # Trouver le meilleur individu de la génération actuelle
        best_individu_gen = max(population, key=lambda x: fitness_idv(x, distance_m))
        best_fitness_gen = fitness_idv(best_individu_gen, distance_m)

        # Comparer avec le meilleur global
        if best_fitness_gen > best_overall_fitness:
            best_overall_fitness = best_fitness_gen
            best_overall_individu = best_individu_gen

        # Imprimer le meilleur individu et la meilleure fitness de la génération actuelle
        print(f"Génération {gen + 1}: Meilleur Individu: {best_individu_gen}, Fitness: {best_fitness_gen:.22f}")

    # Retourne la meilleure solution globale de toutes les générations
    return best_overall_individu


# fonction pour generer des coordonnées aleatoire dans notre canva 
def generer_coordonnees_random(n_points, largeur_canvas, hauteur_canvas):
    coordonnees = []
    for _ in range(n_points):
        x = random.randint(10, largeur_canvas - 10)  # 10 est la marge pour que les points ne soient pas collés aux bords
        y = random.randint(10, hauteur_canvas - 10)
        coordonnees.append((x, y))
    return np.array(coordonnees)
#___________________________________________INTERFACE GRAPHIQUE_______________________________________________________________
#fonction pour dessiner les villes et le chemin optimal 
def dessiner_villes_chemins(canvas, villes, solution):
    taille_ville = len(villes)
    # Dessiner les villes
    points = []
    for i, (x, y) in enumerate(villes):
        #creation des points pour chaque ville 
        point = canvas.create_oval(x - taille_ville, y - taille_ville, x + taille_ville, y + taille_ville, fill='black')
        canvas.create_text(x, y, text=str(i), fill='white', font=('Helvetica', 10, 'bold'))
        points.append((x, y))
    
    # Dessiner les chemins sous forme d'arcs
    for i in range(len(solution)):
        x1, y1 = villes[solution[i]]
        x2, y2 = villes[solution[(i + 1) % len(solution)]]
        canvas.create_line(x1, y1, x2, y2, fill='red', arrow=tk.LAST)  # Ajouter une flèche pour indiquer la direction


# fonction pour creer la fenetre et la canvas 
def creation_interface(villes, solution):
    fenetre = Tk() #creation de la fenetre
    fenetre.title('Visualisation du Problème du Voyageur de Commerce')

    # Configuration du canvas
    canvas = Canvas(fenetre, width=800, height=800, bg='white')  # Adapter les dimensions selon le besoin
    canvas.pack(expand=YES, fill=BOTH)

    # Dessiner les villes et les chemins
    dessiner_villes_chemins(canvas, villes, solution)

    fenetre.mainloop()




#_______________________________________________MAIN________________________________________________

nvilles = int(input("Entrez le nombre de villes : "))
coordinates = generer_coordonnees_random(nvilles,800,800)
pop_size = 300
n_generations = 10
mutation_rate = 0.1
tournament_size = 3
num_parents = pop_size

# Exécution de l'algorithme
best_solution = algo_Genetique(coordinates, pop_size, n_generations, mutation_rate, tournament_size, num_parents)
print("Meilleure solution:", best_solution)
print("Meilleure fitness:", fitness_idv(best_solution, distances(coordinates)))

creation_interface(coordinates,best_solution)