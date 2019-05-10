"""
Our own connexion resolver.
"""
import re

from connexion import Resolver


class MyResolver(Resolver):
    def __init__(self, bindings):
        super().__init__()
        self.bindings = bindings

    def resolve_operation_id(self, operation):
        """
        This function transforms an operation (a path) to a key and a function name.
        For instance, given the operation: GET "/device/{MAC}/vlan/{VLAN}/" it will extract "device" as a key,
        and vlan_get as a function name.

        The function name is the name of the function you implement in your class and the key will be mapped to an
        instance of a class.
        """

        # Path prefix is the first element of the URL. For instance for "/device/{MAC}/vlan/{VLAN}/" it would be
        # "device".
        path_prefix = re.search(r'^/(.*?)/', operation.path).group(1)

        # If an operation ID is specified, we override the behavior by this function and use the operationID as
        # function name.
        if operation.operation_id is not None:
            return f'{path_prefix}|{operation.operation_id}'

        # This part extracts the rest of the URL as in a list (for instance ['{MAC}', 'vlan', '{VLAN}'])
        path_suffix = re.search(r'^/.*?/(.*)$', operation.path).group(1)
        path_suffix = path_suffix.split("/")
        path_suffix = filter(bool, path_suffix)  # Remove empty strings.
        path_suffix = list(path_suffix)

        # The method name will be prefixed to the function name.
        method_name = operation.method

        def is_fixed_url_part(x: str) -> bool:
            """ Everything that is "{something}" is not a fixed part of the URL."""

            if x.startswith('{') and x.endswith('}'):
                return False
            return True

        # GETs on a global resource (for instance GET /vlan/), without an ID, are replaced with 'search'.
        # This is the same behavior as connexion's native RestyResolver.
        if method_name == 'get':
            if path_suffix == [] or is_fixed_url_part(path_suffix[-1]):
                method_name = 'search'

        # Remove all variables from the URL to keep the 'fixed' parts.
        # For instance '['{MAC}', 'vlan', '{VLAN}'] would become ['vlan']
        fixed_url = filter(is_fixed_url_part, path_suffix)
        fixed_url = map(lambda s: s.lower(), fixed_url)
        fixed_url = list(fixed_url)

        # Endpoint ID is the function name of your class.
        # It is a snake_case string ending with the method name.
        endpoint_id = "_".join(fixed_url + [method_name])

        return f'{path_prefix}|{endpoint_id}'

    def resolve_function_from_operation_id(self, operation_id):
        class_name, func_name = operation_id.split('|')
        cls = self.bindings.get(class_name)
        if cls is None:
            raise ValueError(f'endpoint handler "{class_name}" is not provided to the resolver')

        if not hasattr(cls, func_name):
            raise RuntimeError(f'class "{class_name}" does not implement required function "{func_name}"')

        return getattr(cls, func_name)
