// Top navigation hamburger icon
function dynamicTopNav() {
    var x = document.getElementById('top-nav');
    if (x.className === 'topnav') {
        x.className += " responsive";
    } else {
        x.className = 'topnav';
    }
}

// Toastr message options
toastr.options = {
    "closeButton": true,
    "debug": false,
    "progressBar": true,
    "preventDuplicates": false,
    "positionClass": "toast-top-center",
    "onclick": null,
    "showDuration": "400",
    "hideDuration": "1000",
    "timeOut": "8000",
    "extendedTimeOut": "1000",
    "showEasing": "swing",
    "hideEasing": "linear",
    "showMethod": "fadeIn",
    "hideMethod": "fadeOut"
};