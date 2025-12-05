import pandas as pd
import numpy as np
from collections import Counter
from math import log
import random

class Feuille:
    # """
    #     Une feuille contient :
    #         - l'étiquette finale (str)
    #          - l'ensemble des étiquettes
    # """

    def __init__(self, etiquette_maj, nb_total, nb_etiquette, groupe):
        # """
        #     etiquette doit obligatoirement être un str
        # """
        if not isinstance(etiquette_maj, str):
            raise TypeError("etiquette doit être un str et pas un {}" \
                            .format(type(etiquette_maj)))
        
        self.etiquette_maj = etiquette_maj
        self.nb_total=nb_total
        # nombres de diag par étiquette
        #self.liste_etiquettes = {}
        self.liste_etiquettes = nb_etiquette
        self.groupe = groupe
        self.ORHAP = nb_etiquette['hap']/(nb_total-nb_etiquette['hap'])/(1809/13698)
        self.ORpheo = nb_etiquette['ppgl']/(nb_total-nb_etiquette['ppgl'])/(285/15222)
        self.effectif_observe_HAP = nb_etiquette['hap']
        self.effectif_attendu_HAP = round(1809/15507*nb_total)
        self.effectif_observe_ppgl = nb_etiquette['ppgl']
        self.effectif_attendu_ppgl = round(285/15507*nb_total)

class Noeud:

    def __init__(self, attribut,groupe):

        if not isinstance(attribut, str):
            raise TypeError("attribute_teste doit être un str et pas un {}" \
                            .format(type(attribut)))
        #initialisation des valeurs de l'objet
        self.enfants = dict()
        self.attribut_teste = attribut
        self.groupe = groupe
        
class Exemple:
    # """
    #     Un exemple contient 2 valeurs :
    #         - un dictionnaire d'attributs (dict)
    #         - une étiquette (str)
    # """

    def __init__(self, noms_attributs, valeurs_attributs, etiquette=""):
        # """
        #     etiquette peut être non précisée en quel cas on aurait
        #     un exemple non étiqueté
        # """
        #si on a un problème de types
        if not isinstance(noms_attributs, list) \
        or not isinstance(valeurs_attributs, list):
            raise TypeError("noms_attributs et valeurs_attributs doivent être" \
                            " des listes et pas des {0} et {1}" \
                            .format(type(noms_attributs),
                                    type(valeurs_attributs)))
        if not isinstance(etiquette, str):
            raise TypeError("etiquette doit être un str et pas un {}" \
                            .format(type(etiquette)))
        #si les deux listes n'ont pas le même nombre d'éléments
        if len(valeurs_attributs) != len(noms_attributs):
            raise ValueError("noms_attributs et valeurs_attributs doivent " \
                             "avoir le même nombre d'éléments")
        self.etiquette = etiquette
        self.dict_attributs = dict()
        #on ajoute chaque attribut au dictionnaire
        for i in range(len(noms_attributs)):
            self.dict_attributs[noms_attributs[i]] = valeurs_attributs[i]
            
