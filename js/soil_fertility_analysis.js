document.getElementById('soilFertilityForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    // Clear previous results
    const resultDiv = document.getElementById('recommendationResult');
    resultDiv.style.display = 'none';
    const recommendedFertilityElement = document.getElementById('recommendedFertility');
    recommendedFertilityElement.textContent = '';
    
    // Get form values and convert to numbers
    const formData = {
        nitrogen: parseFloat(document.getElementById('nitrogen').value),
        phosphorus: parseFloat(document.getElementById('phosphorus').value),
        potassium: parseFloat(document.getElementById('potassium').value),
        ph: parseFloat(document.getElementById('ph').value),
        ec: parseFloat(document.getElementById('ec').value),
        oc: parseFloat(document.getElementById('oc').value),
        s: parseFloat(document.getElementById('s').value),
        zn: parseFloat(document.getElementById('zn').value),
        fe: parseFloat(document.getElementById('fe').value),
        cu: parseFloat(document.getElementById('cu').value),
        mn: parseFloat(document.getElementById('mn').value),
        b: parseFloat(document.getElementById('b').value)
    };

    // Validate that all values are numbers and non-negative
    for (let key in formData) {
        if (isNaN(formData[key]) || formData[key] < 0) {
            alert(`Please enter a valid non-negative number for ${key}`);
            return;
        }
    }

    try {
        // Show loading state
        const submitButton = e.target.querySelector('button[type="submit"]');
        const originalButtonText = submitButton.innerHTML;
        submitButton.innerHTML = 'Analyzing...';
        submitButton.disabled = true;

        console.log('Sending data to API:', formData);

        // Make API request
        const response = await fetch('http://localhost:5000/soil_fertility_predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || `HTTP error! status: ${response.status}`);
        }

        console.log('Received prediction:', data);

        // Map numeric prediction to recommendations
        let recommendations;
        
        if (data.numeric_prediction === 0) {
            recommendations = [
                "Add organic matter like compost or manure to improve soil structure",
                "Apply balanced NPK fertilizers based on soil test results",
                "Consider using soil amendments to correct nutrient deficiencies",
                "Implement regular soil testing to monitor improvements"
            ];
        } else if (data.numeric_prediction === 1) {
            recommendations = [
                "Maintain current soil management practices",
                "Monitor nutrient levels through periodic testing",
                "Apply fertilizers based on specific crop requirements",
                "Consider crop rotation to maintain soil health"
            ];
        } else if (data.numeric_prediction === 2) {
            recommendations = [
                "Reduce fertilizer application to prevent nutrient excess",
                "Focus on maintaining organic matter content",
                "Monitor for potential nutrient imbalances",
                "Consider planting nutrient-demanding crops"
            ];
        } else {
            recommendations = [
                "Please consult with a local agricultural expert",
                "Consider retesting soil samples",
                "Monitor soil conditions regularly"
            ];
        }

        // Display result with proper formatting
        resultDiv.innerHTML = `
            <div class="alert alert-success" role="alert">
                <h4 class="alert-heading">Soil Fertility Analysis Result</h4>
                <p>Based on your soil parameters, your soil is: <strong>${data.fertility}</strong></p>
                <hr>
                <p class="mb-0">Recommendations:</p>
                <ul>
                    ${recommendations.map(rec => `<li>${rec}</li>`).join('')}
                </ul>
            </div>
        `;
        resultDiv.style.display = 'block';

    } catch (error) {
        console.error('Error:', error);
        resultDiv.innerHTML = `
            <div class="alert alert-danger" role="alert">
                <h4 class="alert-heading">Error</h4>
                <p>${error.message}</p>
            </div>
        `;
        resultDiv.style.display = 'block';
    } finally {
        // Restore button state
        const submitButton = e.target.querySelector('button[type="submit"]');
        submitButton.innerHTML = 'Analyze Soil Fertility';
        submitButton.disabled = false;
    }
});
