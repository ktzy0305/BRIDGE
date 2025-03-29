from dotenv import load_dotenv

import logging, os

logger = logging.getLogger(__name__)

load_dotenv()

def load_environment_variable(variable_name: str) -> str:
    """
    Load an environment variable and throws an exception if not set.
    """
    
    value = os.getenv(variable_name)
    
    if not value:
        logger.error(f"Environment variable {variable_name} is not set.")
        raise EnvironmentError(
            f"Environment variable {variable_name} is not set."
        )        
    
    return value