document.addEventListener('DOMContentLoaded', function () {
    const editLinks = document.querySelectorAll('.edit-link');
    const editForm = document.querySelector('.edit-form');
    const saveButton = document.getElementById('save-changes');

    // Show the edit form and populate fields when an edit link is clicked
    editLinks.forEach((link) => {
        link.addEventListener('click', function (e) {
            e.preventDefault();
            const field = link.getAttribute('data-field');
            const fieldValue = document.getElementById(field).textContent.trim();
            const editField = document.getElementById(`edit-${field}`);

            editForm.style.display = 'block';
            editField.value = fieldValue;
            document.getElementById(field).style.display = 'none';
        });
    });

    // Handle form submission to update the profile information
    document.getElementById('profile-edit-form').addEventListener('submit', function (e) {
        e.preventDefault();

        // Collect the updated information from the form
        const updatedName = document.getElementById('edit-name').value;
        const updatedEmail = document.getElementById('edit-email').value;
        const updatedContact = document.getElementById('edit-contact').value;
        const updatedDesignation = document.getElementById('edit-designation').value;
        const updatedCompany = document.getElementById('edit-company').value;

        // Send an HTTP request to update the user's profile
        // You'll need to implement the server-side logic to handle the update

        // Update the displayed profile
    });
});
