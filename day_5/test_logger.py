from unittest.mock import patch
import logger

@patch('logger.log_warning', wraps=logger.log_warning)
def test_input_validator_logs_warning_for_empty_input(logs):
    validator = logger.InputValidator()
    result = validator.validate("")
    assert result == False
    logs.assert_called_with("Empty input received!")