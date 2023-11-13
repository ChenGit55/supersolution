var productSelect = document.getElementById('product-select');
var priceField = document.getElementById('product-price');
var quantityField = document.getElementById('product-quantity');
var addButton = document.getElementById('add-product-button');
var closeInoviceButton = document.getElementById('close-inovice')
var inovice = document.getElementById('inovice');
var inoviceTotal = document.getElementById('inovice-total');
var paymentMethodSelect = document.getElementById('payment-method');
var amountPaid = document.getElementById('payment-value');
var paymentConfirmationButton = document.getElementById('payment-confirmation');
var payment = document.getElementById('payment');
var paymentTable = document.getElementById('payment-table');
var totalPayment = document.getElementById('total-payment');
var paymentChange = document.getElementById('payment-change');
let currentTotal = 0;


function fCurrency(value) {
    if (typeof value === 'string') {
      value = value.replace(',', '.').replace(/[^0-9.]/g, '');
      return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL'}).format(value);
    } else {
      return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL'}).format(value);
    }
}

function cFloat(value) {
    newValue = parseFloat(value.replace(/[^\d,-]/g, '').replace(',', '.'));
    return newValue;
}

function inoviceData(productID,  productPrice, quantity) {

    var data = {
        product_id: productID,
        product_price: productPrice,
        quantity: quantity
    };

    fetch("{% url 'new-sale' %}", {
        method: 'POST',
        headers: {
            'X-CSRFToken': document.cookie.match(/csrftoken=([^;]+)/)[1], // Obtenha o token CSRF
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(() => {

    })
    .catch(error => {
        console.error('Erro ao enviar dados para o Django:', error);
    });
}

function updateHiddenFields() {
    var productIds = [];
    var productPrices = [];
    var quantities = [];

    var rows = inovice.getElementsByTagName('tr');
    for (var i = 0; i < rows.length; i++) {
        var cells = rows[i].getElementsByTagName('td');
        productIds.push(cells[0].getAttribute('cell-id'));
        productPrices.push(cells[1].getAttribute('cell-price'));
        quantities.push(cells[2].getAttribute('cell-quantity'));
    }

    document.getElementById('product-ids').value = productIds.join(',');
    document.getElementById('product-prices').value = productPrices.join(',');
    document.getElementById('quantities').value = quantities.join(',');
}

document.addEventListener("DOMContentLoaded", function () {

    productSelect.addEventListener('change', function () {
        var product = productSelect.options[productSelect.selectedIndex];
        var selectedPrice = product.getAttribute('data-price');
        priceField.value = fCurrency(selectedPrice);
        if ( quantityField.value === '' ) {
            quantityField.value = 1
        }
    });

    addButton.addEventListener("click", function (event) {
        var product = productSelect.options[productSelect.selectedIndex];
        var productID = product.getAttribute('value');

        if ( product.text !== '' && quantityField.value > 0 && cFloat(priceField.value) > 0 ) {

            const inoviceRow = inovice.insertRow();
            const productCell = inoviceRow.insertCell(0);
            const priceCell = inoviceRow.insertCell(1);
            const quantityCell = inoviceRow.insertCell(2);
            const totalCell = inoviceRow.insertCell(3);

            productCell.textContent = product.text;
            priceCell.textContent = priceField.value;
            quantityCell.textContent = quantityField.value;
            totalCell.textContent = fCurrency(cFloat(priceField.value)*quantityField.value);

            productCell.setAttribute(`cell-id`, productID);
            priceCell.setAttribute(`cell-price`, cFloat(priceCell.textContent));
            quantityCell.setAttribute(`cell-quantity`, cFloat(quantityCell.textContent));
            totalCell.setAttribute(`cell-total`, cFloat(totalCell.textContent));

            currentTotal += cFloat(totalCell.textContent);
            inoviceTotal.textContent = fCurrency(currentTotal);
            amountPaid.value = inoviceTotal.textContent
        } else {
            console.log('dados inválidos');
        }
    });

    let totalPaid = 0
    const totalRow = totalPayment.insertRow();
    const totalTextCell = totalRow.insertCell(0);
    const totalValueCell = totalRow.insertCell(1);
    totalTextCell.textContent = 'Total Pago:'

    const changeRow = paymentChange.insertRow();
    const changeTextCell = changeRow.insertCell(0);
    const changeValueCell = changeRow.insertCell(1);
    changeTextCell.textContent = 'Troco'

    paymentConfirmationButton.addEventListener("click", function (event) {
        var selectPayment = paymentMethodSelect.options[paymentMethodSelect.selectedIndex].text;
        let paymentFound = false;

        for (let i = 0; i < paymentTable.rows.length; i++) {
            const currentRow = paymentTable.rows[i];
            const methodText = currentRow.getAttribute('method-row');
            const methodValue = currentRow.getAttribute('value-row');
            const totalMethodValue = cFloat(methodValue) + cFloat(amountPaid.value);

            if (methodText === selectPayment) {
                const newValue = currentRow.cells[1];
                currentRow.setAttribute('value-row', totalMethodValue);
                newValue.textContent = fCurrency(totalMethodValue);
                paymentFound = true;
                break;
            }
        }

        if (!paymentFound){
            const paymentRow = paymentTable.insertRow();
            const methodCell = paymentRow.insertCell(0);
            const methodValueCell = paymentRow.insertCell(1);

            paymentRow.setAttribute('method-row', selectPayment);
            paymentRow.setAttribute('value-row', amountPaid.value);
            methodCell.textContent = paymentRow.getAttribute('method-row');
            methodValueCell.textContent = fCurrency(paymentRow.getAttribute('value-row'));

            payment.style.display = "block";
        }

        totalPaid += cFloat(amountPaid.value);
        totalValueCell.textContent = fCurrency(totalPaid);

        if (totalPaid >= currentTotal){
            paymentConfirmationButton.disabled = true;
            closeInoviceButton.disabled = false;
            changeValueCell.textContent = fCurrency(totalPaid-currentTotal)
        }

        amountPaid.value = ''
    });

    closeInoviceButton.addEventListener("click", function (event) {
        var product = productSelect.options[productSelect.selectedIndex];
        var productID = product.getAttribute('value');
        const rows = inovice.getElementsByTagName("tr");
        if (rows.length > 0) {
            inoviceData(productID, cFloat(priceField.value), quantityField.value);
            updateHiddenFields();
        } else {
            console.log('selecione um produto');
            event.preventDefault();
        }
    });
});