$("#fav_list").on("click", ".substitut", function(event) {
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
            $("#fav_list").load(" #fav_list > *");            
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

(function(d, s, id) {
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) return;
    js = d.createElement(s); js.id = id;
    js.src = "https://connect.facebook.net/en_US/sdk.js#xfbml=1&version=v3.0";
    fjs.parentNode.insertBefore(js, fjs);
  }(document, 'script', 'facebook-jssdk'));


$(function(){

  $.ui.autocomplete.prototype._renderItem = function (ul, item) {      
      item.label = item.label.replace(new RegExp("(?![^&;]+;)(?!<[^<>]*)(" + $.ui.autocomplete.escapeRegex(this.term) + ")(?![^<>]*>)(?![^&;]+;)", "gi"), "<span style='font-weight:bold; color:#C45525'>$1</span>");
      return $("<li></li>")
              .data("item.autocomplete", item)
              .append("<a>" + item.label + "</a>")
              .appendTo(ul);
  };
    
  $('.prod').autocomplete({
        open: function() { $('.ui-menu').width(350);
  } ,
      source: '/finder/search_auto',
      minLength: 3,      
  });
 
  });

