import subprocess
import os

class Validation:
    """
    Handles validation of changes in the codebase by executing regression tests and ensuring correctness.
    """

    def __init__(self, test_command="pytest", test_dir="tests"):
        """
        Initializes the Validation class.

        :param test_command: The command to run the tests (default is pytest).
        :param test_dir: The directory containing the test files.
        """
        self.test_command = test_command
        self.test_dir = test_dir

    def validate_changes(self):
        """
        Executes regression tests to validate the changes in the codebase.

        :return: True if all tests pass, False otherwise.
        """
        print(f"Running regression tests using {self.test_command} in {self.test_dir}...")

        if not os.path.exists(self.test_dir):
            print(f"Error: Test directory '{self.test_dir}' does not exist.")
            return False

        try:
            result = subprocess.run(
                [self.test_command, self.test_dir],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            print("Test Output:")
            print(result.stdout)
            print("Test Errors:")
            print(result.stderr)

            if result.returncode == 0:
                print("All tests passed successfully.")
                return True
            else:
                print("Some tests failed.")
                return False
        except FileNotFoundError as e:
            print(f"Error: {self.test_command} is not installed or not found in PATH.")
            print(str(e))
            return False
        except Exception as e:
            print("An unexpected error occurred while running tests:")
            print(str(e))
            return False

    def validate_specific_test(self, test_file):
        """
        Runs a specific test file to validate changes.

        :param test_file: The test file to execute.
        :return: True if the test passes, False otherwise.
        """
        print(f"Running specific test: {test_file}...")

        if not os.path.exists(test_file):
            print(f"Error: Test file '{test_file}' does not exist.")
            return False

        try:
            result = subprocess.run(
                [self.test_command, test_file],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            print("Test Output:")
            print(result.stdout)
            print("Test Errors:")
            print(result.stderr)

            if result.returncode == 0:
                print(f"Test {test_file} passed successfully.")
                return True
            else:
                print(f"Test {test_file} failed.")
                return False
        except FileNotFoundError as e:
            print(f"Error: {self.test_command} is not installed or not found in PATH.")
            print(str(e))
            return False
        except Exception as e:
            print("An unexpected error occurred while running the test:")
            print(str(e))
            return False


