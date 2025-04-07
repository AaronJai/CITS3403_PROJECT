// Function to validate password and confirm password
function validatePassword() {
  const password = document.getElementById("password").value;
  const confirmPassword = document.getElementById("confirm-password").value;
  const errorMessage = document.getElementById("password-error");

  // Regex for password validation
  const passwordRegex =
    /^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;

  // Check if password matches the criteria
  if (!passwordRegex.test(password)) {
    errorMessage.textContent =
      "Password must be at least 8 characters long, include one uppercase letter, one number, and one special character.";
    return false;
  }

  // Check if passwords match
  if (password !== confirmPassword) {
    errorMessage.textContent = "Passwords do not match.";
    return false;
  }

  errorMessage.textContent = ""; // Clear error message
  return true;
}

// Function to handle signup form submission
async function handleSignup(event) {
  event.preventDefault(); // Prevent form submission for now

  if (!validatePassword()) {
    return; // Stop execution if password validation fails
  }

  const firstName = document.getElementById("first-name").value;
  const lastName = document.getElementById("last-name").value;
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  console.log("First Name:", firstName);
  console.log("Last Name:", lastName);
  console.log("Email:", email);
  console.log("Password:", password);

  // Placeholder for signup backend communication
  // TODO: Add signup server communication logic here
}

// Ensure DOM is fully loaded before attaching event listener
document.addEventListener("DOMContentLoaded", () => {
  const signupForm = document.querySelector("form[action='/signup']");
  if (signupForm) {
    signupForm.addEventListener("submit", handleSignup);
  } else {
    console.error("Signup form not found.");
  }
});
