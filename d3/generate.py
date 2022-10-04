#!/usr/bin/env/python3

import argparse
import sys
import yaml
import os
import json

here = os.path.abspath(os.path.dirname(__file__))

def get_parser():
    parser = argparse.ArgumentParser(
        description="Node Graph Static Generator",
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

def add_child(data):
    """
    Given data we are exploring and children, append item to children
    """
    name = data.get('label') or data.get('type')
    if not name:
        sys.exit(f'Node missing label AND type {data}')
    node = {'name': name, 'type': data['type'], 'value': data['count']}    
    if "with" in data:
        node['children'] = []

    for child in data.get('with', []):
        node['children'].append(add_child(child))

    return node
 
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
    
    data = {"name": args.root_name, "children": []}
    for resource in resources:
        node = add_child(resource)
        data['children'].append(node)

    if not os.path.exists(args.out):
        os.makedirs(args.out)
       
    prefix = os.path.basename(yamlfile).split('.')[0]
    outfile = os.path.join(args.out, f"{prefix}.json")
    write_json(data, outfile)

if __name__ == "__main__":
    main()
