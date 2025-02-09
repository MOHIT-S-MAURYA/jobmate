// Hide messages after 2 seconds
document.addEventListener("DOMContentLoaded", function () {
  setTimeout(function () {
    var messages = document.querySelectorAll('[id^="message-"]');
    messages.forEach(function (message) {
      message.style.display = "none";
    });
  }, 2000);
});
