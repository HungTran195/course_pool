const navbar = document.querySelector('.navbar');
const navbar_toggler = document.querySelector('.navbar-toggler');
const init = function () {

    let current_page = window.location.href.split('/');

    const nav_container = document.querySelectorAll('.navbar-nav .navbar-text');
    for (let i = 0; i < nav_container.length; i++) {
        if (nav_container[i].classList.contains('active')) {
            nav_container[i].classList.remove('active');
        };
    }
    if (current_page.includes('suggest_course')) {
        document.getElementById('suggest').classList.add('active');
    }
    else if (current_page.includes('favorite')) {
        document.getElementById('favorite').classList.add('active');
    }
    else {
        document.getElementById('home').classList.add('active');
    }

}
init();

const focus_navbar = function () {

}

navbar_toggler.addEventListener('click', () => {
    if (navbar_toggler.ariaExpanded === 'true') {
        document.getElementById("navbarNav").focus();
    }
});