from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

connected_clients = set()  # Keep track of connected clients.

@app.websocket("/ws/{client}")  # Define a WebSocket route that takes a "client" parameter.
async def websocket_endpoint(websocket: WebSocket, client: str):  # Asynchronous function to handle WebSocket connections.
    await websocket.accept()  # Accept the incoming WebSocket connection.
    connected_clients.add((client, websocket))  # Add the newly connected client to the set.
    try:
        while True:  # Continuously listen for messages from the connected client.
            data = await websocket.receive_text()  # Wait and receive a text message from the client.
            # Loop through all connected clients to determine where to forward the message.
            for c, ws in connected_clients:
                # Check if the current message is from the "sender" and the target client is the "receiver".
                if client == "sender" and c == "receiver":
                    await ws.send_text(data)  # Forward the received message to the "receiver" client.
    except WebSocketDisconnect:  # Exception to handle if the WebSocket connection gets disconnected.
        connected_clients.remove((client, websocket))  # Remove the disconnected client from the set.
