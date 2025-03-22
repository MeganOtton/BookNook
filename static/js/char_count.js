document.addEventListener('DOMContentLoaded', function() {
    const textarea = document.querySelector('textarea[name="bookdescription"]');
    const counter = document.createElement('div');
    counter.style.marginTop = '5px';
    textarea.parentNode.appendChild(counter);

    const updateCounter = () => {
        const typed = textarea.value.length;
        counter.textContent = `${typed} / 490 characters`;
    };

    textarea.addEventListener('input', updateCounter);
    updateCounter();
});