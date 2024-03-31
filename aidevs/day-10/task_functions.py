from pydantic import Field, BaseModel
from requests import Response

import api_aidevs

"""
Authorize and retrieve text of the task
"""
token = api_aidevs.auth("functions")
task_json: dict = api_aidevs.get_task(token)

"""
Solution goes below
"""

fn_name_add_user = "addUser"


class AddUserSchema(BaseModel):
    """
    Add User
    """

    name: str = Field(..., description="Name")
    surname: str = Field(..., description="Surname")
    year: int = Field(..., description="year of born")


schema = AddUserSchema.model_json_schema()

openai_function = {
    "name": fn_name_add_user,
    "description": schema['description'],
    "parameters": {
        "type": schema["type"],
        "properties": schema["properties"],
    },
    "required": schema['required'],
}

"""
Sending solution of the task
"""
print("***** Sending answer *****")
response: Response = api_aidevs.send_answer(token, openai_function, debug=True)
