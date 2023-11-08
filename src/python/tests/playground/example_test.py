import json
from azure.mgmt.datafactory import models as _models

from data_factory_testing_framework.generated import Deserializer
from data_factory_testing_framework.generated.models import WebActivity, PipelineResource


def get_pipeline():
    client_models = {k: v for k, v in _models.__dict__.items() if isinstance(v, type)}
    deserializer = Deserializer(client_models)

    with (open('batch_job.json', 'r') as f):
        pipelineJson = json.load(f)
        return deserializer._deserialize("PipelineResource", pipelineJson)


def evaluate(activity: WebActivity):
    # This method will execute all the magic of evaluating all expressions under the activity

    activity.body.evaluate()


class TestPipeline:
    pipeline: PipelineResource

    def test_web_activity(self):
        # Arrange
        web_activity: WebActivity = get_pipeline().activities[0]

        # Act
        evaluate(web_activity)

        # Assert
        assert web_activity.body.value == "test2"
