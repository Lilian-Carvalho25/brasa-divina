const pizzas = [
    {
        imagem: 'pizza-calabresa.png',
        titulo: 'Calabresa',
        preco: 30,
        resumo: 'Mussarela, calabresa trufada, cebola, molho marinara e orégano.'
    },
    {
        imagem: 'pizza-baiana.png',
        titulo: 'Baiana',
        preco: 30,
        resumo: 'Calabresa fatiada, cebola, mussarela.'
    },
    {
        imagem: 'pizza-calabacon.png',
        titulo: 'Calabacon',
        preco: 30,
        resumo: 'Mussarela, bacon, calabresa, tomates, pimenta, e molho marinara.'
    },
    {
        imagem: 'pizza-mussarela.png',
        titulo: 'Mussarela',
        preco: 30,
        resumo: 'Mussarela, orégano, presunto, pimenta, milho e molho bechamel.'
    },
    {
        imagem: 'pizza-pimentao.png',
        titulo: 'Pimentão',
        preco: 30,
        resumo: 'Mussarela, pimentão, orégano, pimenta, milho e molho cheddar.'
    },
    {
        imagem: 'pizza-presunto.png',
        titulo: 'Presunto',
        preco: 30,
        resumo: 'Mussarela, presunto, orégano, brócolis, alho e molho cheddar.'
    },
    {
        imagem: 'pizza-do-chef.png',
        titulo: 'Do chef',
        preco: 30,
        resumo: 'Mussarela, salame, milho, pimentão, brócolis e molho barbecue.'
    },
    {
        imagem: 'pizza-pepperoni.png',
        titulo: 'Pepperoni',
        preco: 30,
        resumo: 'Mussarela, pepperoni, milho, borda crocante e molho marinara.'
    },
    {
        imagem: 'pizza-cogumelos.png',
        titulo: 'Cogumelos',
        preco: 30,
        resumo: 'Cogumelos, pimentão, salame, escarola e molho bechamel.'
    },
    {
        imagem: 'pizza-bufala.png',
        titulo: 'M. Bufala',
        preco: 30,
        resumo: 'Mussarela de bufala, tomates, cogumelos, escarola e molho marinara.'
    },
    {
        imagem: 'pizza-camarao.png',
        titulo: 'Camarão',
        preco: 30,
        resumo: 'Mussarela, camarão, azeitonas, pimentão, pimenta e molho bechamel.'
    },
    {
        imagem: 'pizza-frango.png',
        titulo: 'Frango',
        preco: 30,
        resumo: 'Mussarela, frango desfiado, azeitonas, cebolas e molho cheddar.'
    },
    {
        imagem: 'pizza-margherita.png',
        titulo: 'Margherita',
        preco: 30,
        resumo: 'Mussarela, manjericão, azeitonas, tomates e molho marinara.'
    },
    {
        imagem: 'pizza-pimenta.png',
        titulo: 'Pimenta',
        preco: 30,
        resumo: 'Mussarela, pimenta, manjericão, tomates e molho marinara.'
    },
    {
        imagem: 'pizza-cebolas.png',
        titulo: 'Cebolas',
        preco: 30,
        resumo: 'Mussarela, cebolas, escarola, cogumelos e molho barbecue.'
    },
];

function renderPizzas() {
    const container = document.getElementById('container-pizzas');
    if (!container) return;
    const pizzasDiv = document.createElement('div');
    pizzasDiv.className = 'pizzas';
    pizzas.forEach(pizza => {
        const article = document.createElement('article');
        article.className = 'pizzas-box';
        article.innerHTML = `
            <img src="../static/img/${pizza.imagem}" alt="pizza" class="product-image">
            <div class="title-categories">
                <h3 class="product-title">${pizza.titulo}</h3>
                <h5 class="product-price">R$ ${pizza.preco},00</h5>
            </div>
            <p>${pizza.resumo}</p>
            <button type="submit" class="button-add-cart"
                onclick="addedToCart()"
                data-title="${pizza.titulo}"
                data-price="${pizza.preco}"
                data-image="${pizza.imagem}"
            >Adicionar ao carrinho</button>
        `;
        pizzasDiv.appendChild(article);
    });
    container.innerHTML = '';
    container.appendChild(pizzasDiv);

    // ajuste para o carrinho
    const addToCartButtons = container.getElementsByClassName('button-add-cart');
    for (let i = 0; i < addToCartButtons.length; i++) {
        addToCartButtons[i].addEventListener('click', function(event) {
            const btn = event.target;
            if (btn.dataset && btn.dataset.title) {
                const productImage = '../static/img/' + btn.dataset.image;
                const productName = btn.dataset.title;
                const productPrice = 'R$ ' + btn.dataset.price + ',00';

                const productsCartNames = document.getElementsByClassName("cart-product-title");
                for (var j = 0; j < productsCartNames.length; j++) {
                    if (productsCartNames[j].innerText === productName) {
                        productsCartNames[j].parentElement.parentElement.getElementsByClassName("product-qtd-input")[0].value++;
                        updateTotal();
                        return;
                    }
                }

                let newCartProduct = document.createElement("tr");
                newCartProduct.classList.add("cart-product");
                newCartProduct.innerHTML =
                    `
                      <td class="product-identification">
                        <img src="${productImage}" alt="${productName}" class="cart-product-image">
                        <strong class="cart-product-title">${productName}</strong>
                      </td>
                      <td>
                        <span class="cart-product-price">${productPrice}</span>
                      </td>
                      <td>
                        <input type="number" value="1" min="0" class="product-qtd-input">
                        <button type="button" class="remove-product-button">Remover</button>
                      </td>
                    `;
                const tableBody = document.querySelector(".cart-table tbody");
                tableBody.append(newCartProduct);
                updateTotal();
                newCartProduct.getElementsByClassName("remove-product-button")[0].addEventListener("click", removeProduct);
                newCartProduct.getElementsByClassName("product-qtd-input")[0].addEventListener("change", checkIfInputIsNull);
            } else {
                addProductToCart(event);
            }
        });
    }
}

document.addEventListener('DOMContentLoaded', renderPizzas);