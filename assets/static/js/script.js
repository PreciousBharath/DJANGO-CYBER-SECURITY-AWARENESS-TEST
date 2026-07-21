// Add any JavaScript functionality here if needed
$(document).ready(function() {
    // Example: Smooth scrolling to sections
    $('.nav-link').click(function(event) {
        event.preventDefault();
        $('html, body').animate({
            scrollTop: $($.attr(this, 'href')).offset().top
        }, 500);
    });
});
