import os

import yaml

from kitops.modelkit import Package
from kitops.modelkit.kitfile import Kitfile


def test_initialize_from_path(fixtures: dict[str, str]):
    kitfile = Kitfile(path=str(fixtures["Kitfile_full"]))

    assert kitfile.manifestVersion == "1.0"  # assert package block
    assert kitfile.package.name == "Titanic-Survivability-Predictor"
    assert (
        kitfile.package.description == "A model attempting to predict passenger survivability of  the Titanic Shipwreck"
    )
    assert kitfile.package.authors == ["Jozu"]  # assert code block
    assert len(kitfile.code) == 2
    assert kitfile.code[0].path == "requirements.txt"
    assert kitfile.code[0].description == "Python packages required by this example."
    assert kitfile.code[0].license == "Apache-2.0"
    assert kitfile.code[1].path == "titanic_survivability.ipynb"
    assert kitfile.code[1].description == "Jupyter Notebook used to train, validate, optimize and  export the model."
    assert kitfile.code[1].license == "Apache-2.0"  # assert datasets block
    assert len(kitfile.datasets) == 2
    assert kitfile.datasets[0].name == "training"
    assert kitfile.datasets[0].path == "data/train.csv"
    assert kitfile.datasets[0].description == "Data to be used for model training."
    assert kitfile.datasets[0].license == "Apache-2.0"
    assert kitfile.datasets[1].name == "testing"
    assert kitfile.datasets[1].path == "data/test.csv"
    assert kitfile.datasets[1].description == "Data to be used for model testing."
    assert kitfile.datasets[1].license == "Apache-2.0"  # assert docs block
    assert len(kitfile.docs) == 2
    assert kitfile.docs[0].path == "README.md"
    assert kitfile.docs[0].description == "Important notes about the project."
    assert kitfile.docs[1].path == "images"
    assert kitfile.docs[1].description == (
        "Directory containing figures and graphs exported as image files."
    )  # assert model block
    assert kitfile.model.name == "titanic-survivability-predictor"
    assert kitfile.model.path == "model"
    assert kitfile.model.description == "Directory containing figures and graphs exported as image files."
    assert kitfile.model.framework == "joblib"
    assert kitfile.model.license == "Apache-2.0"
    assert kitfile.model.version == "1.0"

    # assert model parts
    assert len(kitfile.model.parts) == 4
    assert kitfile.model.parts[0].path == "config.json"
    assert kitfile.model.parts[0].name == "config"
    assert kitfile.model.parts[0].type == "config file"
    assert kitfile.model.parts[1].path == "tokenizer.json"
    assert kitfile.model.parts[2].path == "tokenizer_config.json"
    assert kitfile.model.parts[3].path == "vocab.txt"

    # assert model parameters
    assert kitfile.model.parameters["param1"] == "val1"
    assert kitfile.model.parameters["param2"] == "val2"
    assert kitfile.model.parameters["items"] == ["list item 1", "list item 2"]


def test_pydantic_init_from_path_vs_dict(fixtures: dict[str, str]):
    """Test that Kitfile can be initialized from a path and dictionary with same values."""
    kitfile = Kitfile(path=str(fixtures["Kitfile_full"]))
    with open(fixtures["Kitfile_full"], "r", encoding="utf-8") as f:
        kitfile_dict = yaml.safe_load(f)
    kitfile_from_dict = Kitfile(**kitfile_dict)

    assert kitfile.package == kitfile_from_dict.package
    assert kitfile.code == kitfile_from_dict.code
    assert kitfile.datasets == kitfile_from_dict.datasets
    assert kitfile.docs == kitfile_from_dict.docs
    assert kitfile.model == kitfile_from_dict.model
    assert kitfile.model.parts == kitfile_from_dict.model.parts
    assert kitfile.model.parameters == kitfile_from_dict.model.parameters


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
    kitfile.package = Package.model_validate(
        {
            "name": "New-Package",
            "version": "2.0.0",
            "description": "New description",
            "authors": ["Author"],
        }
    )
    assert kitfile.package.name == "New-Package"
    assert kitfile.package.version == "2.0.0"
    assert kitfile.package.description == "New description"
    assert kitfile.package.authors == ["Author"]


def test_empty_kitfile_and_mutate():
    # Create an empty Kitfile and update attributes
    kitfile = Kitfile()

    # Serialize to YAML, make sure nothing fails
    kitfile.to_yaml()
    # Serialize to YAML, make sure nothing fails
    kitfile.to_yaml()

    kitfile.manifestVersion = "3.0"
    kitfile.package = Package.model_validate(
        {
            "name": "Another-Package",
            "version": "3.0.0",
            "description": "Another description",
            "authors": ["Someone"],
        }
    )
    kitfile.package = {
        "name": "Another-Package",
        "version": "3.0.0",
        "description": "Another description",
        "authors": ["Someone"],
    }

    assert kitfile.manifestVersion == "3.0"
    assert kitfile.package.name == "Another-Package"
    assert kitfile.package.version == "3.0.0"
    assert kitfile.package.description == "Another description"
    assert kitfile.package.authors == ["Someone"]

    # Serialize to YAML, make sure nothing fails
    kitfile.to_yaml()
    assert kitfile.manifestVersion == "3.0"
    assert kitfile.package.name == "Another-Package"
    assert kitfile.package.version == "3.0.0"
    assert kitfile.package.description == "Another description"
    assert kitfile.package.authors == ["Someone"]

    # Serialize to YAML, make sure nothing fails
    kitfile.to_yaml()
