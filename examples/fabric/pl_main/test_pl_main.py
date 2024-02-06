import pytest
from data_factory_testing_framework.models.pipeline import Pipeline
from data_factory_testing_framework.state import (
    PipelineRunState
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
    return test_framework.repository.get_pipeline_by_name("pl_main")


def test_read_configuration_file(
    test_framework: TestFramework, pipeline: Pipeline
) -> None:
    # Arrange
    activity = pipeline.get_activity_by_name("Read Configuration File")

    # Act
    state = PipelineRunState()
    activity.evaluate(state)

    # Assert
    expected_data_store_type = "Lakehouse"
    assert expected_data_store_type == (
        activity.type_properties["datasetSettings"]["linkedService"]
        ["properties"]["type"]
    )

    expected_file_name = "lh_config.json"
    assert expected_file_name == (
        activity.type_properties["datasetSettings"]["typeProperties"]
        ["location"]["fileName"]
    )

    expected_folder_name = "config"
    assert expected_folder_name == (
        activity.type_properties["datasetSettings"]["typeProperties"]
        ["location"]["folderPath"]
    )


def test_if(
    test_framework: TestFramework, pipeline: Pipeline
) -> None:
    # Arrange
    foreach_activity = pipeline.get_activity_by_name("ForEach")
    child_activity = next(
        filter(
            lambda a: a.name == "If New Or Updated",
            foreach_activity.activities
        )
    )

    # Act
    state = PipelineRunState(
        iteration_item={"year": "2019",
                        "month": "09",
                        "created": "2023-05-24T11:04:42Z",
                        "lastUpdatedSourceSystem": "2023-05-24T11:04:42Z",
                        "lastUpdatedDatalake": "2023-05-01T11:04:42Z"}
    )

    child_activity.evaluate(state)

    # Assert
    expected_if_evaluation = True
    assert expected_if_evaluation == (
        child_activity.expression.value
    )


def test_invoke_pipeline(
    test_framework: TestFramework, pipeline: Pipeline
) -> None:
    # Arrange
    foreach_activity = pipeline.get_activity_by_name("ForEach")
    if_activity = next(
        filter(
            lambda a: a.name == "If New Or Updated",
            foreach_activity.activities
        )
    )

    inner_pipeline_activity = next(
        filter(
            lambda a: a.name == "Invoke Ingestion Pipeline",
            if_activity.if_true_activities
        )
    )

    # Act
    state = PipelineRunState(
        iteration_item={"year": "2019",
                        "month": "09",
                        "created": "2023-05-24T11:04:42Z",
                        "lastUpdatedSourceSystem": "2023-24-01T11:04:42Z",
                        "lastUpdatedDatalake": "2023-05-24T11:04:42Z"}
    )
    inner_pipeline_activity.evaluate(state)

    # Assert
    expected_pipeline_name = "pl_ingestion"
    assert expected_pipeline_name == (
        inner_pipeline_activity.type_properties["pipeline"]
        ["referenceName"]
    )

    expected_pipeline_parameter_month = "09"
    assert expected_pipeline_parameter_month == (
        inner_pipeline_activity.type_properties["parameters"]
        ["dynamicmonth"].value
    )

    expected_pipeline_parameter_year = "2019"
    assert expected_pipeline_parameter_year == (
        inner_pipeline_activity.type_properties["parameters"]
        ["dynamicyear"].value
    )
