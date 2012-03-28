(function() {
  var getCookie, setCookie;

  setCookie = function(c_name, value, exdays) {
    var c_value, exdate;
    exdate = new Date();
    exdate.setDate(exdate.getDate() + exdays);
    c_value = escape(value) + (!(exdays != null) ? "" : "; expires=" + exdate.toUTCString());
    return document.cookie = c_name + "=" + c_value;
  };

  getCookie = function(c_name) {
    var ARRcookies, i, x, y;
    i = void 0;
    x = void 0;
    y = void 0;
    ARRcookies = document.cookie.split(";");
    i = 0;
    while (i < ARRcookies.length) {
      x = ARRcookies[i].substr(0, ARRcookies[i].indexOf("="));
      y = ARRcookies[i].substr(ARRcookies[i].indexOf("=") + 1);
      x = x.replace(/^\s+|\s+$/g, "");
      if (x === c_name) return unescape(y);
      i++;
    }
  };

  $(function() {
    $('@change-lang').click(function() {
      $('body').toggleClass('lang-en lang-ru');
      return setCookie('lang', ($('body').hasClass('lang-ru') ? 'ru' : 'en'), 300);
    });
    return $('body').removeClass('lang-en lang-ru').addClass(getCookie('lang') === 'ru' ? 'lang-ru' : 'lang-en');
  });

}).call(this);
