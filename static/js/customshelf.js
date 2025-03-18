document.addEventListener('DOMContentLoaded', function() {
  document.getElementById('create-shelf-form').addEventListener('submit', function(e) {
    e.preventDefault();
    let shelfName = document.getElementById('shelf-name').value;
    fetch('/profile/create_shelf/', {  // Updated URL
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-CSRFToken': getCookie('csrftoken')
      },
      body: 'shelf_name=' + encodeURIComponent(shelfName)
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        addShelfToPage(data.shelf_id, shelfName);
      }
    });
  });

  document.querySelectorAll('.shelf-select').forEach(function(select) {
    select.addEventListener('change', function() {
      let bookId = this.dataset.bookId;
      let shelfId = this.value;
      if (shelfId) {
        fetch('/profile/assign_book_to_shelf/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCookie('csrftoken')
          },
          body: 'shelf_id=' + encodeURIComponent(shelfId) + '&book_id=' + encodeURIComponent(bookId)
        })
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            updateBookShelfUI(bookId, shelfId);
          }
        });
      }
    });
  });
});

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function addShelfToPage(shelfId, shelfName) {
  console.log('Adding shelf to page:', shelfId, shelfName);

  let shelfSelects = document.querySelectorAll('.shelf-select');
  console.log('Shelf selects found:', shelfSelects.length);

  let shelfList = document.getElementById('shelf-list');
  console.log('Shelf list found:', !!shelfList);

  let shelvesContainer = document.querySelector('.shelves-container');
  if (!shelvesContainer) {
    console.log('Creating shelves container');
    shelvesContainer = document.createElement('div');
    shelvesContainer.className = 'shelves-container';
    document.body.appendChild(shelvesContainer);
  }
  console.log('Shelves container found:', !!shelvesContainer);
  // Create a new option for the shelf select dropdown
  let option = document.createElement('option');

  option.value = shelfId;
  option.textContent = shelfName;

  // Add the new option to all shelf select dropdowns
  shelfSelects.forEach(select => {
    select.appendChild(option.cloneNode(true));
  });

  // Add the new shelf to the shelf list if it exists
  if (shelfList) {
    let listItem = document.createElement('li');
    listItem.textContent = shelfName;
    shelfList.appendChild(listItem);
  }

  // Add the new shelf to the shelves container if it exists
  if (shelvesContainer) {
    let shelfDiv = document.createElement('div');
    shelfDiv.className = 'shelf';
    shelfDiv.innerHTML = `
      <h3>${shelfName}</h3>
      <div class="shelf-books"></div>
    `;
    shelvesContainer.appendChild(shelfDiv);
    console.log('New shelf added to container');
  }


  // Clear the input field
  let shelfNameInput = document.getElementById('shelf-name');
  if (shelfNameInput) {
    shelfNameInput.value = '';
  }

  // Show a success message
  alert('New shelf created: ' + shelfName);

  // Optionally, refresh the page to ensure all elements are updated
  // window.location.reload();

  // Force a re-render
  document.body.style.display = 'none';
  document.body.offsetHeight; // Trigger a reflow
  document.body.style.display = '';

  console.log('Page re-rendered');
}



function updateBookShelfUI(bookId, shelfId) {
  // This function should update the UI to show that a book has been added to a shelf
  console.log(`Book ${bookId} added to shelf ${shelfId}`);

  // For example, you might want to update a label or move the book element
  let bookElement = document.querySelector(`[data-book-id="${bookId}"]`);
  if (bookElement) {
    let shelfName = document.querySelector(`#shelf-select option[value="${shelfId}"]`).textContent;
    bookElement.querySelector('.shelf-label').textContent = `On shelf: ${shelfName}`;
  }
}
