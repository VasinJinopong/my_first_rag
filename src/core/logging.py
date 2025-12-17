import logging
import sys

def setup_logging():
    """Configure structure"""
    
    logger = logging.getLogger("document-qa")
    logger.setLevel(logging.INFO)
    
    logger.handlers = []
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    console_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    
    return logger

logger = setup_logging()

def log_request(endpoint: str, method: str, **kwargs):
    """Log API request"""
    logger.info(f"Request: {method} {endpoint}", extra=kwargs)
    
def log_error(error: Exception, context: str = ""):
    """Log error with context"""
    logger.error(f"Error in {context}: {str(error)}", exc_info=True)
    
def log_performance(operation:str, duration:float, **kwargs):
    """Log performance metrics"""
    logger.info(f"Performance: {operation} took {duration:.2f}s" ,extra=kwargs)
    