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
        
        self.chromadb1 = _lambda.LayerVersion.from_layer_version_arn(
            scope,
            id="ChromaDB1Layer",
            layer_version_arn="arn:aws:lambda:us-east-2:211125768252:layer:chromadb1:1",
        )
        
        self.chromadb2 = _lambda.LayerVersion.from_layer_version_arn(
            scope,
            id="ChromaDB2Layer",
            layer_version_arn="arn:aws:lambda:us-east-2:211125768252:layer:chromadb2:1",
        )

        self.chroma_layer = _lambda.LayerVersion(
            scope,
            id='ChromaLayer',
            code=_lambda.Code.from_asset(Path.layer('layers/chroma')),
            compatible_runtimes=[_lambda.Runtime.PYTHON_3_9],
            description='',
         )
        
      
