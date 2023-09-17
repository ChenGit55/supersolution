const userID = document.getElementById('user');
const apiProducts = document.getElementById('apiproducts');
const apiProdcutsUrl = apiProducts.getAttribute('data-api-url');
const apiSales = document.getElementById('apisales');
const apiSalesUrl = apiSales.getAttribute('data-api-url');
var priceField = document.getElementById('product-price');
var quantityField = document.getElementById('product-quantity');
var totProductField = document.getElementById('product-total');
const inoviceList = document.getElementById('inovice-list');
const addProductButton = document.getElementById('add-product');
var productsList = [];
var inoviceTotal = document.getElementById('inovice-total');
var currentTotal = 0

// currency format
function fCurrency(value) {
  if (typeof value === 'string') {
    value = value.replace(',', '.').replace(/[^0-9.]/g, '');
    return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL'}).format(value);
  } else {
    return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL'}).format(value);
  }
}

fetch(apiProdcutsUrl)
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
      var selectedProductIndex = productSelect.selectedIndex;
      if(Boolean(priceField.value) && Boolean(quantityField.value) && selectedProductIndex !== -1 ){        
        var productTotal = quantityField.value*parseFloat(priceField.value.replace(',','.'));
        var inoviceItem = document.createElement('li');
        var productTitle = productSelect.options[productSelect.selectedIndex].text;

        var selectedProduct = data[selectedProductIndex];
        var inputPrice = parseFloat(priceField.value.replace(',','.'));
        var inputQuantity = quantityField.value;
        var inputTotal = productTotal;

        currentTotal += productTotal;
        inoviceTotal.textContent = currentTotal

        productsList.push({
          product: selectedProduct.title,
          quantity: inputQuantity,
          price: inputPrice,
          total: inputTotal,
        });
        console.log(productsList);
        
        inoviceItem.textContent = `${productTitle} Preço R$ ${fCurrency(priceField.value)} Qantidade ${quantityField.value} Total: ${fCurrency(productTotal)}`;
        inoviceList.appendChild(inoviceItem);

        priceField.value = '';
        quantityField.value = '';
      } else {

      }
    })
  })
  .catch(function(error) {
    console.error('Erro: ' + error.message);
  });

  // Adicione um evento de clique ao botão "Finalizar Venda"
document.getElementById('close-inovice').addEventListener('click', function() {
  if (productsList.length > 0) {
    // Crie a venda completa com todos os produtos selecionados
    var vendaCompleta = {
      user: userID, // Substitua pelo ID do usuário adequado
      items: productsList
    };

    fetch(apiSalesUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(vendaCompleta),
    })
    .then(function(response) {
      if (!response.ok) {
        throw new Error('Erro ao criar a venda');
      }
      return response.json();
    })
    .then(function(data) {
      console.log('Venda criada com sucesso:', data);
      // Faça algo com a resposta do servidor, se necessário
    })
    .catch(function(error) {
      console.error('Erro ao criar a venda:', error);
    });
  } else {
    console.error('Nenhum produto selecionado. Selecione pelo menos um produto antes de finalizar a venda.');
  }
});
