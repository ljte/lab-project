
export function get(url, callback) {
    makeReq("GET", url, (e) => { 
        let resp = e.target
        if (resp.readyState === 4 && resp.status == 200) {
            callback(resp)
        }
    })
}

function makeReq(method, url, callback) {
    let req = new XMLHttpRequest()
    req.onreadystatechange = callback
    req.open(method, url, true)
    req.send()
}