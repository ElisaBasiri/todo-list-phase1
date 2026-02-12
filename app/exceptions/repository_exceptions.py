# app/exceptions/repository_exceptions.py

class RepositoryError(Exception):
    """Base exception for all repository-related errors"""
    pass


class NotFoundError(RepositoryError):
    """Raised when a requested resource (e.g. project/task) is not found"""
    pass


class DuplicateError(RepositoryError):
    """Raised when trying to create/update with a duplicate unique value (e.g. project name)"""
    pass 
