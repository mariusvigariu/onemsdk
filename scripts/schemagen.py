import json
import os
from os.path import dirname, abspath

import oyaml as yaml
from pydantic.schema import schema

from onemsdk.schema.v1 import (
    MenuItem, Menu, FormItem, MenuItemFormItem, Form, Response
)

BASE_DIR: str = dirname(dirname(abspath(__file__)))

with open(BASE_DIR + '/OPENAPI_SCHEMA_VERSION') as f:
    OPENAPI_SCHEMA_VERSION = f.read()

begin = f"""
openapi: 3.0.0
info:
  version: v{OPENAPI_SCHEMA_VERSION}
  title: 'ONEm JSON response schema'
  description: ''
paths: {{}}
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
        FormItem,
        MenuItemFormItem,
        Form,
        Response,
    ], ref_prefix='#/components/schemas/')

    top_level_schema = json.loads(json.dumps(top_level_schema))
    file_dict['components']['schemas'] = top_level_schema['definitions']
    file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'schema.yaml')
    with open(file, mode="w+") as f:
        f.write(yaml.dump(file_dict))
