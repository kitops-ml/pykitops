from kitops.kitfile import Kitfile

# Usage
path = 'kitops/tests/fixtures/Kitfile_full'
kitfile = Kitfile(path=path)

print("kitfile.manifestVersion: " + kitfile.manifestVersion)
print("kitfile.package: ")
print(kitfile.package)
print("=======================================================")

# Serialize to YAML
yaml_data = kitfile.to_yaml()
print(yaml_data)
print("=======================================================")


kitfile.manifestVersion = "2.0"
kitfile.package = {
    "name": "New-Package",
    "version": "2.0.0",
    "description": "New description",
    "authors": ["Author"]
}

print("kitfile.manifestVersion: " + kitfile.manifestVersion)
print("kitfile.package: ")
print(kitfile.package)
print("=======================================================")
# Serialize to YAML
yaml_data = kitfile.to_yaml()
print(yaml_data)
print("=======================================================")

# Create an empty Kitfile and update attributes
kitfile = Kitfile()
kitfile.manifestVersion = "3.0"
kitfile.package = {
    "name": "Another-Package",
    "version": "3.0.0",
    "description": "Another description",
    "authors": ["Someone"]
}
# Deserialize from YAML
# new_kitfile = Kitfile.from_yaml(yaml_data)
# print("new_kitfile.manifestVersion: " + new_kitfile.manifestVersion)
# print("new_kitfile.package: ")
# print(new_kitfile.package)


# def custom_dict_representer(dumper, data):
#     return dumper.represent_dict(data.items())