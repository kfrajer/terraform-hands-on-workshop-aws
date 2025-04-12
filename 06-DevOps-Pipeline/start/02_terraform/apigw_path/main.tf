
/* **************************************************

resource "aws_api_gateway_resource" "path_health" {
  count = var.create_flag ? 1 : 0
  rest_api_id = var.rest_apigateway_id
  parent_id   = var.apigateway_root_id
  path_part   = var.path_part
}

************************************************** */


# Need all 4 for each method - /test/helloworld/health:

resource "aws_api_gateway_method" "proxy_custom_path" {
  rest_api_id   = var.rest_apigateway_id
  resource_id   = var.apigateway_resource_path_id
  http_method   = var.http_method
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "lambda_integration_custom_path" {
  rest_api_id             = var.rest_apigateway_id
  resource_id             = var.apigateway_resource_path_id
  http_method             = aws_api_gateway_method.proxy_custom_path.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = var.lambda_invoke_arn

  cache_key_parameters = []
  connection_type      = "INTERNET"
  timeout_milliseconds = var.apigateway_timeout
  content_handling     = "CONVERT_TO_TEXT"
  passthrough_behavior = "WHEN_NO_MATCH"
  request_parameters   = {}
  request_templates    = {}

}

resource "aws_api_gateway_method_response" "proxy_custom_path" {
  rest_api_id = var.rest_apigateway_id
  resource_id = var.apigateway_resource_path_id
  http_method = aws_api_gateway_method.proxy_custom_path.http_method
  status_code = "200"

  response_models = { "application/json" = "Empty" }
}

resource "aws_api_gateway_integration_response" "reponse_integration_custom_path" {
  rest_api_id = var.rest_apigateway_id
  resource_id = var.apigateway_resource_path_id
  http_method = aws_api_gateway_method.proxy_custom_path.http_method
  status_code = aws_api_gateway_method_response.proxy_custom_path.status_code

  response_templates = {
    "application/json" = null
  }

  depends_on = [
    aws_api_gateway_method.proxy_custom_path,
    aws_api_gateway_integration.lambda_integration_custom_path
  ]
}