import os

from kitops.modelkit.kitfile import Kitfile


def test_initialize_from_path(fixtures: dict[str, str]):
    kitfile = Kitfile(path=str(fixtures["Kitfile_full"]))

    assert kitfile.manifestVersion == "1.0"

    # assert package block
    assert kitfile.package.get("name") == "Titanic-Survivability-Predictor"
    assert kitfile.package.get("description") == \
        "A model attempting to predict passenger survivability of  the Titanic Shipwreck"
    assert kitfile.package.get("authors") == ["Jozu"]

    # assert code block
    assert len(kitfile.code) == 2
    assert kitfile.code[0].get("path") == "requirements.txt"
    assert kitfile.code[0].get("description") == "Python packages required by this example."
    assert kitfile.code[0].get("license") == "Apache-2.0"
    assert kitfile.code[1].get("path") == "titanic_survivability.ipynb"
    assert kitfile.code[1].get("description") == \
        "Jupyter Notebook used to train, validate, optimize and  export the model."
    assert kitfile.code[1].get("license") == "Apache-2.0"

    # assert datasets block
    assert len(kitfile.datasets) == 2
    assert kitfile.datasets[0].get("name") == "training"
    assert kitfile.datasets[0].get("path") == "data/train.csv"
    assert kitfile.datasets[0].get("description") == "Data to be used for model training."
    assert kitfile.datasets[0].get("license") == "Apache-2.0"
    assert kitfile.datasets[1].get("name") == "testing"
    assert kitfile.datasets[1].get("path") == "data/test.csv"
    assert kitfile.datasets[1].get("description") == "Data to be used for model testing."
    assert kitfile.datasets[1].get("license") == "Apache-2.0"

    # assert docs block
    assert len(kitfile.docs) == 2
    assert kitfile.docs[0].get("path") == "README.md"
    assert kitfile.docs[0].get("description") == "Important notes about the project."
    assert kitfile.docs[1].get("path") == "images"
    assert kitfile.docs[1].get("description") == "Directory containing figures and graphs exported as image files."

    # assert model block
    assert kitfile.model.get("name") == "titanic-survivability-predictor"
    assert kitfile.model.get("path") == "model"
    assert kitfile.model.get("description") == "Directory containing figures and graphs exported as image files."
    assert kitfile.model.get("framework") == "joblib"
    assert kitfile.model.get("license") == "Apache-2.0"
    assert kitfile.model.get("version") == "1.0"
    
    # assert model parts
    assert len(kitfile.model.get("parts")) == 4
    assert kitfile.model.get("parts")[0].get("path") == "config.json"
    assert kitfile.model.get("parts")[0].get("name") == "config"
    assert kitfile.model.get("parts")[0].get("type") == "config file"
    assert kitfile.model.get("parts")[1].get("path") == "tokenizer.json"
    assert kitfile.model.get("parts")[2].get("path") == "tokenizer_config.json"
    assert kitfile.model.get("parts")[3].get("path") == "vocab.txt"

    # assert model parameters
    assert kitfile.model.get("parameters").get("param1") == "val1"
    assert kitfile.model.get("parameters").get("param2") == "val2"
    assert kitfile.model.get("parameters").get("items") == ["list item 1", "list item 2"]

def test_initialize_from_path_and_mutate(fixtures: dict[str, str]):
    current_directory = os.getcwd()
    print(current_directory)

    path = fixtures["Kitfile_full"]
    kitfile = Kitfile(path=str(path))

    assert kitfile.manifestVersion == "1.0"

    # Serialize to YAML, make sure nothing fails
    kitfile.to_yaml()

    kitfile.manifestVersion = "2.0"
    kitfile.package = {
        "name": "New-Package",
        "version": "2.0.0",
        "description": "New description",
        "authors": ["Author"],
    }

    assert kitfile.package.get("name") == "New-Package"
    assert kitfile.package.get("version") == "2.0.0"
    assert kitfile.package.get("description") == "New description"
    assert kitfile.package.get("authors") == ["Author"]

def test_empty_kitfile_and_mutate():
    # Create an empty Kitfile and update attributes
    kitfile = Kitfile()

    # Serialize to YAML, make sure nothing fails
    kitfile.to_yaml()

    kitfile.manifestVersion = "3.0"
    kitfile.package = {
        "name": "Another-Package",
        "version": "3.0.0",
        "description": "Another description",
        "authors": ["Someone"],
    }

    assert kitfile.manifestVersion == "3.0"
    assert kitfile.package.get("name") == "Another-Package"
    assert kitfile.package.get("version") == "3.0.0"
    assert kitfile.package.get("description") == "Another description"
    assert kitfile.package.get("authors") == ["Someone"]

    # Serialize to YAML, make sure nothing fails
    kitfile.to_yaml()
