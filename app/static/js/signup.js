// Function to validate password and confirm password
function validatePassword() {
  const password = document.getElementById("password").value;
  const confirmPassword = document.getElementById("confirm-password").value;
  const errorMessage = document.getElementById("password-error");

  const errors = [];

  if (password.length < 8) errors.push("at least 8 characters");
  if (!/[A-Z]/.test(password)) errors.push("one uppercase letter");
  if (!/\d/.test(password)) errors.push("one number");
  if (!/[@$!%*?&]/.test(password)) errors.push("one special character");

  // If there are password format errors
  if (errors.length > 0) {
    errorMessage.textContent = "Password must include: " + errors.join(", ");
    errorMessage.style.display = "block";
    return false;
  }

  // Check if passwords match
  if (password !== confirmPassword) {
    errorMessage.textContent = "Passwords do not match.";
    errorMessage.style.display = "block";
    return false;
  }

  errorMessage.textContent = ""; // Clear error message
  errorMessage.style.display = "none";
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
  const passwordInput = document.getElementById("password");
  const confirmPasswordInput = document.getElementById("confirm-password");

  if (signupForm) {
    signupForm.addEventListener("submit", handleSignup);
  } else {
    console.error("Signup form not found.");
  }

  // Real-time password validation
  passwordInput.addEventListener("input", validatePassword);
  confirmPasswordInput.addEventListener("input", validatePassword);
});
