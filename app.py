"""
Nutrition Track - Simplified Backend with Better Error Handling
This version is easier to debug and gives better error messages
"""

import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# Load environment variables FIRST
load_dotenv()

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Check API key on startup
API_KEY = os.environ.get('GOOGLE_CLOUD_API_KEY')
if not API_KEY:
    print("\n" + "="*60)
    print("ERROR: GOOGLE_CLOUD_API_KEY not found!")
    print("="*60)
    print("Please create a .env file with:")
    print("GOOGLE_CLOUD_API_KEY=your_actual_key_here")
    print("="*60 + "\n")

def get_nutrition_data(food_items):
    """Simple nutrition estimation without AI (for testing)"""
    nutrition_db = {
        'chicken': {'calories': 165, 'protein': 31, 'carbs': 0, 'fats': 3.6},
        'rice': {'calories': 130, 'protein': 2.7, 'carbs': 28, 'fats': 0.3},
        'salad': {'calories': 25, 'protein': 2, 'carbs': 5, 'fats': 0.3},
        'burger': {'calories': 295, 'protein': 17, 'carbs': 24, 'fats': 14},
        'pizza': {'calories': 266, 'protein': 11, 'carbs': 33, 'fats': 10},
    }
    
    total_cal = 0
    total_protein = 0
    total_carbs = 0
    total_fats = 0
    found = []
    
    for item in food_items:
        for key, values in nutrition_db.items():
            if key in item.lower():
                total_cal += values['calories'] * 1.5
                total_protein += values['protein'] * 1.5
                total_carbs += values['carbs'] * 1.5
                total_fats += values['fats'] * 1.5
                found.append(item)
                break
    
    if not found:
        found = food_items[:3] if food_items else ['Mixed Meal']
        total_cal = 400
        total_protein = 20
        total_carbs = 45
        total_fats = 15
    
    return {
        'food_name': ', '.join(found[:3]),
        'calories': round(total_cal),
        'protein': round(total_protein, 1),
        'carbs': round(total_carbs, 1),
        'fats': round(total_fats, 1),
        'health_tip': 'Well-balanced meal!',
        'detected_labels': found
    }

def analyze_with_vision_api(image_bytes):
    """Use Google Vision API to detect food items"""
    try:
        from google.cloud import vision
        
        if not API_KEY:
            raise ValueError("API key not configured")
        
        # Create client with API key
        client_options = {"api_key": API_KEY}
        client = vision.ImageAnnotatorClient(client_options=client_options)
        
        # Create image object
        image = vision.Image(content=image_bytes)
        
        # Detect labels
        print("Calling Vision API for label detection...")
        label_response = client.label_detection(image=image)
        labels = [label.description for label in label_response.label_annotations[:10]]
        
        print(f"Detected labels: {labels}")
        
        # Detect objects
        print("Calling Vision API for object detection...")
        object_response = client.object_localization(image=image)
        objects = [obj.name for obj in object_response.localized_object_annotations if obj.score > 0.5]
        
        print(f"Detected objects: {objects}")
        
        # Combine results
        all_items = objects + labels
        unique_items = []
        seen = set()
        
        for item in all_items:
            if item.lower() not in seen:
                unique_items.append(item)
                seen.add(item.lower())
        
        return unique_items
        
    except ImportError:
        print("ERROR: google-cloud-vision not installed")
        print("Run: pip install google-cloud-vision")
        return None
    except Exception as e:
        print(f"Vision API Error: {str(e)}")
        return None

@app.route('/')
def index():
    """Render main page"""
    return render_template('index.html')

@app.route('/test')
def test():
    """Test endpoint to check if server is running"""
    return jsonify({
        'status': 'ok',
        'message': 'Backend is working!',
        'api_key_set': bool(API_KEY),
        'api_key_length': len(API_KEY) if API_KEY else 0
    })

@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze food image"""
    try:
        print("\n" + "="*60)
        print("ANALYZE REQUEST RECEIVED")
        print("="*60)
        
        # Check if file is present
        if 'file' not in request.files:
            print("ERROR: No file in request")
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        print(f"File received: {file.filename}")
        
        if file.filename == '':
            print("ERROR: Empty filename")
            return jsonify({'error': 'No file selected'}), 400
        
        # Read image
        image_bytes = file.read()
        print(f"Image size: {len(image_bytes)} bytes")
        
        # Try Vision API
        detected_items = None
        if API_KEY:
            print("Attempting Vision API analysis...")
            detected_items = analyze_with_vision_api(image_bytes)
        else:
            print("WARNING: No API key, using fallback")
        
        # Fallback to dummy data if Vision API fails
        if not detected_items:
            print("Using fallback nutrition data")
            detected_items = ['Food', 'Meal', 'Dish']
        
        # Get nutrition estimates
        nutrition_data = get_nutrition_data(detected_items)
        
        print(f"Returning: {nutrition_data}")
        print("="*60 + "\n")
        
        return jsonify(nutrition_data)
        
    except Exception as e:
        print(f"ERROR in analyze: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("\n" + "="*60)
    print("NUTRITION TRACK - STARTING SERVER")
    print("="*60)
    print(f"API Key Set: {bool(API_KEY)}")
    if API_KEY:
        print(f"API Key Length: {len(API_KEY)} characters")
    print("="*60 + "\n")
    
    print("Starting Flask server...")
    print("Open browser to: http://localhost:5000")
    print("Test endpoint: http://localhost:5000/test")
    print("\nPress Ctrl+C to stop\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
