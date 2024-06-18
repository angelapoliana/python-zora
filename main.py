#!/usr/bin/env python3

import json
import sys
from pathlib import Path
import os
from func import *
from data import *
from report import *

#Delete folder zora
delete_folder("zora")

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

#Load the CSV
zora = load_csv('issues.csv')

#Process the CSV
process_dataframe(zora)

#Remove Namespaces and Resources
namespaces = ['kube-system', 'zora-system', 'flux-system', 'getup', 'monitoring', 'velero', 'logging', 'csi-drivers', 'cert-manager','getup-workload', 'metallb-system']
resources = ['pods', 'replicasets']

drop_namespaces(zora, namespaces)
drop_resources(zora, resources)

#Create excel files
generate_clusters(zora)

#Remove the csv file
os.remove(Path("issues.csv"))

#Delete json file
delete_json(".")
