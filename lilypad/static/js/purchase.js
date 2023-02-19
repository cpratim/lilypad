let amount_form = document.getElementById('quantity-input');
let buy_button = document.getElementById('order-button');
let order_estimate = document.getElementById('order-estimate');
let quantity_input = document.getElementById('quantity-input'); 

document.addEventListener('DOMContentLoaded', () => {
    buy_button.addEventListener('click', () => {
        let amount = amount_form.value;
        let url = '/api/buy';
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({'amount': amount})
        }).then(data => {
            window.location.href = '/purchase';
        });
    });
    quantity_input.addEventListener('change', () => {
        let amount = amount_form.value;
        order_estimate.innerHTML = `Estimated Order Cost: $${amount * 0.01}`;
    });

});