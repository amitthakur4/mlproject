import sys  #whaever the error is sys library will have everything 
from src.logger import logging

# Set the logger level to INFO
#logging.setLevel(logging.INFO)

def error_msg_detail(error, error_detail:sys):
    _ , _, exe_tb = error_detail.exc_info()  #it return 3 things we are intersted in 3rd
    file_name = exe_tb.tb_frame.f_code.co_filename
    error_message = f"Error has been occured in scrip name {file_name} line no {exe_tb.tb_lineno} and error msg {str(error)}"
    
    return error_message

class CustomException(Exception):
    def __init__(self, error_message, error_detail:sys):
        super().__init__(error_message)
        self.error_message = error_msg_detail(error_message, error_detail=error_detail)

    def __str__(self) -> str:
        return self.error_message
    

# if __name__ == "__main__":
#     try:
#         a= 1/0
#     except Exception as e:
#         logging.info("Error has been occured")
#         raise CustomException(e , sys)

