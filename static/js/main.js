
// Main JavaScript File

// Handle mobile menu toggle
document.addEventListener('DOMContentLoaded', function() {
    const navbarToggle = document.querySelector('.navbar-toggle');
    const navbarLinks = document.querySelector('.navbar-links');
    
    if (navbarToggle && navbarLinks) {
        navbarToggle.addEventListener('click', function() {
            navbarLinks.style.display = navbarLinks.style.display === 'flex' ? 'none' : 'flex';
        });
    }
    
    // Close messages
    const messageCloseButtons = document.querySelectorAll('.message-close');
    messageCloseButtons.forEach(button => {
        button.addEventListener('click', function() {
            const message = this.parentElement;
            message.style.opacity = '0';
            setTimeout(() => {
                message.style.display = 'none';
            }, 300);
        });
    });
    
    // Auto-hide messages after 5 seconds
    const messages = document.querySelectorAll('.message');
    if (messages.length > 0) {
        setTimeout(() => {
            messages.forEach(message => {
                message.style.opacity = '0';
                setTimeout(() => {
                    message.style.display = 'none';
                }, 300);
            });
        }, 5000);
    }
    
    // BMI calculator helper
    const bmiInput = document.getElementById('id_bmi');
    if (bmiInput) {
        const bmiHelp = document.createElement('div');
        bmiHelp.className = 'form-help';
        bmiHelp.innerHTML = `
            <i class="fas fa-calculator"></i>
            <span>Need help calculating BMI? <a href="#" id="bmi-calculator-link">Use our calculator</a></span>
        `;
        bmiInput.parentNode.appendChild(bmiHelp);
        
        document.getElementById('bmi-calculator-link').addEventListener('click', function(e) {
            e.preventDefault();
            
            // Create modal
            const modal = document.createElement('div');
            modal.className = 'modal';
            modal.innerHTML = `
                <div class="modal-content">
                    <span class="modal-close">&times;</span>
                    <h2>BMI Calculator</h2>
                    <div class="form-group">
                        <label for="bmi-weight">Weight (kg)</label>
                        <input type="number" id="bmi-weight" placeholder="Enter weight">
                    </div>
                    <div class="form-group">
                        <label for="bmi-height">Height (cm)</label>
                        <input type="number" id="bmi-height" placeholder="Enter height">
                    </div>
                    <button id="calculate-bmi" class="btn btn-primary">Calculate BMI</button>
                    <div id="bmi-result" style="margin-top: 1rem; text-align: center;"></div>
                </div>
            `;
            
            document.body.appendChild(modal);
            
            // Add modal styles if not already in CSS
            const style = document.createElement('style');
            style.textContent = `
                .modal {
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background-color: rgba(0, 0, 0, 0.5);
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    z-index: 1200;
                }
                .modal-content {
                    background-color: white;
                    padding: 2rem;
                    border-radius: 0.375rem;
                    max-width: 400px;
                    width: 100%;
                    position: relative;
                }
                .modal-close {
                    position: absolute;
                    top: 0.75rem;
                    right: 0.75rem;
                    font-size: 1.5rem;
                    cursor: pointer;
                }
            `;
            document.head.appendChild(style);
            
            // Close modal function
            const closeModal = () => {
                document.body.removeChild(modal);
            };
            
            // Add event listeners
            document.querySelector('.modal-close').addEventListener('click', closeModal);
            
            document.getElementById('calculate-bmi').addEventListener('click', function() {
                const weight = parseFloat(document.getElementById('bmi-weight').value);
                const height = parseFloat(document.getElementById('bmi-height').value) / 100; // convert to meters
                
                if (!weight || !height) {
                    document.getElementById('bmi-result').innerHTML = `<p style="color: red;">Please enter valid values</p>`;
                    return;
                }
                
                const bmi = weight / (height * height);
                const roundedBmi = Math.round(bmi * 10) / 10;
                
                let category, color;
                if (bmi < 18.5) {
                    category = 'Underweight';
                    color = '#17a2b8';
                } else if (bmi < 25) {
                    category = 'Normal weight';
                    color = '#28a745';
                } else if (bmi < 30) {
                    category = 'Overweight';
                    color = '#ffc107';
                } else {
                    category = 'Obesity';
                    color = '#dc3545';
                }
                
                document.getElementById('bmi-result').innerHTML = `
                    <h3>Your BMI: <span style="color: ${color};">${roundedBmi}</span></h3>
                    <p>Category: <strong style="color: ${color};">${category}</strong></p>
                    <button id="use-bmi" class="btn btn-sm btn-primary" style="margin-top: 1rem;">Use this BMI</button>
                `;
                
                document.getElementById('use-bmi').addEventListener('click', function() {
                    document.getElementById('id_bmi').value = roundedBmi;
                    closeModal();
                });
            });
        });
    }
});
