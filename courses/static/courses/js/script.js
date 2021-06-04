const navbar = document.querySelector('.navbar');
const navbar_toggler = document.querySelector('.navbar-toggler');
const toggle_favorite_btn = document.querySelectorAll('.toggle-favorite');
const input_field = document.querySelectorAll('input.form-control');
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

// Displace placeholder of input field if value is None
for (let i = 0; i < input_field.length; i++) {
    if (input_field[i].value == 'None') {
        input_field[i].value = '';
    }
};

// Focus navbar when menu is displayed in collapsed mode
// as suggested by bootstrap5
navbar_toggler.addEventListener('click', () => {
    if (navbar_toggler.ariaExpanded === 'true') {
        document.getElementById("navbarNav").focus();
    }
});


// Get CSRFtoken to send POST request to Django
// Code from https://docs.djangoproject.com/en/3.2/ref/csrf/#ajax
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');


// Send course_id to Server to add or remove a course from favorite list
const toggle_favorite = function (toggle_favorite_sign) {
    let course_id = toggle_favorite_sign.id
    fetch('/toggle_favorite', {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest', //Necessary to work with request.is_ajax()
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'course_id': course_id })
    }).then((_res) => {
        // TODO: change toggle_favorite_sign if succees
    }).catch((error) => {
        // TODO: display error if cannot bookmark any course        
    });;
}

// Get click event from favorite sign
for (let i = 0; i < toggle_favorite_btn.length; i++) {
    toggle_favorite_btn[i].addEventListener('click', () => {
        let toggle_favorite_sign = toggle_favorite_btn[i].children[0];
        if (toggle_favorite_sign.classList.contains('fas')) {
            toggle_favorite_sign.classList.replace('fas', 'far');
        }
        else {
            toggle_favorite_sign.classList.replace('far', 'fas');
        };
        toggle_favorite(toggle_favorite_btn[i])
    });
}

