document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('optionsModal');
    const hideOptions = document.querySelectorAll('.hide-option');

    modal.addEventListener('show.bs.modal', function () {
        hideOptions.forEach(option => {
            const checkbox = option.querySelector('.form-check-input');
            const icon = option.querySelector('.toggle-hide');
            updateIconClass(icon, checkbox.checked);
        });
    });
    
    hideOptions.forEach(option => {
        const label = option.querySelector('.form-check-label');
        const checkbox = option.querySelector('.form-check-input');
        const icon = option.querySelector('.toggle-hide');
        
        function toggleOption(e) {
            e.preventDefault();
            checkbox.checked = !checkbox.checked;
            updateIconClass(icon, checkbox.checked);
        }

        // Make the label clickable
        label.addEventListener('click', toggleOption);

        // Make the icon clickable
        icon.addEventListener('click', toggleOption);
    });

    function updateIconClass(icon, isHidden) {
        if (isHidden) {
            icon.classList.remove('fa-eye');
            icon.classList.add('fa-eye-slash');
        } else {
            icon.classList.remove('fa-eye-slash');
            icon.classList.add('fa-eye');
        }
    }
});