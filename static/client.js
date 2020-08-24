

// TODO: handle successful response
function requestData() {
    let loc = window.location;
    let request = new Request(`${loc.protocol}\/\/${loc.hostname}:${loc.port}/data`);
    fetch(request)
        .then(response => {
            if (response.status === 200) {
                console.debug(response.json());
            } else {
                throw new Error('Unable to fetch data');
            }
        })
        .catch(error => {
            console.error(error);
        })
}