import py
import yaml
from typing import Dict
from modelkit.kitfile import Kitfile

class TestKitfileCreation:
    def test_create_full_kitfile(self, fixtures, tmpdir = None):
        kitfile_path = py.path.local(fixtures['Kitfile_full'])
        kitfile = self.load_kitfile(path = kitfile_path)
        assert kitfile is not None
    
    def load_kitfile(self, path : str) -> Kitfile:
        if not path:
            return Kitfile()
        
        try:
            with open(path, 'r') as file:
            # Load the yaml data
                data = yaml.safe_load(file)

            # TEMP
            print(f"type(data):{type(data)} ")
            print(data)
        except yaml.YAMLError as e:
            if hasattr(e, 'problem_mark'):
                mark = e.problem_mark
                print("Error in Kitfile at " +
                      f"line{mark.line+1}, column:{mark.column+1}")
                raise
        kitfile = Kitfile(data)
        # iterate through the loaded kitfile's sections
        # that match the allowed sections
        if kitfile:
            provided_sections = set(kitfile.keys())
            matching_sections = provided_sections.intersection(
                                   Kitfile._allowed_section_names)
            for section in matching_sections:
                class_name = section[0].upper() + section[1:] + "Section"
                class_ref = globals().get(class_name)
                self.__setattr__(section,
                                 class_ref.create_from_yaml(kitfile[section]))
            
        return kitfile


fixtures : Dict[str, str] = {
    'Kitfile_base':
        'modelkit/tests/fixtures/Kitfile_base',
    'Kitfile_full': 
        'modelkit/tests/fixtures/Kitfile_full'
    }

tester = TestKitfileCreation()
tester.test_create_full_kitfile(fixtures=fixtures, tmpdir=None)
