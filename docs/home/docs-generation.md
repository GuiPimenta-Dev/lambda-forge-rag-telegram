# Generating Docs

Lambda Forge excels not only in structuring Lambda functions for scalability but also in facilitating the automatic documentation of key project components. It simplifies the deployment of documents to the cloud, making them readily accessible via API Gateway.

Documentation is seamlessly generated through the `generate_docs` step in CodePipeline and is then deployed to the S3 Bucket defined within your `cdk.json` file. This automated process ensures your project's documentation is always up-to-date and easily accessible.

## API Documentation with Swagger and ReDoc

An API document is a technical resource that provides instructions on how to effectively use and integrate with an API. It includes information about the API's functions, classes, return types, arguments, and more, as well as examples of requests and responses. Good API documentation is critical for developers to understand how to make calls to the API and what results they can expect.

To automatically document your api endpoints with Swagger and Redoc, you should include the `Input` and `Output` dataclasses inside your `main.py` files. Case you have an endpoint that's expecting a path parameter, you can also include it in the `Path` dataclass.

The code snippet below demonstrates all the types of data you can expect to work with, including simple data types, lists, custom objects, optional fields, and literal types, offering a clear understanding of the input and output contracts for the API.

```python
from dataclasses import dataclass
from typing import List, Optional, Literal

# Define a dataclass for path parameters, useful for API endpoints requiring parameters within the URL path.
@dataclass
class Path:
    id: str

# A custom object class that represents a complex type with multiple fields.
@dataclass
class Object:
    a_string: str
    an_int: int

# The input data class represents the expected structure of the request payload.
@dataclass
class Input:
    a_string: str  # A simple string input
    an_int: int  # A simple integer input
    a_boolean: bool  # A boolean value
    a_list: List[str]  # A list of strings
    an_object: Object  # An instance of the custom 'Object' class defined above
    a_list_of_object: List[Object]  # A list containing instances of 'Object'
    a_literal: Literal["a", "b", "c"]  # A literal type, restricting values to 'a', 'b', or 'c'
    an_optional: Optional[str]  # An optional string, which can be either a string or None

# The output data class represents the endpoint's output.
@dataclass
class Output:
    pass # No fields are defined, implying the output is empty.
```

## Setting Up the Docs Endpoints

The endpoints to visualize your docs are configured within `docs/config.py`. This configuration file allows you to specify the types of documents to be displayed and their presentation locations.

Similar to functions, **authorizers can be implemented to safeguard the access to your project's documentation**, maintaining its confidentiality and integrity.

```python title="docs/config.py"
from infra.services import Services

class DocsConfig:
    def __init__(self, services: Services) -> None:
        # Public Swagger at /swagger
        services.api_gateway.create_docs(endpoint="/swagger", artifact="swagger", public=True)

        # Private Swagger at /swagger
        services.api_gateway.create_docs(endpoint="/private/swagger", artifact="swagger", authorizer="secret")

        # Redoc at /redoc
        services.api_gateway.create_docs(endpoint="/redoc", artifact="redoc", public=True)

        # Architecture Diagram at /diagram
        services.api_gateway.create_docs(endpoint="/diagram", artifact="diagram", public=True)

        # Tests Report at /tests
        services.api_gateway.create_docs(endpoint="/tests", artifact="tests", public=True)

        # Coverage Report at /coverage
        services.api_gateway.create_docs(endpoint="/coverage", artifact="coverage", public=True)

        # Page1 Wiki at /page1
        # Use the Wiki's title as artifact
        services.api_gateway.create_docs(endpoint="/page1", artifact="Page1", public=True)

        # Page2 Wiki at /page2
        # Use the Wiki's title as artifact
        services.api_gateway.create_docs(endpoint="/page2", artifact="Page2", public=True)
```

## Available Docs

- Swagger: [https://8kwcovaj0f.execute-api.us-east-2.amazonaws.com/staging/docs](https://8kwcovaj0f.execute-api.us-east-2.amazonaws.com/staging/docs)
- Redoc: [https://8kwcovaj0f.execute-api.us-east-2.amazonaws.com/staging/docs/redoc](https://8kwcovaj0f.execute-api.us-east-2.amazonaws.com/staging/docs/redoc)
- Diagram: [https://0muz5hqwf0.execute-api.us-east-2.amazonaws.com/dev/diagram](https://0muz5hqwf0.execute-api.us-east-2.amazonaws.com/dev/diagram)
- Tests: [https://0muz5hqwf0.execute-api.us-east-2.amazonaws.com/dev/tests](https://0muz5hqwf0.execute-api.us-east-2.amazonaws.com/dev/tests)
- Coverage: [https://0muz5hqwf0.execute-api.us-east-2.amazonaws.com/dev/coverage](https://0muz5hqwf0.execute-api.us-east-2.amazonaws.com/dev/coverage)
- Page 1: [https://0muz5hqwf0.execute-api.us-east-2.amazonaws.com/dev/page1](https://0muz5hqwf0.execute-api.us-east-2.amazonaws.com/dev/page1)
- Page 2: [https://0muz5hqwf0.execute-api.us-east-2.amazonaws.com/dev/page2](https://0muz5hqwf0.execute-api.us-east-2.amazonaws.com/dev/page2)
