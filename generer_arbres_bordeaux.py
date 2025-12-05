from Arbre import Arbre
from Arbre_jeunes import Arbre_jeunes
import json
import pandas as pd

df=pd.DataFrame()
for i in range(1,100000):
    arbre = Arbre('/rapids/notebooks/scripts/jeanbaptiste_work/stratif/bordeaux_feat2.csv')
    arbre.construire()
    ret=[]
    arbre.afficher_groupes(ret)
    df=df.append(pd.DataFrame.from_dict(ret))
    print(df)
df=df.drop_duplicates()
# df = sorted(df)
print(df)
df.to_csv(r'/rapids/notebooks/scripts/jeanbaptiste_work/stratif/OR/OR_all_bordeaux.csv', index = False)


df_jeunes=pd.DataFrame()
for i in range(1,100000):
    arbre = Arbre_jeunes('/rapids/notebooks/scripts/jeanbaptiste_work/stratif/bordeaux_feat2_jeunes.csv')
    arbre.construire()
    ret=[]
    arbre.afficher_groupes(ret)
    df_jeunes=df_jeunes.append(pd.DataFrame.from_dict(ret))
    print(df_jeunes)
df_jeunes=df_jeunes.drop_duplicates()
# df_jeunes = sorted(df_jeunes)
print(df_jeunes)
df_jeunes.to_csv(r'/rapids/notebooks/scripts/jeanbaptiste_work/stratif/OR/OR_jeunes_bordeaux.csv', index = False)


