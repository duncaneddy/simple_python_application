'''The models module contains data types and models that structure the API
methods and respones.
'''
import enum
import pydantic

class Department(enum.Enum):
    aeroastro = "Aero/Astro"
    cs = "Computer Science"
    ee = "Electrical Engineering"

class LabMember(pydantic.BaseModel):
    first: str = pydantic.Schema(..., description='First Name')
    last: str = pydantic.Schema(..., description='Last Name')
    year: int = pydantic.Schema(1, description='Years in program.')
    department: Department = pydantic.Schema('Aero/Astro', description='Student Department')

class ApplicationSecret(pydantic.BaseModel):
    secret: str = pydantic.Schema('CHANGE-ME', description='Application Secret')