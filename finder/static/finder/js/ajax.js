$(".substitut").on('click', function(event) {
    event.preventDefault();  
    var product = $(this).val();           
    var url = '/register/delete/';   
    $.ajax({        
        url: url,        
        type: "POST",
        data:{
            'product': product,            
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
        },
        datatype:'json',
        success: function(data) {
          if (data['success'])            
            $("#fav_list").load(" #fav_list >*");
            // location.reload(true);
        }
    }); 
});



$(".added").on('click', function(event) {
    let addedBtn = $(this);
    console.log(addedBtn)
    event.preventDefault();     
    var product = $(this).val();
    console.log(product)   
    var url = '/finder/add/';   
    $.ajax({        
        url: url,        
        type: "POST",
        data:{
            'product': product,            
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
        },
        datatype:'json',
        success: function(data) {
          if (data['success'])
          addedBtn.parent('.sub_button').hide();   
                       
        }
    }); 
});

