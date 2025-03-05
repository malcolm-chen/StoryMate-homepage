import asyncio
import websockets
import os
from dotenv import load_dotenv
from collections import defaultdict

load_dotenv()

OPENAI_WS_URL = "wss://api.openai.com/v1/realtime?model=gpt-4o-realtime-preview-2024-12-17"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Store user request counts
user_requests = defaultdict(int)
MAX_REQUESTS = 5

def get_client_id(websocket):
    """Get client identifier from websocket."""
    return websocket.remote_address[0]  # Using IP address as identifier

def check_and_update_requests(client_id):
    """Check if user has exceeded request limit and update their count."""
    # Check if user has exceeded limit
    if user_requests[client_id] >= MAX_REQUESTS:
        return False
    
    # Increment count
    user_requests[client_id] += 1
    return True

async def relay(websocket1, websocket2):
    """Relay messages between two websockets."""
    try:
        while True:
            message = await websocket1.recv()
            await websocket2.send(message)
            print(f"Relaying message from {websocket1} to {websocket2}: {message}")
    except websockets.ConnectionClosed:
        # Close the other websocket when one is closed
        await websocket2.close()

async def handler(websocket):
    """Handle incoming WebSocket connections."""
    client_id = get_client_id(websocket)
    
    # Check if user has exceeded request limit
    if not check_and_update_requests(client_id):
        print(f"User {client_id} has exceeded request limit")
        await websocket.close(1008, "Maximum number of requests reached. You have used all your available requests.")
        return

    other_client = None

    # Attempt to connect to the OpenAI WebSocket server
    while other_client is None:
        try:
            other_client = await websockets.connect(
                OPENAI_WS_URL,
                additional_headers={
                    "Authorization": f"Bearer {OPENAI_API_KEY}",
                    "OpenAI-Beta": "realtime=v1"
                }
            )
        except (websockets.ConnectionClosedError, ConnectionRefusedError):
            await asyncio.sleep(1)

    # Relay messages between the client and OpenAI WebSocket
    try:
        await asyncio.gather(
            relay(websocket, other_client),
            relay(other_client, websocket),
        )
    finally:
        # Ensure both websockets are closed gracefully
        await websocket.close()
        await other_client.close()

async def main():
    """Start the WebSocket server."""
    server = await websockets.serve(
        handler, "0.0.0.0", 8767,
        subprotocols=[
            'realtime',
            'openai-insecure-api-key.123',
            'openai-beta.realtime-v1',
        ]
    )
    print("WebSocket server started on ws://0.0.0.0:8767")
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())

