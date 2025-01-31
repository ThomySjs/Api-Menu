const options = document.getElementById("options");

async function get_categories() {
    let products = await fetch('/products').then(response => response.json());
    let categories = {};

    products.forEach(product => {
        if (!categories[product.category]){
            categories[product.category] = null
        }
    });

    return categories
}

async function show_options() {
    let categories = await get_categories()
    Object.keys(categories).forEach(category => {
        let show_category = `
            <a href="#header-${category}">
                <button>${category.toUpperCase()}</button>
            </a>
        `
        options.insertAdjacentHTML("beforeend", show_category)
    })
}

show_options();