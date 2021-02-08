from azureml.core import Workspace
from azureml.core import Webservice
ws = Workspace.from_config()

service = Webservice(ws, 'lpr')
scoring_uri = service.scoring_ui
primary, secondary = service.get_keys()
print(primary)
print(service.get_logs())
