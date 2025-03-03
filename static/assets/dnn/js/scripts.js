// Function to handle theme toggle
function toggleTheme() {
  document.body.classList.toggle("dark-mode");
  // Update localStorage with the current theme preference
  if (document.body.classList.contains("dark-mode")) {
    localStorage.setItem("theme", "dark");
  } else {
    localStorage.setItem("theme", "light");
  }
}

// DOMContentLoaded event to initialize theme and add event listeners
document.addEventListener("DOMContentLoaded", function () {
  // Check if dark mode is already enabled in localStorage
  if (localStorage.getItem("theme") === "dark") {
    document.body.classList.add("dark-mode");
  }

  // Select the theme toggle buttons
  const toggleButton = document.getElementById("theme-toggle");
  const themeSwitcher = document.getElementById("themeSwitcher");

  // Add event listeners for both buttons
  if (toggleButton) {
    toggleButton.addEventListener("click", toggleTheme);
  }

  if (themeSwitcher) {
    themeSwitcher.addEventListener("click", toggleTheme);
  }
});

function scrollLeft(uniqueSliderId) {
  const container = document.getElementById(uniqueSliderId);
  container.scrollBy({ left: -100, behavior: "smooth" });
}

function scrollRight(uniqueSliderId) {
  const container = document.getElementById(uniqueSliderId);
  container.scrollBy({ left: 100, behavior: "smooth" });
}

// universel js for share  start
function scrollLeft(postsId) {
  const container = document.getElementById(shareSlider-${postsId});
  container.scrollBy({ left: -100, behavior: "smooth" });
}

function scrollRight(postsId) {
  const container = document.getElementById(shareSlider-${postsId});
  container.scrollBy({ left: 100, behavior: "smooth" });
}

function copyLink(slug) {
  const link = ${window.location.origin}/${slug};
  navigator.clipboard
    .writeText(link)
    .then(() => alert("Link copied to clipboard!"))
    .catch((err) => console.error("Failed to copy link: ", err));
}
// universel js for share end