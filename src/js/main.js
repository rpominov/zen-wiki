"use strict";

/*global _ $ Markdown prettyPrint */

$(function(){
	var converter = Markdown.getSanitizingConverter();	
	var editor = new Markdown.Editor(converter);
	
	var pp = _.throttle(prettyPrint, 500);
	editor.hooks.chain("onPreviewRefresh", function () {
		$('#wmd-preview code, #wmd-preview pre').addClass('prettyprint');
        pp();
    });
	
	editor.run();
	
	$('#edit-form').hide();
	$('.not-saved #edit-form').show();
	
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
	
	$('#set-private').click(function(){
		$('#set-private-form').submit();
	});
	
	function check_val() {
		var $input = $('#new-input');
		if ($input.val().indexOf(window.rootUrl) !== 0) {
			$input.val(window.rootUrl);
		}
	}
	$('#new-input').bind('change keyup', function(){
		check_val();
		var url = _($(this).val().split('/')).map(encodeURIComponent).join('/');
		$('#new-form').attr('action', url);
	});
	$('#new-input').focus(check_val);
	$('#new-input').focusout(function(){
		if ($(this).val() == window.rootUrl) {
			$(this).val('');
		}
	});
});
