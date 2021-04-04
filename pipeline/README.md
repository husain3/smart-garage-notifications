To create a stack of this pipeline run this cmd statement:

```aws cloudformation create-stack --stack-name smart-garage-notifications-pipeline --template-body file://pipeline.yaml --capabilities CAPABILITY_NAMED_IAM```

To update a stack of this pipeline run this cmd statement:

```aws cloudformation update-stack --stack-name smart-garage-notifications-pipeline --template-body file://pipeline.yaml --capabilities CAPABILITY_NAMED_IAM```