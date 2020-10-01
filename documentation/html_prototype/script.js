window.onload = function() {
    const fileName = window.location.href.split("/").pop()

    document.getElementById('add_btn').addEventListener('click', () => window.location.replace(`add_${fileName.replace('s', '')}`))

    document.getElementsByClassName('edit-btn')[0].addEventListener('click', () => window.location.replace(`edit_${fileName.replace('s', '')}`))

    let deleteBtns = document.getElementsByClassName("delete-btn")
    for (let btn of deleteBtns) {
        btn.addEventListener('click', function(click) {
            const isGoingToDelete = confirm("Are you sure you want to delete the record?")
            if (isGoingToDelete) {
                click.target.parentElement.parentElement.style.display = "none"
            }
        })
    }


}
