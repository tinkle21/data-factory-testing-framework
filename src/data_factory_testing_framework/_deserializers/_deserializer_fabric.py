import json

from data_factory_testing_framework._deserializers._deserializer_base import _parse_pipeline_from_json
from data_factory_testing_framework.models import Pipeline


def parse_fabric_pipeline_from_pipeline_json_files(
    pipeline_json: str, config_json: str, metadata_json: str
) -> Pipeline:
    pipeline_logical_id = _get_pipeline_logical_id_from_config_json(config_json)
    pipeline_name = _get_pipeline_name_from_metadata_json(metadata_json)
    pipeline_json = json.loads(pipeline_json)
    return _parse_pipeline_from_json(pipeline_logical_id, pipeline_name, pipeline_json)


def _get_pipeline_logical_id_from_config_json(config_json: str) -> str:
    config_json = json.loads(config_json)
    return config_json["logicalId"]


def _get_pipeline_name_from_metadata_json(metadata_json: str) -> str:
    metadata_json = json.loads(metadata_json)
    return metadata_json["displayName"]
