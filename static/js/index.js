$(document).ready(function(e) {
    $('#test').scrollToFixed();
    $('.res-nav_click').click(function() {
        $('.main-nav').slideToggle();
        return false
    });
});

wow = new WOW({
    animateClass: 'animated',
    offset: 100
});
wow.init();


$(window).on('load', function() {

    $('.main-nav li a, .servicelink').bind('click', function(event) {
        var $anchor = $(this);

        $('html, body').stop().animate({
            scrollTop: $($anchor.attr('href')).offset().top - 102
        }, 1500, 'easeInOutExpo');
        /*
        if you don't want to use the easing effects:
        $('html, body').stop().animate({
            scrollTop: $($anchor.attr('href')).offset().top
        }, 1000);
        */
        if ($(window).width() < 768) {
            $('.main-nav').hide();
        }
        event.preventDefault();
    });
    $('#form-test-api-submit').bind('click', function(e) {
        alert('Sending Form Pressed...')
        event.preventDefault();
    });
})
