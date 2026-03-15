# 🧪 test_utils.py — Test Documentation

This file explains every test in `test_utils.py`, what it checks, and which **Jest matcher** it maps to in Python's `unittest` framework.

---

## 1. Exact Equality

These tests verify that two values are exactly equal — either by value or by identity.

| Test | Jest Equivalent | Python Method |
|---|---|---|
| `test_sum_numbers_equals_expected` | `toBe` | `assertEqual` |
| `test_create_user_dict_equals_expected` | `toEqual` | `assertDictEqual` |
| `test_sum_numbers_identity` | `toBe` (identity) | `assertIs` |
| `test_create_user_dict_fails_on_wrong_age` | `.not.toEqual` | `assertNotEqual` |

### Notes

- `assertEqual` checks **value equality** — two things that look the same pass, even if they're different objects.
- `assertIs` checks **identity** — both variables must point to the exact same object in memory. This works for small integers in Python (like `4`) because Python caches them internally.
- `assertDictEqual` is a stricter version of `assertEqual` for dictionaries — it gives a clearer diff when the test fails.
- The `datetime.now()` call inside `create_user()` is **mocked** using `unittest.mock.patch` so the test doesn't fail due to a timestamp changing every millisecond.

---

## 2. Negation (`.not`)

These tests verify that two values are **not** equal, not the same object, or that something is not contained somewhere.

| Test | Jest Equivalent | Python Method |
|---|---|---|
| `test_sum_not_equal_to_wrong_value` | `.not.toBe` | `assertNotEqual` |
| `test_none_is_not_zero` | `.not.toBe` | `assertIsNot` |
| `test_letter_not_in_string` | `.not.toContain` | `assertNotIn` |

### Notes

- `assertNotEqual` is the direct inverse of `assertEqual`.
- `assertIsNot` checks that two things are **not the same object** in memory (inverse of `assertIs`).
- `assertNotIn` works for both strings and lists — it checks that a value does not appear inside a container.

---

## 3. Truthiness

These tests check whether a value is truthy, falsy, `None`, or not `None`.

| Test | Jest Equivalent | Python Method |
|---|---|---|
| `test_find_in_list_returns_true` | `toBeTruthy` | `assertTrue` |
| `test_find_in_list_returns_false` | `toBeFalsy` | `assertFalse` |
| `test_none_is_null` | `toBeNull` | `assertIsNone` |
| `test_create_user_is_not_none` | `.not.toBeNull` | `assertIsNotNone` |

### Notes

- `assertTrue` / `assertFalse` accept any expression — they don't require a boolean, just something that evaluates to truthy or falsy.
- `assertIsNone` is stricter than `assertFalse` — it requires the value to be **exactly** `None`, not just falsy (so `0` or `""` would fail it).
- `assertIsNotNone` mirrors Jest's `.not.toBeNull()` — it passes as long as the value is anything other than `None`.

---

## 4. Number Matchers

These tests verify numeric comparisons and floating-point precision.

| Test | Jest Equivalent | Python Method |
|---|---|---|
| `test_sum_is_greater_than_four` | `toBeGreaterThan` | `assertGreater` |
| `test_division_is_less_than_or_equal_to_five` | `toBeLessThanOrEqual` | `assertLessEqual` |
| `test_division_result_is_less_than_ten` | `toBeLessThan` | `assertLess` |
| `test_sum_is_greater_than_or_equal_to_four` | `toBeGreaterThanOrEqual` | `assertGreaterEqual` |
| `test_approximate_division_close_to_three` | `toBeCloseTo` | `assertAlmostEqual` |
| `test_approximate_division_not_close_to_ten` | `.not.toBeCloseTo` | `assertNotAlmostEqual` |

### Notes

- `assertAlmostEqual` is the Python equivalent of Jest's `toBeCloseTo`. It exists because floating-point arithmetic is imprecise — `0.3 / 0.1` in Python gives `2.9999999999999996`, not exactly `3.0`. The `places=5` argument means "match to 5 decimal places", which is enough to handle normal floating-point drift.
- All other comparison methods (`assertGreater`, `assertLess`, etc.) map cleanly to their Jest counterparts.

---

## 5. String Matchers

These tests use regular expressions to check whether a string matches a pattern.

| Test | Jest Equivalent | Python Method |
|---|---|---|
| `test_string_matches_regex` | `toMatch` | `assertRegex` |
| `test_string_does_not_match_regex` | `.not.toMatch` | `assertNotRegex` |
| `test_user_name_matches_pattern` | `toMatch` | `assertRegex` |

### Notes

- `assertRegex(string, pattern)` checks that a string contains a match for the regex pattern — equivalent to Jest's `toMatch(/pattern/)`.
- `assertNotRegex` is the inverse.
- The third test uses a regex (`^[A-Za-z0-9]+$`) to validate that a username only contains letters and numbers — a practical real-world use case.

---

## 6. Arrays / Iterables

These tests check whether a value appears (or does not appear) inside a list or collection.

| Test | Jest Equivalent | Python Method |
|---|---|---|
| `test_name_in_users_list` | `toContain` | `assertIn` |
| `test_name_not_in_users_list` | `.not.toContain` | `assertNotIn` |
| `test_filter_adults_contains_valid_user` | `toContain` | `assertIn` |
| `test_filter_adults_excludes_minor` | `.not.toContain` | `assertNotIn` |

### Notes

- `assertIn(value, container)` works for lists, strings, sets, and dictionaries.
- The last two tests go further by using `filter_adults()` to generate a list first, then asserting the correct users are included or excluded — this is closer to how you'd test real application logic.

---

## 7. Exceptions

These tests check that a function raises an error under the right conditions.

| Test | Jest Equivalent | Python Method |
|---|---|---|
| `test_parse_json_raises_on_none` | `toThrow` | `assertRaises` |
| `test_parse_json_raises_with_correct_message` | `toThrowError("message")` | `assertRaisesRegex` |
| `test_parse_json_raises_on_invalid_json` | `toThrow` | `assertRaises` |
| `test_parse_json_does_not_raise_on_valid_input` | `.not.toThrow` | `try/except` + `self.fail()` |

### Notes

- `assertRaises` is used as a **context manager** (`with self.assertRaises(...):`) — any code inside the `with` block is expected to raise the specified exception.
- `assertRaisesRegex` adds a check on the **error message**, not just the exception type — equivalent to Jest's `toThrowError("expected message")`.
- Python's `json.JSONDecodeError` is a subclass of `ValueError`, so `assertRaises(ValueError)` catches both.
- The "not throw" case (`test_parse_json_does_not_raise_on_valid_input`) uses a plain `try/except` block with `self.fail()` — there's no built-in `assertDoesNotRaise` in Python's `unittest`, so this is the standard pattern.

---

## Running the Tests

```bash
python -m unittest test_utils.py -v
```

The `-v` flag enables verbose output, showing the name and result of each individual test.