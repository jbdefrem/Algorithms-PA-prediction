from Arbre import Arbre
from arbres_fn import Ensemble
from arbres_fn import Noeud
from arbres_fn import Exemple
from arbres_fn import Feuille
import pandas as pd

# tot = Ensemble('/rapids/notebooks/scripts/jeanbaptiste_work/stratif/hta_feat2.csv')
# n_tot = tot.nombre_etiquettes()
# a=tot.groupe
# print(a)

a = {'groupe': ' anciennete_hta_2_1;ka_1_0;mdrd_1;ttt_hta_antialdo_0;', 'OR_HAP': 6.469111137227249, 'OR_HTA_essentielle': 0.2636393838864841, 'OR_Renovasculaire': 0.29584768050321286, 'OR_PPGL': 0.22776343844686342, 'nombre': 471}, {'groupe': ' anciennete_hta_2_0;imc_1_0;mdrd_1;pas_1_0;ttt_hta_antialdo_0;ttt_hta_ic_0;', 'OR_HAP': 0.16461172398875187, 'OR_HTA_essentielle': 2.002463989858604, 'OR_Renovasculaire': 0.7763244779125841, 'OR_PPGL': 1.934554496477414, 'nombre': 658}
b=pd.DataFrame.from_dict(a)
print(b)





