Generate API Gateway Events
===========================

Command to generate event:
```
sam local generate-event apigateway aws-proxy --body '{"data_stuff": "down is the new up"}' --method POST --path 'the/cool/path' --stage 'test'
```
