// Function to validate email format
function validateEmail(email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

// Function to validate form fields in real-time
function validateLoginForm() {
  const emailInput = document.getElementById("email");
  const passwordInput = document.getElementById("password");
  
  if (emailInput) {
    // Find or create email error container
    let emailErrorContainer = document.querySelector(".email-error");
    if (!emailErrorContainer) {
      emailErrorContainer = document.createElement("div");
      emailErrorContainer.className = "email-error text-red-600 text-sm mt-1";
      emailInput.parentNode.appendChild(emailErrorContainer);
    }
    
    emailInput.addEventListener("input", () => {
      if (!emailInput.value) {
        emailErrorContainer.textContent = "Email is required";
      } else if (!validateEmail(emailInput.value)) {
        emailErrorContainer.textContent = "Please enter a valid email address";
      } else {
        emailErrorContainer.textContent = "";
      }
    });
  }
  
  if (passwordInput) {
    // Find or create password error container
    let passwordErrorContainer = document.querySelector(".password-error");
    if (!passwordErrorContainer) {
      passwordErrorContainer = document.createElement("div");
      passwordErrorContainer.className = "password-error text-red-600 text-sm mt-1";
      passwordInput.parentNode.appendChild(passwordErrorContainer);
    }
    
    passwordInput.addEventListener("input", () => {
      if (!passwordInput.value) {
        passwordErrorContainer.textContent = "Password is required";
      } else {
        passwordErrorContainer.textContent = "";
      }
    });
  }
}

// Ensure DOM is fully loaded before attaching event listeners
document.addEventListener("DOMContentLoaded", () => {
  // Set up real-time validation
  validateLoginForm();
  
  // We allow the form to submit normally to the server
  // WTForms will handle the final validation
});
