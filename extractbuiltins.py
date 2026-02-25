# Code to assist syntax highlight by adding all callables to list

__version__ = "Blueconda Usage Only" # Used to indicate that this lib is ONLY FOR USE WITHIN Blueconda

def listfunctions():
    def merge_unique(list1, list2): # USed to combine keyword.kwlist and extracted functions
        """
        Merges two lists while removing duplicates.

        Args:
            list1: The first list.
            list2: The second list.

        Returns:
            A new list containing the unique elements from both lists.
        """
        # Combine lists and convert to a set to remove duplicates
        unique_elements = set(list1 + list2)
        # Convert the set back to a list
        return list(unique_elements)

    import builtins # All python callable builtin functions
    from keyword import kwlist  # List with all keywords within

    # Get all attributes from builtins
    all_attributes = dir(builtins)

    # Filter functions based on their names starting with a lowercase letter
    functions1 = [attr for attr in all_attributes if callable(getattr(builtins, attr)) and not attr.startswith("__")]

    functions = merge_unique(functions1, kwlist)
    # Print the list of function names
    return functions

# Test code (Uncomment when testing)
#list = listfunctions()
#print(list)

