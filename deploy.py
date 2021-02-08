from azureml.core.environment import Environment
from azureml.core.model import InferenceConfig, Model
from azureml.core.compute import ComputeTarget
from azureml.core.webservice import AksWebservice, AciWebservice, LocalWebservice
from azureml.core import Workspace
import click

# https://github.com/Azure/MachineLearningNotebooks/blob/master/how-to-use-azureml/deployment/production-deploy-to-aks/production-deploy-to-aks.ipynb

@click.command()
@click.option('--local/--not-local', '-l', default=False)
@click.option('--aks/--not-aks', '-a', default=False)
@click.option('--aci/--not-aci', default=False)
@click.option('--num-cores', '-n', default=1)
@click.option('--mem-gb', '-m', default=1)
@click.option('--compute-name', '-c', default='lpr-inf-clusters')
def deploy(local, aks, aci, num_cores, mem_gb, compute_name):
    # Get the workspace
    ws = Workspace.from_config()
    # Create inference configuration based on the environment definition and the entry script
    # yolo = Environment.from_conda_specification(name="env", file_path="yolo.yml")
    yolo = Environment.from_pip_requirements(
        name="yolo", file_path="./deployed_requirements.txt")
    # yolo.save_to_directory('')
    yolo.register(workspace=ws)
    inference_config = InferenceConfig(
        entry_script="azure.py", environment=yolo, source_directory="yolov5")
    # Retrieve registered model
    model = Model(ws, id="lpr:1")
    deploy_target = None
    if local:
        # Create a local deployment, using port 8890 for the web service endpoint
        deployment_config = LocalWebservice.deploy_configuration(port=8890)
    elif aks:
        # Create a AKS deployment
        deployment_config = AksWebservice.deploy_configuration(
            cpu_cores=num_cores, memory_gb=mem_gb, compute_target_name=compute_name)
        deploy_target = ComputeTarget(workspace=ws, name=compute_name)
        # if deploy_target.get_status() != "Succeeded":
        #     print(f"Deploy Target: {deploy_target.get_status()}")
        #     deploy_target.wait_for_completion(show_output=True)
    elif aks:
        # Create a AKS deployment
        deployment_config = AciWebservice.deploy_configuration(
            cpu_cores=num_cores, memory_gb=mem_gb, compute_target_name=compute_name)
    else:
        raise NotImplementedError("Choose deploy target please")
    # Deploy the service
    print("Deploying:")
    service = Model.deploy(
        workspace=ws, name="lpr", models=[model],
        inference_config=inference_config, deployment_config=deployment_config,
        overwrite=True, deployment_target=deploy_target)
    # Wait for the deployment to complete
    print("Deploying:")
    service.wait_for_deployment(True)
    # Display the port that the web service is available on
    if local:
        print(service.port)

    # TODO: Test


if "__main__" == __name__:
    deploy()
