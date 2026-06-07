document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll("form").forEach(function (form) {
    form.addEventListener("submit", function () {
      var submitButton = form.querySelector("button[type='submit']");
      if (submitButton) {
        submitButton.disabled = true;
        submitButton.innerHTML =
          "Memproses... <span class='spinner-border spinner-border-sm ms-2' role='status' aria-hidden='true'></span>";
      }
    });
  });
});
