Terraform Module for AWS Lambda
===============================

This module abstracts the details of creating an AWS Lambda function into a simpler, opinionated interface.

Current files used as aprt of the Terraform registry demo


Demo
-------

```
module "lambda" {
  source  = "app.terraform.io/polarys/lambda/aws"
  version = "0.0.1"
  # insert required variables here
}
```


References
-------

* https://github.com/robrich/terraform-hands-on-workshop-aws/tree/main/05-Modules/start


License
-------

MIT