from Arbre import Arbre
import pandas as pd
import json

#a = Arbre_ID3('/rapids/notebooks/scripts/jeanbaptiste_work/stratif/hta_feat_nona.csv')
#b = a.ensemble.sous_ensemble_attribut('ttt_hta_ic', 2)
#c=b.sous_ensemble_attribut('anciennete_hta_1',1)
#d=c.sous_ensemble_attribut('anciennete_hta_2',1)
#d.groupe


#a = Arbre_ID3('/rapids/notebooks/scripts/jeanbaptiste_work/stratif/hta_feat_nona.csv')
#b = a.ensemble.sous_ensemble_attribut('ttt_hta_ic', 0)
#c = b.sous_ensemble_attribut('anciennete_hta_1',0)
#d = c.sous_ensemble_attribut('diabete',0)
#d.groupe

# arbre = Arbre('/rapids/notebooks/scripts/jeanbaptiste_work/stratif/hta_feat2.csv')
# arbre.construire()
# ret=[]
# arbre.afficher_groupes(ret)
# df=pd.DataFrame.from_dict(ret)
# df=df.drop_duplicates()
# print(ret)
# print(df) 

# OR = pd.read_csv('/rapids/notebooks/scripts/jeanbaptiste_work/stratif/OR/OR.csv')
# # OR=sorted(OR)
# print(OR)
# OR.to_csv(r'/rapids/notebooks/scripts/jeanbaptiste_work/stratif/OR/OR_sorted.csv', index = False)



# [{'groupe': ' anciennete_hta_2_1;ka_1_0;mdrd_1;ttt_hta_antialdo_0;', 'OR_HAP': 6.469111137227249, 'OR_HTA_essentielle': 0.2636393838864841, 'OR_Renovasculaire': 0.29584768050321286, 'OR_PPGL': 0.22776343844686342, 'nombre': 471}, {'groupe': ' anciennete_hta_2_0;imc_1_0;mdrd_1;pas_1_0;ttt_hta_antialdo_0;ttt_hta_ic_0;', 'OR_HAP': 0.16461172398875187, 'OR_HTA_essentielle': 2.002463989858604, 'OR_Renovasculaire': 0.7763244779125841, 'OR_PPGL': 1.934554496477414, 'nombre': 658}, {'groupe': ' age_2_0;fc_1_1;ttt_hta_antialdo_1;', 'OR_HAP': 4.041310302420482, 'OR_HTA_essentielle': 0.32359060748243457, 'OR_Renovasculaire': 1.2005413121869508, 'OR_PPGL': 0.9964650432050274, 'nombre': 273}, {'groupe': ' fc_1_0;ttt_hta_antialdo_1;', 'OR_HAP': 3.8036792780284623, 'OR_HTA_essentielle': 0.389664426866686, 'OR_Renovasculaire': 0.8437137555091625, 'OR_PPGL': 0.33277586489588457, 'nombre': 323}]

arbre = Arbre('/rapids/notebooks/scripts/jeanbaptiste_work/stratif/hta_feat2.csv')
arbre.construire()
ret=[]
arbre.afficher_groupes(ret)
print(pd.DataFrame.from_dict(ret))
print(arbre.ensemble.liste_attributs)