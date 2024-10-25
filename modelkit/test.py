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
    def __init__(self, version):
        super().__init__()
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
builder = YAMLBuilder()

with_manifest = AddManifestVersion(base, '1.0')
yaml_content = with_manifest.build()
print(yaml_content)

with_package = AddPackage(base, 'AIProjectName', '1.2.3', 'A brief description of the AI/ML project.', ['Author Name', 'Contributor Name'])
yaml_content = with_package.build()
print(yaml_content)

with_code = AddCode(base, 'src/', 'Source code for the AI models.', 'Apache-2.0')
yaml_content = with_code.build()
print(yaml_content)

with_datasets = AddDatasets(base, [{'name': 'DatasetName', 'path': 'data/dataset.csv', 'description': 'Description of the dataset.', 'license': 'CC-BY-4.0'}])
yaml_content = with_datasets.build()
print(yaml_content)

with_model = AddModel(base, 'ModelName', 'models/model.h5', 'TensorFlow', '1.0', 'Model description.', 'Apache-2.0')
yaml_content = with_model.build()
print(yaml_content)
