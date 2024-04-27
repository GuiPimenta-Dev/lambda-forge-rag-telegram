# Tailoring AWS CodePipeline with CodeBuild Steps

AWS CodePipeline is a continuous integration and continuous deployment (CI/CD) tool that automates the steps required to release a new version of software. It connects directly to a GitHub repository, or other version control systems, to monitor for any changes in the codebase. Upon detecting changes, the pipeline automatically triggers a series of predefined steps that can include building the code, running tests, and deploying the code to various environments.

The CodeBuild step within the pipeline is crucial, since it is the component that actually compiles the source code, runs tests, and produces ready-to-deploy software packages. Each step ensures that only code that passes all defined quality checks and tests is moved forward in the pipeline, leading towards deployment.

## AWS CodeBuild

In AWS CodeBuild, you have the flexibility to choose from a variety of setup options for your build environment. You can opt for AWS-managed images that come pre-equipped with tools for popular development environments, utilize a custom Docker image hosted on Amazon ECR or any other registry to tailor your environment to specific requirements, or precisely orchestrate your build steps through a `buildspec.yml` file. Each method is designed to cater to diverse project needs, offering everything from convenience to extensive customization, with Docker images providing the greatest scope for personalization.

To simplify setting up CodeBuild projects, we've prepared a public Docker image hosted on ECR. This image is pre-configured with all the necessary tools and includes custom Python scripts for validation and docs generation, streamlining your workflow. You can access our optimized build environment here: [https://gallery.ecr.aws/x8r4y7j7/lambda-forge](https://gallery.ecr.aws/x8r4y7j7/lambda-forge).

