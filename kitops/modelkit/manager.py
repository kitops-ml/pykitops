import os
import kitops.cli.kit as kit

from dotenv import load_dotenv
from typing import Optional
from .kitfile import Kitfile
from .reference import ModelKitReference
from .user import UserCredentials
from .utils import get_or_create_directory

class ModelKitManager:
    """
    A class to represent a modelkit manager.
    This class manages the user credentials and modelkit reference.
    Attributes:
        user_credentials (UserCredentials): The user credentials.
        modelkit_reference (ModelKitReference): The modelkit reference.
        Methods:
        __init__():
            Initializes the ModelKitManager instance.
        working_directory:
            Gets or sets the working directory.
        user_credentials:
            Gets or sets the user credentials.
        modelkit_reference:
            Gets or sets the modelkit reference.     
    """
    def __init__(self,
                 working_directory: str = os.getcwd(),
                 user_credentials: Optional[UserCredentials] = None, 
                 modelkit_reference: Optional[ModelKitReference] = None,
                 modelkit_tag: Optional[str] = None):
        """
        Initializes the ModelKitManager instance.

        Args:
            working_directory (str): The working directory. 
                Defaults to os.getcwd(). This is the directory used by
                the ModelKitManager to work with the given ModelKit or 
                used to create a new ModelKit. The ModelKit's Kitfile
                is also read from and saved to this directory. If the 
                given directory does not exist, it will be created, if possible;
                otherwise, an error will be raised.
            user_credentials (Optional[UserCredentials]): The user credentials. Defaults to None.
                If None, the user credentials are loaded from environment variables.
            modelkit_reference (Optional[ModelKitReference]): The modelkit reference. Defaults to None.
                If None, the modelkit reference is created from the modelkit tag.
            modelkit_tag (Optional[str]): The modelkit tag to parse into a ModelKitReference. Defaults to None.
                If None, an empty ModelKitReference is created.

        Examples:
            >>> manager = ModelKitManager()
            >>> manager.working_directory
            <WorkingDirectory>
            >>> manager.user_credentials
            <UserCredentials>
            >>> manager.modelkit_reference
            <ModelKitReference>
        """
        self.working_directory = working_directory

        if user_credentials is not None:
            self.user_credentials = user_credentials
        else:
            self.user_credentials = UserCredentials()
    
        if modelkit_reference is not None:
            self.modelkit_reference = modelkit_reference
        else:
            # try to build the modelkit reference from the tag.
            # if modelkit_tag is None then an empty ModelkitReference 
            # will be created.
            self.modelkit_reference = ModelKitReference(modelkit_tag)

    @property
    def working_directory(self) -> str:
        """
        Gets the working directory.
        
        Returns:
            str: The working directory.
        """
        return self._working_directory    
    
    @working_directory.setter
    def working_directory(self, value: str):
        """
        Sets the working directory.
        
        Args:
            value (str): The working directory to set.
        """
        self._working_directory = get_or_create_directory(value)

    @property
    def user_credentials(self):
        """
        Gets the user credentials.

        Returns:

        """
        return self._user_credentials
    
    @user_credentials.setter
    def user_credentials(self, value: UserCredentials):
        """
        Sets the user credentials.
        
        Args:
            value (UserCredentials): The user credentials to set.
        """
        self._user_credentials = value

    @property
    def modelkit_reference(self) -> ModelKitReference:
        """
        Gets the modelkit reference.
        
        Returns:
            ModelKitReference: The modelkit reference.
        """
        return self._modelkit_reference
    
    @modelkit_reference.setter
    def modelkit_reference(self, value: ModelKitReference):
        """
        Sets the modelkit reference.
        
        Args:
            value (ModelKitReference): The modelkit reference to set.
        """
        self._modelkit_reference = value

    @property
    def kitfile(self) -> Kitfile:
        """
        Gets the Kitfile.
        
        Returns:
            Kitfile: The Kitfile.
        """
        return self._kitfile
    
    @kitfile.setter
    def kitfile(self, value: Kitfile) -> None:
        """
        Sets the Kitfile.
        
        Args:
            value (Kitfile): The Kitfile to set.
        """
        self._kitfile = value

    def pull_and_unpack_modelkit(self, load_kitfile: bool = False,
                                 filters: Optional[list[str]] = None) -> None:
        """
        Unpacks the ModelKit into the working directory.

        Args:
            filters (Optional[list[str]]): The filters to apply when 
                unpacking the ModelKit.  Defaults to None.  The filters
                are used to specify the Kitfile parts to unpack from the
                ModelKit (e.g. ["model", "data"]). If None, all parts
                are unpacked.
            load_kitfile (bool): If True, the Kitfile will be loaded 
                from the working directory afer the ModelKit has been
                unpacked. Defaults to False.

        Returns:
            None
        """
        kit.login(user = self.user_credentials.username, 
                  passwd = self.user_credentials.password,
                  registry = self.modelkit_reference.registry)
        
        if not filters:
            # If no filters are provided, go ahead and issue a pull request
            # before unpacking; otherwise, issue the unpack request only.
            kit.pull(self.modelkit_reference.modelkit_tag)
        kit.unpack(self.modelkit_reference.modelkit_tag, 
                   dir = self.working_directory)
        kit.logout(registry = self.modelkit_reference.registry)

        if load_kitfile:
            kitfile_path = self.working_directory + "/Kitfile"
            self.kitfile = Kitfile(kitfile_path)

    def pack_and_push_modelkit(self, save_kitfile: bool = False) -> None:
        """
        Packs the ModelKit from the working directory and pushes it 
        to the registry.

        Args:
            save_kitfile (bool): If True, the Kitfile will be saved to 
                the working directory before the Kitfile is packed and
                pushed. Defaults to False.

        Returns:
            None
        """
        # save the current directory so we can return to it later
        current_directory = os.getcwd()
        os.chdir(self.working_directory)

        if save_kitfile:
            self.kitfile.save()

        kit.login(user = self.user_credentials.username, 
                  passwd = self.user_credentials.password,
                  registry = self.modelkit_reference.registry)
        kit.pack(self.modelkit_reference.modelkit_tag)
        kit.push(self.modelkit_reference.modelkit_tag)
        kit.logout(registry = self.modelkit_reference.registry)

        # return to the original directory
        os.chdir(current_directory)

    def remove_modelkit(self, local: Optional[bool] = False,
                        remote: Optional[bool] = False) -> None:
        """
        Removes the ModelKit from the registry.

        Args:
            local (Optional[bool]): If True, the ModelKit will be removed
                from the local registry. Defaults to True.
            remote (Optional[bool]): If True, the ModelKit will be removed 
                from the remote registry.

        Returns:
            None

        Examples:
            >>> modelkit_tag = "jozu.ml/brett/titanic-survivability:latest"
            >>> manager = ModelKitManager(working_directory = "temp/titanic-full",
            ...                           modelkit_tag = modelkit_tag)
            >>> manager.remove_modelkit(local = True, remote = True)
        """
        kit.login(user = self.user_credentials.username, 
                  passwd = self.user_credentials.password,
                  registry = self.modelkit_reference.registry)
        if local:
            kit.remove(self.modelkit_reference.modelkit_tag, remote = False)

        if remote:
            kit.remove(self.modelkit_reference.modelkit_tag, remote = True)

        kit.logout(registry = self.modelkit_reference.registry)