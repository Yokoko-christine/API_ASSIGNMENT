payments_api/
│
├── app/
│   ├── main.py                  # FastAPI instantiation, startup events, and global exception handlers
│   ├── routes/                  # HTTP Endpoints (Task 4 & 5)
│   │   ├── customers.py
│   │   ├── payments.py
│   │   └── refunds.py
│   ├── services/                # Core Business Logic (Task 2)
│   │   └── payment_service.py
│   ├── repos/                   # In-Memory Storage & Querying (Task 3)
│   │   └── fake_payment_repo.py
│   └── utils/                   # Pure Functions & Data Checks (Task 1)
│       └── validators.py
│
├── tests/                       # Mirrored structure isolating test concerns
│   ├── unit/                    # Task 1
│   ├── services/                # Task 2
│   ├── repos/                   # Task 3
│   └── routes/                  # Task 4 & 5
│
├── pyproject.toml               # Modern standard packaging, uv config, and pytest paths
(empty)
