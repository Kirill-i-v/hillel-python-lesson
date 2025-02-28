import time
import logging


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class TimerContext:
    def __enter__(self):
        self.start_time = time.time()
        logging.info("Timer started.")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        elapsed_time = time.time() - self.start_time
        logging.info(f"Execution time: {elapsed_time:.4f} seconds")


if __name__ == "__main__":
    with TimerContext():
        time.sleep(2)


GLOBAL_CONFIG = {
    "feature_a": True,
    "feature_b": False,
    "max_retries": 3
}


class Configuration:
    def __init__(self, updates, validator=None):
        self.updates = updates
        self.validator = validator
        self.original_config = None

    def __enter__(self):
        self.original_config = GLOBAL_CONFIG.copy()

        GLOBAL_CONFIG.update(self.updates)
        logging.info("Applied configuration updates: %s", self.updates)

        if self.validator and not self.validator(GLOBAL_CONFIG):
            logging.error("Validation failed during entry. Restoring original configuration.")
            GLOBAL_CONFIG.clear()
            GLOBAL_CONFIG.update(self.original_config)
            raise ValueError("Invalid configuration provided.")

    def __exit__(self, exc_type, exc_value, traceback):
        GLOBAL_CONFIG.clear()
        GLOBAL_CONFIG.update(self.original_config)
        logging.info("Restored original configuration.")


def validate_config(config: dict) -> bool:
    if not isinstance(config.get('max_retries', 0), int) or config['max_retries'] < 0:
        logging.error("Invalid 'max_retries' value: %s", config['max_retries'])
        return False
    if not isinstance(config.get('feature_a', True), bool):
        logging.error("Invalid 'feature_a' value: %s", config['feature_a'])
        return False
    return True


if __name__ == "__main__":
    logging.info("Initial GLOBAL_CONFIG: %s", GLOBAL_CONFIG)

    try:
        with Configuration({"feature_a": False, "max_retries": 5}):
            logging.info("Inside context: %s", GLOBAL_CONFIG)
    except Exception as e:
        logging.error("Error: %s", e)

    logging.info("After context: %s", GLOBAL_CONFIG)

    try:
        with Configuration({"feature_a": "invalid_value", "max_retries": -1}, validator=validate_config):
            logging.info("This should not be printed if validation fails.")
    except Exception as e:
        logging.error("Caught exception: %s", e)

    logging.info("After failed context: %s", GLOBAL_CONFIG)
