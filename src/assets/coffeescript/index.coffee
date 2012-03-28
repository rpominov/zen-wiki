setCookie = (c_name, value, exdays) ->
	exdate = new Date()
	exdate.setDate exdate.getDate() + exdays
	c_value = escape(value) + (if (not (exdays?)) then "" else "; expires=" + exdate.toUTCString())
	document.cookie = c_name + "=" + c_value

getCookie = (c_name) ->
	i = undefined
	x = undefined
	y = undefined
	ARRcookies = document.cookie.split(";")
	i = 0
	while i < ARRcookies.length
		x = ARRcookies[i].substr(0, ARRcookies[i].indexOf("="))
		y = ARRcookies[i].substr(ARRcookies[i].indexOf("=") + 1)
		x = x.replace(/^\s+|\s+$/g, "")
		if x is c_name
			return unescape(y)
		i++

$ ->
	$('@change-lang').click ->
		$('body').toggleClass('lang-en lang-ru')
		setCookie 'lang', (if $('body').hasClass('lang-ru') then 'ru' else 'en'), 300
	$('body')
		.removeClass('lang-en lang-ru')
		.addClass( if getCookie('lang') == 'ru' then 'lang-ru' else 'lang-en' )