
Folders of interest:

## Terraform/
These are the files from chapter4/done folder and started point for Robert/chapter5 exercise.
However it is not pursue as the app sample written in js/ts seems not to work (?). Hence using terraform4 instead


## Terraform2/

Resources where created manually from AWS API GAteway demosntration
This folder captures a full exercise importing AWS resources into terraform state
The end result is an updated version of .tf files as well as a terraform state with the current AWS resources with minimal drift
This was done in uw2 region

## Terraform3/

This aim to test the .tf files created during the tf import operation captured under terraform2/ folder. 
The generation of resources by these files successfully duplicated the functionality that previously existed before terraform2/ operation was completed.
This validation was done in ue2 region!


## Terraform4/

Building from terraform3/, work on the chapt5 exercise to convert a flat pattern into an opinionated modular structure.



## TODO

[x] Define an API Gateway that interacts with resource ID in the path (Python lambda interacting with DynamoDB table)
[ ] Import block #NICE-FEATURE #NICE-TODO 
[ ] Finish chapter 5
[ ] Golang full testing: https://pkg.go.dev/github.com/stretchr/testify/assert
[ ] Lambda automatic tf replacement based on hash
[x] Load python app lambda code from local file
[ ] Module for REST route to remove code duplication (After chapter5)
[x] Define /items route in terraform HCL
