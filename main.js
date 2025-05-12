document.addEventListener('DOMContentLoaded', function() {
    // Print button functionality
    const printBtn = document.getElementById('print-btn');
    if (printBtn) {
        printBtn.addEventListener('click', function() {
            window.print();
        });
    }
    
    // Dynamic form interactions
    const dietSelect = document.getElementById('diet');
    const exerciseSelect = document.getElementById('exercise');
    
    if (dietSelect && exerciseSelect) {
        // You can add dynamic form logic here
    }
});