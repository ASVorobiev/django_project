/**
 * Created by Roman on 10/17/2016.
 */
// django.jQuery(document).find('#set_tags_for_all').onclick( function(event, $row, formsetName) {
// alert("button");
// });

(function($) {
    $(document).on('formset:added', function(event, $row, formsetName) {
        if (formsetName == 'author_set') {
            // Do something
        }
    });

    $(document).on('formset:removed', function(event, $row, formsetName) {
        // Row removed
    });
})(django.jQuery);