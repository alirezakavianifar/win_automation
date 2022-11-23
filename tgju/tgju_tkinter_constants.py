SHARED_VAR = None

def set_shared_var(value):
    global SHARED_VAR
    SHARED_VAR = value
    
def get_shared_var():
    global SHARED_VAR
    return SHARED_VAR