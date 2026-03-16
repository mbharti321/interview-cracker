# user
# name, email, phone

# api takes name, email and phone number as parameter





from pydantic import BaseModel, Field


# Base = BaseModel()

class User(BaseModel):
    # user name, email, phone
    name: str = Field(required = True)
    email: str = Field(required = True)
    phone: str
    

my_user = User("Manish", "mbhart@hmai.com", "9955263333")

