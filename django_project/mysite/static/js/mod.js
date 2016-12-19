/**
 * Created by RBeltsov on 01.09.2016.
 */
$(document).ready(function() {
    $('select').material_select();
    $("select[required]").css({display: "inline", height: 0, padding: 0, width: 0});

    // $(".button-collapse").sideNav();
    $('.materialboxed').materialbox();

    $('.slider').slider({full_width: true, indicators: true, height: 300});
    $('.slider').slider('start');

    $('.button-collapse').sideNav({
      menuWidth: 260, // Default is 240
      edge: 'left', // Choose the horizontal origin
      draggable: true // Choose whether you can drag to open on touch screens
      // menuWidth: 50, // Default is 240
      // edge: 'left' // Choose the horizontal origin
    }
    );
    // $('.tabs-wrapper .row').pushpin({ top: $('.tabs-wrapper').offset().top }); // всё ломает
    $('ul.tabs').tabs();
    // $('.tabs-wrapper .row').pushpin({
    //     top: $('.tabs-wrapper').offset().top,
    //     bottom: 0,
    //     offset: 200
    // });

});
