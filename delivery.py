import logging

from fastapi import FastAPI
from opentelemetry import trace

app = FastAPI()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create console handler and set level to debug
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Creates a tracer from the global tracer provider
tracer = trace.get_tracer("pizza-delivery.workshop")

# Create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Add formatter to console handler
console_handler.setFormatter(formatter)

# Add console handler to logger
logger.addHandler(console_handler)


@app.post('/delivery')
async def deliver_pizza():
    logger.info("Deliver pizza via Eleme")

    return {"status": "Pizza delivered"}
