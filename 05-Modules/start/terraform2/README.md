


## REFERENCE: https://spacelift.io/blog/terraform-api-gateway
## REFERENCE: https://stackoverflow.com/questions/39040739/in-terraform-how-do-you-specify-an-api-gateway-endpoint-with-a-variable-in-the
## REFERENCE, COMPLEMENTARY: flask app in lambda using AWS CDK: https://www.cloudtechsimplified.com/run-python-flask-in-aws-lambda/

## OVERVIEW

Importing resources into this terraform2 folder
Resources where created from AWS tutorial and expanded
Then, resources were imported one by one by updating the terraform code.
Below discussed step-by-step 


Started with files from chapter4/done:
* providers.tf

* vars.tf
* locals.tf
* 00_input.tfvars
* account.tf
* outputs.tf

* dynamodb.tf
* lambda.tf
* api_gateway.tf


The following resources already exist:
* dynamodb
* lambda (python)
* API Gateway with helloworld at stage:test


## FORCE REPLACEMENT (PREVIOUSLY KNOWN AS TAINTING)

Lambda needs to be forced-deploy to pick up the latest cahnges:

* tf state list
* tfapply -replace=aws_lambda_function.api_lambda
* You might need to delete the lmabda from the console and run "tf apply" twice!!!
* ACTUALLY this article is a clever wait to automatically update lambda when the zip content changes: https://www.linkedin.com/pulse/lambda-terraform-deploy-only-when-project-changed-cussa-de-souza


## IMPORTING


export TF_VAR_LOCAL_AWS_PROFILE=confoo
terraform init

terraform import -var-file="00_input.tfvars" aws_dynamodb_table.dynamodb_table dynamodb-extlambdaapigw

terraform import -var-file="00_input.tfvars" aws_lambda_function.api_lambda GetStartedLambdaProxyIntegration

terraform import -var-file="00_input.tfvars" aws_api_gateway_rest_api.my_gateway jeai60f6hc

##WRONG: terraform import -var-file="00_input.tfvars" aws_api_gateway_resource.root jeai60f6hc/1t7mc66k1j
terraform import -var-file="00_input.tfvars" aws_api_gateway_resource.root jeai60f6hc/kvxesw

    Get deploymentId (The latest) using:
    aws apigateway get-deployments --rest-api-id jeai60f6hc

terraform import -var-file="00_input.tfvars" aws_api_gateway_deployment.my_gateway jeai60f6hc/66cf13

terraform import -var-file="00_input.tfvars" aws_api_gateway_stage.gw_stage_name jeai60f6hc/test

STEPS:
aws_api_gateway_rest_api.my_gateway
aws_api_gateway_resource.root
aws_api_gateway_deployment.my_gateway
aws_api_gateway_stage.gw_stage_name
aws_api_gateway_method.proxy
aws_api_gateway_integration.lambda_integration
aws_api_gateway_method_response.proxy
aws_api_gateway_integration_response.reponse_integration
##aws_lambda_permission.apigw_lambda
##aws_iam_role_policy_attachment.lambda_basic

terraform import -var-file="00_input.tfvars" aws_api_gateway_method.proxy jeai60f6hc/kvxesw/ANY

terraform import -var-file="00_input.tfvars" aws_api_gateway_integration.lambda_integration jeai60f6hc/kvxesw/ANY
##WRONG terraform import -var-file="00_input.tfvars" aws_api_gateway_integration.lambda_integration jeai60f6hc/1t7mc66k1j/ANY

terraform import -var-file="00_input.tfvars" aws_api_gateway_method_response.proxy jeai60f6hc/kvxesw/ANY/200

terraform import -var-file="00_input.tfvars" aws_api_gateway_integration_response.reponse_integration jeai60f6hc/kvxesw/ANY/200

