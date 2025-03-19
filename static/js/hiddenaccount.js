// Purchased Book Collapse Arrow Rotation

document.addEventListener('DOMContentLoaded', function () {
    const collapseElement = document.getElementById('purchasedBooks');
    const collapseArrow = document.getElementById('collapseArrow');

    // Check if both elements exist before adding event listeners
    if (collapseElement && collapseArrow) {
        // When the collapse expands
        collapseElement.addEventListener('shown.bs.collapse', function () {
            collapseArrow.classList.remove('fa-chevron-up');
            collapseArrow.classList.add('fa-chevron-down');
        });

        // When the collapse collapses
        collapseElement.addEventListener('hidden.bs.collapse', function () {
            collapseArrow.classList.remove('fa-chevron-down');
            collapseArrow.classList.add('fa-chevron-up');
        });
    } else {
        console.log('One or both elements (purchasedBooks, collapseArrow) not found in the DOM');
    }
});


// Show Tab 
function showTab(tabId) {
    // Show the main tab section
    document.querySelectorAll('.tab-section').forEach(el => el.classList.remove('active'));
    document.getElementById(tabId).classList.add('active');

    // Top buttons - highlight correct one
    const btnSeeHidden = document.getElementById('btnSeeHidden');
    const btnYourReviews = document.getElementById('btnYourReviews');

    if (tabId === 'hiddenTab') {
        btnSeeHidden.classList.add('active');
        btnYourReviews.classList.remove('active');
    } else {
        btnSeeHidden.classList.remove('active');
        btnYourReviews.classList.add('active');

        // Clear inner highlights if leaving hidden tab
        document.querySelectorAll('#hiddenGroup .btn').forEach(btn => btn.classList.remove('active'));
    }

    // Always hide all hidden sections when switching tabs
    document.querySelectorAll('.hidden-section').forEach(el => el.classList.remove('active'));
}

// Show Hidden Section
function showHiddenSection(sectionId, clickedButton) {
    // Show selected hidden section
    document.querySelectorAll('.hidden-section').forEach(el => el.classList.remove('active'));
    const selectedSection = document.getElementById(sectionId);
    if (selectedSection) {
        selectedSection.classList.add('active');
    }

    // Inner hidden section buttons - highlight correct one
    const hiddenGroup = document.getElementById('hiddenGroup');
    if (hiddenGroup) {
        hiddenGroup.querySelectorAll('.btn').forEach(btn => btn.classList.remove('active'));
    }
    
    if (clickedButton && clickedButton.classList) {
        clickedButton.classList.add('active');
    }

    // Force See Hidden button to stay active too
    const btnSeeHidden = document.getElementById('btnSeeHidden');
    const btnYourReviews = document.getElementById('btnYourReviews');
    if (btnSeeHidden) {
        btnSeeHidden.classList.add('active');
    }
    if (btnYourReviews) {
        btnYourReviews.classList.remove('active');
    }
}