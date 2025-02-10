from fastapi import FastAPI
import requests

app = FastAPI()

# Correct Dapr HTTP Port for service_1
DAPR_HTTP_PORT_SERVICE1 = 3500  # Dapr HTTP Port for service_1
DAPR_HTTP_PORT_SERVICE2 = 3600
SERVICE_NAME = "api_1"  # Must match --app-id of `service_1`
DAPR_PUBSUB_NAME = "orderpubsub"  # Must match the component name in rabbitmq.yaml
TOPIC_NAME = "orders"

# Base URL for Service Invocation
BASE_URL = f"http://localhost:{DAPR_HTTP_PORT_SERVICE1}/v1.0/invoke/{SERVICE_NAME}/method"
DAPR_PUBSUB_URL = f"http://localhost:{DAPR_HTTP_PORT_SERVICE2}/v1.0/publish/{DAPR_PUBSUB_NAME}/{TOPIC_NAME}"

@app.get("/")
def root():
    return {"message": "Hello from service_2!"}

@app.post("/invoke-save-items")
def invoke_save_items():
    """Call service_1 to save items via Dapr Service Invocation"""
    response = requests.post(f"{BASE_URL}/save-items")

    if response.status_code == 200:
        return response.json()  # Directly return the response from service_1
    
    return {"error": "Failed to save item via service invocation", "status": response.status_code, "details": response.text}

@app.get("/fetch-items")
def fetch_items():
    """Call service_1 to get items via Dapr Service Invocation"""
    response = requests.get(f"{BASE_URL}/get-items")

    if response.status_code == 200:
        return response.json()  # Directly return the response from service_1

    return {"error": "Failed to fetch items via service invocation", "status": response.status_code, "details": response.text}


@app.post("/make-order")
def make_order(order: dict):
    """Publish an order to RabbitMQ via Dapr Pub/Sub"""
    headers = {"Content-Type": "application/json"}
    response = requests.post(DAPR_PUBSUB_URL, json=order, headers=headers)

    if response.status_code in [200, 204]:  # 204 = No content (Dapr successfully published)
        return {"message": "Order published successfully", "order": order}

    return {"error": "Failed to publish order", "status": response.status_code, "details": response.text}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8020)








# from fastapi import FastAPI
# import requests
# import json

# app = FastAPI()

# # Correct Dapr HTTP Ports
# DAPR_HTTP_PORT_SERVICE1 = 3500  # Dapr HTTP Port for service_1
# DAPR_HTTP_PORT_SERVICE2 = 3600  # Dapr HTTP Port for service_2
# SERVICE_NAME = "api_1"  # Must match --app-id of `service_1`
# STATE_STORE_NAME = "statestore"

# # Base URLs
# BASE_URL = f"http://localhost:{DAPR_HTTP_PORT_SERVICE1}/v1.0/invoke/{SERVICE_NAME}/method"
# DAPR_STATE_URL = f"http://localhost:{DAPR_HTTP_PORT_SERVICE2}/v1.0/state/{STATE_STORE_NAME}"


# @app.get("/")
# def root():
#     return {"message": "Hello from service_2!"}
# @app.post("/invoke-save-items")
# def invoke_save_items():
#     """Call service_1 to save items via Dapr Service Invocation and store all items in Dapr State Store"""
#     response = requests.post(f"{BASE_URL}/save-items")

#     if response.status_code == 200:
#         saved_item = response.json().get("item")

#         if saved_item:
#             # Step 1: Fetch all existing items from State Store
#             fetch_response = requests.get(f"{DAPR_STATE_URL}/items")

#             if fetch_response.status_code == 200:
#                 stored_items = fetch_response.json()

#                 # Ensure the response is a list; if it's a dict, wrap it in a list
#                 if not isinstance(stored_items, list):
#                     stored_items = [stored_items]
#             else:
#                 stored_items = []  # If no previous items, start fresh

#             # Step 2: Append the new item
#             stored_items.append(saved_item)

#             # Step 3: Save updated list to Dapr State Store (Ensure Correct JSON Structure)
#             state_data = [{"key": "items", "value": stored_items}]
#             headers = {"Content-Type": "application/json"}  # Ensure JSON is properly sent
#             state_response = requests.post(DAPR_STATE_URL, json=state_data, headers=headers)

#             if state_response.status_code in [200, 201]:
#                 return {"message": "Item saved successfully in state store", "items": stored_items}

#             return {"error": "Failed to save in state store", "status": state_response.status_code, "details": state_response.text}

#     return {"error": "Failed to save item via service invocation", "status": response.status_code, "details": response.text}


# @app.get("/fetch-items")
# def fetch_items():
#     """Fetch all items from Dapr State Store"""
#     response = requests.get(f"{DAPR_STATE_URL}/items")

#     if response.status_code == 200:
#         data = response.json()
#         if isinstance(data, list) and len(data) > 0:
#             return {"items": data}  # Return all stored items
#         return {"message": "No items found in state"}

#     elif response.status_code == 204:
#         return {"message": "No data found in the state store"}

#     return {"error": "Failed to fetch items", "status": response.status_code, "details": response.text}


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8020)
