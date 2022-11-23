$(document).ready(function(){   
    $('#client_dropdown').on('change', function() {
        value = this.value;
        var val_arr = value.split(',');
        $('#client_id').val(val_arr[0]);
        $('#client_name').val(val_arr[1]);
        $('#client_email').val(val_arr[2]);
        $('#client_address').val(val_arr[3]);
      });



});


$(document).ready(function(){ 
    var total_final = 0;
    $('#add_item_to_table').click(function(){
        value = $('#item_dropdown').val();
        var val_arr = value.split(',');
        qty = $('#item_qty').val();
        total = parseFloat(val_arr[3])*parseFloat(qty);
        var dynamic_tr = "<tr><td>"+val_arr[0]+"</td><td>"+val_arr[1]+"</td><td>"+val_arr[2]+"</td><td>"+val_arr[3]+"</td><td>"+qty+"</td><td>"+total+"</td></tr>"
        $('#item_table tbody').append(dynamic_tr);
        $('#item_qty').val('');

        total_final = total_final +total;
        $('#total_final').text(total_final)
    })


});


$(document).ready(function(){ 
    $('#create_invoice').click(function(){
        json_data = {}
        counter = 0
        $('#item_table tbody tr').each(function() {

            item = []
            
            $(this).find('td').each(function(){
                td_value = $(this).text()
                item.push(td_value)
            })
            json_data[counter] = item
            counter = counter + 1

        });

        client_id = $('#client_id').val();
        total_final = $('#total_final').text();

        $.ajax({
            type: 'POST',
            url: '/dashboard/create_invoice',
            contentType: 'application/json',
            data: JSON.stringify({ 'client_id': client_id,'total_final':total_final,'invoice_data': json_data}),
            dataType: 'json',
            success: function(result){
                window.location.reload();
            }
        });
  
    })


});




