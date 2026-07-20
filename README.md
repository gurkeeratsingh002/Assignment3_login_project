# Assignment 3 - Login Black-Box Testing

## Run the project
```bash
python -m pip install -r requirements.txt
python app.py
```

## Run all tests
```bash
pytest -v
```

Demo login:
- Email: `student@example.com`
- Password: `Password123`

The implementation validates email format and length (maximum 254 characters), and password length (8 to 64 characters), before authenticating the user.
