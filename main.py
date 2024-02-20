import logging
import random

import requests
from fastapi import FastAPI, HTTPException
from opentelemetry import trace
import redis
app = FastAPI()

from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import (
    ConsoleMetricExporter,
    PeriodicExportingMetricReader,
)

metric_reader = PeriodicExportingMetricReader(ConsoleMetricExporter())
provider = MeterProvider(metric_readers=[metric_reader])

# Sets the global default meter provider
metrics.set_meter_provider(provider)

# Creates a meter from the global meter provider
meter = metrics.get_meter("pizza.app.meter")

pizzas_delivered_counter = meter.create_counter(
    "pizzas.delivered", unit="1", description="Counts the amount of pizzas delivered"
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create console handler and set level to debug
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Creates a tracer from the global tracer provider
tracer = trace.get_tracer("pizza-app.workshop")

# Create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Add formatter to console handler
console_handler.setFormatter(formatter)

# Add console handler to logger
logger.addHandler(console_handler)

# Connect to Redis
# Replace 'localhost' and '6379' with your Redis server's host and port if different
redis_client = redis.Redis(host='localhost', port=6379, db=0)


def prepare_dough():
    with tracer.start_as_current_span("prepare_dough"):
        logger.info("Preparing dough")


def add_toppings():
    with tracer.start_as_current_span("add_toppings"):
        logger.info("Adding toppings", extra={"topping1": "pepperoni", "topping2": "cheese"})


def bake_pizza():
    with tracer.start_as_current_span("bake_pizza"):
        oven_id = random.randint(1, 1000)
        redis_key = "pizza_oven_"+str(oven_id)
        redis_client.set(redis_key, "baking pizza in oven")
        logger.info("Baking pizza in oven")
        if random.random() < 0.5:
            logger.error('Pizza has burnt!')
            # Return an error response 50% of the time
            raise HTTPException(status_code=500, detail='Pizza has burnt!')
        redis_client.get(redis_key)
        logger.info("Baking pizza finished")


def deliver_pizza():
    with tracer.start_as_current_span("deliver_pizza"):
        logger.info("Delivering pizza")
        response = requests.post('http://localhost:8001/delivery')

        logger.info('Pizza delivered via Eleme %s', response)
        if response.status_code == 200:
            pizzas_delivered_counter.add(1)
            return response.json()
        else:
            # Handle errors
            raise HTTPException(status_code=500, detail='Failed to deliver pizza via Eleme')


@app.post('/pizza')
async def order_pizza():
    logger.info("Order pizza")

    prepare_dough()
    add_toppings()
    bake_pizza()
    deliver_pizza()

    logger.info("Pizza delivered")

    return {"status": "Pizza delivered"}