terraform import -var-file="00_input.tfvars" aws_api_gateway_resource.path_health jeai60f6hc/okzztd
terraform import -var-file="00_input.tfvars" aws_api_gateway_resource.path_info jeai60f6hc/c4r18p
terraform import -var-file="00_input.tfvars" aws_api_gateway_resource.path_sleep1 jeai60f6hc/a39crv
terraform import -var-file="00_input.tfvars" aws_api_gateway_resource.path_sleep5 jeai60f6hc/3szzgg
terraform import -var-file="00_input.tfvars" aws_api_gateway_resource.path_toc jeai60f6hc/7zl30q
terraform import -var-file="00_input.tfvars" aws_api_gateway_resource.path_delay jeai60f6hc/oca7dv


terraform import -var-file="00_input.tfvars" aws_api_gateway_method.proxy_delay jeai60f6hc/oca7dv/GET
terraform import -var-file="00_input.tfvars" aws_api_gateway_integration.lambda_integration_delay jeai60f6hc/oca7dv/GET
terraform import -var-file="00_input.tfvars" aws_api_gateway_method_response.proxy_delay jeai60f6hc/oca7dv/GET/200
terraform import -var-file="00_input.tfvars" aws_api_gateway_integration_response.reponse_integration_delay jeai60f6hc/oca7dv/GET/200

terraform import -var-file="00_input.tfvars" aws_api_gateway_method.proxy_health jeai60f6hc/okzztd/GET
terraform import -var-file="00_input.tfvars" aws_api_gateway_integration.lambda_integration_health jeai60f6hc/okzztd/GET
terraform import -var-file="00_input.tfvars" aws_api_gateway_method_response.proxy_health jeai60f6hc/okzztd/GET/200
terraform import -var-file="00_input.tfvars" aws_api_gateway_integration_response.reponse_integration_health jeai60f6hc/okzztd/GET/200

terraform import -var-file="00_input.tfvars" aws_api_gateway_method.proxy_info jeai60f6hc/c4r18p/GET
terraform import -var-file="00_input.tfvars" aws_api_gateway_integration.lambda_integration_info jeai60f6hc/c4r18p/GET
terraform import -var-file="00_input.tfvars" aws_api_gateway_method_response.proxy_info jeai60f6hc/c4r18p/GET/200
terraform import -var-file="00_input.tfvars" aws_api_gateway_integration_response.reponse_integration_info jeai60f6hc/c4r18p/GET/200

terraform import -var-file="00_input.tfvars" aws_api_gateway_method.proxy_sleep1 jeai60f6hc/a39crv/GET
terraform import -var-file="00_input.tfvars" aws_api_gateway_integration.lambda_integration_sleep1 jeai60f6hc/a39crv/GET
terraform import -var-file="00_input.tfvars" aws_api_gateway_method_response.proxy_sleep1 jeai60f6hc/a39crv/GET/200
terraform import -var-file="00_input.tfvars" aws_api_gateway_integration_response.reponse_integration_sleep1 jeai60f6hc/a39crv/GET/200

terraform import -var-file="00_input.tfvars" aws_api_gateway_method.proxy_sleep5 jeai60f6hc/3szzgg/GET
terraform import -var-file="00_input.tfvars" aws_api_gateway_integration.lambda_integration_sleep5 jeai60f6hc/3szzgg/GET
terraform import -var-file="00_input.tfvars" aws_api_gateway_method_response.proxy_sleep5 jeai60f6hc/3szzgg/GET/200
terraform import -var-file="00_input.tfvars" aws_api_gateway_integration_response.reponse_integration_sleep5 jeai60f6hc/3szzgg/GET/200

terraform import -var-file="00_input.tfvars" aws_api_gateway_method.proxy_toc jeai60f6hc/7zl30q/GET
terraform import -var-file="00_input.tfvars" aws_api_gateway_integration.lambda_integration_toc jeai60f6hc/7zl30q/GET
terraform import -var-file="00_input.tfvars" aws_api_gateway_method_response.proxy_toc jeai60f6hc/7zl30q/GET/200
terraform import -var-file="00_input.tfvars" aws_api_gateway_integration_response.reponse_integration_toc jeai60f6hc/7zl30q/GET/200


