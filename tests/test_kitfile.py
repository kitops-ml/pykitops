from pathlib import Path

import pytest
import yaml
from pydantic import ValidationError

from kitops.modelkit.kitfile import Kitfile


class TestKitfileCreation:
    def test_create_full_kitfile(self, fixtures: dict[str, Path]):
        """Test creation of a full Kitfile from a fixture."""
        kitfile_path = fixtures["Kitfile_full"]
        kitfile = Kitfile(path=str(kitfile_path))
        assert kitfile is not None
        assert kitfile.manifestVersion == "1.0"
        assert kitfile is not None and kitfile.package.name == "Titanic-Survivability-Predictor"
        assert kitfile is not None and kitfile.model.name == "titanic-survivability-predictor"

    def test_create_from_null_file(self, fixtures: dict[str, Path]):
        """Test creation of a Kitfile from a null file."""
        kitfile_path = fixtures["kitfile_null"]
        with pytest.raises(ValueError):
            Kitfile(path=str(kitfile_path))

    def test_create_invalid_kitfile(self):
        """Test creation of a Kitfile from an invalid file."""
        with pytest.raises(ValueError):
            Kitfile(path="path/does/not/exist/Kitfile")

    def test_create_blank_kitfile(self):
        """Test creation of a blank Kitfile."""
        kitfile = Kitfile()
        assert kitfile is not None and kitfile == Kitfile()

    def test_create_from_template(self, fixtures: dict[str, Path]):
        """Test creation of a Kitfile from a template."""
        kitfile_path = fixtures["Kitfile_full"]
        with pytest.raises(ValueError):
            kitfile = Kitfile(path=str(kitfile_path), manifestVersion="6.9.0")
            assert kitfile is not None and kitfile.manifestVersion == "6.9.0"  # this won't run

    def test_create_from_kwargs(self):
        """Test creation of a Kitfile from keyword arguments."""
        kitfile = Kitfile(
            manifestVersion="6.6.6",
            package={
                "name": "Package Packer",
                "version": "5.2.5",
                "description": "Package your packages with Package Packer",
                "authors": ["Patrick Packer"],
            },
            model={
                "name": "Pack Model",
                "path": "pack_model_path/",
                "framework": "PackageRT",
                "version": "1.2.3",
                "description": "Model for packing packages",
                "license": "Pack License",
                "parts": [],
                "parameters": "",
            },
        )
        assert kitfile.manifestVersion == "6.6.6"
        assert kitfile.package.name == "Package Packer"
        assert kitfile.model.name == "Pack Model"

    def test_create_from_dict(self, fixtures: dict[str, Path]):
        """Test creation of a Kitfile from a dictionary."""
        kitfile_dict = yaml.safe_load(fixtures["Kitfile_full"].read_text("utf-8"))
        assert Kitfile(**kitfile_dict).model_dump(exclude_unset=True) == kitfile_dict

        Kitfile.model_validate(kitfile_dict)  # ensure validation works

    def test_create_null_kitfile(self):
        """Test creation of a Kitfile with None values."""
        with pytest.raises(ValidationError):
            Kitfile(
                manifestVersion=None,
                package=None,
                model=None,
                code=None,
                datasets=None,
                docs=None,
            )

    def test_create_from_invalid_kwargs(self):
        """Test creation of a Kitfile from invalid keyword arguments."""
        with pytest.raises(ValueError):
            Kitfile(
                manifestVersion="onety-one",
                package="Invalid Package Data",  # should be a dict
                model="Invalid Model Data",  # should be a dict
            )


