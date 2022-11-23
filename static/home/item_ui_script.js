$(document).ready(function(){

    $("#add_item_section").hide();

    $("#add_item").click(function(){
      $(this).hide();
      $("#add_item_section").show();
    });

    $("#cancel_item_client").click(function(){
        $("#add_item_section").hide();
        $("#add_item").show();
      });

  });

  $(document).ready(function() {
    $(".item_table_row_data").change(function() {
        data_id = $(this).attr('id');
        value = $('#'+data_id).val();
        var data_arr = data_id.split('_');
        
        $.ajax({
          type: 'POST',
          url: '/dashboard/item_update',
          contentType: 'application/json',
          data: JSON.stringify({ 'id': data_arr[0], 'field': data_arr[1] ,'value':value}),
          dataType: 'json',
          success: function(result){
            
          }
      });


    });
});