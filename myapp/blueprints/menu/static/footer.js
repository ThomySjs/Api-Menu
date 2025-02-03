function set_footer() {
    const container =  document.getElementById('container')

    let footer = `
        <div class="footer">
            <p>This is the footer</p>
        </div> 
    `

    container.insertAdjacentHTML("beforeend", footer)
}

set_footer()