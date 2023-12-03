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

    // home
    // scrollReveal.reveal('.home-heading-container', { origin: 'bottom', distance: '20px', delay: 100 });
    // scrollReveal.reveal('.home-heading', { origin: 'bottom', distance: '20px', delay: 300 });
    // scrollReveal.reveal('.sub-heading', { origin: 'bottom', distance: '20px', delay: 500 });
    // scrollReveal.reveal('.buttons-container', { origin: 'bottom', distance: '20px', delay: 700 });

    // images
    // scrollReveal.reveal('.image1', { origin: 'left', distance: '20px', delay: 200 });
    // scrollReveal.reveal('.image2', { origin: 'bottom', distance: '20px', delay: 400 });
    // scrollReveal.reveal('.image3', { origin: 'right', distance: '20px', delay: 600 });
    // scrollReveal.reveal('.image4', { origin: 'left', distance: '20px', delay: 800 });

    // members
    scrollReveal.reveal('.member-subheading', { origin: 'bottom', distance: '50px', delay: 100, interval: 100 });
    scrollReveal.reveal('.member-heading', { origin: 'bottom', distance: '50px', delay: 300, interval: 100 });
    scrollReveal.reveal('.team-members', { origin: 'top', distance: '50px', delay: 500, interval: 100 });
    scrollReveal.reveal('.members-section .buttons-container', { origin: 'bottom', distance: '50px', delay: 700 });

    // Page Headings and Narrations
    scrollReveal.reveal('.page-subheading, .page-heading, .overview, .narration-column, .narration-hr, .narration-display p', {
        origin: 'left',
        distance: '100px',
        delay: 200,
        interval: 100
    });

    // Form and Chart
    scrollReveal.reveal('.form-display, .chart-column, .form-geo-display, .chart-geo-column', {
        origin: 'right',
        distance: '100px',
        delay: 200,
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