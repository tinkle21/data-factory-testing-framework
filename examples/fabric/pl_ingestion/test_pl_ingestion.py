import pytest
from data_factory_testing_framework.models.pipeline import Pipeline
from data_factory_testing_framework.state import (
    PipelineRunState,
    RunParameter,
    RunParameterType,
)

from data_factory_testing_framework.test_framework import (
    TestFramework,
    TestFrameworkType
)


@pytest.fixture
def test_framework(request: pytest.FixtureRequest) -> TestFramework:
    return TestFramework(
        framework_type=TestFrameworkType.Fabric,
        root_folder_path=request.fspath.dirname,
    )


@pytest.fixture
def pipeline(test_framework: TestFramework) -> Pipeline:
    return test_framework.repository.get_pipeline_by_name("pl_ingestion")


def test_copy_nyc_data(
    test_framework: TestFramework, pipeline: Pipeline
) -> None:
    # Arrange
    activity = pipeline.get_activity_by_name("Copy NYC Data")
    state = PipelineRunState(
        parameters=[
            RunParameter[str](
                RunParameterType.Pipeline, "dynamicmonth", "01"),
            RunParameter[str](
                RunParameterType.Pipeline, "dynamicyear", "2023"),
        ],
    )

    # Act
    activity.evaluate(state)

    # Assert
    expected_http_rel_url = "yellow_tripdata_2023-01.parquet"
    assert expected_http_rel_url == (
        activity.type_properties["source"]
        ["datasetSettings"]["typeProperties"]["location"]["relativeUrl"].value
    )
    expected_file_name = "yellow_tripdata_2023-01.parquet"
    assert expected_file_name == (
        activity.type_properties["sink"]
        ["datasetSettings"]["typeProperties"]["location"]["fileName"].value
    )

    expected_folder_name = "nyc_taxi_data/2023/01"
    assert expected_folder_name == (
        activity.type_properties["sink"]
        ["datasetSettings"]["typeProperties"]["location"]["folderPath"].value
    )
