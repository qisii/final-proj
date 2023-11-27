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
// ////////////////////////////////////////////////////
// ////////////////////////// Chart
// ////////////////////////////////////////////////////


// DENGUE

document.addEventListener('DOMContentLoaded', function () {
    // Parse the JSON data passed from Django
    var overallResults = JSON.parse(document.getElementById('overall_results_json').textContent);

    // Extract data for the chart
    var locations = overallResults.map(result => result.location);
    var casesData = overallResults.map(result => result.overall_cases);
    var deathsData = overallResults.map(result => result.overall_deaths);

    // Create a bar chart using Chart.js
    var ctx = document.getElementById('dengueChart').getContext('2d');
    var dengueChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: locations,
            datasets: [
                {
                    label: 'Overall Cases',
                    data: casesData,
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                },
                {
                    label: 'Overall Deaths',
                    data: deathsData,
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 1
                }
            ]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
});