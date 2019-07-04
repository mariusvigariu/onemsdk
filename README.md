# ONEm Python SDK

[JSON schema proposal](/schema/definition-v1.yaml)

Form example:
```json
{
  "is_form": true,
  "header": "#SETUP",
  "footer": null,
  "action": "/mydomain.xyz/myapp/form-1",
  "method": "POST",
  "confirmation_needed": false,
  "body": [
    {
      "name": "language_id",
      "header": "#SETUP LANGUAGE",
      "footer": "Reply A-B",
      "expected_response": {
        "gt": null,
        "lt": null,
        "type": "option-data"
      },
      "is_form": false,
      "body": [
        {
          "text": "Please select a language:",
          "href": null,
          "data": null,
          "method": "GET"
        },
        {
          "text": "English",
          "href": null,
          "data": "en",
          "method": "GET"
        },
        {
          "text": "French",
          "href": null,
          "data": "fr",
          "method": "GET"
        }
      ]
    },
    {
      "name": "onem-name",
      "header": "#SETUP ONEM NAME",
      "footer": "Reply text",
      "expected_response": {
        "gt": null,
        "lt": null,
        "type": "text"
      },
      "is_form": false,
      "body": [
        {
          "data": null,
          "href": null,
          "text": "Please send your ONEm name",
          "method": "GET"
        }
      ]
    }
  ]
}
```

Form example rendered:
```
// First page (wizard step)

#SETUP LANGUAGE
Please select a language:
a English
b French
--Reply A-B

// Second page (wizard step)

#SETUP ONEM NAME
Please send your ONEm name
--Reply text
```

Menu page example:
```json
{
  "name": null,
  "header": "#WALLET MCOIN",
  "footer": "Reply A-E",
  "expected_response": {
    "gt": null,
    "lt": null,
    "type": "option-data"
  },
  "is_form": false,
  "body": [
    {
      "text": "Balance: 20MCN",
      "href": null,
      "data": null,
      "method": "GET"
    },
    {
      "text": "Escrow: +0/-0",
      "href": null,
      "data": null,
      "method": "GET"
    },
    {
      "data": null,
      "href": "/myapp/form-4",
      "text": "Send",
      "method": "GET"
    },
    {
      "data": null,
      "href": "/myapp/menu-4",
      "text": "Escrow(0)",
      "method": "GET"
    },
    {
      "data": null,
      "href": "/myapp/menu-5",
      "text": "Transactions(3)",
      "method": "GET"
    },
    {
      "data": null,
      "href": "/myapp/menu-7",
      "text": "My address",
      "method": "GET"
    },
    {
      "text": "Change account",
      "href": "/myapp/form-5",
      "data": null,
      "method": "GET"
    }
  ]
}
```

Menu page example rendered:

```
#WALLET MCOIN
Balance: 20MCN
Escrow: +0/-0
a Send
b Escrow(0)
c Transactions(3)
d My address
e Change account
--Reply A-E
```
