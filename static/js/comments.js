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
        let commentRating = e.target.getAttribute("data-rating");

        let commentElement = e.target.closest('.review');
        let commentTitle = safeGetInnerText(commentElement.querySelector(`#title${commentId}`));
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
  }
});