##terraform import -var-file="00_input.tfvars" aws_lambda_permission.apigw_lambda GetStartedLambdaProxyIntegration/AllowExecutionFromAPIGateway
##terraform import -var-file="00_input.tfvars" aws_iam_role_policy_attachment.lambda_basic
##SAMPLE: % terraform import aws_iam_role_policy_attachment.test-attach test-role/arn:aws:iam::xxxxxxxxxxxx:policy/test-policy


Remark:
4. As we saw in 3: Click-Ops, creating an API Gateway is involved.

   - We need to create the 4 pieces: a method, an integration, a method response, and an integration response.
   - We need to create the deployment and the root resource.
   - We need to create a policy and either reference a built-in role or create a new role.
   - We need to give the API Gateway permission to call the Lambda.

ALIGNING RESOURCES ONE-BY-ONE

tfplan -target=aws_dynamodb_table.dynamodb_table

tfrun -target=aws_api_gateway_rest_api.my_gateway

tfrun -target=aws_api_gateway_integration_response.reponse_integration_sleep1






REMOVE operation
* terraform state list
* terraform state rm <name>



ORIGINAL
/
  /api
    GET


API id jeai60f6hc
deployment id 66cf13 <==== stage::default
/               <=== id 1t7mc66k1j
  /helloworld   <=== id kvxesw
    /delay oca7dv
    /health okzztd
    /info c4r18p
    /sleep1  a39crv
    /sleep5  3szzgg
    /toc  7zl30q
  /items  hqvdcs
    /{id}  dy7q11

NOVELTY
/
  /helloworld
    ANY
    /health
      GET
    /info
      GET
    /toc
      GET
    /sleep5
      GET
    /sleep1
      GET
    /delay
      GET
  /items
    GET
    PUT
    POST
    /{id}
      GET
      DELETE


Manula populate via PUT

```
{
    "id": "99",
    "price": 789,
    "name": "mars"
}
```

## OUTPUTS


==== DYNAMODB

cmosquer@CMOSQUER-M-Q4XC terraform2 % terraform import -var-file="00_input.tfvars" aws_dynamodb_table.dynamodb_table dynamodb-extlambdaapigw 
aws_dynamodb_table.dynamodb_table: Importing from ID "dynamodb-extlambdaapigw"...
data.aws_region.current: Reading...
data.aws_caller_identity.current: Reading...
aws_dynamodb_table.dynamodb_table: Import prepared!
  Prepared aws_dynamodb_table for import
aws_dynamodb_table.dynamodb_table: Refreshing state... [id=dynamodb-extlambdaapigw]
data.aws_region.current: Read complete after 0s [id=us-west-2]
data.aws_caller_identity.current: Read complete after 0s [id=924300192870]

Import successful!

The resources that were imported are shown above. These resources are now in
your Terraform state and will henceforth be managed by Terraform.

cmosquer@CMOSQUER-M-Q4XC terraform2 % 



==== LAMBDA

cmosquer@CMOSQUER-M-Q4XC terraform2 % terraform import -var-file="00_input.tfvars" aws_lambda_function.api_lambda GetStartedLambdaProxyIntegration
aws_lambda_function.api_lambda: Importing from ID "GetStartedLambdaProxyIntegration"...
data.aws_region.current: Reading...
data.aws_caller_identity.current: Reading...
aws_lambda_function.api_lambda: Import prepared!
  Prepared aws_lambda_function for import
aws_lambda_function.api_lambda: Refreshing state... [id=GetStartedLambdaProxyIntegration]
data.aws_region.current: Read complete after 0s [id=us-west-2]
data.aws_caller_identity.current: Read complete after 0s [id=924300192870]

Import successful!

The resources that were imported are shown above. These resources are now in
your Terraform state and will henceforth be managed by Terraform.

