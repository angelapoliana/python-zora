import pandas as pd


def load_csv(caminho_csv):
    return pd.read_csv(caminho_csv, sep=';')

def process_dataframe(zora):
    zora[['Namespace', 'Resource Name']] = zora.Namespace.str.split('/', expand=True)
    zora['Resource'] = zora['Resource'].str.replace('apps/', '')
    zora['Resource'] = zora['Resource'].str.replace('v1/', '')

#Function to delete namespaces
def drop_namespaces(zora, namespaces):
    for n in namespaces:
        index_namespace = zora[(zora['Namespace'] == "%s" % n)].index
        zora.drop(index_namespace, inplace=True)

#Function to delete resources
def drop_resources(zora, resources):
    for n in resources:
        index_resources = zora[(zora['Resource'] == "%s" % n)].index
        zora.drop(index_resources, inplace=True)