


## IMPLEMENTATION

* Read endpoint from ENV VAR
* Emit GET for /, health, sleep1 and duration(2)
* Assert reponse
* Match response to curl requests


## CURL REQUESTS

export ENDPOINTUAT='https://jeai60f6hc.execute-api.us-west-2.amazonaws.com/test/helloworld';
echo 'REMARK: No training slash!!!';

QAROOT="$(curl -sk ${ENDPOINTUAT}/)";
if [[ ! "$QAROOT" = *"GET"* ]]; then echo "ERROR::QAROOT assertion failed. No GET in response..."; fi;
echo "INFO:: QAROOT response was :: ${QAROOT}";


QAHEALTH="$(curl -sk ${ENDPOINTUAT}/health)";
if [[ ! "$QAHEALTH" = *"OK"* ]]; then echo "ERROR::QAHEALTH assertion failed. No OK in response..."; fi;
echo "INFO:: QAHEALTH response was :: ${QAHEALTH}";


QASLEEP1="$(curl -sk ${ENDPOINTUAT}/sleep1)";
if [[ ! "$QASLEEP1" = "Successfully executed one-second sleep"* ]]; then echo "ERROR::QASLEEP1 assertion failed. Expected string is missing in response..."; fi;
echo "INFO:: QASLEEP1 response was :: ${QASLEEP1}";


QADELAY="$(curl -sk ${ENDPOINTUAT}'/delay?duration=2')";
if [[ ! "$QADELAY" = *"Executed custom sleep 2"* ]]; then echo "ERROR::QADELAY assertion failed. Expected string is missing in response..."; fi;
echo "INFO:: QADELAY response was :: ${QADELAY}";



## CALLING THE GO APPLICATION


#### Buodling for the first time

go mod init cmosquer/goTest
go mod tidy
go run .

//

go build .
./main

#### Calling the QA Golang application

go run .