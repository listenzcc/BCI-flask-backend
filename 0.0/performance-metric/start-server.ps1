# Ensure Waitress is installed
pip install waitress

# Setup
$hostname = "localhost"
$port = 5090

# Run the Flask application with Waitress
waitress-serve --host=$hostname --port=$port --connection-limit=2000 server:app