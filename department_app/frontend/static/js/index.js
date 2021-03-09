window.onload = function() {
    disableClickable("button")
    disableClickable("a")
    sortTable()
}

function disableClickable(sel) {
    let clickables = document.querySelectorAll(sel);
    for (clickable of clickables) {
    clickable.addEventListener('click', click => {
        setTimeout(() => click.target.disabled = true, 0.05);
        setTimeout(() => click.target.disabled = false, 1);
    })
    }
}

function sortTable() { 
    let headers = document.querySelector("tr").children;

    for (let i = 0; i < headers.length - 2; i++) {
        headers[i].addEventListener('click', sortTable);
    }

    document.getElementById('4').removeEventListener('click', sortTable);

    function sortTable(click) {
    for (header of headers) {
        header.classList.remove('headerSortUp');
        header.classList.remove('headerSortDown');
    }

    const columnNumber = Number(click.target.id);
    let sortDirection = 'ascending',
        switching = true,
        shouldSwitch = false,
        switchCount = 0;

    while (switching) {
        switching = false;

        if (sortDirection == 'ascending') {
            click.target.classList.remove('headerSortDown');
            click.target.classList.add('headerSortUp');
        } else {
            click.target.classList.remove('headerSortUp');
            click.target.classList.add('headerSortDown');
        }

        let rows = document.querySelectorAll("tr");

        for (var i = 1; i < rows.length - 1; i++) {
        // basically x is a value in a clicked column 
        // when y is the value in the same column but in the next row
        let x = rows[i].querySelectorAll("td")[columnNumber].innerHTML.toLowerCase();
        let y = rows[i + 1].querySelectorAll("td")[columnNumber].innerHTML.toLowerCase();

        x = isNaN(x) ? x : Number(x);
        y = isNaN(y) ? y : Number(y);

        if (sortDirection == 'ascending') {

            if (x > y) {
                shouldSwitch = true;
                break;
            }
        } else if (sortDirection == 'descending') {
            if (x < y) {
                shouldSwitch = true;
                break;
            }
        }
        }
        if (shouldSwitch) {
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
            switchCount++;
        } else {
            if (switchCount == 0 && sortDirection == 'ascending') {
                sortDirection = 'descending';
                switching = true;
            }
        }
        }
    }
}