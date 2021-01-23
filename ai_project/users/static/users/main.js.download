/** ==========================================================================================

  Project :   Nutricare - Responsive Multi-purpose HTML5 Template
  Version :   Bootstrap 4.1.1
  Author :    Themetechmount

========================================================================================== */


/** ===============

1. Preloader
2. TopSearch
3. fbar
4. Fixed-header
5. Menu
6. Number rotator
7. Enables menu toggle
8. Skillbar
9. Tab
10. Accordion
11. Isotope
12. Prettyphoto
13. owlCarousel
    
    .. Blog slide
    .. Event slide
    .. Post slide
    .. Testimonial slide
    .. Clients-logo
    .. Team slide
    .. Customer-slide
    .. claasic-blog-slide

13. One Page setting

14. Back to top 

 =============== */



(function($) {

   'use strict'


/*------------------------------------------------------------------------------*/
/* Preloader
/*------------------------------------------------------------------------------*/
// makes sure the whole site is loaded
 $(window).on("load",function() {
        // will first fade out the loading animation
     $("#preloader").fadeOut();
        // will fade out the whole DIV that covers the website.
     $("#status").fadeOut(9000);
})


/*------------------------------------------------------------------------------*/
/* TopSearch
/*------------------------------------------------------------------------------*/
  jQuery(".ttm-header-search-link a").on('click',function()
  {
    jQuery(".ttm-search-overlay").addClass('st-show');
    jQuery(".ttm-overlay-serachform").addClass('st-show');
    jQuery("body").addClass('st-prevent-scroll');
    jQuery(".field.searchform-s").focus();return!1
});
  jQuery(".ttm-icon-close").on('click',function()
    {
        jQuery(".ttm-search-overlay").removeClass('st-show');
        jQuery(".ttm-overlay-serachform").removeClass('st-show');
        jQuery("body").removeClass('st-prevent-scroll');return!1
    });
        jQuery('.ttm-site-searchform').on('click',function(event){event.stopPropagation()})
/*------------------------------------------------------------------------------*/
/* fbar
/*------------------------------------------------------------------------------*/

jQuery(".ttm-fbar-btn > a.ttm-fbar-btn-link").on('click', function(){     
        if( jQuery(this).closest('.ttm-fbar').hasClass('themetechmount-fbar-position-default') ){
            // Fbar top position
            if( jQuery('.ttm-fbar-box-w').css('display')=='none' ){
                jQuery('.ttm-fbar-open-icon', this).fadeOut();
                jQuery('.ttm-fbar-close-icon', this).fadeIn();
                
                jQuery('.ttm-fbar-box-w').slideDown();
            } else {
                jQuery('.ttm-fbar-open-icon', this).fadeIn();
                jQuery('.ttm-fbar-close-icon', this).fadeOut();
                
                jQuery('.ttm-fbar-box-w').slideUp();
            }
        } else {
            // Fbar right position
        }       
        
        return false;
    }); 
        
    // Right btn click event
    jQuery('.ttm-fbar-close, .ttm-fbar-btn > a.ttm-fbar-btn-link, .ttm-float-overlay').on('click', function(){
        jQuery('.ttm-fbar-box-w').toggleClass('animated');
        jQuery('.ttm-float-overlay').toggleClass('animated');
        jQuery('.ttm-fbar-btn').toggleClass('animated');     
    });

/*------------------------------------------------------------------------------*/
/* Fixed-header
/*------------------------------------------------------------------------------*/


$(window).scroll(function(){
    if ( matchMedia( 'only screen and (min-width: 1200px)' ).matches ) 
    {
        if ($(window).scrollTop() >= 50 ) {
            $('.ttm-stickable-header').addClass('fixed-header');
            $('.ttm-stickable-header').addClass('visible-title');
        }
        else {

            $('.ttm-stickable-header').removeClass('fixed-header');
            $('ttm-stickable-header').removeClass('visible-title');
            }
    }
});


/*------------------------------------------------------------------------------*/
/* Menu
/*------------------------------------------------------------------------------*/

    $('ul li:has(ul)').addClass('has-submenu');
    $('ul li ul').addClass('sub-menu');


    $("ul.dropdown li").on({

        mouseover: function(){
           $(this).addClass("hover");
        },  
        mouseout: function(){
           $(this).removeClass("hover");
        }, 

    });
    
    var $menu = $('#menu'), $menulink = $('#menu-toggle-form'), $menuTrigger = $('.has-submenu > a');
    $menulink.on('click',function (e) {

        $menulink.toggleClass('active');
        $menu.toggleClass('active');
    });

    $menuTrigger.on('click',function (e) {
        e.preventDefault();
        var t = $(this);
        t.toggleClass('active').next('ul').toggleClass('active');
    });

    $('ul li:has(ul)');


/*------------------------------------------------------------------------------*/
/* Animation on scroll: Number rotator
/*------------------------------------------------------------------------------*/
    
    $("[data-appear-animation]").each(function() {
        var self      = $(this);
        var animation = self.data("appear-animation");
        var delay     = (self.data("appear-animation-delay") ? self.data("appear-animation-delay") : 0);
        
        if( $(window).width() > 959 ) {
            self.html('0');
            self.waypoint(function(direction) {
                if( !self.hasClass('completed') ){
                    var from     = self.data('from');
                    var to       = self.data('to');
                    var interval = self.data('interval');
                    self.numinate({
                        format: '%counter%',
                        from: from,
                        to: to,
                        runningInterval: 2000,
                        stepUnit: interval,
                        onComplete: function(elem) {
                            self.addClass('completed');
                        }
                    });
                }
            }, { offset:'85%' });
        } else {
            if( animation == 'animateWidth' ) {
                self.css('width', self.data("width"));
            }
        }
    });


/*------------------------------------------------------------------------------*/
/* Skillbar
/*------------------------------------------------------------------------------*/

jQuery('.progress').each(function(){
    jQuery(this).find('.progress-bar').animate({
        width:jQuery(this).attr('data-value')
    },6000);
});


/*------------------------------------------------------------------------------*/
/* Tab
/*------------------------------------------------------------------------------*/ 

$('.ttm-tabs').each(function() {
    $(this).children('.content-tab').children().hide();
    $(this).children('.content-tab').children().first().show();
    $(this).find('.tabs').children('li').on('click', function(e) {  
        var liActive = $(this).index(),
            contentActive = $(this).siblings().removeClass('active').parents('.ttm-tabs').children('.content-tab').children().eq(liActive);
        contentActive.addClass('active').fadeIn('slow');
        contentActive.siblings().removeClass('active');
        $(this).addClass('active').parents('.ttm-tabs').children('.content-tab').children().eq(liActive).siblings().hide();
        e.preventDefault();
    });
});


/*------------------------------------------------------------------------------*/
/* Accordion
/*------------------------------------------------------------------------------*/

/*https://www.antimath.info/jquery/quick-and-simple-jquery-accordion/*/
$('.toggle').eq(0).addClass('active').find('.toggle-content').css('display','block');
$('.accordion .toggle-title').on('click',function(){
    $(this).siblings('.toggle-content').slideToggle('fast');
    $(this).parent().toggleClass('active');
    $(this).parent().siblings().children('.toggle-content:visible').slideUp('fast');
    $(this).parent().siblings().children('.toggle-content:visible').parent().removeClass('active');
});


/*------------------------------------------------------------------------------*/
/* Isotope
/*------------------------------------------------------------------------------*/

$(window).on(function(){

    var $container = $('#isotopeContainer');

    // filter items when filter link is clicked
    $('#filters a').on(function(){
      var selector = $(this).attr('data-filter');
      $container.isotope({ filter: selector });
      return false;
    });

    var $optionSets = $('#filters li'),
        $optionLinks = $optionSets.find('a');

        $optionLinks.on(function(){
            var $this = $(this);
            // don't proceed if already selected
            if ( $this.hasClass('selected') ) {
              return false;
            }
            var $optionSet = $this.parents('#filters');
            $optionSet.find('.selected').removeClass('selected');
            $this.addClass('selected');

            // make option object dynamically, i.e. { filter: '.my-filter-class' }
            var options = {},
                key = $optionSet.attr('data-option-key'),
                value = $this.attr('data-option-value');
            // parse 'false' as false boolean
            value = value === 'false' ? false : value;
            options[ key ] = value;
            if ( key === 'layoutMode' && typeof changeLayoutMode === 'function' ) {
              // changes in layout modes need extra logic
              changeLayoutMode( $this, options )
            } else {
              // otherwise, apply new options
              $container.isotope( options );
            }

            return false;
        });
   });
    
    
/*------------------------------------------------------------------------------*/
/* Prettyphoto
/*------------------------------------------------------------------------------*/
jQuery(document).ready(function(){

 // Normal link
jQuery('a[href*=".jpg"], a[href*=".jpeg"], a[href*=".png"], a[href*=".gif"]').each(function(){
    if( jQuery(this).attr('target')!='_blank' && !jQuery(this).hasClass('prettyphoto') && !jQuery(this).hasClass('modula-lightbox') ){
        var attr = $(this).attr('data-gal');
        if (typeof attr !== typeof undefined && attr !== false && attr!='prettyPhoto' ) {
            jQuery(this).attr('data-rel','prettyPhoto');
        }
    }
});     


jQuery('a[data-gal^="prettyPhoto"]').prettyPhoto();
jQuery('a.ttm_prettyphoto').prettyPhoto();
jQuery('a[data-gal^="prettyPhoto"]').prettyPhoto();
jQuery("a[data-gal^='prettyPhoto']").prettyPhoto({hook: 'data-gal'})

});
    

/*------------------------------------------------------------------------------*/
/* owlCarousel
/*------------------------------------------------------------------------------*/

// ===== 1- Blog slide ==== 

    $(".blog-slide").owlCarousel({  
        loop:true,
        margin:0,
         nav: $('.blog-slide').data('nav'),
        dots: $('.blog-slide').data('dots'),                     
        autoplay: $('.blog-slide').data('auto'),
        smartSpeed: 3000,
        responsive:{
            0:{
                items:1,
            },
            600:{
                items:2,
            },
            992:{
                items: $('.blog-slide').data('item')
            }
        }
    });

// ===== 2- event slide ==== 

    $(".event-slide").owlCarousel({  
        loop:true,
        margin:0,
        nav: $('.event-slide').data('nav'),
        dots: $('.event-slide').data('dots'),                     
        autoplay: $('.event-slide').data('auto'),
        smartSpeed: 1000,
        responsive:{
            0:{
                items:1,
            },
            600:{
                items:2,
            },
            992:{
                items: $('.event-slide').data('item')
            }
        }
    });

// ===== 3 - Post slide ==== 

    $(".post-slide").owlCarousel({  
        loop:true,
        margin:0,
        nav: $('.post-slide').data('nav'),
        dots: $('.post-slide').data('dots'),                     
        autoplay: $('.post-slide').data('auto'),
        smartSpeed: 3000,
        responsive:{
            0:{
                items:1,
            },
            600:{
                items:2,
            },
            992:{
                items: $('.post-slide').data('item')
            }
        }
    });

// ===== 4 - Testimonial slide ==== 

    $(".testimonial-slide").owlCarousel({  
        loop:true,
        margin:0,
        smartSpeed: 1000,
        nav: $('.testimonial-slide').data('nav'),
        dots: $('.testimonial-slide').data('dots'), 
        autoplay: $('.testimonial-slide').data('auto'),
        responsive:{
            0:{
                items:1,
            },
            600:{
                items:1,
            },
            1000:{
                items: $('.testimonial-slide').data('item')
            }
        }
    });

// ===== 5 - Clients-logo ==== 

$(".clients-slide").owlCarousel({ 
    margin: 0,
    loop:true,
    nav: $('.clients-slide').data('nav'),
    dots: $('.clients-slide').data('dots'),                     
    autoplay: $('.clients-slide').data('auto'),
    smartSpeed: 3000,
    responsive:{
        0:{
            items:1
        },
        480:{
            items:2
        },
        575:{
            items:3
        },
        768:{
            items:4
        },
        992:{
            items: $('.clients-slide').data('item')
        }
    }    
});


// ===== 6 - Team slide==== 


    $(".team-slide").owlCarousel({  
        loop:true,
        margin:0,
        nav: $('.team-slide').data('nav'),
        dots: $('.team-slide').data('dots'),                     
        autoplay: $('.team-slide').data('auto'),
        smartSpeed: 3000,
        responsive:{
            0:{
                items:1,
            },
            480:{
                items:2,
            },
            768:{
                items:3
            },
            1200:{
                items: $('.team-slide').data('item')
            }
        }
    });

// ===== 7 - customer slide==== 

    $(".customer-slide").owlCarousel({  
        loop:true,
        margin:0,
        nav: $('.customer-slide').data('nav'),
        dots: $('.customer-slide').data('dots'),                     
        autoplay: $('.customer-slide').data('auto'),
        smartSpeed: 3000,
        animateIn: 'fadeIn',
        animateOut: 'fadeOut',
        responsive:{
            0:{
                items:1,
            },
            1200:{
                items: $('.customer-slide').data('item')
            }
        }
    });


// ===== 8 - classic-blog-slide ==== 

    $(".classic-blog-slide").owlCarousel({  
        loop:true,
        margin:0,
        nav: $('.classic-blog-slide').data('nav'),
        dots: $('.classic-blog-slide').data('dots'),                     
        autoplay: $('.classic-blog-slide').data('auto'),
        smartSpeed: 1000,
        responsive:{
            0:{
                items:1,
            },
            600:{
                items:1,
            },
            992:{
                items: $('.classic-blog-slide').data('item')
            }
        }
    });


/*------------------------------------------------------------------------------*/
/* One Page setting
/*------------------------------------------------------------------------------*/  
jQuery(document).ready(function($) {
  // Scroll to the desired section on click
  // Make sure to add the `data-scroll` attribute to your `<a>` tag.
  // Example: 
  // `<a data-scroll href="#my-section">My Section</a>` will scroll to an element with the id of 'my-section'.
  function scrollToSection(event) {
    event.preventDefault();
    var $section = $($(this).attr('href')); 
    $('html, body').animate({
      scrollTop: $section.offset().top
    }, 500);
  }
  $('[data-scroll]').on('click', scrollToSection);
}(jQuery));



/*------------------------------------------------------------------------------*/
/* Back to top
/*------------------------------------------------------------------------------*/

// ===== Scroll to Top ==== 
jQuery('#totop').hide();
jQuery(window).scroll(function() {
    "use strict";
    if (jQuery(this).scrollTop() >= 100) {        // If page is scrolled more than 50px
        jQuery('#totop').fadeIn(200);    // Fade in the arrow
        jQuery('#totop').addClass('top-visible');
    } else {
        jQuery('#totop').fadeOut(200);   // Else fade out the arrow
        jQuery('#totop').removeClass('top-visible');
    }
});
jQuery('#totop').on( "click", function() {      // When arrow is clicked
    jQuery('body,html').animate({
        scrollTop : 0                       // Scroll to top of body
    }, 500);
    return false;
});


 $(function() {

    });

})(jQuery);
