from enum import Enum


class TaskStatus(Enum):
    """Allowed status values for a task"""
    TODO = "todo"
    DOING = "doing"
    DONE = "done"