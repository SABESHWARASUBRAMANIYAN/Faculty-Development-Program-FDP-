
const contentSection = document.getElementById("content");

document.querySelector(".submenu").addEventListener("click", function(event) {
    if (event.target.tagName === "A") {
        event.preventDefault();
        const target = event.target.getAttribute("data-target");
        loadContent(target);
    }
});

function loadContent(target) {
    let content = "";

    switch (target) {
        case "home":
            content = "<h1>Welcome to Our Website</h1><p>This is the main content of the page.</p>";
            break;
        case "about":
            content = "<h1>About Us</h1><p>We are a company that specializes in...</p>";
            break;
        case "services":
            content = "<h1>Our Services</h1><p>We offer a wide range of services including...</p>";
            break;
        case "contact":
            content = "<h1>Contact Us</h1><p>Feel free to reach out to us at...</p>";
            break;
        default:
            content = "<h1>Welcome to Our Website</h1><p>This is the main content of the page.</p>";
    }

    contentSection.innerHTML = content;
}
