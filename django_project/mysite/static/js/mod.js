/**
 * Created by RBeltsov on 01.09.2016.
 */
$(document).ready(function() {
    $('select').material_select();

    // $(".button-collapse").sideNav();
    $('.materialboxed').materialbox();

    $('.slider').slider({full_width: true, indicators: true, height: 300});
    $('.slider').slider('start');

    $('.button-collapse').sideNav({
      menuWidth: 240, // Default is 240
      edge: 'left', // Choose the horizontal origin
      closeOnClick: true, // Closes side-nav on <a> clicks, useful for Angular/Meteor
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
