// Function to handle login form submission
async function handleLogin(event) {
  event.preventDefault(); // Prevent form submission for now

  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  console.log("Email:", email);
  console.log("Password:", password);

  // Placeholder for login backend communication
  // TODO: Add login server communication logic here
}

// Ensure DOM is fully loaded before attaching event listener
document.addEventListener("DOMContentLoaded", () => {
  const loginForm = document.querySelector("form[action='/login']");
  if (loginForm) {
    loginForm.addEventListener("submit", handleLogin);
  } else {
    console.error("Login form not found.");
  }
});
