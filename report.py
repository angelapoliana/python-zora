import pandas as pd
import os
from pathlib import Path
from func import sheets

def generate_clusters(zora):                              
    clusters = zora.Cluster.unique()                  #obtém os valores únicos da coluna 'Cluster'
    path = Path("zora")      #define o caminho base onde as pastas separadas por cluster serão criadas 
    for cluster in clusters:
       cluster = str(cluster)
       if cluster and cluster != 'nan':
        folder_path = path / cluster                  #cria um caminho completo para a pasta do cluster combinando o caminho base path com o valor do cluster.
        folder_path.mkdir(parents=True, exist_ok=True) 
        name_cluster = zora.query('Cluster == "'f'{cluster}"')   #csv separado por cluster
        name_cluster.to_csv(folder_path / f'{cluster}.csv', sep=';') 
        clus = pd.read_csv(folder_path / f'{cluster}.csv', sep=';', index_col=0)
        clus.reset_index(drop=True, inplace=True)
        severity = clus.Severity.unique()
        for s in severity:
                medium = clus.query('Severity == "'f'{s}"')        #csv separado por severidade 
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
                grouped_pivot.to_excel(folder_path / f'{s}.xlsx') 
                
                
                #remove os arquivos csv (separado por severidade) apos a criacao das pivot_tables
                os.remove(folder_path / f'{s}.csv')
        
        #remove os arquivos csv (separado por cluster) apos a criacao das pivot_tables
        os.remove(folder_path / f'{cluster}.csv')
        input_directory = 'zora/'f'{cluster}'
        output_directory = 'zora/'f'{cluster}'
        
        sheets(input_directory, output_directory, cluster)
        for s in severity:
            os.remove(folder_path / f'{s}.xlsx')