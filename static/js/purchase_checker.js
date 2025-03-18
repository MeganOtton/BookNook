// This script is used to check if the user has purchased the game or not
// If the user has purchased the game, the purchase button will be disabled
// If the user has not purchased the game, the purchase button will be enabled

// The script will be executed when the page is loaded
// The script will check if the URL has a parameter named 'purchased'
// If the parameter is 'true', the game has been purchased
// If the parameter is 'false', the game has not been purchased
// If the parameter is not present, the script will check the purchase status of the game

window.onload = function () {
    const urlParams = new URLSearchParams(window.location.search);
    const checkForm = document.getElementById("id_check_book_purchased");
    checkForm.addEventListener('submit', function (event) {
        event.preventDefault();
        const checkPurchasedButton = document.getElementById("checkPurchasedButton");
        checkPurchasedButton.innerText = "Checking...";
        checkPurchasedButton.disabled = true;
        checkForm.submit();

    });

    if (urlParams.has('purchased') && urlParams.get('purchased') === 'true') {
        checkBookPurchasedTrue();
    } else
        if (urlParams.has('purchased') && urlParams.get('purchased') === 'false') {
            checkBookPurchasedFalse();
        } else {
            checkBookFirstLoad();
        }


};

// This function will be called when the page is loaded
// This function will check if the game has been purchased
function checkBookFirstLoad() {
    document.getElementById("checkPurchasedButton").click();
    console.log ('checkBookFirstLoad')
}

// This function will be called when the game has been purchased
// This function will disable the purchase button
// The purchase button will display 'Purchased'
function checkBookPurchasedTrue() {
    const purchaseButton = document.getElementById('purchasedButton');
    purchaseButton.textContent = 'Purchased';
    purchaseButton.disabled = true;
    console.log ('checkBookPurchasedTrue')

}

// This function will be called when the game has not been purchased
// This function will enable the purchase button
// The purchase button will display 'Purchase'
function checkBookPurchasedFalse() {
    const purchaseButton = document.getElementById('purchasedButton');
    purchaseButton.disabled = false;
    console.log ('checkBookPurchasedFalse')
    return;
}