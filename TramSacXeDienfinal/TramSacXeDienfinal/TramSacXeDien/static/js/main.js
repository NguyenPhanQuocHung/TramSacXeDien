// Global state
let currentData = {
    coordinates: [],
    populations: [],
    lastSolution: null,
    lastResult: null
};

let charts = {};

// Check if Chart.js is loaded
if (typeof Chart === 'undefined') {
    console.error('Chart.js not loaded! Check CDN connection.');
}

// Global error handler
window.addEventListener('error', function(event) {
    console.error('Global error:', event.error);
});

// DOM Elements
const generateBtn = document.getElementById('generateBtn');
const rrHCBtn = document.getElementById('rrHCBtn');
const saBtn = document.getElementById('saBtn');
const compareBtn = document.getElementById('compareBtn');

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    generateBtn.addEventListener('click', generateData);
    rrHCBtn.addEventListener('click', () => runAlgorithm('rrhc'));
    saBtn.addEventListener('click', () => runAlgorithm('sa'));
    compareBtn.addEventListener('click', compareAlgorithms);
    
    // Tab switching
    document.querySelectorAll('.tab-button').forEach(button => {
        button.addEventListener('click', switchTab);
    });
});

// Generate Data
async function generateData() {
    const numAreas = parseInt(document.getElementById('numAreas').value);
    const statusDiv = document.getElementById('generateStatus');
    
    try {
        statusDiv.className = 'status-message status-loading';
        statusDiv.textContent = 'Đang tạo dữ liệu...';
        
        const response = await fetch('/api/generate_data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ num_areas: numAreas })
        });
        
        if (!response.ok) throw new Error('Failed to generate data');
        
        const data = await response.json();
        
        if (data.success) {
            currentData.coordinates = data.coordinates;
            currentData.populations = data.populations;
            
            statusDiv.className = 'status-message status-success';
            statusDiv.textContent = `✓ Đã tạo ${numAreas} khu vực thành công!`;
            
            // Update visualization
            updateMapVisualization();
            updatePopulationChart();
            
            // Clear previous results
            clearResults();
        }
    } catch (error) {
        statusDiv.className = 'status-message status-error';
        statusDiv.textContent = `✗ Lỗi: ${error.message}`;
    }
}

// Run Algorithm
async function runAlgorithm(algorithm) {
    if (currentData.coordinates.length === 0) {
        alert('Vui lòng tạo dữ liệu trước!');
        return;
    }
    
    const kStations = parseInt(document.getElementById('kStations').value);
    const numRestarts = parseInt(document.getElementById('numRestarts').value);
    const statusDiv = document.getElementById('algorithmStatus');
    
    try {
        statusDiv.className = 'status-message status-loading';
        statusDiv.textContent = 'Đang chạy thuật toán...';
        
        const response = await fetch('/api/run_algorithm', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                algorithm: algorithm,
                k_stations: kStations,
                num_restarts: numRestarts
            })
        });
        
        if (!response.ok) throw new Error('Failed to run algorithm');
        
        const data = await response.json();
        
        if (data.success) {
            currentData.lastSolution = data.result.solution;
            currentData.lastResult = data.result;
            
            statusDiv.className = 'status-message status-success';
            statusDiv.textContent = '✓ Thuật toán chạy thành công!';
            
            displayResults(data.result, kStations);
            updateMapVisualization();
            
            if (algorithm === 'rrhc' && data.result.all_costs) {
                updateCostChart(data.result.all_costs, 'Chu kỳ', 'Chi phí');
            } else if (algorithm === 'sa' && data.result.costs) {
                updateCostChart(data.result.costs, 'Bước', 'Chi phí');
            }
        }
    } catch (error) {
        statusDiv.className = 'status-message status-error';
        statusDiv.textContent = `✗ Lỗi: ${error.message}`;
    }
}