class Ensemble:
    # """
    #     Un ensemble contient deux valeurs :
    #         - les noms des attributs (list)
    #         - les exemples (list)
    # """

    def __init__(self, chemin=""):
        # """
        #     chemin est l'emplacement du fichier contenant les données.
        #     Cette variable peut être non précisée en quel cas les variables
        #         seront initialisées comme des listes vides.
        # """
        #Python est un langage à typage dynamique fort,
        #il faut donc vérifier que l'utilisateur ne fait pas n'importe quoi
        #en passant autre chose qu'un str
        if not isinstance(chemin, str):
            raise TypeError("chemin doit être un str et non {}" \
                            .format(type(chemin)))
        self.groupe = {}
        if chemin == "":
            #initialisation en listes vides
            self.liste_attributs = list()
            self.liste_exemples = list()
        else:
            with open(chemin, 'r') as fichier:
                #on stocke chaque mot de la première ligne dans liste_attributs
                self.liste_attributs = \
                                fichier.readline().lower().strip().split(',')
                self.liste_attributs.pop()
                #ensuite on stocke la liste d'exemples dans liste_exemples
                self.liste_exemples = self.liste_en_exemples(
                                        fichier.read().strip().lower().split('\n'),
                                        self.liste_attributs
                                      )
        

    @staticmethod #fonction statique car ne dépend pas de l'objet mais est commune à toute instance de la classe
    def liste_en_exemples(exemples, noms_attributs):
        
    # """
    #     retourne une liste d'exemples sur base d'une liste de str contenant
    #     les valeurs et d'une liste de str contenant les noms des attributs
    # """
    #on initialise la liste à retourner
        ret = list()
        for ligne in exemples:
        #on stocke chaque mot de la ligne dans une liste attributs
            attributs = ligne.lower().strip().split(',')
        #met l'étiquette par défaut si elle n'est pas dans la ligne
            etiquette = attributs[-1]
        #on retire l'étiquette des attributs
            attributs = attributs
            attributs.pop()
        #on ajoute un objet de type Exemple contenant la ligne
            ret.append(Exemple(noms_attributs,
                           attributs[:len(noms_attributs)],
                           etiquette))
        return ret
    
    def __len__(self):
    # """
    #     retourne la longueur de l'ensemble
    # """
        return len(self.liste_exemples)
    
    def etiquettes_possibles(self):
    # """
    #     retourne une liste contenant les étiquettes de l'ensemble
    # """
    #on initialise la valeur de retour
        ret = list()
    #pour chaque exemple de l'ensemble
        for exemple in self.liste_exemples:
        #si l'étiquette n'est pas déjà dans la liste
            if not exemple.etiquette in ret:
            #on l'ajoute
                ret.append(exemple.etiquette)
        return ret
    
    def sous_ensemble_attribut(self, nom_attribut, valeur):
    # """
    #     retourne un sous-ensemble contenant uniquement les exemples ayant
    #     la bonne valeur pour l'attribut
    # """
        ret = Ensemble()
    #on prend tous les attributs sauf celui passé en paramètre
        ret.liste_attributs = self.liste_attributs[:]
        ret.liste_attributs.remove(nom_attribut)
        if nom_attribut == 'sexe' and valeur == 1:
            if 'hdl_f' in ret.liste_attributs:
                ret.liste_attributs.remove('hdl_f')
            if 'perim_abdo_f' in ret.liste_attributs:
                ret.liste_attributs.remove('perim_abdo_f')
        if nom_attribut == 'sexe' and valeur == 0:
            if 'hdl_m' in ret.liste_attributs:
                ret.liste_attributs.remove('hdl_m')
            if 'perim_abdo_m' in ret.liste_attributs:
                ret.liste_attributs.remove('perim_abdo_m')        
        ret.groupe = self.groupe.copy()
        ret.groupe[nom_attribut]=valeur
        print(ret.groupe)
    #pour chaque exemple de l'ensemble
        for exemple in self.liste_exemples:
        #s'il a la bonne valeur
            if exemple.dict_attributs[nom_attribut] == valeur:
            #on l'ajoute
                ret.liste_exemples.append(exemple)
    #et on retourne la liste
        return ret
    
    
    def entropie(self):
    # """
    #     retourne l'entropie de Shannon de l'ensemble
    # """
    #initialisation de la variable retournée
        ret = 0
    #pour chaque étiquette de l'ensemble
        for etiquette in self.etiquettes_possibles():
        #on crée un sous-ensemble qui ne contient que les éléments de
        #self ayant etiquette comme étiquette
            sous_ensemble = self.sous_ensemble_etiquette(etiquette)
        #on ajoute |c| * log_2(|c|) à ret
            longueur_sous_ensemble = len(sous_ensemble)
            ret += longueur_sous_ensemble * log(longueur_sous_ensemble, 2)
    #on retourne log_2(|S|) - ret/|S|
        return log(len(self), 2) - ret/len(self)


    def sous_ensemble_etiquette(self, etiquette):
    # """
    #     retourne un ensemble contenant uniquement les exemples ayant
    #     etiquette comme étiquette
    # """
    #initialisation de la valeur de retour
        ret = Ensemble()
    #on copie la liste d'attributs
        ret.liste_attributs = self.liste_attributs[:]
    #pour chaque exemple de l'ensemble initial
        for exemple in self.liste_exemples:
        #si l'étiquette est bonne
            if exemple.etiquette == etiquette:
            #on l'ajoute au sous-ensemble
                ret.liste_exemples.append(exemple)
        return ret
    
    def nombre_etiquettes(self):
    # """
    #     retourne un dictionnaire avec le nombre de chaque type d'étiquettes
    # """
        ret = {}
        etiquettes_possibles = ['hta_essentielle','hap','renovasculaire','ppgl','autre']
        for etiquette in etiquettes_possibles:
            ret[etiquette] = 0
            for exemple in self.liste_exemples:
                if exemple.etiquette == etiquette:
            #on l'ajoute au sous-ensemble
                    ret[etiquette] +=1
        return ret
    
    def attribut_optimal(self, ID3=True):
    # """
    #     retourne un str avec le nom de l'attribut à tester
    # """
        max, ret = float("-inf"), ""
    #pour chaque attribut
        for attribut in self.liste_attributs:
            gain = self.gain_entropie(attribut)
        #si le gain d'entropie est la plus grande
            if gain >= max:
            #on le garde en mémoire
                max, ret = gain, attribut
    #et on le retourne
        return ret
    
    def attribut_aleatoire(self, ID3=True):
    # """
    #     retourne un str avec le nom de l'attribut à tester
    # """
        ret = random.choice(self.liste_attributs)
    #et on le retourne
        return ret
    
#     def attribut_suivant(self)
#         for attribut in self.list_attribut
    

    def valeurs_possibles_attribut(self, nom_attribut):
    # """
    #     retourne une liste contenant toutes les
    #     valeurs possibles de l'attribut
    # """
        ret = list()
    #pour chaque exemple
        for exemple in self.liste_exemples:
        #si cette valeur n'est pas encore dans la liste
            if not exemple.dict_attributs[nom_attribut] in ret and not pd.isna(exemple.dict_attributs[nom_attribut]) and not exemple.dict_attributs[nom_attribut] == '':
            #on l'ajoute
                ret.append(exemple.dict_attributs[nom_attribut])
    #et on retourne la liste
        return ret
    
    def gain_entropie(self, nom_attribut):
    # """
    #     retourne la perte d'entropie selon la définition de Ross Quinlan
    # """
        somme = 0
    #pour chaque valeur de l'attribut en question
        for valeur in self.valeurs_possibles_attribut(nom_attribut):
        #déclaration de Sv
            sous_ensemble = self.sous_ensemble_attribut(nom_attribut, valeur)
        #somme = somme sur v de |Sv| * Entropie(Sv)
            somme += len(sous_ensemble) * sous_ensemble.entropie()
    #Gain(S, A) = Entropie(S) - 1/|S| * somme
        return self.entropie() - somme/len(self)