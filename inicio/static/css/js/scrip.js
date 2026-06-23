const menuvtn = document.querySelector('.menu-btn');
const navlinks = document.getElementById('nav-links');
const links = navlinks.navlinks.querySelectorAll('a');
menuvtn.addEventListener('click', () => {
    navlinks.classList.toggle("activate");
    if (navlinks.classList.contains("activate")){
        menuBtn.innerHTML = "X";
        menuBtn.setAttribute('aria-expanded', 'true');
    } else {
        menuBtn.innerHTML = "☰";
        menuBtn.setAttribute("aria-expanded", "false");
    }
});
links.forEach(link => {
    link.addEventListener('click', () => {
        navlinks.classList.remove("activate");
        menuBtn.innerHTML = "☰";
        menuBtn.setAttribute("aria-expanded", "false");
    });
});    