// Compare Algorithms
async function compareAlgorithms() {
    if (currentData.coordinates.length === 0) {
        alert('Vui lòng tạo dữ liệu trước!');
        return;
    }
    
    const kStations = parseInt(document.getElementById('kStations').value);
    const numRestarts = parseInt(document.getElementById('numRestarts').value);
    const statusDiv = document.getElementById('algorithmStatus');
    
    try {
        statusDiv.className = 'status-message status-loading';
        statusDiv.textContent = 'Đang so sánh các thuật toán...';
        
        const response = await fetch('/api/compare_algorithms', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                k_stations: kStations,
                num_restarts: numRestarts
            })
        });
        
        if (!response.ok) throw new Error('Failed to compare algorithms');
        
        const data = await response.json();
        
        if (data.success) {
            console.log('Comparison data:', data);
            statusDiv.className = 'status-message status-success';
            statusDiv.textContent = '✓ So sánh hoàn tất!';
            
            displayComparison(data);
            
            // Switch to comparison tab
            setTimeout(() => {
                const compTab = document.querySelector('[data-tab="comparison"]');
                if (compTab) {
                    compTab.click();
                }
            }, 100);
        } else {
            throw new Error(data.error || 'Unknown error');
        }
    } catch (error) {
        console.error('Comparison error:', error);
        statusDiv.className = 'status-message status-error';
        statusDiv.textContent = `✗ Lỗi: ${error.message}`;
    }
}

// Display Results
function displayResults(result, kStations) {
    const resultAlg = document.getElementById('resultAlgorithm');
    const resultCost = document.getElementById('resultCost');
    const resultStations = document.getElementById('resultStations');
    const resultSolution = document.getElementById('resultSolution');
    const resultDetails = document.getElementById('resultDetails');
    
    resultAlg.textContent = result.algorithm;
    resultCost.textContent = `${result.cost.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ',')} VND`;
    resultStations.textContent = kStations;
    resultSolution.textContent = `[${result.solution.join(', ')}]`;
    
    let detailsHtml = `<p><strong>Chi phí tối ưu:</strong> ${result.cost.toFixed(2)}</p>`;
    
    if (result.algorithm.includes('Random Restart')) {
        detailsHtml += `<p><strong>Trung bình:</strong> ${result.all_costs ? (result.all_costs.reduce((a, b) => a + b) / result.all_costs.length).toFixed(2) : 'N/A'}</p>`;
        detailsHtml += `<p><strong>Tối đa:</strong> ${result.all_costs ? Math.max(...result.all_costs).toFixed(2) : 'N/A'}</p>`;
        detailsHtml += `<p><strong>Độ lệch chuẩn:</strong> ${result.all_costs ? getStdDev(result.all_costs).toFixed(2) : 'N/A'}</p>`;
        detailsHtml += `<p><strong>Số lần khởi động lại:</strong> ${result.num_restarts}</p>`;
    } else {
        detailsHtml += `<p><strong>Số bước:</strong> ${result.num_steps}</p>`;
        detailsHtml += `<p><strong>Nhiệt độ cuối cùng:</strong> ${result.final_temp.toFixed(2)}</p>`;
    }
    
    resultDetails.innerHTML = detailsHtml;
}

