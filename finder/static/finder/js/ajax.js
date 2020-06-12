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
            $('#navigation .nav_button').css({"background-color":"#C45525", "color":"white"});
            $('#navigation .nav_button').first().css({"background-color":"white", "color":"black"});                                           
        }
    }); 
});

$(".row").on('click', ".added", function(event) {
    let addedBtn = $(this);
    console.log(addedBtn)
    event.preventDefault();
    event.stopPropagation();
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
          addedBtn.hide();             
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


$(function() {
  $('.prod2').autocomplete({
    open: function() {
      $('.ui-menu').width(350);
    },
    source: '/finder/search_auto',
    minLength: 3,
  }).data("ui-autocomplete")._renderItem = function(ul, item) {
    item.label = item.label.replace(new RegExp("(?![^&;]+;)(?!<[^<>]*)(" + $.ui.autocomplete.escapeRegex(this.term) + ")(?![^<>]*>)(?![^&;]+;)", "gi"), "<span style='font-weight:bold; color:#C45525'>$1</span>");
    return $("<li>")
      .data("item.autocomplete", item)
      .append("<div><img src='" + item.img + "' height='55' /> " + item.label + "</div>")
      .appendTo(ul);
  };
});


$(function() {
  $('.prod').autocomplete({
    open: function() {
      $('.ui-menu').width(350);
    },
    source: '/finder/search_auto',
    minLength: 3,
    appendTo: '#my-suggestions',
  }).data("ui-autocomplete")._renderItem = function(ul, item) {
    item.label = item.label.replace(new RegExp("(?![^&;]+;)(?!<[^<>]*)(" + $.ui.autocomplete.escapeRegex(this.term) + ")(?![^<>]*>)(?![^&;]+;)", "gi"), "<span style='font-weight:bold; color:#C45525'>$1</span>");
    return $("<li>")
      .data("item.autocomplete", item)
      .append("<div><img src='" + item.img + "' height='55' /> " + item.label + "</div>")
      .appendTo(ul);
  };
});


$(".nav_button").on("click", function(event) {
    event.preventDefault();      
    var page = $(this).val();
    $('#navigation .nav_button').css({"background-color":"#C45525", "color":"white"});
    $(this).css({"background-color":"white", "color":"black"});                   
    var url = '/register/account/';
    $.ajax({        
        url: url,        
        type: "POST",
        data:{
            'page': page,            
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
        },        
        datatype:'html',        
        success: function(resp) {            
            $('#fav_list').html('');          
            $('#fav_list').html(resp);                 
        }
    }); 
});


$(".nav_button_search").on("click", function(event) {
  event.preventDefault();      
  var query = $(this).val();
  $('#navigation .nav_button_search').css({"background-color":"#C45525", "color":"white"});
  $(this).css({"background-color":"white", "color":"black"});                          
  var url = '/finder/search/';   
  $.ajax({        
        url: url,        
        type: "POST",
        data:{
            'query': query,            
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
        },        
        datatype:'html',        
        success: function(resp) {
            console.log(resp)                       
            $('.row').html('');                  
            $('.row').html(resp);                         
        }
    }); 
});

$(".nav_button_sub").on("click", function(event) {
  event.preventDefault();      
  var query = $(this).val();
  $("#navigation .nav_button_sub").css({"background-color":"#C45525", "color":"white"});
  $(this).css({"background-color":"white", "color":"black"});
  $('#loading-indicator').show();                         
  var url = '/finder/sub/';   
  $.ajax({        
        url: url,        
        type: "POST",
        data:{
            'query': query,            
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),            
        },        
        datatype:'html',        
        success: function(resp) {                                   
            $('.row').html('');                  
            $('.row').html(resp);
            $('#loading-indicator').hide();                         
        }
    }); 
});
