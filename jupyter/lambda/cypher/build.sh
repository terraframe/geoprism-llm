pip install --target ./package neo4j

cd package
zip -r ../my_deployment_package.zip .

cd ..
zip my_deployment_package.zip dummy_lambda.py