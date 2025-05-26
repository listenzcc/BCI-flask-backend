# Ensure Waitress is installed
pip install waitress

# Setup
$hostname = "localhost"
$port = 7384

# Run the Flask application with Waitress
waitress-serve --host=$hostname --port=$port server:app