// Display Comparison
function displayComparison(data) {
    try {
        if (!data || !data.rrhc || !data.sa) {
            console.error('Invalid data structure:', data);
            throw new Error('Invalid comparison data');
        }
        
        const rrHCDiv = document.getElementById('rrHCComparison');
        const saDiv = document.getElementById('saComparison');
        
        if (!rrHCDiv || !saDiv) {
            console.error('Comparison divs not found');
            return;
        }
        
        const rrhc = data.rrhc;
        const sa = data.sa;
        
        rrHCDiv.innerHTML = `
            <p><strong>Chi phí tối ưu:</strong> ${rrhc.cost.toFixed(2)}</p>
            <p><strong>Trung bình:</strong> ${rrhc.avg_cost.toFixed(2)}</p>
            <p><strong>Tối đa:</strong> ${rrhc.max_cost.toFixed(2)}</p>
            <p><strong>Độ lệch chuẩn:</strong> ${rrhc.std_cost.toFixed(2)}</p>
            <p><strong>Vị trí:</strong> [${rrhc.solution.join(', ')}]</p>
        `;
        
        saDiv.innerHTML = `
            <p><strong>Chi phí tối ưu:</strong> ${sa.cost.toFixed(2)}</p>
            <p><strong>Số bước:</strong> ${sa.num_steps}</p>
            <p><strong>Nhiệt độ cuối:</strong> ${sa.final_temp.toFixed(2)}</p>
            <p><strong>Vị trí:</strong> [${sa.solution.join(', ')}]</p>
            <p><strong style="color: ${sa.cost < rrhc.cost ? '#10b981' : '#ef4444'}">
                ${sa.cost < rrhc.cost ? '✓ SA tốt hơn' : '✗ RRHC tốt hơn'} 
                (${Math.abs(data.improvement).toFixed(2)}%)
            </strong></p>
        `;
        
        // Update comparison charts
        updateComparisonCharts(data);
        
    } catch (error) {
        console.error('Error in displayComparison:', error);
        document.getElementById('algorithmStatus').innerHTML = `<p style="color: red;">Lỗi hiển thị so sánh: ${error.message}</p>`;
    }
}

// Update Visualizations
function updateMapVisualization() {
    const canvas = document.getElementById('mapChart');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    
    // Destroy existing chart if any
    if (charts.map) {
        try { charts.map.destroy(); } catch(e) {}
    }
    
    const areas = currentData.coordinates.map((coord, idx) => ({
        x: coord[0],
        y: coord[1],
        r: 4,
        idx: idx,
        isStation: currentData.lastSolution && currentData.lastSolution.includes(idx)
    }));
    
    const stationIndices = currentData.lastSolution || [];
    const stations = areas.filter(a => a.isStation);
    const nonStations = areas.filter(a => !a.isStation);
    
    charts.map = new Chart(ctx, {
        type: 'bubble',
        data: {
            datasets: [
                {
                    label: 'Khu vực dân cư',
                    data: nonStations,
                    backgroundColor: 'rgba(59, 130, 246, 0.5)',
                    borderColor: 'rgba(37, 99, 235, 1)',
                    borderWidth: 1
                },
                {
                    label: 'Trạm sạc xe',
                    data: stations,
                    backgroundColor: 'rgba(34, 197, 94, 0.7)',
                    borderColor: 'rgba(16, 185, 129, 1)',
                    borderWidth: 2
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'top'
                }
            },
            scales: {
                x: {
                    title: { display: true, text: 'X (Tọa độ)' }
                },
                y: {
                    title: { display: true, text: 'Y (Tọa độ)' }
                }
            }
        }
    });
}

function updatePopulationChart() {
    const canvas = document.getElementById('populationChart');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    
    if (charts.population) {
        try { charts.population.destroy(); } catch(e) {}
    }
    
    const populations = currentData.populations.slice(0, 20);
    const labels = populations.map((_, i) => `Khu ${i + 1}`);
    
    charts.population = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Dân số',
                data: populations,
                backgroundColor: 'rgba(99, 102, 241, 0.6)',
                borderColor: 'rgba(79, 70, 229, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            indexAxis: 'x',
            plugins: {
                legend: {
                    display: true
                }
            },
            scales: {
                y: {
                    title: { display: true, text: 'Dân số' }
                }
            }
        }
    });
}

function updateCostChart(costs, xLabel, yLabel) {
    const canvas = document.getElementById('comparisonChart');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    
    if (charts.cost) {
        try { charts.cost.destroy(); } catch(e) {}
    }
    
    const labels = Array.from({ length: costs.length }, (_, i) => i + 1);
    
    charts.cost = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Chi phí',
                data: costs,
                borderColor: 'rgba(236, 72, 153, 1)',
                backgroundColor: 'rgba(236, 72, 153, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: true }
            },
            scales: {
                x: { title: { display: true, text: xLabel } },
                y: { title: { display: true, text: yLabel } }
            }
        }
    });
}

