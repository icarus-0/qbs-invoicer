$(document).ready(function(){

    $("#add_client_section").hide();

    $("#add_client").click(function(){
      $(this).hide();
      $("#add_client_section").show();
    });

    $("#cancel_add_client").click(function(){
        $("#add_client_section").hide();
        $("#add_client").show();
      });

  });

  $(document).ready(function() {
    $(".client_table_row_data").change(function() {
        data_id = $(this).attr('id');
        value = $('#'+data_id).val();
        var data_arr = data_id.split('_');
        
        $.ajax({
          type: 'POST',
          url: '/dashboard/client_update',
          contentType: 'application/json',
          data: JSON.stringify({ 'id': data_arr[0], 'field': data_arr[1] ,'value':value}),
          dataType: 'json',
          success: function(result){
            
          }
      });


    });
});