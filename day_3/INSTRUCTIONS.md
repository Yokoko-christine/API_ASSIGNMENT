# 🧪 Assignment: Utility Module Testing (Python Version)

## Context

You have a small Python utility module that provides several simple functions. You'll write unit tests for this module using Python's `unittest` framework. Your goal is to cover all the common Jest matchers (translated to their Python equivalents):

| Jest Matcher | Python Equivalent (`unittest`) |
|---|---|
| `toBe` | `assertIs` / `assertEqual` |
| `toEqual` | `assertEqual` |
| `toStrictEqual` | `assertDictEqual`, `assertListEqual`, etc. |
| `.not` | `assertNotEqual`, `assertIsNot`, `assertNotIn`, etc. |
| Truthiness (`toBeNull`, etc.) | `assertIsNone`, `assertIsNotNone`, `assertTrue`, `assertFalse` |
| Number matchers | `assertGreater`, `assertLessEqual`, etc. |
| `toBeCloseTo` | `assertAlmostEqual` |
| `toMatch` | regex via `assertRegex`, `assertNotRegex` |
| `toContain` | `assertIn`, `assertNotIn` |
| `toThrow` | `assertRaises` |

---

## 🧩 Provided Module — `utils.py`
```python
# utils.py
import json
from datetime import datetime

def sum_numbers(a, b):
    return a + b

def create_user(name, age):
    return {
        "name": name,
        "age": age,
        "created_at": datetime.now()
    }

def filter_adults(users):
    return [user for user in users if user["age"] >= 18]

def find_in_list(lst, value):
    return value in lst

def parse_json(json_string):
    if not json_string:
        raise ValueError("No JSON string provided")
    return json.loads(json_string)

def approximate_division(a, b):
    return a / b
```

---

## 🧠 Your Task

Write a test file named **`test_utils.py`**. Your tests should use `unittest.TestCase` and include **at least one passing and one failing test** for each matcher type.

Each section below corresponds to Jest's *"Using Matchers"* documentation.

---

### 1. Exact Equality

✅ **Use:** `assertEqual`, `assertDictEqual`, `assertListEqual`, `assertIs`
```python
self.assertEqual(sum_numbers(2, 2), 4)                          # like toBe
self.assertDictEqual(create_user("Alice", 30), expected_user)   # like toEqual
self.assertIs(sum_numbers(2, 2), 4)                             # same identity
```

> 💡 **Failing test example:** compare dictionaries that differ slightly.

---

### 2. Negation (`.not`)

✅ **Use:** `assertNotEqual`, `assertIsNot`, `assertNotIn`
```python
self.assertNotEqual(sum_numbers(1, 1), 3)
self.assertIsNot(None, 0)
self.assertNotIn("z", "apple")
```

---

### 3. Truthiness

✅ **Use:** `assertIsNone`, `assertIsNotNone`, `assertTrue`, `assertFalse`
```python
self.assertTrue(find_in_list([1, 2, 3], 2))
self.assertFalse(find_in_list([1, 2, 3], 4))
self.assertIsNone(None)
self.assertIsNotNone(create_user("Bob", 25))
```

---

### 4. Number Matchers

✅ **Use:** `assertGreater`, `assertGreaterEqual`, `assertLess`, `assertLessEqual`, `assertAlmostEqual`
```python
self.assertGreater(sum_numbers(2, 3), 4)
self.assertLessEqual(approximate_division(10, 2), 5)
self.assertAlmostEqual(approximate_division(0.3, 0.1), 3.0, places=5)
```

---

### 5. String Matchers

✅ **Use:** `assertRegex`, `assertNotRegex`
```python
self.assertRegex("Hello World", r"World")
self.assertNotRegex("Hello World", r"Python")
```

---

### 6. Arrays / Iterables

✅ **Use:** `assertIn`, `assertNotIn`
```python
users = ["Alice", "Bob", "Charlie"]
self.assertIn("Alice", users)
self.assertNotIn("David", users)
```

---

### 7. Exceptions

✅ **Use:** `assertRaises`
```python
with self.assertRaises(ValueError):
    parse_json(None)

# Optional: check message
with self.assertRaisesRegex(ValueError, "No JSON string provided"):
    parse_json("")
```

---

## 🧾 Assignment Deliverables

1. `utils.py` — provided above.
2. `test_utils.py` — your test file covering all matcher equivalents.
3. *(Optional)* `README.md` — explaining each test and its corresponding Jest matcher.

---

## 📊 Evaluation Criteria

| Criteria | Description |
|---|---|
| ✅ Coverage | All Jest matchers mapped to Python equivalents |
| 💡 Correctness | Assertions accurately represent the intended matcher |
| 🧱 Structure | Uses `unittest.TestCase` with meaningful test names |
| 🔄 Determinism | Tests give consistent results (no random or time-dependent values unless mocked) |
| 🧩 Clarity | Each test clearly labeled with a comment explaining which Jest matcher it mirrors |