// index.js
function submitToDatabase(event) {
    event.preventDefault(); // Prevent default form submission behavior

    var userInput = document.getElementById('user_input').value;

    if (!userInput) {
        alert("Please enter a valid input");
        return;
    }

    // Show loading spinner
    document.getElementById('loading-spinner').style.display = 'block';

    fetch("/", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
        body: "user_input=" + userInput,
    })
    .then(response => response.text())
    .then(data => {
        // Hide loading spinner
        document.getElementById('loading-spinner').style.display = 'none';

        // Update the content
        var tempContainer = document.createElement('div');
        tempContainer.innerHTML = data;

        var chatContainer = tempContainer.querySelector('#completion_history');
        if (chatContainer) {
            var actualChatContainer = document.getElementById('completion_history');
            actualChatContainer.innerHTML = chatContainer.innerHTML;

            // Optionally, you can also scroll to the bottom after updating the content
            actualChatContainer.scrollTop = actualChatContainer.scrollHeight;
        }
    })
    .catch(error => {
        // Hide loading spinner on error
        document.getElementById('loading-spinner').style.display = 'none';
        console.error('Error:', error);
        alert("An error occurred. Please try again.");
    });
}