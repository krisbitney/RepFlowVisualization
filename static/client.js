
var table = null;

function requestData() {
    let loc = window.location;
    let request = new Request(`${loc.protocol}\/\/${loc.hostname}:${loc.port}/data`);
    fetch(request)
        .then(response => response.json())
        .then(result => {
            table = parseJsonData(JSON.parse(result));
            drawHistAbs();
            drawHistLog();
            drawPie();
            drawLorenz();
        })
        .catch(error => {
            console.error(error);
        })
}

function parseJsonData(jsonData) {
    let address = [];
    let balance_abs = [];
    let balance_log = [];
    for (row of jsonData) {
        address.push(row["address"]);
        balance_abs.push(row["balance_quadrillions"]);
        balance_log.push(row["log10_balance"]);
    }

    return {
        address: address,
        balance_abs: balance_abs,
        balance_log: balance_log,
        units: 12
    }
}


function drawHistAbs() {
    let data = [{
        x: table.balance_abs,
        type: 'histogram',
      }];

    let layout = {
        title: 'Reputation Distribution (in quadrillions)',
        height: 400,
        width: 400,
        showlegend: false
    };

    Plotly.newPlot('hist_abs', data, layout);
}

function drawHistLog() {
    let data = [{
        x: table.balance_log,
        type: 'histogram',
      }];

    let layout = {
        title: 'Reputation Distribution (log scale)',
        height: 400,
        width: 400,
        showlegend: false
    };

    Plotly.newPlot('hist_log', data, layout);
}

function drawPie() {
    let data = [
        {
            domain: {column: 1},
            values: table.balance_abs,
            labels: table.address,
            hoverinfo: 'label+percent',
            hole: .4,
            type: 'pie'
        }];

    let layout = {
        title: 'Reputation Shares',
        height: 400,
        width: 400,
        showlegend: false
    };

    Plotly.newPlot('pie', data, layout);
}

function sum(x) {
    return x.reduce((previous, current) => current += previous)
}

function gini(x) {
    let n = x.length;
    // mean absolute difference
    let mad = 0.0;
    for (i of x) {
        for (j of x) {
            mad += Math.abs(i - j);
        }
    }
    mad = mad / (n*n);
    // relative mean absolute difference
    let total = sum(x);
    let avg = total / n;
    rmad = mad / avg;
    // divide by 2
    return 0.5 * rmad;
}

function divide(numerator, denominator) {
    return numerator / denominator
}

function drawLorenz() {
    // prep lorenz/gini
    let gini_coef = gini(table.balance_abs);
    const cumulativeSum = (sum => value => sum += value)(0);
    let total = sum(table.balance_abs);
    let cumulativePct = table.balance_abs.map(cumulativeSum).map(x => x / total);
    let bins = _.range(table.balance_abs.length).map(x => x / (table.balance_abs.length - 1));

    let data = [
        {
            x: bins,
            y: bins,
            type: 'scatter'
        },
        {
            x: bins,
            y: cumulativePct,
            type: 'lines'
        }];

    let layout = {
        title: 'Lorenz Curv (Gini=' + gini_coef.toFixed(3) + ')',
        height: 400,
        width: 400,
        showlegend: false,
        sliders: [{
            currentvalue: {
                prefix: 'add months: ',
                font: {
                    color: '#888',
                    size: 14
                }
            },
            steps: [
                {
                    label: 0,
                    method: 'restyle',
                    args: ['line.color', 'red']
                },
                {
                    label: 1,
                    method: 'restyle',
                    args: ['line.color', 'green']
                },
                {
                    label: 2,
                    method: 'restyle',
                    args: ['line.color', 'blue']
                }]
        }]
    };

    Plotly.newPlot('lorenz', data, layout);
}