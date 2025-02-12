"""
Copyright 2024 The KitOps Authors.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

SPDX-License-Identifier: Apache-2.0
"""

from typing import Optional

from .utils import load_environment_variables


class UserCredentials:
    """
    A class to manage user credentials loaded from environment variables.
    Attributes:
        username (str): The username for the user.
        password (str): The password for the user.
        registry (Optional[str]): The registry information for the user.
        namespace (Optional[str]): The namespace information for the user.
    Methods:
        __init__():
            Initializes the UserCredentials instance by loading environment variables.
        username:
            Gets or sets the username.
        password:
            Gets or sets the password.
        registry:
            Gets or sets the registry information.
        namespace:
            Gets or sets the namespace information.
    """

    def __init__(
        self,
        username: Optional[str] = None,
        password: Optional[str] = None,
        registry: Optional[str] = None,
        namespace: Optional[str] = None,
    ):
        """
        Initializes the UserCredentials instance with the values provided.
        If no values are provided, they are loaded from environment variables.
        Initializes the private attributes _username, _password, _registry, and _namespace.
        Raises:
            ValueError: If either username or password is missing from the provided arguments or environment variables.

            Examples:
            >>> user = UserCredentials()
            >>> user.username
            'user'
            >>> user.password
            'password'
            >>> user.registry
            'registry'
            >>> user.namespace
            'namespace'
        """
        try:
            vars = load_environment_variables()
            self.username = username or vars.get("username")
            self.password = password or vars.get("password")
            self.registry = registry or vars.get("registry")
            self.namespace = namespace or vars.get("namespace")
        except ValueError as e:
            if not username or not password:
                raise ValueError(
                    "Username and password must be provided either as arguments or in environment variables."
                ) from e
            self.username = username
            self.password = password
            self.registry = registry
            self.namespace = namespace

    @property
    def username(self) -> Optional[str]:
        """
        Gets the username.

            Examples:
            >>> user = UserCredentials()
            >>> user.username
            'user'
        """
        return self._username

    @username.setter
    def username(self, value: Optional[str]):
        """
        Sets the username.
        Args:
            value (str): The username to set.
            Raises:
                ValueError: If the username is not a string.

                Examples:
                >>> user = UserCredentials()
                >>> user.username = 'new_user'
                >>> user.username
                'new_user'
        """
        if value is not None and not isinstance(value, str):
            raise ValueError(
                f"Username must be a string or None. Received: {type(value).__name__}"
            )
        self._username = value

    @property
    def password(self) -> Optional[str]:
        """
        Gets the password.

            Examples:
            >>> user = UserCredentials()
            >>> user.password = 'new_password'
            >>> user.password
            'new_password'
        """
        return self._password

    @password.setter
    def password(self, value: Optional[str]):
        """
        Sets the password.
        Args:
            value (str): The password to set.
            Raises:
                ValueError: If the password is not a string.

                Examples:
                >>> user = UserCredentials()
                >>> user.password = 'new_password'
                >>> user.password
                'new_password'
        """
        if value is not None and not isinstance(value, str):
            raise ValueError(
                f"Password must be a string or None. Received: {type(value).__name__}"
            )
        self._password = value

    @property
    def registry(self) -> Optional[str]:
        """
        Gets the registry information.

            Examples:
            >>> user = UserCredentials()
            >>> user.registry = 'new_registry'
            >>> user.registry
            'new_registry'
        """
        return self._registry

    @registry.setter
    def registry(self, value: Optional[str]):
        """
        Sets the registry information.

        Args:
            value (str | None): The registry information to set.
            Raises:
                ValueError: If the registry information is not a string
                    or None.

                Examples:
                >>> user = UserCredentials()
                >>> user.registry = 'new_registry'
                >>> user.registry
                'new_registry'
        """
        if value is not None and not isinstance(value, str):
            raise ValueError(
                f"Registry must be a string or None. Received: {type(value).__name__}"
            )
        self._registry = value

    @property
    def namespace(self) -> Optional[str]:
        """
        Gets the namespace information.

            Examples:
            >>> user = UserCredentials()
            >>> user.namespace = 'new_namespace'
            >>> user.namespace
            'new_namespace'
        """
        return self._namespace

    @namespace.setter
    def namespace(self, value: Optional[str]):
        """
        Sets the namespace information.

        Args:
            value (str | None): The namespace information to set.
            Raises:
                ValueError: If the namespace information is not a string.

                Examples:
                >>> user = UserCredentials()
                >>> user.namespace = 'new_namespace'
                >>> user.namespace
                'new_namespace'
        """
        if value is not None and not isinstance(value, str):
            raise ValueError(
                f"Namespace must be a string or None. Received: {type(value).__name__}"
            )
        self._namespace = value
