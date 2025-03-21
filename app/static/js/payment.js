document.addEventListener("DOMContentLoaded", function () {
    const confirmBtn = document.getElementById("confirm-btn");
    const phoneInput = document.getElementById("phone");
    const amountInput = document.getElementById("amount");
    const loadingContainer = document.getElementById("loading-container");
    const statusMessage = document.getElementById("status-message");

    confirmBtn.addEventListener("click", function () {
        const phoneNumber = phoneInput.value.trim();
        const amount = amountInput.value.trim();

        if (!phoneNumber) {
            alert("Please enter your phone number.");
            return;
        }

        // Show loading spinner
        loadingContainer.style.display = "flex";
        statusMessage.innerText = "";

        fetch('api-pay', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ phone: phoneNumber, amount: amount })
        })
        .then(response => response.json())
        .then(data => {
            loadingContainer.style.display = "none"; // Hide spinner

            if (data.message === "success") {
                statusMessage.innerHTML = "<span style='color: green;'>✅ Payment Successful! Redirecting...</span>";
                setTimeout(() => {
                    window.location.href = "/shop/";  // Change to your target page
                }, 2000);
            } else {
                statusMessage.innerHTML = `<span style='color: orange;'>⚠️ ${data.message}</span>`;
            }
        })
        .catch(error => {
            loadingContainer.style.display = "none"; // Hide spinner
            statusMessage.innerHTML = "<span style='color: red;'>❌ Payment Failed. Please try again.</span>";
        });
    });
});
