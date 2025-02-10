from fastapi import FastAPI
import logging

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)

@app.get("/")
def root():
    return {"message": "Hello from service_3!"}

@app.post("/orders")
async def process_order(order: dict):
    """Process incoming orders from RabbitMQ via Dapr Pub/Sub"""
    logging.info(f"Received order: {order}")

    user_id = order.get("userId")
    items = order.get("items")

    if not user_id or not items:
        return {"error": "Invalid order format"}

    return {"message": "Order processed successfully", "userId": user_id, "items": items}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8030)
