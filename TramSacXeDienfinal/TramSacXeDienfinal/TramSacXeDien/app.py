from flask import Flask, render_template, request, jsonify
import json
import numpy as np
import random
import sys
import os

# Add the TramSacXeDien directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from TramSacXeDien.dataset import (
    generate_data,
    weighted_distance,
    random_restart_hill_climbing,
    simulated_annealing
)

app = Flask(__name__, template_folder='templates', static_folder='static')

# Store data in session
session_data = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/generate_data', methods=['POST'])
def generate_data_api():
    """Generate random data for areas"""
    try:
        data = request.json
        num_areas = int(data.get('num_areas', 30))
        
        # Generate data
        coordinates, populations = generate_data(num_areas)
        
        # Store in session
        session_data['coordinates'] = coordinates.tolist()
        session_data['populations'] = populations.tolist()
        
        return jsonify({
            'success': True,
            'message': f'Generated {num_areas} areas',
            'num_areas': num_areas,
            'coordinates': session_data['coordinates'],
            'populations': session_data['populations']
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/run_algorithm', methods=['POST'])
def run_algorithm():
    """Run optimization algorithm"""
    try:
        data = request.json
        algorithm = data.get('algorithm', 'rrhc')
        k_stations = int(data.get('k_stations', 5))
        num_restarts = int(data.get('num_restarts', 100))
        
        if 'coordinates' not in session_data:
            return jsonify({'success': False, 'error': 'No data generated yet'}), 400
        
        coords = np.array(session_data['coordinates'])
        pops = np.array(session_data['populations'])
        
        result = {}
        
        if algorithm == 'rrhc':
            solution, cost, all_costs = random_restart_hill_climbing(
                coords, pops, K=k_stations, num_restarts=num_restarts, verbose=False
            )
            result = {
                'algorithm': 'Random Restart Hill Climbing',
                'solution': [int(x) for x in solution],
                'cost': float(cost),
                'all_costs': [float(c) for c in all_costs],
                'num_restarts': num_restarts
            }
        elif algorithm == 'sa':
            solution, cost, temps, costs = simulated_annealing(
                coords, pops, K=k_stations, verbose=False
            )
            result = {
                'algorithm': 'Simulated Annealing',
                'solution': [int(x) for x in solution],
                'cost': float(cost),
                'temperatures': [float(t) for t in temps],
                'costs': [float(c) for c in costs],
                'num_steps': len(temps) - 1,
                'final_temp': float(temps[-1])
            }
        
        # Store best solution
        session_data['last_solution'] = result['solution']
        session_data['last_cost'] = result['cost']
        
        return jsonify({
            'success': True,
            'result': result,
            'k_stations': k_stations
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/compare_algorithms', methods=['POST'])
def compare_algorithms():
    """Compare both algorithms"""
    try:
        data = request.json
        k_stations = int(data.get('k_stations', 5))
        num_restarts = int(data.get('num_restarts', 50))
        
        if 'coordinates' not in session_data:
            return jsonify({'success': False, 'error': 'No data generated yet'}), 400
        
        coords = np.array(session_data['coordinates'])
        pops = np.array(session_data['populations'])
        
        # Run RRHC
        rrhc_sol, rrhc_cost, rrhc_costs = random_restart_hill_climbing(
            coords, pops, K=k_stations, num_restarts=num_restarts, verbose=False
        )
        
        # Run SA
        sa_sol, sa_cost, sa_temps, sa_costs = simulated_annealing(
            coords, pops, K=k_stations, verbose=False
        )
        
        improvement = ((rrhc_cost - sa_cost) / rrhc_cost) * 100
        
        return jsonify({
            'success': True,
            'rrhc': {
                'solution': [int(x) for x in rrhc_sol],
                'cost': float(rrhc_cost),
                'avg_cost': float(np.mean(rrhc_costs)),
                'max_cost': float(max(rrhc_costs)),
                'std_cost': float(np.std(rrhc_costs)),
                'all_costs': [float(c) for c in rrhc_costs]
            },
            'sa': {
                'solution': [int(x) for x in sa_sol],
                'cost': float(sa_cost),
                'num_steps': len(sa_temps) - 1,
                'final_temp': float(sa_temps[-1]),
                'temperatures': [float(t) for t in sa_temps],
                'costs': [float(c) for c in sa_costs]
            },
            'improvement': float(improvement),
            'better_algorithm': 'SA' if sa_cost < rrhc_cost else 'RRHC'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/get_visualization', methods=['GET'])
def get_visualization():
    """Get data for visualization"""
    if 'coordinates' not in session_data or 'last_solution' not in session_data:
        return jsonify({'success': False, 'error': 'No data available'}), 400
    
    coords = session_data['coordinates']
    pops = session_data['populations']
    solution = session_data['last_solution']
    
    # Prepare data for visualization
    vis_data = {
        'areas': [],
        'stations': [],
        'coordinates': coords,
        'populations': pops
    }
    
    for i, (coord, pop) in enumerate(zip(coords, pops)):
        if i in solution:
            vis_data['stations'].append({
                'index': i,
                'x': coord[0],
                'y': coord[1],
                'population': int(pop)
            })
        else:
            vis_data['areas'].append({
                'index': i,
                'x': coord[0],
                'y': coord[1],
                'population': int(pop)
            })
    
    return jsonify({'success': True, 'data': vis_data})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
