pip install --target ./package requests

cd package
zip -r ../my_deployment_package.zip .

cd ..
zip my_deployment_package.zip dummy_lambda.py