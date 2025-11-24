from pydantic import BaseModel

class Log_in_Data_validation(BaseModel):
    email:str
    password:str


class Qrdatavalidation(BaseModel):
    qr_data:str
    latitude:float
    longitude:float

class Qrdata(BaseModel):
    email:str
    qr_data:str