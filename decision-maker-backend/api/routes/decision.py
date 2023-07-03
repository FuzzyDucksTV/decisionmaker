from flask import Blueprint, request, jsonify
from api.services.decision_maker import make_decision, get_amazon_recommendations

decision_routes = Blueprint('decision', __name__)

@decision_routes.route('/make-decision', methods=['POST'])
def make_decision_route():
    data = request.json
    if not data or 'options' not in data:
        return jsonify({'error': 'No options provided'}), 400

    options = data['options']
    if not isinstance(options, list) or len(options) == 0:
        return jsonify({'error': 'Invalid options format'}), 400

    try:
        decision = make_decision(options)
        return jsonify({'decision': decision})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@decision_routes.route('/recommendations', methods=['GET'])
def get_recommendations():
    category = request.args.get('category')
    if not category:
        return jsonify({'error': 'Category is required'}), 400

    try:
        recommendations = get_amazon_recommendations(category)
        decision = make_decision(recommendations)
        return jsonify(decision)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
