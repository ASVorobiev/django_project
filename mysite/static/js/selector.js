/**
 * Created by RBeltsov on 01.09.2016.
 */
$(document).ready(function() {
$('select').material_select();
$('.datepicker').pickadate({
selectMonths: true, // Creates a dropdown to control month
selectYears: 16 // Creates a dropdown of 15 years to control year
});
$(".button-collapse").sideNav();
});