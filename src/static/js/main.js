(function() {

  $(function() {
    var ORIG_TEXT, ORIG_TITLE, check_val, converter, editor, pp, toggleMove;
    converter = Markdown.getSanitizingConverter();
    editor = new Markdown.Editor(converter);
    ORIG_TEXT = $("@edit-form textarea").val();
    ORIG_TITLE = $('title').text();
    pp = _.throttle(prettyPrint, 500);
    editor.hooks.chain("onPreviewRefresh", function() {
      var changed;
      $("#wmd-preview code, #wmd-preview pre").addClass("prettyprint");
      $("#wmd-preview table").addClass("striped");
      changed = !(ORIG_TEXT === $("@edit-form textarea").val());
      $('@edit-form [type=submit]').prop({
        disabled: !changed
      });
      $('body').toggleClass('changed', changed);
      $('title').text("" + (changed ? '*' : '') + ORIG_TITLE);
      return pp();
    });
    toggleMove = function() {
      $("@path-block, @move-form").toggle();
      if ($("@move-form:visible").length > 0) return $("@move-form input").focus();
    };
    $("@move-page-button").click(toggleMove);
    $("@move-form input").focusout(toggleMove);
    $("@edit-page-button").click(function() {
      return $("@edit-form").fadeToggle();
    });
    $("@cancel").click(function() {
      $("@edit-form").fadeOut()[0].reset();
      return editor.refreshPreview();
    });
    $("@delete-page-button").click(function() {
      if (confirm("Delete this page?")) return $("@delete-form").submit();
    });
    $("@set-private-status-button").click(function() {
      return $("@set-private-form").submit();
    });
    check_val = function() {
      var $input;
      $input = $("@new-input");
      if ($input.val().indexOf(ROOT_URL) !== 0) return $input.val(ROOT_URL);
    };
    $("@new-input").bind("change keyup", function() {
      var url;
      check_val();
      url = _($(this).val().split("/")).map(encodeURIComponent).join("/");
      return $("@new-form").attr("action", url);
    });
    $("@new-input").focus(check_val);
    $("@new-input").focusout(function() {
      if ($(this).val() === ROOT_URL) return $(this).val("");
    });
    editor.run();
    return $(".not-saved @edit-form").show();
  });

}).call(this);
