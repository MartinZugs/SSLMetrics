const axios = require("axios");
const fs = require('fs')
const Path = require('path')
var express = require("express");
var app = express();

app.set('view engine', 'ejs');

let data = "";
const url = "http://192.168.99.100:5000/"

// app.get("/data", (req, res, next) => {
//     console.log(data)
//     res.send(data)
// });

function getRandomColor() {
    var letters = '0123456789ABCDEF';
    var color = '#';
    for (var i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}

app.get('/chart', function (req, res) {
    let fileName = 'SSLMetrics_historical.db'
    console.log("Database filename:")
    console.log(fileName);

    let rawData = {}
    let headers = [];
    let dates = [];

    // Read in DB
    var knex = require("knex")({
        client: "sqlite3",
        connection: {
            filename: "./database/" + fileName
        }
    })

    // Get all rows from master (all metrics compiled) table in DB
    let result = knex.from("MASTER").select("*")
    result.then(function (rows) {
        // Get all column names in headers array
        headers = Object.keys(rows[0])

        // Initialize an empty array in the rawData object for each metric
        for (var i = 0; i < headers.length; i++) {
            rawData[headers[i]] = []
        }

        // Ppopulate all metrics arrays (effectively columns of the table) one row at a time
        for (var j = 0; j < rows.length; j++) {
            for (var k = 0; k < headers.length; k++) {
                rawData[headers[k]].push(rows[j][headers[k]])
            }
        }

        // Remove dates from rawData object
        dates = rawData['date']
        delete rawData['date']

        console.log("Dates:")
        console.log(dates)
        console.log()
        console.log("Raw Data:")
        console.log(rawData)

        // Create chart dataset object array from rawData
        let chartDatasets = [];
        for (metric in rawData) {
            let randomColor = getRandomColor()
            chartDatasets.push({
                label: metric,
                data: rawData[metric].reverse(),
                backgroundColor: randomColor,
                borderColor: randomColor,
                fill: false,
            });
        }

        console.log("Chart Datasets in app.js:")
        console.log(chartDatasets)
        console.log(JSON.stringify(dates))
        res.render('chart', {
            greeting: 'howdy',
            dates: JSON.stringify(dates),
            chartDatasets: JSON.stringify(chartDatasets)
        });
    });
})

app.listen(3000, '0.0.0.0', () => {
    console.log("Server running on port 3000");
});