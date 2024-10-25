import yaml

class YAMLBuilder:
    def __init__(self):
        self.data = {}

    def build(self):
        return yaml.dump(self.data, default_flow_style=False)

class BaseDecorator:
    def __init__(self, builder):
        self._builder = builder

    def build(self):
        return self._builder.build()

class AddManifestVersion(BaseDecorator):
    def __init__(self, builder, version):
        super().__init__(builder)
        self.version = version

    def build(self):
        self._builder.data['manifestVersion'] = self.version
        return super().build()

class AddPackage(BaseDecorator):
    def __init__(self, builder, name, version, description, authors):
        super().__init__(builder)
        self.package = {
            'name': name,
            'version': version,
            'description': description,
            'authors': authors
        }

    def build(self):
        self._builder.data['package'] = self.package
        return super().build()

class AddCode(BaseDecorator):
    def __init__(self, builder, path, description, license):
        super().__init__(builder)
        self.code = [{
            'path': path,
            'description': description,
            'license': license
        }]

    def build(self):
        self._builder.data['code'] = self.code
        return super().build()

class AddDatasets(BaseDecorator):
    def __init__(self, builder, datasets):
        super().__init__(builder)
        self.datasets = datasets

    def build(self):
        self._builder.data['datasets'] = self.datasets
        return super().build()

class AddModel(BaseDecorator):
    def __init__(self, builder, name, path, framework, version, description, license):
        super().__init__(builder)
        self.model = {
            'name': name,
            'path': path,
            'framework': framework,
            'version': version,
            'description': description,
            'license': license
        }

    def build(self):
        self._builder.data['model'] = self.model
        return super().build()

# Usage
base = YAMLBuilder()
with_manifest = AddManifestVersion(base, '1.0')
with_package = AddPackage(with_manifest, 'AIProjectName', '1.2.3', 'A brief description of the AI/ML project.', ['Author Name', 'Contributor Name'])
with_code = AddCode(with_package, 'src/', 'Source code for the AI models.', 'Apache-2.0')
with_datasets = AddDatas













import yaml

# Helper function to read the project's Kitfile from disk into
# a python dictionary object
def import_kitfile() -> dict:
    # Open the Kitfile 
    with open('Kitfile', 'r') as file:
        # Load the contents into a Python dictionary
        kitfile = yaml.safe_load(file)
    return kitfile

# Helper function to print the contents of the python dictionary object
# representing the project's Kitfile
def print_kitfile_contents(kitfile):
    print('Kitfile Contents...')
    print('===================\n')
    print(yaml.safe_dump(kitfile, sort_keys=False))

# Helper function to export the python dictionary object 
# representing the project's Kitfile to disk
def export_kitfile(kitfile):
    # Open the Kitfile 
    yaml.safe_dump(kitfile, open('Kitfile', 'w'), sort_keys=False)

kitfile = import_kitfile()
print_kitfile_contents(kitfile)








# add the 'images' folder to the 'docs' section of the Kitfile
image_dir_info = {
    "path": "images",
    "description": "Directory containing figures and graphs exported as image files." 
}
kitfile["docs"].append(image_dir_info)

# save the updated Kitfile contents to disk
export_kitfile(kitfile)

# reload the Kitfile from disk and display the contents
# to make sure it was persisited correctly
kitfile = import_kitfile()
print_kitfile_contents(kitfile)




allowed_keys = {'name', 'path', 'type'}
my_dict = {'key1': 'value1', 'key2': 'value2', 'key3': 'value3', 'key4': 'value4'}

filtered_dict = {k: v for k, v in my_dict.items() if k in allowed_keys}

print(filtered_dict)