
document.addEventListener("DOMContentLoaded", function() {
    const confirmBtn = document.getElementById("confirm-btn");
    const phoneInput = document.getElementById("phone");
    const amountInput = document.getElementById("amount");
    const loadingSpinner = document.getElementById("loading");

    confirmBtn.addEventListener("click", function() {
        const phoneNumber = phoneInput.value.trim();
        const amount = amountInput.value.trim();

        if (!phoneNumber) {
            alert("Please enter your phone number.");
            return;
        }

        // Show loading spinner
        loadingSpinner.style.display = "block";

        // Simulate processing delay (5 seconds)
        setTimeout(() => {
            loadingSpinner.style.display = "none";
         
            fetch('api-pay', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ phone: phoneNumber, amount: amount })
            })
            .then(response => response.json())
            .then(data => {
                // alert(data.message);
            if (data.message === "success") {
                window.location.href = "/shop/";  // Change to your target page
            }})
            .catch(error => {
                alert("Error processing payment."+error);
            });

        }, 5000); 
    });
});

