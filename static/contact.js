
    // Function to handle form submission
    document.getElementById("contact-form").addEventListener("submit", function(event) {
        event.preventDefault(); // Prevent default form submission
        
        // Get form data
        var name = document.getElementById("name").value;
        var email = document.getElementById("email").value;
        var msg = document.getElementById("msg").value;
        
        // Dummy AJAX request (replace with actual AJAX call)
        // Simulate submission success after 1 second
        setTimeout(function() {
            var messageDiv = document.getElementById("message");
            messageDiv.innerHTML = "Your query is submitted. Thank you, " + name + "!";
            messageDiv.style.color = "green";
        }, 1000);
    });

