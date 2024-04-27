from aws_cdk import aws_lambda as _lambda
from lambda_forge import Path


class Layers:
    def __init__(self, scope) -> None:

        self.langchain = _lambda.LayerVersion.from_layer_version_arn(
            scope,
            id="LangchainLayer",
            layer_version_arn="arn:aws:lambda:us-east-2:211125768252:layer:langchain:1",
        )
        
        self.langchain_openai = _lambda.LayerVersion.from_layer_version_arn(
            scope,
            id="LangchainOpenAILayer",
            layer_version_arn="arn:aws:lambda:us-east-2:211125768252:layer:langchain_openai:1",
        )
        
        self.chromadb = _lambda.LayerVersion.from_layer_version_arn(
            scope,
            id="ChromaDBLayer",
            layer_version_arn="arn:aws:lambda:us-east-2:211125768252:layer:chromadb:1",
        )

        self.chroma_layer = _lambda.LayerVersion(
            scope,
            id='ChromaLayer',
            code=_lambda.Code.from_asset(Path.layer('layers/chroma')),
            compatible_runtimes=[_lambda.Runtime.PYTHON_3_9],
            description='',
         )
        
        self.fast_api_layer = _lambda.LayerVersion(
            scope,
            id='FastAPILayer',
            layer_version_arn="arn:aws:lambda:us-east-2:770693421928:layer:Klayers-p39-fastapi:2",
         )
