# ==================================================
## API GATEWAY - CORE
#

// Inspired by:
// https://spacelift.io/blog/terraform-api-gateway
// https://github.com/sumeetninawe/tf-lambda-apig/blob/main/apigateway.tf

resource "aws_api_gateway_rest_api" "my_gateway" {

  name        = local.api_gateway_name
  description = "API Gateway for the Terraform workshop"

  endpoint_configuration {
    types = ["REGIONAL"]
  }

  tags = var.tags
}

##RESOURCE: https://registry.terraform.io/providers/hashicorp/time/latest/docs/resources/sleep
resource "time_sleep" "wait_x_seconds" {
  depends_on = [aws_api_gateway_resource.path_delay]

  create_duration = "70s"
}

resource "aws_api_gateway_deployment" "my_gateway" {
  ##TODO: Below is required for Tf's lifecycle! Usinf time_sleep as an alternative
  #depends_on = [
  #  aws_api_gateway_integration.lambda_integration
  #]
  depends_on  = [time_sleep.wait_x_seconds]
  rest_api_id = aws_api_gateway_rest_api.my_gateway.id

  lifecycle {
    create_before_destroy = true
  }
}


resource "aws_api_gateway_stage" "gw_stage_name" {
  deployment_id = aws_api_gateway_deployment.my_gateway.id
  rest_api_id   = aws_api_gateway_rest_api.my_gateway.id
  stage_name    = "test"
}

# allow the gateway to call the lambda


resource "aws_iam_role_policy_attachment" "lambda_basic" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
  role       = module.api_lambda.role_name
}


resource "aws_lambda_permission" "apigw_lambda" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = module.api_lambda.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.my_gateway.execution_arn}/*/*/*"
}


# ==================================================
## API GATEWAY - RESOURCES UNDER helloworld/
#


resource "aws_api_gateway_resource" "root" {
  rest_api_id = aws_api_gateway_rest_api.my_gateway.id
  parent_id   = aws_api_gateway_rest_api.my_gateway.root_resource_id
  path_part   = "helloworld" ###=> "api"
}



resource "aws_api_gateway_resource" "path_health" {
  rest_api_id = aws_api_gateway_rest_api.my_gateway.id
  parent_id   = aws_api_gateway_resource.root.id
  path_part   = "health"
}

resource "aws_api_gateway_resource" "path_info" {
  rest_api_id = aws_api_gateway_rest_api.my_gateway.id
  parent_id   = aws_api_gateway_resource.root.id
  path_part   = "info"
}

resource "aws_api_gateway_resource" "path_sleep1" {
  rest_api_id = aws_api_gateway_rest_api.my_gateway.id
  parent_id   = aws_api_gateway_resource.root.id
  path_part   = "sleep1"
}

resource "aws_api_gateway_resource" "path_sleep5" {
  rest_api_id = aws_api_gateway_rest_api.my_gateway.id
  parent_id   = aws_api_gateway_resource.root.id
  path_part   = "sleep5"
}

resource "aws_api_gateway_resource" "path_toc" {
  rest_api_id = aws_api_gateway_rest_api.my_gateway.id
  parent_id   = aws_api_gateway_resource.root.id
  path_part   = "toc"
}

resource "aws_api_gateway_resource" "path_delay" {
  rest_api_id = aws_api_gateway_rest_api.my_gateway.id
  parent_id   = aws_api_gateway_resource.root.id
  path_part   = "delay"
}


# ==================================================
## API GATEWAY - RESOURCES UNDER items/
#

##REFERENCE: API-GW REST with variable in request path: https://stackoverflow.com/questions/39040739/in-terraform-how-do-you-specify-an-api-gateway-endpoint-with-a-variable-in-the


#GET, PUT, (fake) POST
resource "aws_api_gateway_resource" "path_items" {
  rest_api_id = aws_api_gateway_rest_api.my_gateway.id
  parent_id   = aws_api_gateway_rest_api.my_gateway.root_resource_id
  path_part   = "items"
}

#GET, DELETE
resource "aws_api_gateway_resource" "path_items_id" {
  rest_api_id = aws_api_gateway_rest_api.my_gateway.id
  parent_id   = aws_api_gateway_resource.path_items.id
  path_part   = "{id}"
}
