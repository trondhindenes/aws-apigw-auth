#!/usr/bin/env python3

from aws_cdk import aws_apigateway as apigateway
from aws_cdk import aws_lambda as lambda_
from aws_cdk import aws_lambda_python
from aws_cdk import core
from aws_cdk import core as cdk


class FastApiJwtStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        lambda_python_handler = aws_lambda_python.PythonFunction(
            self, "lambdaPythonHandler", entry="../app", index="main.py", handler="handler",
            runtime=lambda_.Runtime.PYTHON_3_9
        )

        lambda_integration = apigateway.LambdaIntegration(
            handler=lambda_python_handler,
            proxy=True

        )

        gw = apigateway.RestApi(
            self, "gw",
            default_integration=lambda_integration,
            default_method_options=apigateway.MethodOptions(
                authorization_type=apigateway.AuthorizationType.IAM,
            ),
        )
        well_known_endpoint = apigateway.Resource(
            self, "well_known_endpoint", path_part=".well-known",
            parent=gw.root,
            default_method_options=apigateway.MethodOptions(
                authorization_type=apigateway.AuthorizationType.NONE
            )
        )
        jwk_endpoint = apigateway.Resource(
            self, "jwk_endpoint", path_part="jwks.json",
            parent=well_known_endpoint
        )
        jwk_endpoint.add_method("GET")

        login_endpoint = apigateway.Resource(
            self, "login_endpoint", path_part="login",
            parent=gw.root,
        )
        login_endpoint.add_method("GET")

        gw.arn_for_execute_api


        # stuff2 = apigateway.Resource(
        #     self, "stuff2", path_part="{path}",
        #     parent=gw.root
        # )
        # stuff2.add_method("GET")
        # gw.root.add_method(http_method="GET", )


app = core.App()
FastApiJwtStack(app, "FastApiJwtStack", )
app.synth()
