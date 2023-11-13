import re

from data_factory_testing_framework.exceptions.state_iteration_item_not_set import StateIterationItemNotSet
from data_factory_testing_framework.models.state.pipeline_run_state import PipelineRunState


def find_and_replace_iteration_item(expression: str, state: PipelineRunState):
    pattern = r"(@?{?item\(\)\}?)"
    matches = re.finditer(pattern, expression, re.MULTILINE)
    for match in matches:
        if state.iteration_item is None:
            raise StateIterationItemNotSet()

        expression = expression.replace(match.group(0), state.iteration_item)

    return expression
