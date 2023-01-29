function close_button_function(event) {
    const el = event.target;
    const parent = el.parentNode;
    console.log(parent.id);
    parent.classList.remove("show");
}