from azureml.core.environment import Environment
from azureml.core.model import InferenceConfig, Model
from azureml.core.webservice import LocalWebservice
from azureml.core import Workspace

# Get the workspace
ws = Workspace.from_config()
# Create inference configuration based on the environment definition and the entry script
# yolo = Environment.from_conda_specification(name="env", file_path="yolo.yml")
yolo = Environment.from_pip_requirements(
    name="yolo", file_path="./yolov5/requirements.txt")
# yolo.save_to_directory('')
yolo.register(workspace=ws)
inference_config = InferenceConfig(
    entry_script="azure.py", environment=yolo, source_directory="yolov5")
# Retrieve registered model
model = Model(ws, id="lpr:1")
# Create a local deployment, using port 8890 for the web service endpoint
deployment_config = LocalWebservice.deploy_configuration(port=8890)
# Deploy the service
service = Model.deploy(
    ws, "lpr", [model], inference_config, deployment_config)
# Wait for the deployment to complete
service.wait_for_deployment(True)
# Display the port that the web service is available on
print(service.port)
