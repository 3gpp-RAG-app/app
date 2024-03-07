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
        // Create a temporary container to parse the HTML
        var tempContainer = document.createElement('div');
        tempContainer.innerHTML = data;

        // Find the chat area or message container in the parsed HTML
        var chatContainer = tempContainer.querySelector('#completion_history');

        // Check if the chat area is found
        if (chatContainer) {
            // Update the content of the actual chat area
            var actualChatContainer = document.getElementById('completion_history');
            actualChatContainer.innerHTML = chatContainer.innerHTML;

            // Optionally, you can also scroll to the bottom after updating the content
            actualChatContainer.scrollTop = actualChatContainer.scrollHeight;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert("An error occurred. Please try again.");
    });
}
