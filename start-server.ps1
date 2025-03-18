# Ensure Waitress is installed
pip install waitress

# Run the Flask application with Waitress
waitress-serve --host=localhost --port=5000 server:app