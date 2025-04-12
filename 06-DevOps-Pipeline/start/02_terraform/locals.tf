locals {
  dynamodb_table_name = "dynamodb-${var.ENV_NAME}"
  lambda_name         = "LambdaProxyIntegration-${var.ENV_NAME}"
  lambda_handler      = "main3.lambda_handler" ###=> "app.dynamoDbQueryHandler" // the name of the function in the lambda typescript project
  api_gateway_name    = "LambdaProxyAPI"


  helloworld_list_paths = ["delay", "health", "info", "sleep1", "sleep5", "toc"]

  items_id_paths = ["GET", "DELETE"]

  items_paths = ["GET", "PUT", "POST"]

  /*
  helloworld_paths = [
    {
      path_part = "delay", 
    },
    {
      path_part = "health", 
    },
    {
      path_part = "info", 
    },
    {
      path_part = "sleep1",
    },
    {
      path_part = "sleep5",
    },
    {
      path_part = "toc",
    }
  ]

  items_paths = [
    {
      name        = "items_id_get",
      ref_path    = "ref_items_id",
      http_method = "GET",
      create_flag = true
    },
    {
      name        = "items_id_rm",
      ref_path    = "ref_items_id",
      http_method = "DELETE",
      create_flag = false
    },
    {
      name        = "items_get",
      ref_path    = "ref_items",
      http_method = "GET",
      create_flag = true
    },
    {
      name        = "items_put",
      ref_path    = "ref_items"
      http_method = "PUT",
      create_flag = false
    },
    {
      name        = "items_post",
      ref_path    = "ref_items",
      http_method = "POST",
      create_flag = false
    }
  ]
  */

  environment_variables = {
    "DYNAMODB_TABLE" : local.dynamodb_table_name,
    "ENV_NAME" : var.ENV_NAME
    "NODE_PORT" : "3000" #tostring(local.fargate_container_port)
    "NODE_ENV" : "production"
  }

}
