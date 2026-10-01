const form = document.getElementById("login-form");
const message = document.getElementById("message");
const submitted = document.getElementById("submitted");

function show(text, ok) {
  message.textContent = text;
  message.className = ok ? "ok" : "";
}

function clientError(email, password) {
  if (email === "" || password === "") {
    return "Email and password are required.";
  }
  if (!email.includes("@") || email.startsWith("@") || email.endsWith("@")) {
    return "Email must contain @.";
  }
  if (password.length < 8) {
    return "Password must be at least 8 characters.";
  }
  return "";
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value;
  submitted.textContent = "";

  const error = clientError(email, password);
  if (error) {
    show(error);
    return;
  }

  const response = await fetch("/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  const data = await response.json();
  show(data.message, data.ok);
  submitted.textContent = "Submitted email: " + email;
});
