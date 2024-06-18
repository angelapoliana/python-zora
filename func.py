import shutil
import os
import glob
import os
import pandas as pd

#Delete Folder
def delete_folder(path_folder):
    if os.path.exists(path_folder):
       shutil.rmtree(path_folder)  

#Delete json files
def delete_json(path_file):
    files_json = glob.glob(os.path.join(path_file, '*.json'))
    for path_file in files_json:
        try:
            os.remove(path_file)
        except Exception:
            pass


def sheets(input_path, output_path,cluster_name):
    # Lista de arquivos de entrada
    files = [os.path.join(input_path, 'High.xlsx'),
             os.path.join(input_path, 'Medium.xlsx'),
             os.path.join(input_path, 'Low.xlsx')]

    # Caminho do arquivo de saída
    output_file = os.path.join(output_path, f'{cluster_name}.xlsx')

    # Criar um objeto ExcelWriter
    with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
        # Iterar sobre os arquivos
        for file in files:
            # Extrair o nome do arquivo sem a extensão
            sheet_name = os.path.basename(file).split('.')[0]

            # Ler o arquivo Excel
            df = pd.read_excel(file, index_col=0)

            # Escrever o DataFrame em uma sheet com o nome do arquivo
            df.to_excel(writer, sheet_name=sheet_name, index=False)
