#!/usr/bin/env python3

from aws_cdk import core

from hello_serverless.hello_serverless_stack import HelloServerlessStack

app = core.App()

HelloServerlessStack(app, "prod",
        env=core.Environment(region="eu-west-1"),
        prod=True,
        )

HelloServerlessStack(app, "stage",
        env=core.Environment(region="eu-west-1"),
        prod=False,
        )
app.synth()
