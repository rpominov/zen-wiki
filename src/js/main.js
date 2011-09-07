"use strict";

/*global $ Markdown */

$(function(){
	var converter = Markdown.getSanitizingConverter();
	var editor = new Markdown.Editor(converter);
	editor.run();
	
	$('#edit').click(function(){
		$('#edit-form').toggle();
	});
	
	function toggleMove(){ 
		$('.path, #move-form').toggle();
		if ($('#move-form:visible').length > 0) {
			$('#move-input').focus();
		}
	}
	$('#move').click(toggleMove);
	$('#move-input').focusout(toggleMove);
	
	$('#cancel').click(function(){
		window.location.reload();
	});
	
	$('#delete').click(function(){
		if (confirm('Delete this page?')) {
			$('#delete-form').submit();
		}
	});
	
	function check_val() {
		var $input = $('#new-input');
		if ($input.val().indexOf(window.rootUrl) !== 0) {
			$input.val(window.rootUrl);
		}
	}
	$('#new-input').bind('change keyup', function(){
		check_val();
		var url = $(this).val().split('/').map(encodeURIComponent).join('/');
		$('#new-form').attr('action', url);
	});
	$('#new-input').focus(check_val);
	$('#new-input').focusout(function(){
		if ($(this).val() == window.rootUrl) {
			$(this).val('');
		}
	});

});
