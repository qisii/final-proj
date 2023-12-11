// Smooth scrolling
document.addEventListener('DOMContentLoaded', function () {
    // Smooth scroll 
    document.querySelector('.member-button').addEventListener('click', function () {
        setTimeout(function () {
            document.querySelector('#members-section').scrollIntoView({
                behavior: 'smooth'
            });
        }, 300);
    });
});

// scroll reveal animations
document.addEventListener('DOMContentLoaded', function () {
    const scrollReveal = ScrollReveal({
        duration: 1000,
        reset: true,
    });

    // Page Headings and Narrations
    scrollReveal.reveal('.narration-column, .narration-hr, .narration-display p', {
        origin: 'left',
        distance: '100px',
        delay: 200,
        interval: 100
    });

    // Form and Chart
    scrollReveal.reveal('.form-display, .chart-column, .form-geo-display, .chart-geo-column, .chart-region-column', {
        origin: 'right',
        distance: '100px',
        delay: 200,
        interval: 100
    });

    // index
    scrollReveal.reveal('.member-subheading, .member-heading, .team-members, .members-section .buttons-container',{
        origin: 'top',
        distance: '50px',
        delay: 100,
        interval: 100
    });

    // More
    scrollReveal.reveal('.more-hr', {
        origin: 'left',
        distance: '100px',
        delay: 200,
        interval: 100
    });

});
