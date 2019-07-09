# ONEm Python SDK

## Installation
```bash
$ pip install git+https://github.com/romeo1m/onemsdk.git
```

## Usage example
0. Create a ONEm app in developer portal (eg "MY-FIRST-APP")
1. Create `menu.html` file and fill it with:
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
  <footer>my footer</footer>
</section>
```
2. In your request handler
```python
import json

from onemsdk.schema.v1 import create_response, load_html


def handle_request(request):
    ...
    tag = load_html(html_file="menu.html")
    return json.dumps(create_response(tag))
```
3. The response will be a JSON:
```json
{
  "header": "my menu",
  "footer": "my footer",
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
```
4. The user will receive an SMS similar with:
```
#MY-FIRST-APP MY MENU
a First item
b Second item
c Third item
--My footer
```