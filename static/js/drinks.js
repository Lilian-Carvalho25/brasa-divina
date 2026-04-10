const drinks = [
    {
        imagem: 'refri-cola.png',
        titulo: 'R. Cola',
        preco: 13,
        resumo: 'Refrigerante tipo cola, 2 litros.'
    },
    {
        imagem: 'refri-laranja.png',
        titulo: 'R. Laranja',
        preco: 13,
        resumo: 'Refrigerante tipo laranja, 2 litros.'
    },
    {
        imagem: 'refri-limao.png',
        titulo: 'R. Limão',
        preco: 13,
        resumo: 'Refrigerante tipo limão, 2 litros'
    },
    {
        imagem: 'suco-maca.png',
        titulo: 'S. Maça',
        preco: 13,
        resumo: 'Suco concentrado tipo maçã, 2 litros'
    },
    {
        imagem: 'suco-tangerina.png',
        titulo: 'S. Tangerina',
        preco: 13,
        resumo: 'Suco concentrado tipo tangerina, 2 litros'
    },
    {
        imagem: 'suco-pera.png',
        titulo: 'S. Pêra',
        preco: 13,
        resumo: 'Suco concentrado tipo pêra, 2 litros'
    },
    {
        imagem: 'latinha-morango.png',
        titulo: 'S. Morango',
        preco: 8,
        resumo: 'Suco concentrado tipo morango, 600 mls'
    },
    {
        imagem: 'suco-abacaxi.png',
        titulo: 'S. Abacaxi',
        preco: 13,
        resumo: 'Suco concentrado tipo abacaxi, 2 litros'
    },
    {
        imagem: 'suco-maca_v.png',
        titulo: 'S. Maça v.',
        preco: 13,
        resumo: 'Suco concentrado tipo maça verde, 2 litros'
    }
];

function renderDrinks() {
    const container = document.getElementById('container-drinks');
    if (!container) return;
    const drinksDiv = document.createElement('div');
    drinksDiv.className = 'drinks';
    drinks.forEach(drink => {
        const article = document.createElement('article');
        article.className = 'drinks-box';
        article.innerHTML = `
            <img src="../static/img/${drink.imagem}" alt="Bebida" class="product-image">
            <div class="title-categories">
                <h3 class="product-title">${drink.titulo}</h3>
                <h5 class="product-price">R$ ${drink.preco},00</h5>
            </div>
            <p>${drink.resumo}</p>
            <button type="submit" class="button-add-cart" onclick="addedToCart()">Adicionar ao carrinho</button>
        `;
        drinksDiv.appendChild(article);
    });
    container.innerHTML = '';
    container.appendChild(drinksDiv);
}

document.addEventListener('DOMContentLoaded', renderDrinks);
