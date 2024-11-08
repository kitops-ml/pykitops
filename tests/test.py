import kitops.cli.kit as kit
from kitops.modelkit.manager import ModelKitManager
from kitops.modelkit.user import UserCredentials
from kitops.modelkit.reference import ModelKitReference


modelkit_tag = "jozu.ml/brett/titanic_survivability:trained_model_v2"
manager = ModelKitManager(modelkit_tag=modelkit_tag)

print(manager.working_directory)
print(manager.user_credentials)
print(manager.modelkit_reference)

kit.version()

kit.login(user = manager.user_credentials.username, 
          passwd = manager.user_credentials.password,
          registry = manager.user_credentials.registry)




