import { get } from './request.js'

const URL = window.location.href

window.onload = () => {
    get(`${URL}api/departments/`, (resp) => {
        const json = JSON.parse(resp.responseText)
        let table = document.querySelector("table")
        for (const dep of json) {
            const trow = `
                <tr>
                    <td>${dep.id}</td>
                    <td>${dep.name}</td>
                    <td>${dep.num_of_employees}</td>
                    <td>${dep.avg_salary}</td>
                    <td>edit</td>
                    <td>delete</td>
                </tr>
            `
            table.innerHTML += trow
        }
    })
}