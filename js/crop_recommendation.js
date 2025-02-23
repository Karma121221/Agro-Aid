document.getElementById('cropRecommendationForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    // Clear previous recommendation
    const resultDiv = document.getElementById('recommendationResult');
    resultDiv.style.display = 'none';
    const recommendedCropElement = document.getElementById('recommendedCrop');
    recommendedCropElement.textContent = '';
    
    // Get form values
    const formData = {
        nitrogen: document.getElementById('nitrogen').value,
        phosphorus: document.getElementById('phosphorus').value,
        potassium: document.getElementById('potassium').value,
        temperature: document.getElementById('temperature').value,
        humidity: document.getElementById('humidity').value,
        ph: document.getElementById('ph').value,
        rainfall: document.getElementById('rainfall').value
    };

    try {
        // Show loading state
        const submitButton = e.target.querySelector('button[type="submit"]');
        const originalButtonText = submitButton.innerHTML;
        submitButton.innerHTML = 'Getting Recommendation...';
        submitButton.disabled = true;

        // Make API request
        const response = await fetch('http://localhost:5000/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });

        const data = await response.json();

        if (response.ok) {
            // Show result
            recommendedCropElement.textContent = `Based on your soil conditions and environmental factors, we recommend growing: ${data.crop}`;
            resultDiv.style.display = 'block';

            // Scroll to result
            resultDiv.scrollIntoView({ behavior: 'smooth' });
        } else {
            throw new Error(data.error || 'Failed to get recommendation');
        }
    } catch (error) {
        // Show error
        alert('Error: ' + error.message);
    } finally {
        // Reset button state
        submitButton.innerHTML = originalButtonText;
        submitButton.disabled = false;
    }
});
