import hashlib
from flask import Flask, request, jsonify
from consistent_hashing import ConsistentHashing
import logging

app = Flask(__name__)

# Initialize Consistent Hashing
hashing = ConsistentHashing()

# Predefined server replicas
server_replicas = []
# Add the predefined server replicas to the consistent hashing ring
for server in server_replicas:
    hashing.add_node(server)

def get_hash(key):
    """
    Get a hash value for the given key using MD5.
    
    Parameters:
    key (str): The key to hash.
    
    Returns:
    int: The hashed key value.
    """
    return int(hashlib.md5(key.encode('utf-8')).hexdigest(), 16)

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
    unique_id = request.args.get('id', 'default_id')
    key = f"{request.remote_addr}_{unique_id}"  # Use remote address and query param for hashing
    node_id = hashing.get_node(get_hash(key))
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

@app.route('/rep')
def get_replicas():
    """
    Endpoint to get the list of current server replicas.
    """
    response_data = {
        'message': {
            'N': len(server_replicas),  # Number of replicas
            'replicas': server_replicas  # List of replicas
        },
        'status': 'successful'
    }
    return jsonify(response_data), 200

@app.route('/add', methods=['POST'])
def add_replica():
    """
    Endpoint to add new server replicas.
    """
    data = request.get_json()  # Get the JSON data from the request
    n = data.get('n')  # Number of replicas to add
    hostnames = data.get('hostnames')  # List of hostnames to add

    logging.debug(f"Adding {n} replicas: {hostnames}")

    # Validate the input
    if len(hostnames) > n:
        return jsonify({
            'message': 'Error, number of hostnames is greater than newly added instances',
            'status': 'failure'
        }), 400
    else:
        # Add the new hostnames to the replicas and consistent hashing ring
        for hostname in hostnames:
            if hostname not in server_replicas:
                server_replicas.append(hostname)
                hashing.add_node(hostname)
                logging.debug(f"Added replica: {hostname}")

        response_data = {
            'message': {
                'N': len(server_replicas),  # Updated number of replicas
                'replicas': server_replicas  # Updated list of replicas
            },
            'status': 'successful',
        }
        logging.debug(f"Updated replicas list: {server_replicas}")
        return jsonify(response_data), 200

@app.route('/rm', methods=['DELETE'])
def remove_replicas():
    """
    Endpoint to remove existing server replicas.
    """
    data = request.get_json()  # Get the JSON data from the request
    n = data.get('n')  # Number of replicas to remove
    hostnames = data.get('hostnames')  # List of hostnames to remove

    logging.debug(f"Removing {n} replicas: {hostnames}")

    # Validate the input
    if len(hostnames) > n:
        return jsonify({
            'message': 'Error, number of hostnames is greater than removable instances',
            'status': 'failure'
        }), 400
    else:
        # Remove the hostnames from the replicas and consistent hashing ring
        for hostname in hostnames:
            if hostname in server_replicas:
                server_replicas.remove(hostname)
                hashing.remove_node(hostname)
                logging.debug(f"Removed replica: {hostname}")

        response_data = {
            'message': {
                'N': len(server_replicas),  # Updated number of replicas
                'replicas': server_replicas  # Updated list of replicas
            },
            'status': 'successful'
        }
        logging.debug(f"Updated replicas list: {server_replicas}")
        return jsonify(response_data), 200

@app.route('/<path>')
def route_to_replica(path):
    """
    Endpoint to route a request to a specific server based on the path.
    """
    # Validate the path
    if path != 'home':
        return jsonify({
            'message': f'Error, {path} endpoint does not exist in server replicas',
            'status': 'failure'
        }), 400
    else:
        # Get the node responsible for the hashed value of the path
        node_id = hashing.get_node(get_hash(path))
        return jsonify({
            'message': f'Hello from server: {node_id}',
            'status': 'successful'
        }), 200

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)  # Enable debug logging
    app.run(debug=True)  # Run the Flask application in debug mode
