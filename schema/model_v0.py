import json
from enum import Enum
from typing import Optional, List, Union

import oyaml as yaml
from devtools import pprint
from pydantic import BaseModel
from pydantic.schema import schema


class MenuItemType(str, Enum):
    option = 'option'
    content = 'content'


class MenuItem(BaseModel):
    type: MenuItemType
    description: str
    method: Optional[str]
    path: Optional[str]


class Menu(BaseModel):
    type = 'menu'
    header: Optional[str]
    footer: Optional[str]
    body: List[MenuItem]


class FormStepContentType(str, Enum):
    string = 'string'
    date = 'date'


class FormItemContent(BaseModel):
    type: FormStepContentType
    name: str
    description: str
    path: str
    method: str
    header: Optional[str]
    footer: Optional[str]


class FormItemMenuItem(BaseModel):
    type = 'option'
    value: str
    description: str


class FormItemMenu(Menu):
    type = 'form-menu'
    body: List[FormItemMenuItem]


class FormMeta(BaseModel):
    completion_status_show: bool = True
    completion_status_in_header: bool = True
    confirmation_needed: bool = True


class Form(BaseModel):
    type = 'form'
    header: Optional[str]
    footer: Optional[str]
    meta: Optional[FormMeta]
    method: str = 'POST'
    path: str
    body: List[Union[FormItemContent, Menu]]


begin = """
openapi: 3.0.0
info:
  version: 'v1'
  title: ''
  description: ''
paths: {}
# Added by API Auto Mocking Plugin
servers:
  - description: SwaggerHub API Auto Mocking
    url: https://virtserver.swaggerhub.com/romeo1m/schemajson/v1
components:
  schemas:
"""

if __name__ == '__main__':
    file_dict = yaml.safe_load(begin)

    top_level_schema = schema([
        MenuItem,
        Menu,
        FormItemContent,
        FormItemMenu,
        FormItemMenuItem,
        Form
    ], ref_prefix='#/components/schemas/')

    top_level_schema = json.loads(json.dumps(top_level_schema))
    file_dict['components']['schemas'] = top_level_schema['definitions']
    pprint(file_dict)
    with open('model_v0_definition-v1.yaml', mode="w+") as f:
        f.write(yaml.dump(file_dict))
