import sys

def error_message_detail(error, error_detail: sys) -> str:
    """
    Extracts runtime tracking statistics (file name, exact execution line number, 
    and systemic error description string) from the system's execution trace.
    """
    _, _, exc_tb = error_detail.exc_info()
    
    # Defaults in case traceback context is unreachable
    file_name = "Unknown_Source_File"
    line_number = "Unknown_Line"
    
    if exc_tb is not None:
        file_name = exc_tb.tb_frame.f_code.co_filename
        line_number = exc_tb.tb_lineno

    # Compiles an explicit trace tracking message
    error_message = f"Error occurred in script: [{file_name}] at line number: [{line_number}] -> Error Message: [{str(error)}]"
    return error_message


class CustomException(Exception):
    """
    Custom Exception tracking class that wraps Python's standard error runtime 
    with enriched file and line trace statistics.
    """
    def __init__(self, error_message, error_detail: sys):
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message, error_detail=error_detail)

    def __str__(self) -> str:
        return self.error_message