#!/usr/bin/env/python3

import argparse
import sys
import yaml
import os
import json
import diagrams

from diagrams import Cluster, Diagram
from diagrams.aws import compute as aws
from diagrams.aws.network import ELB
from diagrams.aws.database import RDS
from diagrams.generic import blank, compute, place, device, database, network, storage
from diagrams.generic import os as dos

# Note that if we like this idea we can make custom icons
# https://diagrams.mingrammer.com/docs/nodes/custom

here = os.path.abspath(os.path.dirname(__file__))

def get_parser():
    parser = argparse.ArgumentParser(
        description="Node Diagram Static Generator",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("yaml", help="yaml file with resources to parse")
    parser.add_argument("--out", help="output folder to write json", default=os.path.join(here, "data"))
    parser.add_argument("--root-name", help="label for the root of the graph", default="Flux Resource Graph")
    return parser

def read_yaml(filename):
    with open(filename, "r") as stream:
        content = yaml.safe_load(stream)
    return content

def recursive_find(base, pattern="tutorial.yaml"):
    for root, _, filenames in os.walk(base):
        for filename in fnmatch.filter(filenames, pattern):
            yield os.path.join(root, filename)


def write_yaml(yaml_dict, filename):
    with open(filename, "w") as filey:
        filey.writelines(yaml.dump(yaml_dict))
    return filename


def write_json(obj, filename):
    with open(filename, 'w') as fd:
        fd.write(json.dumps(obj, indent=4))

# Lookup to map node types to diagram pictures
lookup = {'cluster': place.Datacenter, 
          'rack': aws.EC2,
          'birack': aws.EC2,
          'node': aws.Compute,
          'socket': ELB,
          'slot': aws.ECS,
          'core': RDS, 
          'gpu': database.SQL,
          'memory': compute.Rack}


def add_child(data, root):
    """
    Given data we are exploring and children, append item to children
    """
    name = data.get('label') or data.get('type')
    if not name:
        sys.exit(f'Node missing label AND type {data}')

    with Cluster(name) as node:
        if "with" in data:
            workers = []
            for child in data.get('with', []):
                child_name = data.get('label') or data.get('type')               
                child_node = lookup[data['type']](child_name)
                workers.append(child_node)
                add_child(child, child_node)
            root >> workers
        else:
            root
def main():

    parser = get_parser()

    # If an error occurs while parsing the arguments, the interpreter will exit with value 2
    args, extra = parser.parse_known_args()

    # Show args to the user
    print("yaml: %s" % args.yaml)
    print(" out: %s" % args.out) 

    if not os.path.exists(args.yaml):
        sys.exit("File %s does not exist." % args.yaml)

    yamlfile = os.path.abspath(args.yaml)

    resources = read_yaml(yamlfile)
    if "resources" not in resources:
        sys.exit(f'Missing key "resources" in graph {yamlfile}')
    resources = resources['resources']
    
    with Diagram(args.root_name, show=False):
        root = aws.Batch(args.root_name)
        for r in resources:
            add_child(r, root)
           
if __name__ == "__main__":
    main()
