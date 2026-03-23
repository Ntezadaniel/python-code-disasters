# bad_error_handling.py
# Source: Inspired by common patterns found in Flask open-source projects on GitHub
# This file demonstrates POORLY written error handling — used for analysis purposes

import requests
import json

# ----------------------------------------------------------------
# PROBLEM 1: Bare except clause — catches everything including
#            system exits and keyboard interrupts
# ----------------------------------------------------------------
def fetch_user_data(user_id):
    try:
        response = requests.get(f"https://api.example.com/users/{user_id}")
        data = response.json()
        return data
    except:
        print("something went wrong")
        return None


# ----------------------------------------------------------------
# PROBLEM 2: Swallowing exceptions silently — no logging,
#            no re-raise, caller never knows what failed
# ----------------------------------------------------------------
def read_config(filepath):
    try:
        with open(filepath, "r") as f:
            config = json.load(f)
        return config
    except Exception:
        pass  # silently ignored


# ----------------------------------------------------------------
# PROBLEM 3: Using generic Exception for everything —
#            no distinction between a file not found vs
#            a JSON parse error vs a permission error
# ----------------------------------------------------------------
def process_payment(amount, account_id):
    try:
        if amount <= 0:
            raise Exception("Bad amount")
        # simulate payment processing
        result = {"status": "success", "account": account_id, "amount": amount}
        return result
    except Exception as e:
        print(e)
        return None


# ----------------------------------------------------------------
# PROBLEM 4: No logging at all — impossible to debug in production
# ----------------------------------------------------------------
def delete_record(record_id, db_connection):
    try:
        db_connection.execute(f"DELETE FROM records WHERE id = {record_id}")
        db_connection.commit()
    except Exception as e:
        db_connection.rollback()
        return False
    return True


# ----------------------------------------------------------------
# PROBLEM 5: Catching and re-raising without preserving context
#            (loses the original traceback)
# ----------------------------------------------------------------
def load_model(model_path):
    try:
        with open(model_path, "rb") as f:
            model = f.read()
        return model
    except Exception as e:
        raise Exception("Model loading failed")  # original traceback lost
