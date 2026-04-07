(function () {
  "use strict";

  function flash(msg, kind) {
    var $f = $("#flash");
    $f.removeClass("flash-ok flash-err");
    if (!msg) {
      $f.text("");
      return;
    }
    $f.addClass(kind === "ok" ? "flash-ok" : "flash-err");
    $f.text(msg);
  }

  function fillForm(c) {
    $("#customer_name").val(c.name || "");
    $("#customer_address").val(c.address || "");
    $("#customer_status").val(c.status || "");
  }

  function clearDetail() {
    $("#customer_name").val("");
    $("#customer_address").val("");
    $("#customer_status").val("");
  }

  function currentId() {
    var v = $("#customer_id").val();
    var n = parseInt(v, 10);
    return Number.isFinite(n) && n > 0 ? n : null;
  }

  $("#btn-retrieve").on("click", function () {
    flash("");
    var id = currentId();
    if (!id) {
      flash("Enter a customer ID.", "err");
      clearDetail();
      return;
    }
    $.ajax({
      url: "/customers/" + id,
      method: "GET",
      dataType: "json",
    })
      .done(function (data) {
        $("#customer_id").val(data.id);
        fillForm(data);
        flash("Success", "ok");
      })
      .fail(function (xhr) {
        clearDetail();
        var msg = "Customer not found.";
        if (xhr.responseJSON && xhr.responseJSON.message) {
          msg = xhr.responseJSON.message;
        }
        flash(msg, "err");
      });
  });

  function putStatus(pathSuffix, okVerb) {
    flash("");
    var id = currentId();
    if (!id) {
      flash("Retrieve a customer first.", "err");
      return;
    }
    $.ajax({
      url: "/customers/" + id + pathSuffix,
      method: "PUT",
    })
      .done(function (data) {
        fillForm(data);
        flash("Customer " + okVerb + ".", "ok");
      })
      .fail(function (xhr) {
        var msg = "Request failed.";
        if (xhr.responseJSON && xhr.responseJSON.message) {
          msg = xhr.responseJSON.message;
        }
        flash(msg, "err");
      });
  }

  $("#btn-suspend").on("click", function () {
    putStatus("/suspend", "suspended");
  });

  $("#btn-activate").on("click", function () {
    putStatus("/activate", "activated");
  });
})();
