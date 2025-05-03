// Function to validate password and confirm password
function validatePassword() {
  const password = document.getElementById("password").value;
  const confirmPassword = document.getElementById("confirm-password").value;
  
  // Find or create error containers
  let passwordErrorContainer = document.querySelector(".password-error");
  if (!passwordErrorContainer) {
    passwordErrorContainer = document.createElement("div");
    passwordErrorContainer.className = "password-error text-red-600 text-sm mt-1";
    document.getElementById("password").parentNode.appendChild(passwordErrorContainer);
  }
  
  const errors = [];

  if (password.length < 8) errors.push("at least 8 characters");
  if (!/[A-Z]/.test(password)) errors.push("one uppercase letter");
  if (!/\d/.test(password)) errors.push("one number");
  if (!/[@$!%*?&]/.test(password)) errors.push("one special character");

  // If there are password format errors
  if (errors.length > 0) {
    passwordErrorContainer.textContent = "Password must include: " + errors.join(", ");
    return false;
  }

  // Check if passwords match
  if (password !== confirmPassword && confirmPassword.length > 0) {
    passwordErrorContainer.textContent = "Passwords do not match.";
    return false;
  }

  passwordErrorContainer.textContent = ""; // Clear error message
  return true;
}

// Function to handle form input validation in real-time
function setupRealTimeValidation() {
  const passwordInput = document.getElementById("password");
  const confirmPasswordInput = document.getElementById("confirm-password");
  
  if (passwordInput) {
    passwordInput.addEventListener("input", validatePassword);
  }
  
  if (confirmPasswordInput) {
    confirmPasswordInput.addEventListener("input", validatePassword);
  }
}

// Ensure DOM is fully loaded before attaching event listeners
document.addEventListener("DOMContentLoaded", () => {
  // Set up real-time validation
  setupRealTimeValidation();
  
  // We allow the form to submit normally to the server
  // WTForms will handle the final validation
});