In line with our commitment to transparency, the complete source code used to construct this Docker image is accessible in the following public repository: [https://github.com/GuiPimenta-Dev/lambda-forge-ecr](https://github.com/GuiPimenta-Dev/lambda-forge-ecr).

For those interested in customizing further, you're encouraged to use this image as a foundation to build your own project-specific private image. The necessary steps and configurations can be found in the Dockerfile provided below.

```Dockerfile title="Dockerfile"
FROM python:3.9-slim

WORKDIR /lambda-forge

COPY . /lambda-forge

# Install nvm with Node.js and npm
ENV NODE_VERSION=16.13.0
RUN apt-get update \
  && apt-get install -y curl jq
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
ENV NVM_DIR=/root/.nvm
RUN . "$NVM_DIR/nvm.sh" && nvm install ${NODE_VERSION}
RUN . "$NVM_DIR/nvm.sh" && nvm use v${NODE_VERSION}
RUN . "$NVM_DIR/nvm.sh" && nvm alias default v${NODE_VERSION}
ENV PATH="/root/.nvm/versions/node/v${NODE_VERSION}/bin/:${PATH}"
RUN node --version
RUN npm --version

# Install Node.js dependencies
RUN apt-get update && apt-get install -y gnupg \
  && curl -fsSL https://deb.nodesource.com/setup_14.x | bash - \
  && apt-get install -y nodejs graphviz \
  && apt-get clean && rm -rf /var/lib/apt/lists/* \
  && npm install -g aws-cdk redoc-cli cdk-dia

# Install Python dependencies
RUN pip install --upgrade pip \
  && pip install pyyaml pytest-html coverage awscli boto3==1.33.2 botocore==1.33.2 \
  && pip install -r base-requirements.txt \
  && pip install lambda-forge --extra-index-url https://pypi.org/simple --extra-index-url https://test.pypi.org/simple/ --upgrade

# Set environment variables
ENV TRACK=true
```

## Default Steps

As previously mentioned, the public image we used to create the container includes some python scripts that can be utilized as steps in your local projects. Whether you choose to use them is entirely up to you. Each step is defined in the `infra/steps/__init__.py` file.

The table below exemplifies the functionality of each step.

<!DOCTYPE html>
<html>
<head>
<style>
table {
  font-family: arial, sans-serif;
  border-collapse: collapse;
  width: 100%;
}

td, th {
border: 1px solid #dddddd;
text-align: left;
padding: 8px;
}

tr:nth-child(even) {
background-color: #dddddd;
}
</style>

</head>
<body>

<table>
  <tr>
    <th>Step</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>UnitTests</td>
    <td>Run the unit tests and fails if any test is broken</td>
  </tr>
  <tr>
    <td>Coverage</td>
    <td>Measure the coverage of the application and fails if it is below the theshold defined on the cdk.json file</td>
  </tr>
  <tr>
    <td>ValidateDocs</td>
    <td>Validates if a main.py file is missing the Input/Output dataclasses necessary to generate docs</td>
  </tr>
  <tr>
    <td>ValidateIntegrationTests</td>
    <td>Validates if for each api gateway endpoint it has at least one integration test decorated with the pytest.mark.integration decorator</td>
  </tr>
  <tr>
    <td>IntegrationTests</td>
    <td>Run the integration tests and fails if any test is broken</td>
  </tr>
  <tr>
    <td>Swagger</td>
    <td>Document the Api Gateway endpoints with Swagger based on the Input/Output dataclasses and deploy to the S3 bucket defined on the cdk.json file</td>
  </tr>
  <tr>
    <td>Redoc</td>
    <td>Document the Api Gateway endpoints with Redoc based on the Input/Output dataclasses and deploy to the S3 bucket defined on the cdk.json file</td>
  </tr>
  <tr>
    <td>Diagram</td>
    <td>Generates the AWS Architecture Diagram and deploy to the S3 bucket defined on the cdk.json file</td>
  </tr>
  <tr>
    <td>Wikis</td>
    <td>Generate Wiki pages and deploy to the S3 bucket defined on the cdk.json file</td>
  </tr>
  <tr>
    <td>TestReport</td>
    <td>Generate a test report and deploy to the S3 bucket defined on the cdk.json file</td>
  </tr>
  <tr>
    <td>CoverageReport</td>
    <td>Generate a coverage report and deploy to the S3 bucket defined on the cdk.json file</td>
  </tr>
</table>

</body>
</html>

## Custom Steps

To support extensive customization, Lambda Forge keeps track of created functions. Each time you run the `cdk synth` command, it refreshes the function list in the `cdk.json` file.

In order to prevent unnecessary cluttering of the `cdk.json` file, this feature is disabled by default. If you need to enable it for debugging purposes while creating your custom scripts, ensure to include the `TRACK=true` environment variable.

```title=".env"
TRACK=true
```

Then run the synth command:

```
cdk synth
```

You'll notice a new `functions` key within your `cdk.json` file.

```json title="cdk.json" linenums="60"
  "functions": [
            {
                "name": "SecretAuthorizer",
                "path": "./authorizers/secret",
                "description": "An authorizer to validate requests based on a secret present on the headers"
            },
            {
                "name": "HelloWorld",
                "path": "./functions/hello_world",
                "description": "A simple hello world",
                "method": "GET",
                "endpoint": "/hello_world"
            },
            {
                "name": "Private",
                "path": "./functions/private",
                "description": "A private function",
                "method": "GET",
                "endpoint": "/private"
            },
            {
                "name": "External",
                "path": "./functions/external",
                "description": "A function that uses an external library",
                "method": "GET",
                "endpoint": "/layers/external"
            },
            {
                "name": "Custom",
                "path": "./functions/custom",
                "description": "A function to make use of the custom layer",
                "method": "GET",
                "endpoint": "/layers/custom"
            }
        ]
```

This list of functions can now be leveraged to add new and tailored steps to your application.

For instance, let's create a straightforward custom script that iterates over each file described in the functions list. It will raise an error if it encounters a comment `# TODO`, thereby preventing the pipeline from proceeding if a TODO is included as a comment.

Let's create a new file at `infra/scripts/validate_todo.py`:

```python title="infra/scripts/validate_todo.py"
import json
import os

def check_functions_for_todo(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)

    functions = data.get("functions", [])

    for function in functions:
        path = function.get("path", "")
        with open(path, 'r') as file:
            if '# TODO' in file.read():
                raise ValueError(f"TODO found in file: {path}")

    print("No TODO found in any files.")

if __name__ == "__main__":
    json_file_path = "cdk.json"
    check_functions_for_todo(json_file_path)
```

In the upcoming section, we'll dive into the seamless integration of these steps into our multi-stage pipelines, unlocking a world of possibilities for streamlining our deployment processes.
