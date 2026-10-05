// ==================================================
// SMART BLOOD BANK
// Theme Controller
// ==================================================

const themeToggle = document.getElementById("themeToggle");


// --------------------------------------------------
// LOAD SAVED THEME
// --------------------------------------------------

const savedTheme = localStorage.getItem("bloodBankTheme");

if (savedTheme === "dark") {
    document.body.classList.add("dark-mode");
}


// --------------------------------------------------
// UPDATE TOGGLE ICON
// --------------------------------------------------

function updateThemeIcon() {

    if (!themeToggle) {
        return;
    }

    if (document.body.classList.contains("dark-mode")) {
        themeToggle.textContent = "☀️";
        themeToggle.title = "Switch to Light Mode";
    } else {
        themeToggle.textContent = "🌙";
        themeToggle.title = "Switch to Dark Mode";
    }
}

updateThemeIcon();


// --------------------------------------------------
// TOGGLE THEME
// --------------------------------------------------

if (themeToggle) {

    themeToggle.addEventListener("click", function () {

        document.body.classList.toggle("dark-mode");

        const isDark =
            document.body.classList.contains("dark-mode");

        localStorage.setItem(
            "bloodBankTheme",
            isDark ? "dark" : "light"
        );

        updateThemeIcon();

    });

}