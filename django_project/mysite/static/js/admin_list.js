/**
 * Created by RBeltsov on 23.09.2016.
 */
{% load staticfiles %}

function countRabbits(id) {
  console.log(id);
      $.ajax({
              type: 'POST',
              url: {% url 'jq' %},
    dateType: 'json',
        data
:
    {
        description:$('#description').val(),
            csrfmiddlewaretoken
    :
        $('input[name=csrfmiddlewaretoken]').val()
    }
,
    success:function (json) {
        $("#modal_results_content").html(json.message);
        $('#check_text').attr("disabled", false);

        $('#set_progress').replaceWith('<div id="set_progress" class="determinate red" style="width: ' + json.result_json.unique + '">' + json.result_json.unique + '%</div>');
        $('#modal_results').openModal();
        $('#modal_results_content').empty();
    }
});
}

// {#<script type="application/javascript">#}
// {#  $(document).getElementById('set_priority').onclick = function() {#}
// {#    alert('Спасибо')#}
//
// {#  set_priority.onclick = function() {#}
// {#  document.getElementById('set_priority').onclick = function() {#}
// {#    alert( 'Спасибо' );#}
// {#  }#}
// {#  #}
// {#  document.getElementById('set_priority').addEventListener( "click" , function() {alert('Спасибо!')});#}
// {#</script>#}
