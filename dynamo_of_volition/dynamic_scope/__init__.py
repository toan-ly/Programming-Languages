from typing import Dict, Any, Iterator, Optional
from collections import abc
from types import FunctionType
import inspect


class DynamicScope(abc.Mapping):
    '''
    A class to simulate dynamic scoping by capturing variables from the call stack.
    Inherits from collections.abc.Mapping to provide dictionary-like behavior.
    '''
    def __init__(self):
        '''
        Initialize DynamicScope with empty environment dictionary to store variable
        names as key and their corresponding values.

        '''
        self.env: Dict[str, Optional[Any]] = {}

    def __getitem__(self, key: str) -> Optional[Any]:
        '''
        Retrieve value of a variable from the environment.
        Raises NameError if variable is not defined.
        Raises UnboundLocalError if variable is unbound.
        
        Parameters:
        key (str): Variable name to retrieve.
        
        Returns:
        Optional[Any]: Value of the variable.
        '''
        if key not in self.env:
            raise NameError(f"Name '{key}' is not defined.")
        elif self.env[key] == '__unbound__':
            raise UnboundLocalError(f"Local variable '{key}' referenced before assignment.")
        return self.env[key]
    
    def __setitem__(self, key: str, value: Optional[Any]) -> None:
        '''
        Set value of a variable in the environment if it does not exist.

        Parameters:
        key (str): Variable name to set.
        value (Optional[Any]): Value of variable to assign.
        '''
        if key not in self.env:
            self.env[key] = value
        
    def __iter__(self) -> Iterator[str]:
        '''
        Return an iterator over the variable names in the environment.

        Returns:
        Iterator[str]: An iterator over variable names.
        '''
        return self.env.__iter__()
    
    def __len__(self) -> int:
        '''
        Return the number of variables in the environment.

        Returns:
        int: Number of variables.
        '''
        return len(self.env)


def get_dynamic_re() -> DynamicScope:
    '''
    Create DynamicScope instance and populate it with local variables from
    the current call stack.
    
    Returns:
    DynamicScope: Populated DynamicScope instance.
    '''
    scope = DynamicScope()
    stack = inspect.stack() # Get current call stack

    # Iterate through each frame in the call stack, excluding the current frame
    for frame_info in stack[1:]:
        frame = frame_info.frame # Frame object from the stakc frame info
        local_vars = frame.f_locals # Local variables in the frame
        free_vars = frame.f_code.co_freevars # Free variables in the frame
        all_vars = frame.f_code.co_cellvars + frame.f_code.co_varnames # All declared variables

        # Add local variables to the dynamic scope
        for var in local_vars:
            if var not in scope.env and var not in free_vars:
                scope.env[var] = local_vars[var]

        # Add unbound variables to the dynamic scope
        for var in all_vars:
            if var not in scope.env and var not in local_vars:
                scope.env[var] = '__unbound__'
        
    return scope


