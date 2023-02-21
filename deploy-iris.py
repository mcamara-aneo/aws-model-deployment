#from mlflow.sagemaker import sagemaker_deploy, save_model
from mlflow.deployments import get_deploy_client
# from mlflow.sagemaker import deploy

experiment_id = "437095618945083435"
run_id = "59e0e8d4eaf74f5e83b002abc8eb670f" # the model you want to deploy - this run_id was saved when we trained our model
region = "eu-west-3" # region of your account
aws_id = "335059175490" # from the aws-cli output
arn = "arn:aws:iam::335059175490:role/aws-sagemaker-for-deploy-ml-model" #f"arn:aws:iam::{aws_id}:user/MamadouCamara"
app_name = "iris-rf-1"
bucket_name = "mlflow-bucket-iris"
work_dir = "/home/mcamara/aws-model-deployment"
model_uri = f"{work_dir}/mlruns/{experiment_id}/{run_id}/artifacts/random-forest-model" # edit this path based on your working directory
image_url = f"{aws_id}.dkr.ecr.{region}.amazonaws.com/mlflow-pyfunc:2.1.1" # change to your mlflow version
instance_type="ml.t2.medium" 



# MLFLOW 2.1.1 neither support sagemakerdeploy, sagemaker_deploy, save_model FUNCTIONS
# deploy(app_name=app_name, 
#         model_uri=model_uri, 
#         region_name=region, 
#         mode="create",
#         execution_role_arn=arn,
#         image_url=image_url)

# sagemaker_deploy(app_name=app_name,
#                 model_uri=model_uri,
#                 region_name=region,
#                 mode="create",
#                 execution_role_arn=arn,
#                 image_url=image_url)




# DON'T WANT TO SPECIFY VPC AND SUBNET USE DEFAULT ONES
# vpc_config = {
#     'SecurityGroupIds': [
#         'sg-123456abc',
#     ],
#     'Subnets': [
#         'subnet-123456abc',
#     ]
# }
config=dict(
    execution_role_arn=arn,
    bucket=bucket_name,
    image_url=image_url,
    region_name=region,
    archive=False,
    instance_type=instance_type,
    instance_count=1,
    synchronous=True,
    timeout_seconds=1000,
    env={"DISABLE_NGINX": "1", "GUNICORN_CMD_ARGS": "--timeout 60"}, 
    tags={"training_timestamp": "2023-02-01T05:13:15"}
)


client = get_deploy_client(f"sagemaker:/{region}")
existing_deployments = client.list_deployments(app_name)
if len(existing_deployments) > 0:
    # Si un déploiement existe déjà, mettez à jour avec la nouvelle configuration
    client.update_deployment(app_name, model_uri=model_uri, config=config)
else:
    # Sinon, créez un nouveau déploiement
    client.create_deployment(
        app_name,
        model_uri=model_uri,
        flavor="python_function",
        config=config
    )