cmosquer@CMOSQUER-M-Q4XC terraform2 % 




==== APIGW

cmosquer@CMOSQUER-M-Q4XC terraform2 % terraform import -var-file="00_input.tfvars" aws_api_gateway_rest_api.my_gateway jeai60f6hc
aws_api_gateway_rest_api.my_gateway: Importing from ID "jeai60f6hc"...
data.aws_caller_identity.current: Reading...
data.aws_region.current: Reading...
aws_api_gateway_rest_api.my_gateway: Import prepared!
  Prepared aws_api_gateway_rest_api for import
aws_api_gateway_rest_api.my_gateway: Refreshing state... [id=jeai60f6hc]
data.aws_region.current: Read complete after 0s [id=us-west-2]
data.aws_caller_identity.current: Read complete after 0s [id=924300192870]

Import successful!

The resources that were imported are shown above. These resources are now in
your Terraform state and will henceforth be managed by Terraform.

cmosquer@CMOSQUER-M-Q4XC terraform2 % 

==== 

cmosquer@CMOSQUER-M-Q4XC terraform2 % terraform import -var-file="00_input.tfvars" aws_api_gateway_resource.root jeai60f6hc/kvxesw
data.aws_region.current: Reading...
data.aws_caller_identity.current: Reading...
aws_api_gateway_resource.root: Importing from ID "jeai60f6hc/kvxesw"...
data.aws_region.current: Read complete after 0s [id=us-west-2]
aws_api_gateway_resource.root: Import prepared!
  Prepared aws_api_gateway_resource for import
aws_api_gateway_resource.root: Refreshing state... [id=kvxesw]
data.aws_caller_identity.current: Read complete after 0s [id=924300192870]

Import successful!

The resources that were imported are shown above. These resources are now in
your Terraform state and will henceforth be managed by Terraform.

====

cmosquer@CMOSQUER-M-Q4XC terraform2 % terraform import -var-file="00_input.tfvars" aws_api_gateway_deployment.my_gateway jeai60f6hc/66cf13
data.aws_region.current: Reading...
data.aws_caller_identity.current: Reading...
data.aws_region.current: Read complete after 0s [id=us-west-2]
aws_api_gateway_deployment.my_gateway: Importing from ID "jeai60f6hc/66cf13"...
aws_api_gateway_deployment.my_gateway: Import prepared!
  Prepared aws_api_gateway_deployment for import
aws_api_gateway_deployment.my_gateway: Refreshing state... [id=66cf13]
data.aws_caller_identity.current: Read complete after 0s [id=924300192870]

Import successful!

The resources that were imported are shown above. These resources are now in
your Terraform state and will henceforth be managed by Terraform.

====

cmosquer@CMOSQUER-M-Q4XC terraform2 % terraform import -var-file="00_input.tfvars" aws_api_gateway_stage.gw_stage_name jeai60f6hc/test
data.aws_caller_identity.current: Reading...
data.aws_region.current: Reading...
data.aws_region.current: Read complete after 0s [id=us-west-2]
aws_api_gateway_stage.gw_stage_name: Importing from ID "jeai60f6hc/test"...
aws_api_gateway_stage.gw_stage_name: Import prepared!
  Prepared aws_api_gateway_stage for import
aws_api_gateway_stage.gw_stage_name: Refreshing state... [id=ags-jeai60f6hc-test]
data.aws_caller_identity.current: Read complete after 0s [id=924300192870]

Import successful!

The resources that were imported are shown above. These resources are now in
your Terraform state and will henceforth be managed by Terraform.

====

cmosquer@CMOSQUER-M-Q4XC terraform2 % terraform import -var-file="00_input.tfvars" aws_api_gateway_method.proxy jeai60f6hc/kvxesw/ANY
data.aws_caller_identity.current: Reading...
data.aws_region.current: Reading...
data.aws_region.current: Read complete after 0s [id=us-west-2]
aws_api_gateway_method.proxy: Importing from ID "jeai60f6hc/kvxesw/ANY"...
aws_api_gateway_method.proxy: Import prepared!
  Prepared aws_api_gateway_method for import
