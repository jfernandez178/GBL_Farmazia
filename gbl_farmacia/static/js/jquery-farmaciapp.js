$(document).ready(function() {
  $(function() {
	    $( ".vDateField" ).datepicker({ dateFormat: 'yy-mm-dd' }).val();
	  });
});


function konfirmazioa(form_id){
    alertify.confirm("Ziur al zaude erabakiarekin?", function (e) {
	    if (e) {
	        document.getElementById(form_id).submit();
	    }
	    else {
		}
    });                   
}


function informazioa(informazioa){
    alertify.alert(informazioa, function(){
        //alertify.message('OK');
    });
}

  


  