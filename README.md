# ONEm Python SDK

## Installation
```bash
$ pip install onemsdk
```

## Usage example

In the following example we will show 3 different ways of creating 
a very simple **ONEm SMS app** using ONEmSDK:
1. Using a static HTML file
2. Using a template (Jinja2)
3. Using pure Python code

Our example app will display a simple menu and the SMS received by
the user will look like the one below.

```
#MY-FIRST-APP MY MENU
A First item
B Second item
C Third item
--Reply A-C
```

Note that the high level structure of each SMS is very similar with a web page:
- it starts with a **header** indicating where the SMS is coming from,
- it continues with a **body**,
- and it ends with a **footer** what the user can do next.

Before going to writing code please make sure you have an account on the
developer portal and registered an app. We will assume your app is called
**my-first-app**.

### 1. Using a static HTML file
#### 1.1. Create `menu.html` file:
```html
<section>
  <header>my menu</header>
  <ul>
    <li>
      <a href="/callback-url/item1" method="GET">First item</a>
    </li>
    <li>
      <a href="/callback-url/item2" method="GET">Second item</a>
    </li>
    <li>
      <a href="/callback-url/item3" method="POST">Third item</a>
    </li>
  </ul>
  <footer>Reply A-C</footer>
</section>
```

#### 1.2. In your request handler:
```python
from onemsdk.parser import load_html
from onemsdk.schema.v1 import Response


def handle_request(request):
    ...
    # Turn the HTML into a Python tag object
    root_tag = load_html(html_file="menu.html")

    # Turn the tag object into a Response object compatible with the JSON schema
    response = Response.from_tag(root_tag)

    # Optionally add the message_id received in request to response
    response.message_id = 'get the message id from request'

    # Jsonify the response and send it the over the wire
    return response.json()
```

### 2. Using a template (Jinja2)

#### 2.1. Create `menu.j2` file:
```jinja2
<section>
  <header>{{ header }}</header>
  <ul>
    {% for item in items %}
    <li>
      <a href="{{ item['href'] }}" 
         method="{{ item['method'] }}">
          {{ item['description'] }}
      </a>
    </li>
    {% endfor %}
  </ul>
  <footer>{{ footer }}</footer>
</section>
```

#### 2.2. In your request handler:
```python
from onemsdk.schema.v1 import Response
from onemsdk.parser import load_template


def handle_request_with_template(request):
    ...
    data = {
        'header': 'my menu',
        'footer': 'Reply A-C',
        'items': [
            {
                'method': 'GET', 
                'href': '/callback-url/item1', 
                'description': 'First item'
            },
            {
                'method': 'GET', 
                'href': '/callback-url/item2', 
                'description': 'Second item'
            },
            {
                'method': 'POST', 
                'href': '/callback-url/item3', 
                'description': 'Third item'
            },
        ]
    }
    
    # Turn the HTML template into Python object
    root_tag = load_template(template_file="menu.j2", **data)

    # Turn the tag object into a Response object compatible with the JSON schema
    response = Response.from_tag(root_tag)

    # Optionally add the message_id received in request to response
    response.message_id = 'get the message id from request'

    # Jsonify the response and send it the over the wire
    return response.json()
```

### 3. Using pure Python code

There are two possibilities of building ONEm apps using pure Python: 
- If you are more comfortable with the HTML side you can use the lower level Python
object tags located in [/onemsdk/parser/tag.py](/onemsdk/parser/tag.py), which are very 
similar with the HTML tags (eg. `FormTag`, `SectionTag`, `UlTag` etc).
- Otherwise, if you feel you are closer to the JSON schema, you can use the
higher level Python models located in [/onemsdk/schema/v1.py](/onemsdk/schema/v1.py) 
(eg. `Form`, `Menu` etc).

#### Using Python object tags
```python
from onemsdk.parser import UlTag, LiTag, ATag, ATagAttrs, SectionTag, SectionTagAttrs
from onemsdk.schema.v1 import Response


def handle_request_with_object_tags(request):
    data = {
        'header': 'my menu',
        'footer': 'Reply A-C',
        'items': [
            {
                'method': 'GET', 
                'href': '/callback-url/item1', 
                'description': 'First item'
            },
            {
                'method': 'GET', 
                'href': '/callback-url/item2', 
                'description': 'Second item'
            },
            {
                'method': 'POST', 
                'href': '/callback-url/item3', 
                'description': 'Third item'
            },
        ]
    }

    menu = UlTag(children=[
                LiTag(children=[
                    ATag(children=[item['description']],
                         attrs=ATagAttrs(href=item['href'], method=item['method']))
                ])
        for item in data['items']
    ])

    root_tag = SectionTag(
        attrs=SectionTagAttrs(header=data['header'], footer=data['footer']),
        children=[menu]
    )

    # Turn the tag object into a Response object compatible with the JSON schema
    response = Response.from_tag(root_tag)

    # Optionally add the message_id received in request to response
    response.message_id = 'get the message id from request'

    # Jsonify the response and send it the over the wire
    return response.json()
```

#### Using Python higher level objects
```python
from onemsdk.schema.v1 import Response, Menu, MenuItem, MenuItemType


def handle_request_with_object_tags(request):

    menu_items = [
        MenuItem(type=MenuItemType.option,
                 description='First item',
                 method='GET',
                 path='/callback-url/item1'),
        MenuItem(type=MenuItemType.option,
                 description='Second item',
                 method='GET',
                 path='/callback-url/item2'),
        MenuItem(type=MenuItemType.option,
                 description='Third item',
                 method='POST',
                 path='/callback-url/item3')
    ]

    menu = Menu(header='my menu', footer='Reply A-C', body=menu_items)

    # Wrap the Menu object into a Response object compatible with the JSON schema
    response = Response(content=menu)

    # Optionally add the message_id received in request to response
    response.message_id = 'get the message id from request'

    # Jsonify the response and send it the over the wire
    return response.json()
```

### Response

All the above 3 methods of creating the menu will generate the same JSON response:

```json
{
  "message_id": "get the message id from request",
  "content_type": "menu",
  "content": {
    "header": "my menu",
    "footer": "Reply A-C",
    "body": [
      {
        "type": "option",
        "description": "First item",
        "method": "GET",
        "path": "/callback-url/item1"
      },
      {
        "type": "option",
        "description": "Second item",
        "method": "GET",
        "path": "/callback-url/item2"
      },
      {
        "type": "option",
        "description": "Third item",
        "method": "POST",
        "path": "/callback-url/item3"
      }
    ],
    "type": "menu"
  }
}
```