aws_api_gateway_method.proxy: Refreshing state... [id=agm-jeai60f6hc-kvxesw-ANY]
data.aws_caller_identity.current: Read complete after 0s [id=924300192870]

Import successful!

The resources that were imported are shown above. These resources are now in
your Terraform state and will henceforth be managed by Terraform.

====

cmosquer@CMOSQUER-M-Q4XC terraform2 % terraform import -var-file="00_input.tfvars" aws_api_gateway_integration.lambda_integration jeai60f6hc/kvxesw/ANY
data.aws_caller_identity.current: Reading...
data.aws_region.current: Reading...
data.aws_region.current: Read complete after 0s [id=us-west-2]
aws_api_gateway_integration.lambda_integration: Importing from ID "jeai60f6hc/kvxesw/ANY"...
aws_api_gateway_integration.lambda_integration: Import prepared!
  Prepared aws_api_gateway_integration for import
aws_api_gateway_integration.lambda_integration: Refreshing state... [id=agi-jeai60f6hc-kvxesw-ANY]
data.aws_caller_identity.current: Read complete after 0s [id=924300192870]

Import successful!

The resources that were imported are shown above. These resources are now in
your Terraform state and will henceforth be managed by Terraform.


====

cmosquer@CMOSQUER-M-Q4XC terraform2 % terraform import -var-file="00_input.tfvars" aws_api_gateway_method_response.proxy jeai60f6hc/kvxesw/ANY/200
data.aws_region.current: Reading...
data.aws_caller_identity.current: Reading...
data.aws_region.current: Read complete after 0s [id=us-west-2]
aws_api_gateway_method_response.proxy: Importing from ID "jeai60f6hc/kvxesw/ANY/200"...
aws_api_gateway_method_response.proxy: Import prepared!
  Prepared aws_api_gateway_method_response for import
aws_api_gateway_method_response.proxy: Refreshing state... [id=agmr-jeai60f6hc-kvxesw-ANY-200]
data.aws_caller_identity.current: Read complete after 1s [id=924300192870]

Import successful!

The resources that were imported are shown above. These resources are now in
your Terraform state and will henceforth be managed by Terraform.

====

cmosquer@CMOSQUER-M-Q4XC terraform2 % terraform import -var-file="00_input.tfvars" aws_api_gateway_integration_response.reponse_integration jeai60f6hc/kvxesw/ANY/200
data.aws_caller_identity.current: Reading...
data.aws_region.current: Reading...
data.aws_region.current: Read complete after 0s [id=us-west-2]
aws_api_gateway_integration_response.reponse_integration: Importing from ID "jeai60f6hc/kvxesw/ANY/200"...
aws_api_gateway_integration_response.reponse_integration: Import prepared!
  Prepared aws_api_gateway_integration_response for import
aws_api_gateway_integration_response.reponse_integration: Refreshing state... [id=agir-jeai60f6hc-kvxesw-ANY-200]
data.aws_caller_identity.current: Read complete after 0s [id=924300192870]

Import successful!

The resources that were imported are shown above. These resources are now in
your Terraform state and will henceforth be managed by Terraform.

====

cmosquer@CMOSQUER-M-Q4XC terraform2 % terraform import -var-file="00_input.tfvars" aws_api_gateway_resource.path_health jeai60f6hc/okzztd
data.aws_caller_identity.current: Reading...
data.aws_region.current: Reading...
aws_api_gateway_resource.path_health: Importing from ID "jeai60f6hc/okzztd"...
aws_api_gateway_resource.path_health: Import prepared!
  Prepared aws_api_gateway_resource for import
data.aws_region.current: Read complete after 0s [id=us-west-2]
aws_api_gateway_resource.path_health: Refreshing state... [id=okzztd]
data.aws_caller_identity.current: Read complete after 0s [id=924300192870]

