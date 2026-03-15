# Imports
import unittest
from unittest.mock import patch
from utils import sum_numbers, create_user, filter_adults, find_in_list, parse_json, approximate_division


class TestUtils(unittest.TestCase):

    # Exact Equality Tests
    def test_sum_numbers_equals_expected(self):
        self.assertEqual(sum_numbers(2, 2), 4)

    def test_create_user_dict_equals_expected(self):
        fixed_time = __import__("datetime").datetime(2024, 1, 1, 12, 0, 0)
        with patch("utils.datetime") as mock_dt:
            mock_dt.now.return_value = fixed_time
            result = create_user("Alice", 30)

        expected = {"name": "Alice", "age": 30, "created_at": fixed_time}
        self.assertDictEqual(result, expected)

    def test_sum_numbers_identity(self):
        result = sum_numbers(2, 2)
        self.assertIs(result, 4)

    def test_create_user_dict_fails_on_wrong_age(self):
        fixed_time = __import__("datetime").datetime(2024, 1, 1)
        with patch("utils.datetime") as mock_dt:
            mock_dt.now.return_value = fixed_time
            result = create_user("Alice", 30)

        wrong_expected = {"name": "Alice", "age": 99, "created_at": fixed_time}
        self.assertNotEqual(result, wrong_expected)

    # Negation Tests
    def test_sum_not_equal_to_wrong_value(self):
        self.assertNotEqual(sum_numbers(1, 1), 3)

    def test_none_is_not_zero(self):
        self.assertIsNot(None, 0)

    def test_letter_not_in_string(self):
        self.assertNotIn("z", "apple")

    # Truthiness Tests
    def test_find_in_list_returns_true(self):
        self.assertTrue(find_in_list([1, 2, 3], 2))

    def test_find_in_list_returns_false(self):
        self.assertFalse(find_in_list([1, 2, 3], 4))

    def test_parse_json_none_on_null_string(self):
        self.assertIsNone(parse_json("null"))

    def test_create_user_is_not_none(self):
        self.assertIsNotNone(create_user("Bob", 25))

    # Number Matcher Tests
    def test_sum_is_greater_than_four(self):
        self.assertGreater(sum_numbers(2, 3), 4)

    def test_division_is_less_than_or_equal_to_five(self):
        self.assertLessEqual(approximate_division(10, 2), 5)

    def test_division_result_is_less_than_ten(self):
        self.assertLess(approximate_division(10, 3), 10)

    def test_sum_is_greater_than_or_equal_to_four(self):
        self.assertGreaterEqual(sum_numbers(2, 2), 4)

    def test_approximate_division_close_to_three(self):
        self.assertAlmostEqual(approximate_division(0.3, 0.1), 3.0, places=5)

    def test_approximate_division_not_close_to_ten(self):
        self.assertNotAlmostEqual(approximate_division(0.3, 0.1), 10.0, places=5)

    # String Matcher Tests
    def test_string_matches_regex(self):
        self.assertRegex("Hello World", r"World")

    def test_string_does_not_match_regex(self):
        self.assertNotRegex("Hello World", r"Python")

    def test_user_name_matches_pattern(self):
        user = create_user("Alice123", 25)
        self.assertRegex(user["name"], r"^[A-Za-z0-9]+$")

    # Array/Iterable Tests
    def test_name_in_users_list(self):
        users = ["Alice", "Bob", "Charlie"]
        self.assertIn("Alice", users)

    def test_name_not_in_users_list(self):
        users = ["Alice", "Bob", "Charlie"]
        self.assertNotIn("David", users)

    def test_filter_adults_contains_valid_user(self):
        users = [{"name": "Alice", "age": 30}, {"name": "Kid", "age": 10}]
        adults = filter_adults(users)
        self.assertIn({"name": "Alice", "age": 30}, adults)

    def test_filter_adults_excludes_minor(self):
        users = [{"name": "Alice", "age": 30}, {"name": "Kid", "age": 10}]
        adults = filter_adults(users)
        self.assertNotIn({"name": "Kid", "age": 10}, adults)

    # Exception Handling Tests
    def test_parse_json_raises_on_none(self):
        with self.assertRaises(ValueError):
            parse_json(None)

    def test_parse_json_raises_with_correct_message(self):
        with self.assertRaisesRegex(ValueError, "No JSON string provided"):
            parse_json("")

    def test_parse_json_raises_on_invalid_json(self):
        with self.assertRaises(ValueError):
            parse_json("{bad json}")

    def test_parse_json_does_not_raise_on_valid_input(self):
        try:
            result = parse_json('{"name": "Alice"}')
            self.assertEqual(result["name"], "Alice")
        except Exception:
            self.fail("parse_json raised an exception on valid JSON")


if __name__ == "__main__":
    unittest.main()
