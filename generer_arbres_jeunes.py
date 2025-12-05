from Arbre_jeunes import Arbre
import json
import pandas as pd

df_jeunes=pd.DataFrame()
for i in range(1,100000):
    arbre = Arbre('/rapids/notebooks/scripts/jeanbaptiste_work/stratif/hta_feat2_jeunes.csv')
    arbre.construire()
    ret=[]
    arbre.afficher_groupes(ret)
    df_jeunes=df_jeunes.append(pd.DataFrame.from_dict(ret))
    print(df_jeunes)
df_jeunes=df_jeunes.drop_duplicates()
# df_jeunes = sorted(df_jeunes)
print(df_jeunes)
df_jeunes.to_csv(r'/rapids/notebooks/scripts/jeanbaptiste_work/stratif/OR/OR_jeunes_v2.csv', index = False)
    # tf = open("/rapids/notebooks/scripts/jeanbaptiste_work/stratif/OR/ret{}.json".format(i), "w")
    # json.dump(ret,tf)
    # tf.close()