Import successful!

The resources that were imported are shown above. These resources are now in
your Terraform state and will henceforth be managed by Terraform.


====

...
...
...

====

cmosquer@CMOSQUER-M-Q4XC terraform2 % terraform import -var-file="00_input.tfvars" aws_api_gateway_method.proxy_delay jeai60f6hc/oca7dv/GET
data.aws_caller_identity.current: Reading...
data.aws_region.current: Reading...
data.aws_region.current: Read complete after 0s [id=us-west-2]
aws_api_gateway_method.proxy_delay: Importing from ID "jeai60f6hc/oca7dv/GET"...
aws_api_gateway_method.proxy_delay: Import prepared!
  Prepared aws_api_gateway_method for import
aws_api_gateway_method.proxy_delay: Refreshing state... [id=agm-jeai60f6hc-oca7dv-GET]
data.aws_caller_identity.current: Read complete after 0s [id=924300192870]

Import successful!

The resources that were imported are shown above. These resources are now in
your Terraform state and will henceforth be managed by Terraform.

====

cmosquer@CMOSQUER-M-Q4XC terraform2 % terraform import -var-file="00_input.tfvars" aws_api_gateway_integration.lambda_integration_delay jeai60f6hc/oca7dv/GET
data.aws_caller_identity.current: Reading...
data.aws_region.current: Reading...
data.aws_region.current: Read complete after 0s [id=us-west-2]
aws_api_gateway_integration.lambda_integration_delay: Importing from ID "jeai60f6hc/oca7dv/GET"...
aws_api_gateway_integration.lambda_integration_delay: Import prepared!
  Prepared aws_api_gateway_integration for import
aws_api_gateway_integration.lambda_integration_delay: Refreshing state... [id=agi-jeai60f6hc-oca7dv-GET]
data.aws_caller_identity.current: Read complete after 0s [id=924300192870]

Import successful!

The resources that were imported are shown above. These resources are now in
your Terraform state and will henceforth be managed by Terraform.

====

cmosquer@CMOSQUER-M-Q4XC terraform2 % terraform import -var-file="00_input.tfvars" aws_api_gateway_method_response.proxy_delay jeai60f6hc/oca7dv/GET/200
data.aws_region.current: Reading...
data.aws_caller_identity.current: Reading...
data.aws_region.current: Read complete after 0s [id=us-west-2]
aws_api_gateway_method_response.proxy_delay: Importing from ID "jeai60f6hc/oca7dv/GET/200"...
aws_api_gateway_method_response.proxy_delay: Import prepared!
  Prepared aws_api_gateway_method_response for import
aws_api_gateway_method_response.proxy_delay: Refreshing state... [id=agmr-jeai60f6hc-oca7dv-GET-200]
data.aws_caller_identity.current: Read complete after 0s [id=924300192870]

Import successful!

The resources that were imported are shown above. These resources are now in
your Terraform state and will henceforth be managed by Terraform.

====

cmosquer@CMOSQUER-M-Q4XC terraform2 % terraform import -var-file="00_input.tfvars" aws_api_gateway_integration_response.reponse_integration_delay jeai60f6hc/oca7dv/GET/200
data.aws_caller_identity.current: Reading...
data.aws_region.current: Reading...
data.aws_region.current: Read complete after 0s [id=us-west-2]
aws_api_gateway_integration_response.reponse_integration_delay: Importing from ID "jeai60f6hc/oca7dv/GET/200"...
aws_api_gateway_integration_response.reponse_integration_delay: Import prepared!
  Prepared aws_api_gateway_integration_response for import
aws_api_gateway_integration_response.reponse_integration_delay: Refreshing state... [id=agir-jeai60f6hc-oca7dv-GET-200]
data.aws_caller_identity.current: Read complete after 0s [id=924300192870]

Import successful!

The resources that were imported are shown above. These resources are now in
your Terraform state and will henceforth be managed by Terraform.

====

...
...
...

====