function updateComparisonCharts(data) {
    try {
        // Validate data
        if (!data || !data.rrhc || !data.sa) {
            console.error('Invalid comparison data:', data);
            return;
        }
        
        // Biểu đồ chi phí theo chu kỳ (RRHC)
        const costCanvas = document.getElementById('comparisonChart');
        if (costCanvas && data.rrhc.all_costs && Array.isArray(data.rrhc.all_costs)) {
            try {
                const ctx = costCanvas.getContext('2d');
                
                if (charts.cost) {
                    try { charts.cost.destroy(); } catch(e) {}
                }
                
                const labels = Array.from({ length: data.rrhc.all_costs.length }, (_, i) => i + 1);
                
                charts.cost = new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: labels,
                        datasets: [{
                            label: 'Chi phí HC',
                            data: data.rrhc.all_costs,
                            borderColor: 'rgba(99, 102, 241, 1)',
                            backgroundColor: 'rgba(99, 102, 241, 0.1)',
                            borderWidth: 2,
                            fill: true,
                            tension: 0.4
                        }]
                    },
                    options: {
                        responsive: true,
                        plugins: {
                            legend: { display: true }
                        },
                        scales: {
                            x: { title: { display: true, text: 'Lần khởi động' } },
                            y: { title: { display: true, text: 'Chi phí' } }
                        }
                    }
                });
            } catch(e) {
                console.error('Error creating cost chart:', e);
            }
        }
        
        // Biểu đồ so sánh hiệu suất
        const performanceCanvas = document.getElementById('performanceChart');
        if (performanceCanvas) {
            try {
                const ctx = performanceCanvas.getContext('2d');
                
                if (charts.comparison) {
                    try { charts.comparison.destroy(); } catch(e) {}
                }
                
                charts.comparison = new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: ['Random Restart HC', 'Simulated Annealing'],
                        datasets: [{
                            label: 'Chi phí tối ưu',
                            data: [data.rrhc.cost, data.sa.cost],
                            backgroundColor: [
                                'rgba(99, 102, 241, 0.6)',
                                'rgba(34, 197, 94, 0.6)'
                            ],
                            borderColor: [
                                'rgba(79, 70, 229, 1)',
                                'rgba(16, 185, 129, 1)'
                            ],
                            borderWidth: 2
                        }]
                    },
                    options: {
                        responsive: true,
                        indexAxis: 'y',
                        plugins: {
                            legend: { display: true }
                        }
                    }
                });
            } catch(e) {
                console.error('Error creating performance chart:', e);
            }
        }
    } catch (error) {
        console.error('Error in updateComparisonCharts:', error);
    }
}

// Tab Switching
function switchTab(e) {
    const target = e.target.getAttribute('data-tab');
    
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    
    document.querySelectorAll('.tab-button').forEach(btn => {
        btn.classList.remove('active');
    });
    
    document.getElementById(target).classList.add('active');
    e.target.classList.add('active');
}

// Utility Functions
function getStdDev(arr) {
    const mean = arr.reduce((a, b) => a + b) / arr.length;
    const variance = arr.reduce((a, b) => a + Math.pow(b - mean, 2)) / arr.length;
    return Math.sqrt(variance);
}

function clearResults() {
    document.getElementById('resultAlgorithm').textContent = '-';
    document.getElementById('resultCost').textContent = '-';
    document.getElementById('resultStations').textContent = '-';
    document.getElementById('resultSolution').textContent = '-';
    document.getElementById('resultDetails').innerHTML = '';
}

// Format number with thousand separator
function formatNumber(num) {
    return num.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}
