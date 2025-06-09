from loguru import logger

logger.add('model-debug.log',
           level='DEBUG',
           rotation='5 MB',
           retention="2 days",
           enqueue=True,
           backtrace=True,
           diagnose=True,
           compression="zip")

logger.add('model-info.log',
           level='INFO',
           rotation='5 MB',
           retention="2 days",
           enqueue=True,
           backtrace=True,
           diagnose=True,
           compression="zip")
