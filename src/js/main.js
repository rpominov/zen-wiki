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
	
	$('#new-input').change(function(){
		$('#new-form').attr('action', window.rootUrl + '/' + $(this).val());
	});

});
