from arbres_fn import Ensemble
from arbres_fn import Noeud
from arbres_fn import Exemple
from arbres_fn import Feuille
import pandas as pd

class Arbre:
   # """
   #     Un arbre ID3 contient deux valeurs :
   #         - un ensemble d'exemples (Ensemble)
   #         - un arbre (Noeud)
   # """
    def __init__(self, chemin=""):
       # """
       #     chemin est l'emplacement du fichier contenant les données
       # """
       #initialisation de l'ensemble avec le fichier dans chemin
        self.ensemble = Ensemble(chemin)
       #initialisation du noeud principal de l'arbre
        self.arbre = None
    
    def construire(self):
       # """
       #     génère l'arbre sur base de l'ensemble pré-chargé
       # """
       self.arbre = self.__construire_arbre(self.ensemble)

    def __construire_arbre(self, ensemble):
       # """
       #     fonction privée et récursive pour la génération de l'arbre
       # """
        if not isinstance(ensemble, Ensemble):
            raise TypeError("ensemble doit être un Ensemble et non un {}" \
                           .format(type(ensemble)))
       #si la liste est vide
        if len(ensemble) == 0:
            raise ValueError("la liste d'exemples ne peut être vide !")
       #testons si tous les exemples ont la même étiquette
        if ensemble.entropie() == 0:
           #on retourne l'étiquette en question
            nb_total = len(ensemble)
            nb_etiquette = ensemble.nombre_etiquettes()
            groupe = ensemble.groupe
            return Feuille(ensemble.liste_exemples[0].etiquette,nb_total,nb_etiquette,groupe)
        #éliminer les noeuds avec trop peu de patients
        if len(ensemble) < 200:
            max, etiquette_finale = 0, ""
           #on teste toutes les étiquettes possibles de l'ensemble
            for etiquette in ensemble.etiquettes_possibles():
                sous_ensemble = ensemble.sous_ensemble_etiquette(etiquette)
                #si c'est la plus fréquente, c'est celle qu'on choisit
                if len(sous_ensemble) > max:
                    max, etiquette_finale = len(sous_ensemble), etiquette
            nb_total = len(ensemble)
            nb_etiquette = ensemble.nombre_etiquettes()
            groupe = ensemble.groupe
           # et on la retourne dans une feuille
            return Feuille(etiquette_finale,nb_total, nb_etiquette,groupe)
       #s'il ne reste d'attribut à tester
        if len(ensemble.liste_attributs) == 0:
            max, etiquette_finale = 0, ""
           #on teste toutes les étiquettes possibles de l'ensemble
            for etiquette in ensemble.etiquettes_possibles():
                sous_ensemble = ensemble.sous_ensemble_etiquette(etiquette)
                if len(sous_ensemble) > max:
                    max, etiquette_finale = len(sous_ensemble), etiquette
            nb_total = len(ensemble)
            nb_etiquette = ensemble.nombre_etiquettes()
            groupe = ensemble.groupe
            return Feuille(etiquette_finale,nb_total, nb_etiquette,groupe)
        
        a_tester = ensemble.attribut_aleatoire()
        #si trop peu de patients chez les enfants : stop
        taille_min_enfants = float("+inf")
        for valeur in ensemble.valeurs_possibles_attribut(a_tester):
            #on crée un sous-ensemble
            sous_ensemble = ensemble.sous_ensemble_attribut(a_tester, valeur)
            #et on en crée un nouveau nœud
            if len(sous_ensemble) < taille_min_enfants:
                taille_min_enfants = len(sous_ensemble)
        if taille_min_enfants < 100:
            max, etiquette_finale = 0, ""
           #on teste toutes les étiquettes possibles de l'ensemble
            for etiquette in ensemble.etiquettes_possibles():
                sous_ensemble = ensemble.sous_ensemble_etiquette(etiquette)
                if len(sous_ensemble) > max:
                    max, etiquette_finale = len(sous_ensemble), etiquette
            nb_total = len(ensemble)
            nb_etiquette = ensemble.nombre_etiquettes()
            groupe = ensemble.groupe
            return Feuille(etiquette_finale,nb_total, nb_etiquette,groupe)
        #OR enfants moins intéressants : stop
        nb_etiquette = ensemble.nombre_etiquettes()
        nb_total=len(ensemble)
        ORHTAe = nb_etiquette['hta_essentielle']/(nb_total-nb_etiquette['hta_essentielle'])/(15609/4033)
        ORRenovasc = nb_etiquette['renovasculaire']/(nb_total-nb_etiquette['renovasculaire'])/(1377/18265)
        y=1
        for valeur in ensemble.valeurs_possibles_attribut(a_tester):
            #on crée un sous-ensemble
            sous_ensemble = ensemble.sous_ensemble_attribut(a_tester, valeur)
            sous_nb_etiquette = sous_ensemble.nombre_etiquettes()
            sous_nb_total=len(sous_ensemble)
            if (sous_nb_total==sous_nb_etiquette['hta_essentielle']) or (sous_nb_total==sous_nb_etiquette['renovasculaire']):
                max, etiquette_finale = 0, ""
                #on teste toutes les étiquettes possibles de l'ensemble
                for etiquette in ensemble.etiquettes_possibles():
                    sous_ensemble = ensemble.sous_ensemble_etiquette(etiquette)
                    if len(sous_ensemble) > max:
                        max, etiquette_finale = len(sous_ensemble), etiquette
                        nb_total = len(ensemble)
                        nb_etiquette = ensemble.nombre_etiquettes()
                        groupe = ensemble.groupe
                return Feuille(etiquette_finale,nb_total, nb_etiquette,groupe)
            if ((sous_nb_etiquette['hta_essentielle']/(sous_nb_total-sous_nb_etiquette['hta_essentielle'])/(15609/4033) < ORHTAe and ORHTAe > 3) or (sous_nb_etiquette['hta_essentielle']/(sous_nb_total-sous_nb_etiquette['hta_essentielle'])/(15609/4033) > ORHTAe and ORHTAe < 0.5)) :
                y=0
            if  ((sous_nb_etiquette['renovasculaire']/(sous_nb_total-sous_nb_etiquette['renovasculaire'])/(1377/18265) < ORRenovasc and ORRenovasc > 3) or (sous_nb_etiquette['renovasculaire']/(sous_nb_total-sous_nb_etiquette['renovasculaire'])/(15609/4033) > ORRenovasc and ORRenovasc < 0.5)):
                y=0
        if y == 0:
            max, etiquette_finale = 0, ""
           #on teste toutes les étiquettes possibles de l'ensemble
            for etiquette in ensemble.etiquettes_possibles():
                sous_ensemble = ensemble.sous_ensemble_etiquette(etiquette)
                if len(sous_ensemble) > max:
                    max, etiquette_finale = len(sous_ensemble), etiquette
            nb_total = len(ensemble)
            nb_etiquette = ensemble.nombre_etiquettes()
            groupe = ensemble.groupe
            return Feuille(etiquette_finale,nb_total, nb_etiquette,groupe)
        
       #si on arrive ici, on retourne d'office un nœud et pas une feuille
        groupe = ensemble.groupe
        noeud = Noeud(a_tester, groupe)
        ### on choisit les cut-off adaptés pour les hommes et les femmes si attribut = sexe
        ### on élimine les cut-offs différents pour la même variable
        if a_tester=='ka_1':
            if 'ka_2' in ensemble.liste_attributs:
                ensemble.liste_attributs.remove('ka_2')
            if 'ka_3' in ensemble.liste_attributs:
                ensemble.liste_attributs.remove('ka_3')
        if a_tester=='ka_2':
            if 'ka_1' in ensemble.liste_attributs:
                ensemble.liste_attributs.remove('ka_1')
            if 'ka_3' in ensemble.liste_attributs:
                ensemble.liste_attributs.remove('ka_3')
        if a_tester=='ka_3':
            if 'ka_2' in ensemble.liste_attributs:
                ensemble.liste_attributs.remove('ka_2')
            if 'ka_1' in ensemble.liste_attributs:
                ensemble.liste_attributs.remove('ka_1')
        if a_tester=='age_1':
            if 'age_2' in ensemble.liste_attributs:
                ensemble.liste_attributs.remove('age_2')
            if 'age_3' in ensemble.liste_attributs:
                ensemble.liste_attributs.remove('age_3')
        if a_tester=='age_2':
            if 'age_1' in ensemble.liste_attributs:
                ensemble.liste_attributs.remove('age_1')
            if 'age_3' in ensemble.liste_attributs:
                ensemble.liste_attributs.remove('age_3')
        if a_tester=='age_3':
            if 'age_1' in ensemble.liste_attributs:
                ensemble.liste_attributs.remove('age_1')
            if 'age_2' in ensemble.liste_attributs:
                ensemble.liste_attributs.remove('age_2') 
        if a_tester=='anciennete_hta_1':
            if 'anciennete_hta_2' in ensemble.liste_attributs:
                ensemble.liste_attributs.remove('anciennete_hta_2')
        if a_tester=='anciennete_hta_2':
            if 'anciennete_hta_1' in ensemble.liste_attributs:
                ensemble.liste_attributs.remove('anciennete_hta_1') 
        if a_tester=='fc_1':
            if 'fc_2' in ensemble.liste_attributs:
                ensemble.liste_attributs.remove('fc_2')
        if a_tester=='fc_2':
            if 'fc_1' in ensemble.liste_attributs:
                ensemble.liste_attributs.remove('fc_1')
        if a_tester=='imc_1':
            if 'imc_2' in ensemble.liste_attributs:
                ensemble.liste_attributs.remove('imc_2')
        if a_tester=='imc_2':
            if 'imc_1' in ensemble.liste_attributs:
                ensemble.liste_attributs.remove('imc_1')
        if a_tester=='ldl_1':
            if 'ldl_2' in ensemble.liste_attributs:
                ensemble.liste_attributs.remove('ldl_2')
        if a_tester=='ldl_2':
            if 'ldl_1' in ensemble.liste_attributs:
                ensemble.liste_attributs.remove('ldl_1')
        if a_tester=='pas_1':
            if 'pas_2' in ensemble.liste_attributs:
                ensemble.liste_attributs.remove('pas_2')
            if 'pas_3' in ensemble.liste_attributs:
                ensemble.liste_attributs.remove('pas_3')
        if a_tester=='pas_2':
            if 'pas_1' in ensemble.liste_attributs:
                ensemble.liste_attributs.remove('pas_1')
            if 'pas_3' in ensemble.liste_attributs:
                ensemble.liste_attributs.remove('pas_3')
        if a_tester=='pas_3':
            if 'pas_1' in ensemble.liste_attributs:
                ensemble.liste_attributs.remove('pas_1')
            if 'pas_2' in ensemble.liste_attributs:
                ensemble.liste_attributs.remove('pas_2')
        if a_tester=='pad_1':
            if 'pad_2' in ensemble.liste_attributs:
                ensemble.liste_attributs.remove('pad_2')
            if 'pad_3' in ensemble.liste_attributs:
                ensemble.liste_attributs.remove('pad_3')
        if a_tester=='pad_3':
            if 'pad_1' in ensemble.liste_attributs:
                ensemble.liste_attributs.remove('pad_1')
            if 'pad_2' in ensemble.liste_attributs:
                ensemble.liste_attributs.remove('pad_2')
        if a_tester=='pad_2':
            if 'pad_1' in ensemble.liste_attributs:
                ensemble.liste_attributs.remove('pad_1')
            if 'pad_3' in ensemble.liste_attributs:
                ensemble.liste_attributs.remove('pad_3')
        if a_tester=='pas_max_1':
            if 'pas_max_2' in ensemble.liste_attributs:
                ensemble.liste_attributs.remove('pas_max_2')
        if a_tester=='pas_max_2':
            if 'pas_max_1' in ensemble.liste_attributs:
                ensemble.liste_attributs.remove('pas_max_1') 
        if a_tester=='taille_1':
            if 'taille_2' in ensemble.liste_attributs:
                ensemble.liste_attributs.remove('taille_2')
        if a_tester=='taille_2':
            if 'taille_1' in ensemble.liste_attributs:
                ensemble.liste_attributs.remove('taille_1') 
       # pour les autres attributs pour chaque valeur que peut prendre l'attribut à tester
        for valeur in ensemble.valeurs_possibles_attribut(a_tester):
           #on crée un sous-ensemble
           sous_ensemble = ensemble.sous_ensemble_attribut(a_tester, valeur)
           #et on en crée un nouveau nœud
           noeud.enfants[valeur] = self.__construire_arbre(sous_ensemble)
       #on retourne le nœud que l'on vient de créer
        return noeud
    
    def afficher(self):
       # """
       #     affiche l'entièreté de l'arbre à l'écran
       # """
       self.__afficher_arbre(self.arbre)
        
    def __afficher_arbre(self, noeud, nb_tabs=0):
     
        if isinstance(noeud, Noeud):
           #on affiche le nom de l'attribut testé
            print('\t' * nb_tabs + noeud.attribut_teste)
           #on parcourt ses enfants
            for enfant in noeud.enfants:
               #on affiche la valeur de l'attribut
                print('\t' * nb_tabs + '-' + str(enfant))
                self.__afficher_arbre(noeud.enfants[enfant], nb_tabs+1)
       #si c'est une feuille
        elif isinstance(noeud, Feuille):
           #on affiche l'étiquette
           print('\t' * nb_tabs + '.' + noeud.etiquette_maj)
        else:
            raise TypeError("noeud doit être un Noeud/Feuille et pas un {}" \
                           .format(type(noeud)))
            
            
    def afficher_groupes(self,ret):
       # """
       #     affiche l'entièreté de l'arbre à l'écran
       # """
       self.__afficher_groupes(self.arbre,ret) 
        
        
        
    def __afficher_groupes(self, feuille,ret,nb_tabs=0):
        if isinstance(feuille, Noeud):
           #on parcourt ses enfants
            for enfant in feuille.enfants:
                # print('\t' * nb_tabs + feuille.attribut_teste)
                # print('\t' * nb_tabs + str(enfant))
                self.__afficher_groupes(feuille.enfants[enfant],ret,nb_tabs+1)
       #si c'est une feuille
        elif isinstance(feuille, Feuille):
           #on affiche les nombres
            if feuille.ORHTAe > 3 or feuille.ORRenovasc > 3 :
                # for i in feuille.liste_etiquettes.items():
                #     # print('\t' * nb_tabs + feuille.attribut_teste)
                #     print(i)
                # print('nombre_total = ' + str(feuille.nb_total))
                # print(feuille.groupe)
                # print(feuille.ORHAP)
                keys = feuille.groupe.keys()
                sorted_keys = sorted(keys)
                sorted_groupes = {}
                for key in sorted_keys:
                    sorted_groupes[key] = feuille.groupe[key]
                res = ' '
                for item in sorted_groupes:
                    res += item + '_' + str(sorted_groupes[item]+ ' / ')
                sorted_groupes = {}
                sorted_groupes['groupe']=res
                sorted_groupes['nombre']=feuille.nb_total
                sorted_groupes['OR_HTA_essentielle']=feuille.ORHTAe
                sorted_groupes['effectif_observe_HTAe']=feuille.effectif_observe_HTAe
                sorted_groupes['effectif_attendu_HTAe']=feuille.effectif_attendu_HTAe
                sorted_groupes['OR_Renovasculaire']=feuille.ORRenovasc
                sorted_groupes['effectif_observe_renovasc']=feuille.effectif_observe_renovasc
                sorted_groupes['effectif_attendu_renovasc']=feuille.effectif_attendu_renovasc
                
                # print(feuille.groupe)
                ret.append(sorted_groupes)
                ret = pd.DataFrame.from_dict(ret)
                
        else:
            raise TypeError("noeud doit être un Noeud/Feuille et pas un {}" \
                           .format(type(noeud)))
        return ret

        
            
    # def etiqueter(self, exemple):
    #    # """
    #    #     assigne la bonne étiquette à l'exemple passé en paramètre
    #    # """
    #    #on initialise le nœud actuel avec le haut de l'arbre
    #     noeud_actuel = self.arbre
    #    #tant que l'on est sur un nœud et pas sur une feuille,
    #    #on continue d'explorer
    #     while not isinstance(noeud_actuel, Feuille):
    #        #pour savoir quel est le prochain nœud, on récupère d'abord
    #        #l'attribut testé avec noeud_actuel.attribut_teste puis on récupère
    #        #la valeur de l'exemple pour cet attribut avec
    #        #exemple.dict_attributs[noeud_actuel.attribut_teste]
    #        #puis on prend l'enfant de noeud_actuel ayant cette valeur.
    #         valeur = exemple.dict_attributs[noeud_actuel.attribut_teste]
    #         noeud_actuel = noeud_actuel.enfants[valeur]
    #    #on finit en donnant comme étiquette l'étiquette
    #    #contenue dans la feuille finale
    #     exemple.etiquette = noeud_actuel.etiquette