// AUTHENTICATION PAGE
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
