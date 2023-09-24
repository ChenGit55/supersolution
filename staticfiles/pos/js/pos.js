const userElement = document.getElementById('user');
const productSelect = document.getElementById('product-select');
const priceField = document.getElementById('product-price');
const quantityField = document.getElementById('product-quantity');
const inoviceList = document.getElementById('inovice-list');
const addProductButton = document.getElementById('add-product');
const inoviceTotal = document.getElementById('inovice-total');
const closeInvoiceButton = document.getElementById('close-inovice');

const apiProdcutsUrl = document.getElementById('apiproducts').getAttribute('data-api-url');
const userID = userElement ? userElement.value : null;

const productsList = [];
let currentTotal = 0;

// Currency format function
function fCurrency(value) {
  if (typeof value === 'string') {
    value = value.replace(',', '.').replace(/[^0-9.]/g, '');
    return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL'}).format(value);
  } else {
    return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL'}).format(value);
  }
}

// function to get the CSRF token
function getCSRFToken() {
  const cookieValue = document.cookie
    .split('; ')
    .find(row => row.startsWith('csrftoken='))
    .split('=')[1];
  return cookieValue;
}

// shows up the product to client
function addProduct(productTitle, price, quantity, productTotal) {
  const inoviceProduct = document.createElement('li');
  inoviceProduct.textContent = `${productTitle} - ${fCurrency(price)} x ${quantity} - Total: ${fCurrency(productTotal)}`;
  inoviceList.appendChild(inoviceProduct);
}

// Fetch products from the API
fetch(apiProdcutsUrl)
  .then(response => {
    if (!response.ok) {
      throw new Error('API REQUEST ERROR!');
    }
    return response.json();
  })
  .then(data => {
    //select menu with API data
    data.forEach(product => {
      const option = document.createElement('option');
      option.text = product.title;
      option.value = product.price;
      option.setAttribute('data-id', product.id);
      productSelect.appendChild(option);
    });   

    addProductButton.addEventListener('click', () => {
      const selectedProductIndex = productSelect.selectedIndex;
      if (
        Boolean(priceField.value) &&
        Boolean(quantityField.value) &&
        selectedProductIndex !== -1
      ) {
        const productID = productSelect.options[selectedProductIndex].getAttribute('data-id');
        const productTitle = productSelect.options[productSelect.selectedIndex].text;
        const inputPrice = parseFloat(priceField.value.replace(',', '.'));
        const inputQuantity = quantityField.value;
        const productTotal = quantityField.value * parseFloat(priceField.value.replace(',', '.'));

        // Criar campos dinâmicos com nomes únicos

        productsList.push({
            id: productID,
            product: productTitle,
            quantity: inputQuantity,
            price: inputPrice,
        });
        
        addProduct(productTitle, priceField.value, quantityField.value, productTotal);
            
        //sum all products totals
        currentTotal += productTotal;
        inoviceTotal.textContent = fCurrency(currentTotal);

        priceField.value = '';
        quantityField.value = '';
      }
    });
  })
  .catch(error => {
    console.error('Erro: ' + error.message);
  });

// Close invoice button click event
closeInvoiceButton.addEventListener('click', () => {
  if (productsList.length > 0) {
    const salesForm = document.getElementById('new-sale-form');
    document.getElementById('user').value = userID;
    productsList.forEach((product, index) => {

      const inputID = document.createElement('input');
      inputID.type = 'hidden';
      inputID.name = `product-${index+1}-id`;
      inputID.value = product.id;
      salesForm.appendChild(inputID);
      
      const inputProduct = document.createElement('input');
      inputProduct.type = 'hidden';
      inputProduct.name = `product-${index + 1}-title`;
      inputProduct.value = product.product;
      salesForm.appendChild(inputProduct);

      const inputPrice = document.createElement('input');
      inputPrice.type = 'hidden';
      inputPrice.name = `product-${index + 1}-price`;
      inputPrice.value = product.price;
      salesForm.appendChild(inputPrice);

      const inputQuantity = document.createElement('input');
      inputQuantity.type = 'hidden';
      inputQuantity.name = `product-${index + 1}-quantity`;
      inputQuantity.value = product.quantity;
      salesForm.appendChild(inputQuantity);
    });
    salesForm.submit()
  } else {
    console.error('Nenhum produto selecionado. Selecione pelo menos um produto antes de finalizar a venda.');
  }
});

 //shows up the default price when change the selected product
 productSelect.addEventListener('change', () => {
  const selectedPrice = productSelect.options[productSelect.selectedIndex].value;
  priceField.value = selectedPrice.replace('.', ',');
  quantityField.value = 1;
}); 
