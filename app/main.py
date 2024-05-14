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
    data = request.get_json()  
    n = data.get('n')  
    hostnames = data.get('hostnames')  

    if len(hostnames) > n:
        return jsonify({
            'message': 'Error, number of hostnames is greater than newly added instances',
            'status': 'failure'
        }), 400
    else:
        for hostname in hostnames:
            server_replicas.append(hostname)
            hashing.add_node(hostname)

        response_data = {
            'message': {
                'N': len(server_replicas), 
                'replicas': server_replicas 
            },
            'status': 'successful',
        }
        return jsonify(response_data), 200

@app.route('/rm', methods=['DELETE'])
def remove_replicas():
    """
    Endpoint to remove existing server replicas.
    """
    data = request.get_json()  
    n = data.get('n')  
    hostnames = data.get('hostnames') 

    # Validate the input
    if len(hostnames) > n:
        return jsonify({
            'message': 'Error, number of hostnames is greater than removable instances',
            'status': 'failed'
        }), 400
    else:
        for hostname in hostnames:
            if hostname in server_replicas:
                server_replicas.remove(hostname)
                hashing.remove_node(hostname)

        response_data = {
            'message': {
                'N': len(server_replicas),  
                'replicas': server_replicas 
            },
            'status': 'successful'
        }
        return jsonify(response_data), 200

@app.route('/<path>')
def route_to_replica(path):
    """
    Endpoint to route a request to a specific server based on the path.
    """
    # Validate the path
    if path != 'home':
        return jsonify({
            'message': 'Error, endpoint does not exist in server replicas',
            'status': 'failure'
        }), 400
    else:
        node_id = hashing.get_node(hash(path))
        return jsonify({
            'message': f'Hello from server: {node_id}',
            'status': 'successful'
        }), 200

if __name__ == '_main_':
    logging.basicConfig(level=logging.DEBUG)  
    app.run(debug=True)