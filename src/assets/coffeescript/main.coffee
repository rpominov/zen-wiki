$ ->

	converter = Markdown.getSanitizingConverter()
	editor = new Markdown.Editor(converter)

	pp = _.throttle(prettyPrint, 500)
	editor.hooks.chain "onPreviewRefresh", ->
		$("#wmd-preview code, #wmd-preview pre").addClass "prettyprint"
		pp()

	$("@edit-page-button").click ->
		$("@edit-form").toggle()

	$("@move-form").hide()
	toggleMove = ->
		$("@path-block, @move-form").toggle()
		if $("@move-form:visible").length > 0
			$("@move-form input").focus()
	$("@move-page-button").click toggleMove
	$("@move-form input").focusout toggleMove
	$("@cancel").click ->
		window.location.reload()

	$("@delete-page-button").click ->
		if confirm("Delete this page?")
			$("@delete-form").submit()

	$("@set-private-status-button").click ->
		$("@set-private-form").submit()

	check_val = ->
		$input = $("@new-input")
		if $input.val().indexOf(ROOT_URL) isnt 0
			$input.val ROOT_URL
	$("@new-input").bind "change keyup", ->
		check_val()
		url = _($(this).val().split("/")).map(encodeURIComponent).join("/")
		$("@new-form").attr "action", url
	$("@new-input").focus check_val
	$("@new-input").focusout ->
		if $(this).val() is ROOT_URL
			$(this).val ""

	editor.run()
	$("@edit-form").hide()
	$(".not-saved @edit-form").show()

