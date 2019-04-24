from enum import Enum


class Mutation(Enum):
    """
    Mutation state.
    """
    NOT_SET = 1


def _is_set(v):
    """
    Check if a field in a MutationRequest is set.
    """
    return v != Mutation.NOT_SET
