/*!
 * Start Bootstrap - Creative Bootstrap Theme (http://startbootstrap.com)
 * Code licensed under the Apache License v2.0.
 * For details, see http://www.apache.org/licenses/LICENSE-2.0.
 */

(function($) {
    "use strict"; // Start of use strict

    // jQuery for page scrolling feature - requires jQuery Easing plugin
    $('a.page-scroll').bind('click', function(event) {
        var $anchor = $(this);
        $('html, body').stop().animate({
            scrollTop: ($($anchor.attr('href')).offset().top - 50)
        }, 1250, 'easeInOutExpo');
        event.preventDefault();
    });

    // Highlight the top nav as scrolling occurs
    $('body').scrollspy({
        target: '.navbar-fixed-top',
        offset: 51
    })

    // Closes the Responsive Menu on Menu Item Click
    $('.navbar-collapse ul li a').click(function() {
        $('.navbar-toggle:visible').click();
    });

    // Fit Text Plugin for Main Header
    $("h1").fitText(
        1.2, {
            minFontSize: '35px',
            maxFontSize: '65px'
        }
    );

    // Offset for Main Navigation
    /*
    $('#mainNav').affix({
        offset: {
            top: 100
        }
    })
    */

    // Initialize WOW.js Scrolling Animations
    new WOW().init();

    //Hide messages after timeout
    setTimeout(function(){
        $(".alert").slideUp(1000);
    }, 3000);


    jQuery.validator.addMethod("nospace", function(value, element) {
         return value.indexOf(" ") < 0 && value != "";
      }, "Space are not allowed.");

    jQuery.validator.addMethod("specialCharacters", function(value, element) {
         return this.optional(element) || /^[a-z0-9\-\_\s]+$/i.test(value);
      }, "Letters, Numbers or dashes only.");

    //handle url shorten form validation
    $("#shorten-form").validate({
      errorPlacement: function(error, element) {
         $("#validateError").html(error);
       },
            success: function (error) {
                error.remove();
            }
     });


    //handle url shorten form validation
    $("#update_shortened_link_form").validate();



})(jQuery); // End of use strict
