// Loader
window.addEventListener('load', function() {
    const loader = document.querySelector('.loader_container');
    if (loader) {
        loader.style.display = 'none';
    }
});

// Copyright year
document.addEventListener('DOMContentLoaded', function() {
    const yearElement = document.getElementById('currentYear');
    if (yearElement) {
        yearElement.textContent = new Date().getFullYear();
    }
});
