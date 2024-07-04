async function uploadImage() {
    const imageInput = document.getElementById('image-input');
    const file = imageInput.files[0];

    if (file) {
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();
        displayResults(result);
    } else {
        alert('Please select an image to upload.');
    }
}

function displayResults(result) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '';

    result.classifications.forEach((classification, index) => {
        const colorDiv = document.createElement('div');
        colorDiv.classList.add('color-box');
        colorDiv.style.backgroundColor = `rgb(${classification.color.join(',')})`;

        const text = `
            <p>Color ${index + 1}: RGB ${classification.color.join(', ')}</p>
            <p>Season: ${classification.season_type}</p>
            <p>Saturation: ${classification.saturation_level}</p>
            <p>Temperature: ${classification.temperature}</p>
        `;
        colorDiv.innerHTML = text;
        resultsDiv.appendChild(colorDiv);
    });

    const paletteTitle = document.createElement('h2');
    paletteTitle.textContent = 'Complementary Color Palette:';
    resultsDiv.appendChild(paletteTitle);

    result.complementary_palette.forEach(color => {
        const colorDiv = document.createElement('div');
        colorDiv.classList.add('color-box');
        colorDiv.style.backgroundColor = `rgb(${color.join(',')})`;
        resultsDiv.appendChild(colorDiv);
    });
}
