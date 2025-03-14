# Updated payment page with a fully responsive design

payment_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Confirm Payment</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/payment.css') }}">
</head>
<body>
    <div class="container">
        <h2>Confirm Your Payment</h2>
        <form id="payment-form">
            <label for="phone">Phone Number:</label>
            <input type="tel" id="phone" name="phone" placeholder="Enter your phone number" required>
            
            <div class="amount-box">
                <p>Total Amount: <span id="amount">{{ amount }}</span></p>
            </div>

            <button type="button" id="confirm-btn">Confirm Checkout</button>
        </form>
    </div>

    <script src="{{ url_for('static', filename='js/payment.js') }}"></script>
</body>
</html>
"""

payment_css = """
/* Responsive Payment Page */
body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    background: #f4f4f4;
}

.container {
    width: 90%;
    max-width: 400px;
    background: white;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    text-align: center;
}

h2 {
    margin-bottom: 20px;
}

label {
    display: block;
    text-align: left;
    margin-bottom: 5px;
    font-weight: bold;
}

input {
    width: 100%;
    padding: 10px;
    margin-bottom: 15px;
    border: 1px solid #ccc;
    border-radius: 5px;
    font-size: 16px;
}

.amount-box {
    background: #e0e0e0;
    padding: 10px;
    border-radius: 5px;
    margin-bottom: 15px;
}

button {
    width: 100%;
    padding: 12px;
    background: #28a745;
    color: white;
    border: none;
    border-radius: 5px;
    font-size: 16px;
    cursor: pointer;
    transition: 0.3s ease;
}

button:hover {
    background: #218838;
}

/* Responsive Adjustments */
@media (max-width: 600px) {
    .container {
        padding: 15px;
    }

    button {
        padding: 14px;
    }
}
"""

payment_js = """
document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("confirm-btn").addEventListener("click", function() {
        let phone = document.getElementById("phone").value.trim();
        let amount = document.getElementById("amount").innerText.trim();
        let cartId = "12345"; // This should be dynamically set based on the session

        if (!phone.match(/^\\d{10,}$/)) {
            alert("Please enter a valid phone number!");
            return;
        }

        let requestData = {
            phone: phone,
            amount: amount,
            cartId: cartId
        };

        fetch("/process-payment", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(requestData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert("Payment request sent successfully!");
            } else {
                alert("Payment failed. Try again!");
            }
        })
        .catch(error => {
            console.error("Error:", error);
            alert("Something went wrong!");
        });
    });
});
"""

(payment_html, payment_css, payment_js)
