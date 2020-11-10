let buttons = document.querySelectorAll(".btn");
for (button of buttons) {
  button.addEventListener('click', (click) => {
      // disable clicked button so the user can not send the same request
      // set timeout so the form data can be send to the view function
      setTimeout(() => click.target.disabled = true, 0.1);
  })
}