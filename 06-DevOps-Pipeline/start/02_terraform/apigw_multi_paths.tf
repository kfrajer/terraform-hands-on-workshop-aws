# ==================================================
## 
#


## DONE: How to iterate over two lists, 2 vars
## REFERENCE: https://serverfault.com/questions/833810/terraform-use-nested-loops-with-count
/*
variable "helloworld_path" {
  type = map(list(string))
  default = {
    "delay"  = aws_api_gateway_resource.path_delay.id,
    "health" = aws_api_gateway_resource.path_health.id,
    "info"   = aws_api_gateway_resource.path_info.id,
    "sleep1" = aws_api_gateway_resource.path_sleep1.id,
    "sleep5" = aws_api_gateway_resource.path_sleep5.id,
    "toc"    = aws_api_gateway_resource.path_toc.id
  }
}


variable "helloworld_apigw_resource_paths" {
  default = [
    aws_api_gateway_resource.path_delay.id,
    aws_api_gateway_resource.path_health.id,
    aws_api_gateway_resource.path_info.id,
    aws_api_gateway_resource.path_sleep1.id,
    aws_api_gateway_resource.path_sleep5.id,
    aws_api_gateway_resource.path_toc.id
  ]
}

locals {
  helloworld_paths = zipmap(var.helloworld_list_paths, helloworld_apigw_resource_paths)
}

module "api_gateway_helloworld_paths" {
  source = "./apigw_path"
  ## REFERENCE: Using for_each: https://stackoverflow.com/questions/58594506/how-to-for-each-through-a-listobjects-in-terraform-0-12
  #for_each   = toset(local.helloworld_paths)
  count = length(local.helloworld_paths)

  rest_apigateway_id = aws_api_gateway_rest_api.my_gateway.id
  #apigateway_root_id = aws_api_gateway_resource.root.id
  apigateway_resource_path_id = local.helloworld_paths[keys(local.helloworld_paths)[count.index]]
  path_part                   = keys(local.helloworld_paths)[count.index] #each.key
  lambda_invoke_arn           = module.api_lambda.lambda_invoke_arn
}
*/


//TODO: Next is untested
//TODO: Test this locally then via GHActions!!!
module "api_gateway_helloworld_default_path" {
  source = "./apigw_path"

  rest_apigateway_id          = aws_api_gateway_rest_api.my_gateway.id
  apigateway_resource_path_id = aws_api_gateway_resource.root.id
  #path_part                   = "/"
  lambda_invoke_arn = module.api_lambda.lambda_invoke_arn
}

module "api_gateway_helloworld_delay_path" {
  source = "./apigw_path"

  rest_apigateway_id          = aws_api_gateway_rest_api.my_gateway.id
  apigateway_resource_path_id = aws_api_gateway_resource.path_delay.id
  #path_part                   = "delay"
  lambda_invoke_arn = module.api_lambda.lambda_invoke_arn
}

module "api_gateway_helloworld_health_path" {
  source = "./apigw_path"

  rest_apigateway_id          = aws_api_gateway_rest_api.my_gateway.id
  apigateway_resource_path_id = aws_api_gateway_resource.path_health.id
  #path_part                   = "health"
  lambda_invoke_arn = module.api_lambda.lambda_invoke_arn
}

module "api_gateway_helloworld_info_path" {
  source = "./apigw_path"

  rest_apigateway_id          = aws_api_gateway_rest_api.my_gateway.id
  apigateway_resource_path_id = aws_api_gateway_resource.path_info.id
  #path_part                   = "info"
  lambda_invoke_arn = module.api_lambda.lambda_invoke_arn
}

module "api_gateway_helloworld_sleep1_path" {
  source = "./apigw_path"

  rest_apigateway_id          = aws_api_gateway_rest_api.my_gateway.id
  apigateway_resource_path_id = aws_api_gateway_resource.path_sleep1.id
  #path_part                   = "sleep1"
  lambda_invoke_arn = module.api_lambda.lambda_invoke_arn
}

module "api_gateway_helloworld_sleep5_path" {
  source = "./apigw_path"

  rest_apigateway_id          = aws_api_gateway_rest_api.my_gateway.id
  apigateway_resource_path_id = aws_api_gateway_resource.path_sleep5.id
  #path_part                   = "sleep5"
  lambda_invoke_arn = module.api_lambda.lambda_invoke_arn
}

module "api_gateway_helloworld_toc_path" {
  source = "./apigw_path"

  rest_apigateway_id          = aws_api_gateway_rest_api.my_gateway.id
  apigateway_resource_path_id = aws_api_gateway_resource.path_toc.id
  #path_part                   = "toc"
  lambda_invoke_arn = module.api_lambda.lambda_invoke_arn
}



# ==================================================
## 
#


module "api_gateway_items_id_paths" {
  source   = "./apigw_path"
  for_each = toset(local.items_id_paths)
  /*
  for_each   = {
    for index, a_path in local.items_paths:
    a_path.name => a_path
  }
  */

  rest_apigateway_id = aws_api_gateway_rest_api.my_gateway.id
  #apigateway_root_id = each.value.ref_path == "ref_items_id" ? aws_api_gateway_rest_api.my_gateway.root_resource_id : aws_api_gateway_resource.path_items.id
  apigateway_resource_path_id = aws_api_gateway_resource.path_items_id.id
  #path_part          = each.value.ref_path == "ref_items_id" ? "items" : "{id}"
  http_method       = each.key
  lambda_invoke_arn = module.api_lambda.lambda_invoke_arn
}


# ==================================================
## 
#


module "api_gateway_items_paths" {
  source   = "./apigw_path"
  for_each = toset(local.items_paths)

  rest_apigateway_id          = aws_api_gateway_rest_api.my_gateway.id
  apigateway_resource_path_id = aws_api_gateway_resource.path_items.id
  http_method                 = each.key
  lambda_invoke_arn           = module.api_lambda.lambda_invoke_arn
}