const editButtons = document.getElementsByClassName("btn-edit");
const commentTitle_Value = document.getElementById("id_title");
const commentRating_Value = document.getElementById("id_rating");
const commentBody_Value = document.getElementById("id_body");
const commentForm = document.getElementById("commentForm");
const submitButton = document.getElementById("submitButton");

const deleteModal = new bootstrap.Modal(document.getElementById("deleteModal"));
const deleteButtons = document.getElementsByClassName("btn-delete");
const deleteConfirm = document.getElementById("deleteConfirm");

function safeGetElementById(id) {
    return document.getElementById(id) || { value: '' };
}

function safeGetInnerText(element) {
    return element ? element.innerText.trim() : '';
}

function convertRatingToChoice(rating) {
    const numericRating = parseInt(rating);
    const ratingMap = {
        1: '1 ★',
        2: '2 ★★',
        3: '3 ★★★',
        4: '4 ★★★★',
        5: '5 ★★★★★'
    };
    return ratingMap[numericRating] || numericRating.toString();
}

for (let button of editButtons) {
    button.addEventListener("click", (e) => {
        let commentId = e.target.getAttribute("data-comment_id");

        let commentElement = e.target.closest('.review');
        let commentTitle = safeGetInnerText(commentElement.querySelector(`#title${commentId}`));
        let commentRating = safeGetInnerText(commentElement.querySelector('.User-Review-Rating')).split('/')[0];
        let commentText = safeGetInnerText(commentElement.querySelector(`#text${commentId}`));

        if (commentTitle_Value) commentTitle_Value.value = commentTitle;
        if (commentRating_Value) commentRating_Value.value = commentRating;
        if (commentBody_Value) commentBody_Value.value = commentText;

        if (submitButton) submitButton.innerText = "Update";
        if (commentForm) commentForm.setAttribute("action", `edit_comment/${commentId}`);

        // Show the review form
        const leaveReviewForm = document.querySelector('.leave-review-form');
        if (leaveReviewForm) {
            leaveReviewForm.style.display = 'block';
        }

        // Scroll to the form
        if (commentForm) commentForm.scrollIntoView({behavior: "smooth"});
    });
}

/**
 * Initializes deletion functionality for the provided delete buttons.
 */
for (let button of deleteButtons) {
    button.addEventListener("click", (e) => {
        let commentId = e.target.getAttribute("data-comment_id");
        if (deleteConfirm) deleteConfirm.href = `delete_comment/${commentId}`;
        if (deleteModal) deleteModal.show();
    });
}


// NEW REVIEW FORM TOGGLE
document.addEventListener('DOMContentLoaded', function() {
  const toggleReviewForm = document.querySelector('.toggle-review-form');
  const leaveReviewForm = document.querySelector('.leave-review-form');

  if (toggleReviewForm && leaveReviewForm) {
      toggleReviewForm.addEventListener('click', function() {
          leaveReviewForm.style.display = leaveReviewForm.style.display === 'none' ? 'block' : 'none';
          this.classList.toggle('fa-chevron-down');
          this.classList.toggle('fa-chevron-up');
      });
  } else {
      console.log('Review form toggle elements not found');
  }

//   // New code for handling the delay and refresh
//   const urlParams = new URLSearchParams(window.location.search);
//   const isPurchased = urlParams.get('purchased');

//   console.log('Initial isPurchased:', isPurchased);
//   console.log('Initial Hash:', window.location.hash);

//   if (isPurchased === null) {
//     console.log('purchased parameter not found, adding after delay');
//     // If 'purchased' parameter is not in the URL, add it after a delay
//     setTimeout(() => {
//       const bookIsPurchased = checkIfBookIsPurchased(); 
//       console.log('checkIfBookIsPurchased result:', bookIsPurchased);
//       const newUrl = new URL(window.location.href);
//       newUrl.searchParams.set('purchased', bookIsPurchased ? 'true' : 'false');
//       console.log('Redirecting to:', newUrl.toString());
//       window.location.href = newUrl.toString();
//     }, 1000); // 1 second delay
//   } else {
//     console.log('purchased parameter found, checking conditions for scrolling');
//     // If 'purchased' parameter is already in the URL, handle scrolling
//     console.log('Hash:', window.location.hash);
//     console.log('isPurchased:', isPurchased);

//     if(window.location.hash && isPurchased === 'true') {
//       console.log('Conditions met for scrolling');
//       const id = window.location.hash.substring(1);
//       console.log('Searching for element with id:', id);
//       const element = document.getElementById(id);
//       if(element) {
//         console.log('Element found, scrolling to:', id);
//         // Delay scrolling by 2 seconds
//         setTimeout(() => {
//           // Scroll to the element
//           element.scrollIntoView({ behavior: 'smooth', block: 'center' });
          
//           // Highlight the comment temporarily
//           element.style.transition = 'background-color 0.5s';
//           element.style.backgroundColor = '#ffffd0';  // Light yellow highlight
//           setTimeout(() => {
//               element.style.backgroundColor = '';  // Remove highlight after 2 seconds
//           }, 2000);
//         }, 2000); // 2 second delay before scrolling
//       } else {
//         console.log('Element not found:', id);
//       }
//     } else {
//       console.log('Conditions not met for scrolling:');
//       console.log('window.location.hash:', window.location.hash);
//       console.log('isPurchased === "true":', isPurchased === 'true');
//     }
//   }
});

// function checkIfBookIsPurchased() {
//   // This is a placeholder. Replace with your actual logic.
//   console.log('checkIfBookIsPurchased called');
//   return true;
// }