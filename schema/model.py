import datetime
import json
from enum import Enum
from typing import List, Optional, Union

import oyaml as yaml
from devtools import pprint
from pydantic import BaseModel, Schema
from pydantic.schema import schema


class ResponseType(str, Enum):
    option_data = 'option-data'
    text = 'text'
    datetime = 'datetime'
    date = 'date'
    any = 'any'


class ResponseDescription(BaseModel):
    type: ResponseType = ResponseType.any

    gt: Optional[int]
    lt: Optional[Union[int, float, datetime.datetime, datetime.date]]


ResponseDescription.update_forward_refs()


class Block(BaseModel):
    text: str = Schema(..., description='A line of text')
    href: str = Schema(None,
                       description='The path to redirect to (it also transforms the block in an option item)')
    data: str = Schema(None,
                       description='The data to be returned as the wizard step data (it makes sense only if the page is a wizard step)')
    method: str = Schema('POST', description='The method used for sending data or href')


class Page(BaseModel):
    is_form: bool = False
    name: str = Schema(..., description='Used as key for the wizard step data')
    header: str = Schema(None, description='This will be decorated by ONEm platform')
    footer: str = Schema(None, description='This will be decorated by ONEm platform')
    expected_response: ResponseDescription = Schema(ResponseDescription(),
                                                    description='The type and constraints that the expected response should respect')
    body: List[Block] = Schema(..., description='The content of a page')


class Form(BaseModel):
    is_form: bool = True
    header: str = Schema(None,
                         description='It will overridden by the page header if specified')
    footer: str = Schema(None,
                         description='It will overridden by the page header if specified')
    action: str = Schema(..., description='The url to send the form data to')
    method: str = 'POST'
    confirmation_needed: bool = False
    body: List[Page] = Schema(...,
                              description='The content of a form (a sequence of pages)')


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
        ResponseDescription,
        Block,
        Page,
        Form
    ], ref_prefix='#/components/schemas/')

    top_level_schema = json.loads(json.dumps(top_level_schema))
    file_dict['components']['schemas'] = top_level_schema['definitions']
    pprint(file_dict)
    with open('definition-v1.yaml', mode="w+") as f:
        f.write(yaml.dump(file_dict))
