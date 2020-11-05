#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from '@aws-cdk/core';
import { HelloServerlessCdkStack } from '../lib/hello_serverless_cdk-stack';

const app = new cdk.App();
new HelloServerlessCdkStack(app, 'prod',{
  prod: true,
  env: { 
    region: 'eu-west-1'
  }
});

new HelloServerlessCdkStack(app, 'staging',{
  prod: false,
  env: { 
    region: 'eu-west-1'
  }
});