class TestKitfileMutation:
    """Tests for mutating attributes of a Kitfile."""

    def full_kitfile(self, fixtures: dict[str, Path]) -> Kitfile:
        """Helper method to create a full Kitfile from a fixture."""
        kitfile_path = fixtures["Kitfile_full"]
        return Kitfile(path=str(kitfile_path))

    def test_mutate_manifestVersion(self, fixtures: dict[str, Path]):
        """Test mutation of manifestVersion attribute in Kitfile."""
        kitfile = self.full_kitfile(fixtures)

        kitfile.manifestVersion = "2.0"
        assert kitfile.manifestVersion == "2.0"
        with pytest.raises(TypeError):
            kitfile.manifestVersion = []  # type: ignore

    def test_mutate_package(self, fixtures: dict[str, Path]):
        """Test mutation of package attribute in Kitfile."""
        kitfile = self.full_kitfile(fixtures)
        kitfile.package = {
            "name": "New Package Name",
            "version": "2.0.0",
            "description": "Updated description",
            "authors": ["New Author"],
        }
        kitfile.package.name = "Newer Package Name"
        assert kitfile.package.name == "Newer Package Name"
        with pytest.raises(TypeError):
            kitfile.package = 123  # type: ignore

    def test_mutate_model(self, fixtures: dict[str, Path]):
        """Test mutation of model attribute in Kitfile."""
        kitfile = self.full_kitfile(fixtures)
        kitfile.model = {
            "name": "New Model Name",
            "path": "new_model_path/",
            "framework": "new_framework",
            "version": "2.0.0",
            "description": "Updated model description",
            "license": "New License",
            "parts": [],
            "parameters": "",
        }
        kitfile.model.name = "Newer Model Name"
        assert kitfile.model.name == "Newer Model Name"
        with pytest.raises(TypeError):
            kitfile.model = 123  # type: ignore

    def test_mutate_code(self, fixtures: dict[str, Path]):
        """Test mutation of code attribute in Kitfile."""
        kitfile = self.full_kitfile(fixtures)
        kitfile.code = [
            {
                "path": "new_code_path/",
                "description": "Updated code description",
                "license": "New Code License",
            }
        ]
        kitfile.code[0].path = "new_code_path2/"
        assert kitfile.code[0].path == "new_code_path2/"
        with pytest.raises(TypeError):
            kitfile.code = 123  # type: ignore

    def test_mutate_datasets(self, fixtures: dict[str, Path]):
        """Test mutation of datasets attribute in Kitfile."""
        kitfile = self.full_kitfile(fixtures)
        kitfile.datasets = [
            {
                "name": "New Dataset Name",
                "path": "new_dataset_path/",
                "description": "Updated dataset description",
                "license": "New Dataset License",
            }
        ]
        kitfile.datasets[0].name = "Newer Dataset Name"
        assert kitfile.datasets[0].name == "Newer Dataset Name"
        with pytest.raises(TypeError):
            kitfile.datasets = 123  # type: ignore

    def test_mutate_docs(self, fixtures: dict[str, Path]):
        """Test mutation of docs attribute in Kitfile."""
        kitfile = self.full_kitfile(fixtures)
        kitfile.docs = [
            {
                "path": "new_docs_path/",
                "description": "Updated docs description",
            }
        ]
        kitfile.docs[0].path = "new_docs_path2/"
        assert kitfile.docs[0].path == "new_docs_path2/"
        with pytest.raises(TypeError):
            kitfile.docs = 123  # type: ignore


