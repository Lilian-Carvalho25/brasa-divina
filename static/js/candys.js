const candys = [
    {
        imagem: 'pizza-banana-c-chocolate.png',
        titulo: 'Banana',
        preco: 20,
        resumo: 'Chocolate ao leite e bananas assadas com mel e cravos.'
    },
    {
        imagem: 'pizza-chocolate-c-morango.png',
        titulo: 'Morangos',
        preco: 20,
        resumo: 'Chocolate meio amargo, leite condensado e morangos.'
    },
    {
        imagem: 'pizza-frutas.png',
        titulo: 'Frutas',
        preco: 20,
        resumo: 'Chocolate ao leite, morangos, bananas, kiwis, amoras, etc.'
    },
    {
        imagem: 'pizza-brigadeiro.png',
        titulo: 'Brigadeiro',
        preco: 20,
        resumo: 'Chocolate ao leite e 50% e granulado artesanal'
    },
    {
        imagem: 'pizza-ao-leite.png',
        titulo: 'Ao leite',
        preco: 20,
        resumo: 'Chocolate ao leite, borda crocante, e caramelo'
    },
    {
        imagem: 'pizza-meio-a-meio.png',
        titulo: 'Meio a meio',
        preco: 25,
        resumo: 'Chocolate ao leite e branco, biscoitos, morangos e bombons.'
    },
    {
        imagem: 'doce-cookies.png',
        titulo: 'Cookies',
        preco: 15,
        resumo: '5 unidades de cookies com chocolate meio amargo crocante.'
    },
    {
        imagem: 'doce-donuts.png',
        titulo: 'Donuts',
        preco: 10,
        resumo: '2 unidades de donuts com cobertura de chocolate e morango.'
    },
    {
        imagem: 'doce-pudim.png',
        titulo: 'Pudim',
        preco: 15,
        resumo: '1 unidade de pudim de chocolate com frutas vermelhas.'
    },
    {
        imagem: 'doce-torta.png',
        titulo: 'Tortinha',
        preco: 15,
        resumo: '1 unidade de torta de limão com merengue italiano.'
    },
    {
        imagem: 'doce-churros.png',
        titulo: 'Churros',
        preco: 15,
        resumo: '5 unidades de churros recheados com chocolate, com açucar e canela.'
    },
    {
        imagem: 'doce-brownie.png',
        titulo: 'Brownies',
        preco: 20,
        resumo: '3 unidades de brownies 50% cacau com nozes e avelãs.'
    }
];


function renderCandys() {
    const container = document.getElementById('container-candys');
    if (!container) return;
    container.className = 'container-drinks';
    const drinksDiv = document.createElement('div');
    drinksDiv.className = 'drinks';
    candys.forEach(candy => {
        const article = document.createElement('article');
        article.className = 'drinks-box';
        article.innerHTML = `
            <img src="../static/img/${candy.imagem}" alt="Doce" class="product-image">
            <div class="title-categories">
                <h3 class="product-title">${candy.titulo}</h3>
                <h5 class="product-price">R$ ${candy.preco},00</h5>
            </div>
            <p>${candy.resumo}</p>
            <button type="submit" class="button-add-cart" onclick="addedToCart()">Adicionar ao carrinho</button>
        `;
        drinksDiv.appendChild(article);
    });
    container.innerHTML = '';
    container.appendChild(drinksDiv);
}

document.addEventListener('DOMContentLoaded', renderCandys);
