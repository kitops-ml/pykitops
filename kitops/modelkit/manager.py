import os
from dotenv import load_dotenv
from typing import Optional
from .reference import ModelKitReference
from .user import UserCredentials

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
        user_credentials:
            Gets or sets the user credentials.
        modelkit_reference:
            Gets or sets the modelkit reference.     
    """
    def __init__(self,
                 user_credentials: Optional[UserCredentials] = None, 
                 modelkit_reference: Optional[ModelKitReference] = None,
                 modelkit_tag: Optional[str] = None):
        """
        Initializes the ModelKitManager instance.

        Args:
            user_credentials (Optional[UserCredentials]): The user credentials.
            modelkit_reference (Optional[ModelKitReference]): The modelkit reference.
            modelkit_tag (Optional[str]): The modelkit tag to parse into a ModelKitReference.

        Examples:
            >>> manager = ModelKitManager()
            >>> manager.user_credentials
            <UserCredentials>
            >>> manager.modelkit_reference
            <ModelKitReference>
        """
        if user_credentials is not None:
            self._user_credentials = user_credentials
        else:
            self._user_credentials = UserCredentials()
    
        if modelkit_reference is not None:
            self._modelkit_reference = modelkit_reference
        else:
            # try to build the modelkit reference from the tag.
            # if modelkit_tag is None then an empty ModelkitReference 
            # will be created.
            self._modelkit_reference = ModelKitReference(modelkit_tag)
        

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
    def modelkit_reference(self):
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
