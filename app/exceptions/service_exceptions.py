# app/exceptions/service_exceptions.py

class ServiceError(Exception):
    """Base exception for all service-layer errors"""
    pass


class ValidationError(ServiceError):
    """Raised when input data fails validation rules"""
    pass


class NotFoundError(ServiceError):
    """Raised when a requested entity is not found"""
    pass


class LimitExceededError(ServiceError):
    """Raised when a configured limit is exceeded"""
    pass


class DuplicateError(ServiceError):
    """Raised when trying to create/update with duplicate unique value (e.g. project name)"""
    pass