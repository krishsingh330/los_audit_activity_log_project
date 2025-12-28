from loguru import logger
import sys
import os


def setup_logger():
    logger.remove()

    # Console logger
    logger.add(
        sys.stdout,
        level="INFO",
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
               "<level>{level}</level> | "
               "<cyan>{name}</cyan>:<cyan>{function}</cyan> | "
               "{message}",
    )

    os.makedirs("logs", exist_ok=True)

    # INFO & WARNING logs
    logger.add(
        "logs/app_{time:YYYY-MM-DD}.log",
        rotation="00:00",
        retention="7 days",
        level="INFO",
        enqueue=True,
        backtrace=False, 
        diagnose=False,    
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    )
    
    # ERROR ONLY 
    logger.add(
        "logs/error_{time:YYYY-MM-DD}.log",
        rotation="00:00",
        retention="14 days",
        level="ERROR",
        enqueue=True,
        backtrace=False,
        diagnose=False,    
        format="{time:YYYY-MM-DD HH:mm:ss} | ERROR | {message}",
    )

    return logger
