const container = document.getElementById("all-tables-container");

async function get_list() {
    let lista = await fetch('/products').then(response => response.json());
    return lista;
}

async function get_categories() {
    let products = await get_list();  // Ensure products are fetched before continuing
    let categories = {};

    products.forEach(product => {
        // If there is not a key with the value of the product's category, create it
        if (!categories[product.category]) {
            categories[product.category] = [];
        }
        // Pushes the product into its category key
        categories[product.category].push(product);
    });

    return categories;
}

async function create_tables() {
    let categories = await get_categories();  // Wait until categories are fetched
    let counter = 0
    let container_number = 0;
    // Gets each category key and creates a table for each one
    Object.keys(categories).forEach(category => {
        //This sections creates a new container every 2 iterations to allow 
        // only 2 tables per container.
        if (counter % 2 === 0) {
            container_number ++;
            let cat_container = `
                <div class="two-tables-container" id="tables-${container_number}"></div>
            `;
            container.insertAdjacentHTML("beforeend", cat_container);
        }

        let menu = document.getElementById(`tables-${container_number}`);

        let table = `
            <div class="table-container">
                <h1 class="headers" id="header-${category}">${category}</h1>
                <hr>
                <table id="${category}">
                </table>
            </div>
        `;
        menu.insertAdjacentHTML("beforeend", table);

        // Gets each product from the current category and adds it to the corresponding table
        let select_table = document.getElementById(category);
        categories[category].forEach(producto => {
            let show_product = `
                <tr>
                    <td>${producto.product_name}<br><p>${producto.description}</p></td>
                    <td>${producto.price}</td>
                </tr>
            `;
            select_table.insertAdjacentHTML("beforeend", show_product);
        });

        counter ++;
    });

}


create_tables();  // Start the table creation process
