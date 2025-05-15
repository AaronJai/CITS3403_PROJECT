document.addEventListener("DOMContentLoaded", () => {
        // Updating to use the proper WTForms field IDs
        const form = document.querySelector("form");
        const newPassword = document.getElementById("new_password");
        const confirmPassword = document.getElementById("confirm_password");

        // Set up real-time validation if needed for better UX
        if (newPassword && confirmPassword) {
            const validatePassword = () => {
                if (!newPassword.value) return; // Don't validate empty fields

                // The server-side validation will handle the actual validation and error messages
                // This is just for a better user experience
            };

            newPassword.addEventListener("input", validatePassword);
            confirmPassword.addEventListener("input", validatePassword);
        }
    });

    function confirmDeletion() {
        const confirmation = prompt("To confirm deletion, type DELETE in the box below:");

        if (confirmation && confirmation.trim() === "DELETE") {
            const feedback = document.createElement("div");
            feedback.textContent = "DELETING YOUR ACCOUNT...";
            feedback.className = "fixed top-6 left-1/2 transform -translate-x-1/2 bg-red-100 text-red-800 font-bold py-2 px-6 rounded-md shadow z-50";
            document.body.appendChild(feedback);
            setTimeout(() => {
                document.getElementById("delete_account_form").submit();
            }, 2000); // Remove after 2 seconds
        } else if (confirmation !== null) {
            alert("Incorrect confirmation. Account was not deleted.");
        }
    }