from bson import ObjectId

from typing import List, Optional
from fastapi import FastAPI
from pydantic import BaseModel, Field
from pymongo import MongoClient

import settings

#creating a connection with MongoClient and its attributes from settings.py
client = MongoClient(settings.mongodb_URI,settings.port)
#assigning database to a variable db  
db = client['Nightfury']

app = FastAPI()


#To create a model in Pydantic library, you have to declare a class that inherits from the BaseModel class. 
#All the fields you want to validate and make part of the model must be declared as attributes.
class PyObjectId(ObjectId):
    #To use with an already created database, we’re going to create a custom validator class. 
    
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)

#Basically, we have implemented  two methods, get_validators and validate, so Pydantic knows how to deal with it.

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')

#creating channel class to store schema 
class Channel(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    #id:ObjectId()
    name: str
    description: Optional[str] = None
    members: List[str] = []
    type:str
    dp:Optional[str]
    admins:List[str] = []

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }
        