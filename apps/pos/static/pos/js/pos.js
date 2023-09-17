console.log('test')
var api = document.getElementById('api');
var apiUrl = api.getAttribute('data-api-url');
var priceField = document.getElementById('product-price');
var quantityField = document.getElementById('product-quantity');
var totProductField = document.getElementById('product-total');
const inoviceList = document.getElementById('inovice-list');
const addProductButton = document.getElementById('add-product');

// currency format
function fCurrency(value) {
  if (typeof value === 'string') {
    value = value.replace(',', '.').replace(/[^0-9.]/g, '');
    return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL'}).format(value);
  } else {
    return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL'}).format(value);
  }
}

fetch(apiUrl)
  .then(function(response) {
    // Verifique se a resposta da API está OK (código de status 200)
    if (!response.ok) {
      throw new Error('API REQUEST ERROR!');
    }
    // Parse a resposta JSON
    return response.json();
  })
  .then(function(data) {
    // Agora, 'data' contém o objeto JSON da API
    console.log(data);

    
    // criando menu select com os dados da api
    var productSelect = document.getElementById('product-select');
    data.forEach(function(product){
        var option = document.createElement('option');
        option.text = `${product.title}`;
        option.value = product.price;
        productSelect.appendChild(option);        
    });
    productSelect.addEventListener('change', function() {
      var selectedPrice = productSelect.options[productSelect.selectedIndex].value;
      priceField.value = selectedPrice.replace('.',',');
      quantityField.value = 1
    })

    addProductButton.addEventListener('click', function() {
      var productTotal = quantityField.value*parseFloat(priceField.value.replace(',','.'));
      var inoviceItem = document.createElement('li');
      var productTitle = productSelect.options[productSelect.selectedIndex].text;
      inoviceItem.textContent = `${productTitle} Preço R$ ${fCurrency(priceField.value)} Qantidade ${quantityField.value} Total: ${fCurrency(productTotal)}`;
      inoviceList.appendChild(inoviceItem);

      priceField.value = '';
      quantityField.value = '';
    })

  })
  .catch(function(error) {
    console.error('Erro: ' + error.message);
  });