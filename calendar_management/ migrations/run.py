from app import create_app

# Create the Flask application using the configuration for the desired environment
app = create_app(config_name="development")  # You can change to "production" or "testing" as needed

if __name__ == "__main__":
    # Run the Flask app with debug mode enabled for development
    app.run(host="0.0.0.0", port=5000, debug=True)
