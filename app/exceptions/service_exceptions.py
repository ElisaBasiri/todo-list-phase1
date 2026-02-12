# app/exceptions/service_exceptions.py

class ServiceError(Exception):
    """Base exception for all service-layer errors"""
    pass


class ValidationError(ServiceError):
    """Raised when input data fails validation rules (e.g. too many words, empty required field)"""
    pass


class NotFoundError(ServiceError):
    """Raised when a requested entity (project/task) does not exist"""
    pass


class LimitExceededError(ServiceError):
    """Raised when a limit (max projects, max tasks per project, etc.) is exceeded"""
    pass 
