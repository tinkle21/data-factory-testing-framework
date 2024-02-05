from lark import Tree

from data_factory_testing_framework.exceptions.expression_evaluation_error import ExpressionEvaluationError
from data_factory_testing_framework.functions.evaluator.exceptions import ExpressionEvaluationInvalidChildTypeError
from data_factory_testing_framework.functions.evaluator.rules.expression_rule import EvaluationResult

from .expression_rule import ExpressionRuleEvaluator


class EvaluationExpressionRuleEvaluator(ExpressionRuleEvaluator):
    def __init__(self, tree: Tree) -> None:
        """Initializes the expression rule evaluator."""
        super().__init__(tree)

        if len(self.children) < 1:
            raise ExpressionEvaluationError(
                f"Invalid number of children. Minimum required: 1, Actual: {len(self.children)}"
            )

        if not isinstance(self.children[0], ExpressionRuleEvaluator):
            raise ExpressionEvaluationInvalidChildTypeError(
                child_index=0, expected_types=ExpressionRuleEvaluator, actual_type=type(self.children[0])
            )

        for i, child in enumerate(self.children[1:]):
            if not isinstance(child, EvaluationResult):
                raise ExpressionEvaluationInvalidChildTypeError(
                    child_index=i + 1, expected_types=EvaluationResult, actual_type=type(child)
                )

        self.expression = self.children[0]
        self.accessors = self.children[1:]

    def evaluate(self) -> EvaluationResult:
        expression_value = self.evaluate_child(self.expression)

        current_value = expression_value.value
        for accessor in self.accessors:
            current_value = current_value[accessor.value]

        return EvaluationResult(current_value)
