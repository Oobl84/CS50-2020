<<<<<<< HEAD
document.getElementById("logo").addEventListener("click", swapStyle);

function swapStyle() {
    var password = "Directorate S";
    var logo = document.getElementById("logo").src;
    var currentStyle = document.getElementById("pagestyle").getAttribute("href");

    if (currentStyle === "styles.css") {

        var pw = prompt("Please enter your password");

        if (pw === password) {
            document.getElementById("pagestyle").setAttribute("href", "styles-c.css");
            logo = "images/communist.png";
            alert("Welcome, Comrade")
        }
    }
    else {
        document.getElementById("pagestyle").setAttribute("href", "styles.css");
        logo = "images/dupont-circle-logo.png";
    }
    
=======
document.getElementById("logo").addEventListener("click", swapStyle);

function swapStyle() {
    var password = "Directorate S";
    var logo = document.getElementById("logo").src;
    var currentStyle = document.getElementById("pagestyle").getAttribute("href");

    if (currentStyle === "styles.css") {

        var pw = prompt("Please enter your password");

        if (pw === password) {
            document.getElementById("pagestyle").setAttribute("href", "styles-c.css");
            logo = "images/communist.png";
            alert("Welcome, Comrade")
        }
    }
    else {
        document.getElementById("pagestyle").setAttribute("href", "styles.css");
        logo = "images/dupont-circle-logo.png";
    }
    
>>>>>>> c8d7d510cdb1182d61c999fb1ac603c6e2d94e3f
}