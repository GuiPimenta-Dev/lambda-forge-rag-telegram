from infra.services import Services

class QuestionConfig:
    def __init__(self, services: Services) -> None:

        function = services.aws_lambda.create_function(
            name="Question",
            path="./functions/question",
            description="Make rag questions about lforge",
            layers=[services.layers.chromadb1],
            
        )

        services.api_gateway.create_endpoint("POST", "/question", function, public=True)

            