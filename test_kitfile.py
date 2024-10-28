from modelkit.kitfile import Kitfile
from modelkit.manifest_version import ManifestVersionSection
#from modelkit.package import PackageSection
from modelkit.package_alt import PackageSection
from modelkit.code import CodeEntry, CodeSection
from modelkit.datasets import DatasetsEntry, DatasetsSection
from modelkit.docs import DocsEntry, DocsSection
from modelkit.model_parts import ModelPartsEntry, ModelPartsSection
from modelkit.model import ModelSection

kitfile = Kitfile()

print("--- manifest_version initialized with setter")
kitfile.manifest_version_section = ManifestVersionSection(
                                    version = "1.0")

print("--- package initialized with setter")
kitfile.package_section = PackageSection(
                            name = "My AI/ML Project", 
                            version = "1.0.0",
                            authors = ['brett', 'brad'])
print(kitfile.build())

print("--- package updated with description")
kitfile.package_section.description = "Description text..."
print(kitfile.build())

print("--- package updated with authors removed")
kitfile.package_section.authors = None
print(kitfile.build())

print("--- package updated with author added")
kitfile.package_section.authors = ['brett']
print(kitfile.build())

print("--- code initialized with constructor")
kitfile.code_section = CodeSection()
print(kitfile.build())

print("--- code initialized with add_entries")
kitfile.code_section.add_entry(
    CodeEntry(
        path = "source.py",
        description = "my source code",
        license = "Apache-2.0"))
kitfile.code_section.add_entry(
    CodeEntry(
        path = "requirementes.txt",
        description = "required packages"))
kitfile.code_section.add_entry(
    CodeEntry(
        path = ".gitignore"))
print(kitfile.build())

print("--- datasets initialized with constructor")
kitfile.datasets_section = DatasetsSection()
print(kitfile.build())

print("--- datasets initialized with add_entries")
kitfile.datasets_section.add_entry(
    DatasetsEntry(
        path = "raw.csv",
        name = "raw data",
        description = "raw data in CSV format",
        license = "Apache-2.0"))
kitfile.datasets_section.add_entry(
    DatasetsEntry(
        path = "test.csv",
        name = "test data",
        description = "test data in CSV format"))
kitfile.datasets_section.add_entry(
    DatasetsEntry(
        path = "training.csv",
        name = "training data"))
kitfile.datasets_section.add_entry(
    DatasetsEntry(
        path = "raw.csv"))
print(kitfile.build())

print("--- docs initialized with constructor")
kitfile.docs_section = DocsSection()
print(kitfile.build())

print("--- docs initialized with add_entries")
kitfile.docs_section.add_entry(
    DocsEntry(
        path = "README.md",
        description = "Read Me"))
kitfile.docs_section.add_entry(
    DocsEntry(
        path = "notes.txt"))
print(kitfile.build())

print("--- model inialized with constructor")
kitfile.model_section = ModelSection(path = "model.joblib",
                                     name = "my model")
print(kitfile.build())

print("--- model inialized with setters")
kitfile.model_section = ModelSection(path = "model.joblib",
                                     name = "my model")
model_parts_section = ModelPartsSection()
model_parts_section.add_entry(
    ModelPartsEntry(
        path = "config.json",
        name = "config",
        type = "json config file"
    ))
kitfile.model_section.parts = model_parts_section
kitfile.model_section.parameters = '''
age: 52
city: Florence
items:
- list item 1
- list item 2
'''
print(kitfile.build())