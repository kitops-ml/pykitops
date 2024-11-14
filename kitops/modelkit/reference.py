
from typing import Optional
from .utils import parse_modelkit_tag

class ModelKitReference:
    """
    A class to represent a modelkit reference broken down into its parts.
    This class parses a modelkit tag and provides access to its components.
    These include the registry, namespace, model, and tag.
    
    Attributes:
        registry (str): The registry for the model.
        namespace (str): The namespace for the model.
        model (str): The model name.
        tag (str): The tag for the model.

    Methods:
        __init__():
            Initializes the ModelKitReference instance by parsing a tag.
        registry:
            Gets or sets the registry.
        namespace:
            Gets or sets the namespace.
        repository:
            Gets or sets the repository name.
        tag:
            Gets or sets the tag.
    """
    def __init__(self, modelkit_tag: Optional[str]):
        """
        Initializes the ModelKitReference instance by parsing a tag.
        
        Args:
            modelkit_tag (Optional[str]): The tag to parse. It should be in the form of:
                {registry}/{namespace}/{model}:{tag}
            
        Examples:
            >>> ref = ModelKitReference("jozu.ml/jozu-demos/titanic-survivability:latest")
            >>> ref.registry
            'jozu.ml'
            >>> ref.namespace
            'jozu-demos'
            >>> ref.repository
            'titanic-survivability'
            >>> ref.tag
            'latest'
        """
        if not modelkit_tag:
            self.registry = None
            self.namespace = None
            self.repository = None
            self.tag = None
        else:
            # try to parse the modelkit tag into its components. 
            try:
                parts = parse_modelkit_tag(modelkit_tag)
                self.registry = parts.get("registry")
                self.namespace = parts.get("namespace")
                self.repository = parts.get("model")
                self.tag = parts.get("tag")
            except ValueError as e:
                raise ValueError(
                        f"Error parsing modelkit tag: {modelkit_tag}"
                      ) from e

    @property
    def registry(self) -> Optional[str]:
        """
        Gets the registry.
        """
        return self._registry
    
    @registry.setter
    def registry(self, value: Optional[str]):
        """
        Sets the registry.
        
        Args:
            value (str): The registry to set.
        
        Raises:
            ValueError: If the registry is not a string or is not None
        
        Examples:
            >>> ref = ModelKitReference("jozu.ml/jozu-demos/titanic-survivability:latest")
            >>> ref.registry = "new_registry"
            >>> ref.registry
            'new_registry'
        """
        if value is not None and not isinstance(value, str):
            raise ValueError("Registry must be a string or None")
        self._registry = value

    @property
    def namespace(self) -> Optional[str]:
        """
        Gets the namespace.
        
        Examples:
            >>> ref = ModelKitReference("jozu.ml/jozu-demos/titanic-survivability:latest")
            >>> ref.namespace = "new_namespace"
            >>> ref.namespace
            'new_namespace'
        """
        return self._namespace
    
    @namespace.setter
    def namespace(self, value: Optional[str]):
        """
        Sets the namespace.
        
        Args:
            value (str): The namespace to set.
            
            Raises:
                ValueError: If the namespace is not a string or is not None.
                
                Examples:
                >>> ref = ModelKitReference("jozu.ml/jozu-demos/titanic-survivability:latest")
                >>> ref.namespace = "new_namespace"
                >>> ref.namespace
                'new_namespace'
        """
        if value is not None and not isinstance(value, str):
            raise ValueError("Namespace must be a string or None.")
        self._namespace = value

    @property
    def repository(self) -> Optional[str]:
        """
        Gets the repository name.
        
        Examples:
            >>> ref = ModelKitReference("jozu.ml/jozu-demos/titanic-survivability:latest")
            >>> ref.repository = "new_model"
            >>> ref.repository
            'new_repository'    
        """
        return self._repository
    
    @repository.setter
    def repository(self, value: Optional[str]):
        """
        Sets the repository name.
        
        Args:
            value (str): The repository name to set.
            
            Raises:
                ValueError: If the repository name is not a string or is None.
                
            Examples:
                >>> ref = ModelKitReference("jozu.ml/jozu-demos/titanic-survivability:latest")
                >>> ref.repository = "new_repository"
                >>> ref.repository
                'new_repository'
        """
        if value is not None and not isinstance(value, str):
            raise ValueError("Model name must be a string.")
        self._repository = value

    @property
    def tag(self) -> Optional[str]:
        """
        Gets the tag.

        Examples:
            >>> ref = ModelKitReference("jozu.ml/jozu-demos/titanic-survivability:latest")
            >>> ref.tag = "new_tag"
            >>> ref.tag
            'new_tag'
        """
        return self._tag
    
    @tag.setter
    def tag(self, value: Optional[str]):
        """
        Sets the tag.
        
        Args:
            value (str): The tag to set.
            
            Raises:
                ValueError: If the tag is not a string or None.
                
            Examples:
                >>> ref = ModelKitReference("jozu.ml/jozu-demos/titanic-survivability:latest")
                >>> ref.tag = "new_tag"
                >>> ref.tag
                'new_tag'
        """
        if value is not None and not isinstance(value, str):
            raise ValueError("Tag must be a string or None.")
        self._tag = value

    @property
    def modelkit_tag(self):
        if not self.registry:
            raise ValueError("Registry must be set to a non-empty string.")
        if not self.namespace:
            raise ValueError("Namespace must be set to a non-empty string.")
        if not self.repository:
            raise ValueError("Repository must be set to a non-empty string.")
        if not self.tag:
            raise ValueError("tag must be set to a non-empty string.")
        return f"{self.registry}/{self.namespace}/{self.repository}:{self.tag}"