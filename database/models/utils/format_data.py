def mod_string(string_ibject: str) -> str:
    """Replace spaces in string with underscores"""
    string_parts = string_ibject.split(' ')
    return '_'.join(string_parts)
