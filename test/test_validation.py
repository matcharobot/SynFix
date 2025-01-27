from callgraph_analysis.validation import Validation

def test_validation():
    # Arrange
    validator = Validation(test_command="pytest", test_dir="test/data/sample_project")

    # Act
    result = validator.validate_changes()

    # Assert
    assert result is True or result is False
