from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import sys
from werkzeug.utils import secure_filename
from config import config
from ocr_processor import process_image

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Load configuration
env = os.getenv('FLASK_ENV', 'development')
app.config.from_object(config[env])

# Enable CORS - Allow React frontend to access this API
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

# Create uploads folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'OK', 'message': 'OCR API is running'}), 200


@app.route('/api/extract', methods=['POST'])
def extract():
    """Main OCR extraction endpoint"""
    try:
        # Check if file is in request
        if 'image' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['image']

        # Check if file has name
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        # Validate file
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed'}), 400

        # Check file size
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        
        if file_size > app.config['MAX_FILE_SIZE']:
            return jsonify({'error': 'File size exceeds limit'}), 400

        # Save file temporarily
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Process image with OCR
        result = process_image(filepath)

        # Clean up - delete temporary file
        try:
            os.remove(filepath)
        except:
            pass

        # Return result to frontend
        return jsonify(result), 200

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': f'Processing failed: {str(e)}'}), 500


@app.route('/api/supported-formats', methods=['GET'])
def supported_formats():
    """Return list of supported file formats"""
    return jsonify({
        'formats': list(app.config['ALLOWED_EXTENSIONS']),
        'max_size_mb': app.config['MAX_FILE_SIZE'] / (1024 * 1024)
    }), 200


if __name__ == '__main__':
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('DEBUG', 'False') == 'True'
    app.run(host='0.0.0.0', port=port, debug=debug)