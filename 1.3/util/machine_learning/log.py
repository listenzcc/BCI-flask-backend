from loguru import logger
from datetime import datetime

t = datetime.strftime(datetime.now(), '%Y%m%d-%H%M%S')

logger.add(f'log/model-debug.{t}.log',
           level='DEBUG',
           enqueue=True,
           backtrace=True,
           diagnose=True,
           )

logger.add(f'log/model-info.{t}.log',
           level='INFO',
           enqueue=True,
           backtrace=True,
           diagnose=True,
           )
