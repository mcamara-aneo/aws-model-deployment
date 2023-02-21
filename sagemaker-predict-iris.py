## test endpoint 
## from https://docs.databricks.com/_static/notebooks/mlflow/mlflow-quick-start-deployment-aws.html
import boto3
import pandas as pd
from mlflow.deployments import get_deploy_client
from sklearn import datasets
from sklearn.model_selection import train_test_split


iris = datasets.load_iris()
x = iris.data[:, 2:]
y = iris.target
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=7)


REGION = "eu-west-3"
APP_NAME = "iris-rf-1"
APP_ARN = "arn:aws:sagemaker:eu-west-3:335059175490:endpoint/iris-rf-1"

def check_status(app_name):
    client = get_deploy_client(f"sagemaker:/{REGION}")
    end_point = client.get_deployment(app_name)
    endpoint_status = end_point['EndpointStatus']
    
    return endpoint_status

def query_endpoint(app_name, input_df):
    client = boto3.session.Session().client("sagemaker-runtime", REGION)
    client = get_deploy_client(f"sagemaker:/{REGION}")
    predict = client.predict(app_name, input_df)
    #print("Received response: {}".format(predict))
    return predict

## check endpoint status
print("Application status is: {}".format(check_status(APP_NAME)))

## create test data and make inference from enpoint
query_input = pd.DataFrame(X_test)
prediction = query_endpoint(app_name=APP_NAME, input_df=query_input)

print(f"Predictions : {prediction}")
print("DELETING AWS DEPLOYMENT")
client = get_deploy_client(f"sagemaker:/{REGION}")
client.delete_deployment(APP_NAME)
list_deployments = client.list_deployments()
if len(list_deployments) > 0:
    print("It exists deployments model")
else:
    print("All deployment is deleted")