@pytest.mark.parametrize(
    "fixture_name",
    [
        "Kitfile_base",
        "Kitfile_base_thru_code",
        "Kitfile_base_thru_datasets",
        "Kitfile_base_thru_docs",
        "Kitfile_base_thru_model",
        "Kitfile_full",
        "Kitfile_manifestVersion_only",
    ],
)
class TestKitfileAttributeAccess:
    """Tests accessing attributes of a Kitfile using nearly all fixture types."""

    def setup_kitfile(self, fixture_name: str, fixtures: dict[str, Path]) -> Kitfile:
        """Helper method to set up a Kitfile from a fixture."""
        return Kitfile(path=str(fixtures[fixture_name]))

    def setup_expected(self, fixture_name: str, fixtures: dict[str, Path]) -> dict:
        """Helper method to load expected data from a fixture."""
        return yaml.safe_load(fixtures[fixture_name].read_text("utf-8"))

    def test_access_manifestVersion(self, fixture_name: str, fixtures: dict[str, Path]):
        """Test access to manifestVersion attribute in Kitfile."""
        kitfile = self.setup_kitfile(fixture_name, fixtures)
        expected = self.setup_expected(fixture_name, fixtures)
        assert kitfile.manifestVersion == expected["manifestVersion"]

    def test_access_package(self, fixture_name: str, fixtures: dict[str, Path]):
        """Test access to package attribute in Kitfile."""
        kitfile = self.setup_kitfile(fixture_name, fixtures)
        expected = self.setup_expected(fixture_name, fixtures)

        if "package" in expected:  # check when package is present
            assert kitfile.package.name == expected["package"]["name"]
            assert kitfile.package.version == expected["package"]["version"]
            assert kitfile.package.description == expected["package"]["description"]
            assert kitfile.package.authors == expected["package"]["authors"]

    def test_access_model(self, fixture_name: str, fixtures: dict[str, Path]):
        """Test access to model attribute in Kitfile."""
        kitfile = self.setup_kitfile(fixture_name, fixtures)
        expected = self.setup_expected(fixture_name, fixtures)

        if "model" in expected:  # check when model is present
            assert kitfile.model.name == expected["model"]["name"]
            assert kitfile.model.path == "model"
            assert kitfile.model.framework == "joblib"
            assert kitfile.model.version == "1.0"
            assert kitfile.model.description == "Directory containing figures and graphs exported as image files."
            assert kitfile.model.license == "Apache-2.0"

    def test_access_code(self, fixture_name: str, fixtures: dict[str, Path]):
        """Test access to code attribute in Kitfile."""
        kitfile = self.setup_kitfile(fixture_name, fixtures)
        expected = self.setup_expected(fixture_name, fixtures)

        if "code" in expected:  # check when code is present
            assert len(kitfile.code) == len(expected["code"])
            for c, e in zip(kitfile.code, expected["code"]):
                assert c.path == e["path"]
                assert c.description == e["description"]
                assert c.license == e["license"]

    def test_access_datasets(self, fixture_name: str, fixtures: dict[str, Path]):
        """Test access to datasets attribute in Kitfile."""
        kitfile = self.setup_kitfile(fixture_name, fixtures)
        expected = self.setup_expected(fixture_name, fixtures)

        if "datasets" in expected:  # check when datasets are present
            assert len(kitfile.datasets) == len(expected["datasets"])
            for d, e in zip(kitfile.datasets, expected["datasets"]):
                assert d.name == e["name"]
                assert d.path == e["path"]
                assert d.description == e["description"]
                assert d.license == e["license"]

    def test_access_docs(self, fixture_name: str, fixtures: dict[str, Path]):
        """Test access to docs attribute in Kitfile."""
        kitfile = self.setup_kitfile(fixture_name, fixtures)
        expected = self.setup_expected(fixture_name, fixtures)

        if "docs" in expected:  # check when docs are present
            assert len(kitfile.docs) == len(expected["docs"])
            for d, e in zip(kitfile.docs, expected["docs"]):
                assert d.path == e["path"]
                assert d.description == e["description"]

    def test_access_parts(self, fixture_name: str, fixtures: dict[str, Path]):
        """Test access to parts attribute in Kitfile."""
        kitfile = self.setup_kitfile(fixture_name, fixtures)
        expected = self.setup_expected(fixture_name, fixtures)

        if "model" in expected and "parts" in expected["model"] and kitfile.model.parts:  # check when parts are present
            assert len(kitfile.model.parts) == len(expected["model"]["parts"])
            for part, expected_part in zip(kitfile.model.parts, expected["model"]["parts"]):
                assert part.path == expected_part["path"]

                if "name" in expected_part:
                    assert part.name == expected_part["name"]

                if "type" in expected_part:
                    assert part.type == expected_part["type"]
