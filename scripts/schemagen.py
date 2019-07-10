import json
import os

import oyaml as yaml
from pydantic.schema import schema

from onemsdk.schema.v1.component import MenuItem, Menu, FormItemContent, FormItemMenu, \
    FormItemMenuItem, Form, Response

begin = """
openapi: 3.0.0
info:
  version: 'm1'
  title: 'ONEm JSON response schema'
  description: ''
paths: {}
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
        Form,
        Response,
    ], ref_prefix='#/components/schemas/')

    top_level_schema = json.loads(json.dumps(top_level_schema))
    file_dict['components']['schemas'] = top_level_schema['definitions']
    file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'schema.yaml')
    with open(file, mode="w+") as f:
        f.write(yaml.dump(file_dict))
