variable "create_flag" {
  type        = bool
  description = "Create api_gateway_resource"
  default     = true
}

variable "rest_apigateway_id" {
  type        = string
  description = "aws_api_gateway_rest_api.my_gateway.id"
}

##variable "apigateway_root_id" {
##  type        = string
##  description = "aws_api_gateway_resource.root.id"
##}

variable "apigateway_resource_path_id" {
  type        = string
  description = "aws_api_gateway_resource.path_health.id"
}

variable "apigateway_timeout" {
  type        = number
  description = ""
  default     = 29000
}

##variable "path_part" {
##  type        = string
##  description = "path_part"
##}

variable "http_method" {
  type        = string
  description = "http_method"
  default     = "GET"
}

variable "lambda_invoke_arn" {
  type        = string
  description = "lambda invoke arn"
}