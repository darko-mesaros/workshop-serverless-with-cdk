from aws_cdk import (
        aws_lambda as _lambda,
        aws_apigateway as apigw,
        aws_dynamodb as dynamodb,
        core
        )

class HelloServerlessStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, prod: bool,  **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # The code that defines your stack goes here
        if prod:
            dynamodb_read_write_cap = 200
            api_gw_name = "PROD_CDK_API"
            table_name = "PROD_CDK_USERS"
            concurrency = 100
        else:
            dynamodb_read_write_cap = 5
            api_gw_name = "STAGE_CDK_API"
            table_name = "STAGE_CDK_USERS"
            concurrency = 5 

        # --- dynamodb ---
        table = dynamodb.Table(
                self, "people",
                partition_key = dynamodb.Attribute(name="name", type=dynamodb.AttributeType.STRING),
                table_name = table_name,
                read_capacity = dynamodb_read_write_cap,
                billing_mode = dynamodb.BillingMode.PROVISIONED,
                )
        # --- api gateway ---
        api = apigw.RestApi(self, "the_api")

        # --- lambdas ---
        ## Hello World Lambda
        hello_lambda = _lambda.Function(
                self, "hello_lambda",
                runtime = _lambda.Runtime.PYTHON_3_8,
                code= _lambda.Code.from_asset("lambda"),
                handler = "hello.handler",
                environment={"table":table.table_name},
                )
        hello_integ = apigw.LambdaIntegration(hello_lambda)
        api_hello = api.root.add_resource("hello")
        api_hello.add_method("GET", hello_integ)

        ## Create User Lambda
        create_lambda = _lambda.Function(
                self, "create_lambda",
                runtime = _lambda.Runtime.PYTHON_3_8,
                code= _lambda.Code.from_asset("lambda"),
                handler = "create.handler",
                environment={"table":table.table_name},
                )
        create_integ = apigw.LambdaIntegration(create_lambda)
        api_create = api.root.add_resource("create")
        api_create.add_method("POST", create_integ)

        ## Read User Lambda
        read_lambda = _lambda.Function(
                self, "read_lambda",
                runtime = _lambda.Runtime.PYTHON_3_8,
                code= _lambda.Code.from_asset("lambda"),
                handler = "read.handler",
                environment={"table":table.table_name},
                )
        read_integ = apigw.LambdaIntegration(read_lambda)
        api_read = api.root.add_resource("read")
        api_read.add_method("GET", read_integ)

        # --- table permissions ---
        table.grant_read_data(read_lambda)
        table.grant_read_write_data(create_lambda)
