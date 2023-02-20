import mlflow.sagemaker as mfs

experiment_id = "437095618945083435"
run_id = "59e0e8d4eaf74f5e83b002abc8eb670f" # the model you want to deploy - this run_id was saved when we trained our model
region = "eu-west-3" # region of your account
aws_id = "335059175490" # from the aws-cli output
arn = f"arn:aws:iam::{aws_id}:user/MamadouCamara"
app_name = "iris-rf-1"
work_dir = "/home/mcamara/aws-model-deployment"
model_uri = f"{work_dir}/{experiment_id}/{run_id}/artifacts/random-forest-model" # edit this path based on your working directory
image_url = f"{aws_id}.dkr.ecr.{region}.amazonaws.com/mlflow-pyfunc:2.1.1" # change to your mlflow version

mfs.deploy(app_name=app_name, 
           model_uri=model_uri, 
           region_name=region, 
           mode="create",
           execution_role_arn=arn,
           image_url=image_url)