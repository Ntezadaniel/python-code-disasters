# improved_error_handling.py
# Improved version of bad_error_handling.py
# Fixes: specific exceptions, meaningful logging, preserved tracebacks

import requests
import json
import logging
import logging.config


# LOGGING CONFIGURATION
# Sets up a logger that writes to both console and a log file

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    handlers=[
        logging.StreamHandler(),                        # console output
        logging.FileHandler("app.log", encoding="utf-8")  # file output
    ]
)
logger = logging.getLogger(__name__)



# FIX 1: Replace bare except with specific exceptions
#         Log the error with context before returning

def fetch_user_data(user_id):
    """Fetch user data from external API with proper error handling."""
    url = f"https://api.example.com/users/{user_id}"
    logger.info("Fetching user data for user_id=%s", user_id)
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()           # raises HTTPError for 4xx/5xx
        data = response.json()
        logger.debug("Successfully fetched data for user_id=%s", user_id)
        return data
    except requests.exceptions.ConnectionError:
        logger.error("Network error: could not reach %s", url)
    except requests.exceptions.Timeout:
        logger.error("Request timed out for user_id=%s (url=%s)", user_id, url)
    except requests.exceptions.HTTPError as e:
        logger.error("HTTP error for user_id=%s: %s", user_id, e)
    except requests.exceptions.JSONDecodeError:
        logger.error("Response for user_id=%s was not valid JSON", user_id)
    return None



# FIX 2: Never silently swallow exceptions
#         Log clearly, and let callers handle the failure

def read_config(filepath):
    """Read and parse a JSON config file."""
    logger.info("Reading config file: %s", filepath)
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            config = json.load(f)
        logger.debug("Config loaded successfully from %s", filepath)
        return config
    except FileNotFoundError:
        logger.error("Config file not found: %s", filepath)
        raise                                   # re-raise so caller can decide
    except PermissionError:
        logger.error("Permission denied reading config: %s", filepath)
        raise
    except json.JSONDecodeError as e:
        logger.error("Config file %s contains invalid JSON: %s", filepath, e)
        raise



# FIX 3: Use specific, meaningful custom exceptions
#         instead of a generic Exception

class InvalidPaymentAmountError(ValueError):
    """Raised when a payment amount is zero or negative."""

class PaymentProcessingError(RuntimeError):
    """Raised when payment processing fails unexpectedly."""

def process_payment(amount, account_id):
    """Process a payment with validated inputs and meaningful exceptions."""
    logger.info("Processing payment: amount=%.2f account_id=%s", amount, account_id)
    if not isinstance(amount, (int, float)):
        raise TypeError(f"amount must be numeric, got {type(amount).__name__}")
    if amount <= 0:
        logger.warning("Invalid payment amount %.2f for account %s", amount, account_id)
        raise InvalidPaymentAmountError(
            f"Payment amount must be positive, got {amount}"
        )
    try:
        # simulate payment processing
        result = {"status": "success", "account": account_id, "amount": amount}
        logger.info("Payment successful for account_id=%s amount=%.2f", account_id, amount)
        return result
    except Exception as e:
        logger.exception("Unexpected error processing payment for account_id=%s", account_id)
        raise PaymentProcessingError("Payment processing failed") from e



# FIX 4: Add structured logging around every meaningful operation
#         so production issues are traceable

def delete_record(record_id, db_connection):
    """Delete a record from the database with full audit logging."""
    logger.info("Attempting to delete record_id=%s", record_id)
    try:
        db_connection.execute(
            "DELETE FROM records WHERE id = ?", (record_id,)  # parameterized query
        )
        db_connection.commit()
        logger.info("Record deleted successfully: record_id=%s", record_id)
        return True
    except Exception as e:
        logger.error(
            "Failed to delete record_id=%s, rolling back. Error: %s",
            record_id, e
        )
        db_connection.rollback()
        return False



# FIX 5: Preserve exception context using `raise ... from e`
#         so the full traceback chain is visible in logs

def load_model(model_path):
    """Load a binary model file with full traceback preservation."""
    logger.info("Loading model from path: %s", model_path)
    try:
        with open(model_path, "rb") as f:
            model = f.read()
        logger.debug("Model loaded successfully (%d bytes) from %s", len(model), model_path)
        return model
    except FileNotFoundError as e:
        logger.error("Model file not found: %s", model_path)
        raise FileNotFoundError(f"Model not found at '{model_path}'") from e  # preserves chain
    except OSError as e:
        logger.error("OS error reading model file %s: %s", model_path, e)
        raise RuntimeError(f"Failed to load model from '{model_path}'") from e
