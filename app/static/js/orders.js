document.addEventListener("DOMContentLoaded", function () {
    const modal = document.getElementById("order-items-modal");
    const closeModal = document.querySelector(".close-btn");
    const orderItemsBody = document.getElementById("order-items-body");

    document.querySelectorAll(".inspect-btn").forEach(button => {
        button.addEventListener("click", function () {
            const orderId = this.getAttribute("data-order-id");

            fetch(`/user/orders/${orderId}/items`)
                .then(response => response.json())
                .then(data => {
                    orderItemsBody.innerHTML = "";
                    data.items.forEach(item => {
                        const row = document.createElement("tr");

                        row.innerHTML = `
                            <td>
                                <a href="/shop/product/${item.product_id}" target="_blank">
                                    <img src="${item.image_url}" class="product-img">
                                    ${item.product_name}
                                </a>
                            </td>
                            <td>${item.quantity}</td>
                            <td>$${parseFloat(item.price_at_purchase).toFixed(2)}</td>
                        `;

                        orderItemsBody.appendChild(row);
                    });

                    modal.classList.add("show"); // Show modal
                });
        });
    });

    closeModal.addEventListener("click", function () {
        modal.classList.remove("show"); // Hide modal
    });

    window.addEventListener("click", function (event) {
        if (event.target === modal) {
            modal.classList.remove("show"); // Close modal if clicking outside
        }
    });
});


