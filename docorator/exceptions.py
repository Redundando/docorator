class DocoratorError(Exception):
    pass

class AuthenticationError(DocoratorError):
    pass

class DocumentNotFoundError(DocoratorError):
    pass

class DocumentCreationError(DocoratorError):
    pass

class DocumentSaveError(DocoratorError):
    pass

class ConversionError(DocoratorError):
    pass