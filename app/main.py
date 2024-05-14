from flask import Flask, request, jsonify
from consistent_hashing import ConsistentHashing
import logging

app = Flask(_name_)

# Initialize Consistent Hashing
hashing = ConsistentHashing()

# Predefined server replicas
server_replicas = ['server1', 'server2', 'server3']
# Add the predefined server replicas to the consistent hashing ring
for server in server_replicas:
    hashing.add_node(server)

@app.route('/')
def home():
    """
    Root endpoint that returns a simple homepage message.
    """
    return "Homepage"

@app.route('/home')
def getname():
    """
    Endpoint to get a greeting message from a specific server.
    """
    # Get the node responsible for the hashed value of 'home'
    node_id = hashing.get_node(hash('home'))
    response_data = {
        'message': f'Hello from server: {node_id}',
        'status': 'successful'
    }
    return jsonify(response_data), 200

@app.route('/heartbeat')
def heartbeat():
    """
    Endpoint to check if the server is alive.
    """
    return "", 200

if __name__ == '__main__':
    app.run(debug=True)