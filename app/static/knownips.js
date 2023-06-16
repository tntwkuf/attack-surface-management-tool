function highlightRow(){
	$('.field-empl_role span').each(function() {
		if($(this).attr('state') === 'disable'){
			$(this).parent().parent().css( "background-color", "rgb(207 214 216 / 73%)" ).css( "color", "grey" );
		} else if ($(this).attr('state') === 'warning') {
			$(this).parent().parent().css( "background-color", "#ffcdd2" );
		} else if ($(this).attr('state') === 'good') {
			$(this).parent().parent().css( "background-color", "#9ee29e" );
		}
	});
}

function Import() {
	$('#import_CVE').on ('click', function (event) {
		event.preventDefault();

		$('.popUp_import_wrapp').css('display','block');
	});

	$("#bulletin_import_popup_close").on ("click", function (event) {
		event.preventDefault();
		location.reload();
		$('.popUp_import_wrapp').css('display','none');});
}

document.addEventListener('DOMContentLoaded', function(){
	highlightRow();
	Import();
	});