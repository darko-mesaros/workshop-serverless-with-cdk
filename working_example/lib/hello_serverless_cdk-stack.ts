import * as cdk from '@aws-cdk/core';
import * as lambda from '@aws-cdk/aws-lambda';
import * as apigw from '@aws-cdk/aws-apigateway';
import * as dynamodb from '@aws-cdk/aws-dynamodb';

// Properties defined where we determine if this is a prod stack or not
interface EnvStackProps extends cdk.StackProps {
    prod: boolean;
}

export class HelloServerlessCdkStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: EnvStackProps) {
    super(scope, id, props);

    // The code that defines your stack goes here
    // Defining the prod or no prod
    if (props && props.prod) { // prod
      var dynamoDbReadWrite = 200;
      var apiGatewayName = 'PROD_cdk_api';
      var tableName = 'PROD_cdk_users';
      var lambdaVars = { 'TABLE_NAME': tableName};
      var concurrency = 100;
    } else { // not prod
      var tableName = 'STAGING_cdk_users';
      var apiGatewayName = 'STAGING_cdk_api';
      var dynamoDbReadWrite = 5;
      var lambdaVars = { 'TABLE_NAME': tableName};
      var concurrency = 5;
    }
    // --- dynamodb ---
    const table = new dynamodb.Table(this, 'people', {
      partitionKey: { name: 'name', type: dynamodb.AttributeType.STRING},
      tableName: tableName,
      readCapacity: dynamoDbReadWrite,
      billingMode: dynamodb.BillingMode.PROVISIONED
    });
    // --- hello lambda ---
    const welcomeLambda = new lambda.Function(this, 'HelloHandler', {
      runtime: lambda.Runtime.NODEJS_12_X,
      code: lambda.Code.fromAsset('lambda'),
      reservedConcurrentExecutions: concurrency,
      handler:'hello.handler'
    });

    // --- api gateway ---
    const api = new apigw.RestApi(this, apiGatewayName)

    // --- api gw integration ---
    const apiHelloInteg = new apigw.LambdaIntegration(welcomeLambda)
    const apiHello = api.root.addResource('hello')
    apiHello.addMethod('GET', apiHelloInteg)

    // --- read lambda ---
    const readLambda = new lambda.Function(this, 'ReadHandler', {
      runtime: lambda.Runtime.NODEJS_12_X,
      code: lambda.Code.fromAsset('lambda'),
      reservedConcurrentExecutions: concurrency,
      environment: lambdaVars,
      handler:'readUser.handler'
    });

    // --- write lambda ---
    const createLambda = new lambda.Function(this, 'CreateHandler', {
      runtime: lambda.Runtime.NODEJS_12_X,
      code: lambda.Code.fromAsset('lambda'),
      reservedConcurrentExecutions: concurrency,
      environment: lambdaVars,
      handler:'createUser.handler'
    });

    const apiReadInteg = new apigw.LambdaIntegration(readLambda)
    const apiRead = api.root.addResource('read')
    apiRead.addMethod('GET', apiReadInteg)

    const apiCreateInteg = new apigw.LambdaIntegration(createLambda)
    const apiCreate = api.root.addResource('create')
    apiCreate.addMethod('POST', apiCreateInteg)

    // --- table permissions ---
    table.grantReadData(readLambda)
    table.grantWriteData(createLambda)

  }
}
