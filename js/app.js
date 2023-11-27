console.log('JS is working!')

// write a function that is called whenever the user clicks on the button with id="submit_button"
var submitButton = document.getElementById('submit_button');

function submit() {
    console.log('Button was clicked!');
}

submitButton.addEventListener('click', submit);