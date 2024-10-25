class NullOrEmptyStringError(ValueError):
    pass

class NullOrEmptyListError(ValueError):
    pass

class KitfileError(ValueError):
    pass

class ManifestVersionError(KitfileError):
    pass

class PackageError(KitfileError):
    pass