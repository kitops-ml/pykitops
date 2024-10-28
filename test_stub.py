import yaml

def import_kitfile() -> dict:
    # Open the Kitfile 
    with open('resources/kitfile_template.yaml', 'r') as template:
        # Load the contents into a Python dictionary
        kitfile = yaml.safe_load(template)
    return kitfile

def print_kitfile_contents(kitfile) -> None:
    print('Kitfile Contents...')
    print('===================\n')
    print(yaml.safe_dump(kitfile, sort_keys=False,
                         default_flow_style=False))

def export_kitfile(kitfile) -> None:
    with open('resources/Kitfile', 'w') as kitfile_out:
        yaml.safe_dump(kitfile, kitfile_out, sort_keys=False,
                       default_flow_style=False)

kitfile = import_kitfile()
print_kitfile_contents(kitfile)
export_kitfile(kitfile)