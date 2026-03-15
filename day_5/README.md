# TDD Day 5 Exercises

This directory contains several exercises focused on advanced **Test-Driven Development (TDD)** concepts in Python. The primarily goal is to learn how to test code in isolation when it depends on external services, APIs, databases, or secondary functions.

## Context & Key Takeaways

In real-world applications, your logic usually relies on external systems:
- A database might be down.
- An email service charges per API call.
- A weather API provides constantly changing data.

**Key Takeaway**: You shouldn't hit real databases, networks, or external APIs in your unit tests. Instead, you use **Test Doubles** (Mocks, Fakes, Stubs) to isolate your code. This makes tests fast, deterministic (always returning the same results), and free of side effects. Pytest fixtures also help to cleanly scaffold and provision these dependencies before tests run.

---

## Hands-On Exercise Implementations

Here is a breakdown of how the tasks from the exercise were implemented:

### 1. `WeatherAlertService`
*   **Task**: Stub `get_temperature()` / `getTemperature()` to return controlled values. Test HIGH / LOW / NORMAL alert logic without hitting any real API.
*   **Implementation**: Used `@patch('weather.get_temperature')` to replace the real temperature API. By setting `mock_get.return_value = 55`, `30`, or `5`, we deterministically tested the `"HIGH"`, `"NORMAL"`, and `"LOW"` alert strings.

### 2. `OrderEmailService`
*   **Task**: Mock the email sender. Verify it's called with the correct recipient and subject when an order is placed. Verify it's NOT called when order fails.
*   **Implementation**: 
    - Used `@pytest.fixture` to instantiate a reusable `OrderEmailService`.
    - Used `@patch('order.send_email')` to completely replace the actual email sending function. Verified behavior using `mock_send_email.assert_called_with(email, "Order Placed")` on success, and asserted no emails were sent on failure using `mock_send_email.assert_not_called()`.

### 3. `UserRepository` (Fake)
*   **Task**: Build an in-memory `FakeUserRepository`. Use it to test a `UserService` that saves, finds, and lists users — multiple operations in one test.
*   **Implementation**: Created a `FakeUserRepository` class that acts exactly like a database but stores records in an internal Python dictionary. Injected the fake repository into `UserService(repo)`. The tests then verify the state of this fake repository for `register_user`, `get_user`, and `list_users` without a real database connection.

### Bonus: Spy on Logger
*   **Task**: Use `jest.spyOn` / `patch(wraps=)` to assert that your service logs a warning when given invalid input — without mocking the logger completely.
*   **Implementation**: Used the `@patch('logger.log_warning', wraps=logger.log_warning)` decorator to spy on the internal `log_warning` function. We verified the behavior by using `mock_log.assert_called_with("Empty input received!")` to guarantee the system logged a warning on invalid input.

---

## TDD Rules of Thumb

As emphasized in the exercise, these are the golden rules followed across these implementations:
- **Write the failing test FIRST**
- **Mock only what you don't own**
- **Never mock the unit under test**
- **One assert per behaviour**
- **Reset mocks between tests**
- **Tests must run in under 100 ms**
