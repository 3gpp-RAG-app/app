function submitToDatabase(event) {
    event.preventDefault(); // Prevent default form submission behavior

    var userInput = document.getElementById('user_input').value;

    if (!userInput) {
        alert("Please enter a valid input");
        return;
    }

    fetch("/", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
        body: "user_input=" + userInput,
    })
    .then(response => response.text())
    .then(data => {
        document.body.innerHTML = data;
    })
    .catch(error => {
        console.error('Error:', error);
        alert("An error occurred. Please try again.");
    });
}