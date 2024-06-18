#!/usr/bin/env python3
import pandas as pd
import json
import sys
from pathlib import Path
import shutil
import os
import glob

#Deletar pasta Zora
def delete_folder(path_folder):
    if os.path.exists(path_folder):
       shutil.rmtree(path_folder)
  
path_folder = "/home/angela/python_zora/zora"

delete_folder(path_folder)

print("Severity;Category;Cluster;Resource;Namespace;Issues")

for filename in sys.argv[1:]:
    with open(filename, 'r') as f:
        data = json.load(f)
        for plugin_name, plugin in data['pluginStatus'].items():
            if not 'issues' in plugin:
                continue
            for issue in plugin['issues']:
                severity = issue.get("severity", "N/A")  # Usando get() com valor padrão caso a chave não exista
                resources = issue.get("resources", {})
                for resource_kind, resources_info in resources.items():
                    for resource in resources_info:
                        res = '/'.join(filter(lambda x: x, [resource.get('namespace', None), resource.get('name')]))
                        category = issue.get("category", "N/A")  # Usando get() com valor padrão caso a chave não exista
                        print(f"{severity};{category}", end='')
                        print(f";{data['name']};{resource_kind}", end='')
                        print(f";{res};{issue['message']}")

#gera csv completo com todas as severidades
zora = pd.read_csv('issues.csv', sep = ';')

zora[['Namespace', 'Resource Name']] = zora.Namespace.str.split('/', expand = True)
zora['Resource'] = zora['Resource'].str.replace('apps/', '')
zora['Resource'] = zora['Resource'].str.replace('v1/', '')

#remover namespace
namespace = ['kube-system', 'zora-system', 'flux-system', 'getup', 'monitoring', 'velero', 'logging', 'csi-drivers', 'cert-manager','getup-workload', 'metallb-system']
for n in namespace:
    index_namespace = zora[(zora['Namespace']=="%s" % n)].index
    zora.drop(index_namespace, inplace=True)

#remover resources
resources = ['pods', 'replicasets']
for n in resources:
    index_resources = zora[(zora['Resource']=="%s" % n)].index
    zora.drop(index_resources, inplace=True)

def generate_clusters():                              
    clusters = zora.Cluster.unique()                  #obtém os valores únicos da coluna 'Cluster'
    path = Path("/home/angela/python_zora/zora")      #define o caminho base onde as pastas separadas por cluster serão criadas 
    for cluster in clusters:
       str(cluster)
       if cluster:
        folder_path = path / cluster                  #cria um caminho completo para a pasta do cluster combinando o caminho base path com o valor do cluster.
        folder_path.mkdir(parents=True, exist_ok=True)
        name_cluster = zora.query('Cluster == "%s"'%cluster)  #csv separado por cluster 
        name_cluster.to_csv(folder_path / f'{cluster}.csv', sep=';') 
        clus = pd.read_csv(folder_path / f'{cluster}.csv', sep=';', index_col=0)
        clus.reset_index(drop=True, inplace=True)
        severity = clus.Severity.unique()
        for s in severity:
                medium = clus.query('Severity == "%s"'% s)   #csv separado por severidade
                pivot = medium[['Namespace', 'Issues', 'Resource', 'Resource Name']].copy()
                pivot['Resource Name'] = pivot['Resource Name'].astype(str)
                grouped_pivot = pivot.groupby(['Issues', 'Namespace']).agg({
                    'Resource': lambda x: '\n'.join(x),
                    'Resource Name': lambda x: '\n'.join(x)
                }).reset_index()
                
                cols = grouped_pivot.columns.tolist()
                cols.remove('Issues')
                cols.append('Issues')
                grouped_pivot = grouped_pivot[cols]
                
                medium.to_csv(folder_path / f'{s}.csv', index=False, sep=';')
                grouped_pivot.to_excel(folder_path / f'pivot_{s}.xlsx') 
                
                
                #remove os arquivos csv (separado por severidade) apos a criacao das pivot_tables
                os.remove(folder_path / f'{s}.csv')
        
        #remove os arquivos csv (separado por cluster) apos a criacao das pivot_tables
        os.remove(folder_path / f'{cluster}.csv')
generate_clusters()

csv_path_atual = Path("/home/angela/python_zora/issues.csv")
#Deleta o arquivo csv com todos os clusters e issus
os.remove(csv_path_atual / "/home/angela/python_zora/issues.csv")

#Move o arquivo csv para a pasta zora
#pasta_destino = Path("/home/angela/python_zora/zora")
#shutil.move(csv_path_atual, pasta_destino / "issues.csv")


#Deletar arquivos json
def delete_json(path_file):
    files_json = glob.glob(os.path.join(path_file, '*.json'))
    for path_file in files_json:
        try:
            os.remove(path_file)
        except Exception:
            pass

path_file = "/home/angela/python_zora"
delete_json(path_file)