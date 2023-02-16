// Import json data
import { wardGeoJson } from './ward.js'
import { prabhagGeojson } from './prabhag.js'
import { regionGeojson } from './region_new_merged.js'
import { buildingGeojson } from './building.js'


//fetch Geojson data
// let url =
// "https://earthquake.usgs.gov/earthquakes/feed/v1.0/" +
// "summary/4.5_week.geojson";
// fetch(url)
// .then(function(response) {
// return response.json();
// })
// .then(function(data) {
// L.geoJSON(data).addTo(map);
// });let geojson



// console.log(buildingGeojson.layer)
let layerNo = 0

wardGeoJson.features.forEach(function (arrayItem) {
    arrayItem.properties.wetWaste = parseInt(Math.random() * 50 + 1)
    arrayItem.properties.solidWaste = parseInt(Math.random() * 300 + 1)
    arrayItem.properties.totalWaste = arrayItem.properties.wetWaste + arrayItem.properties.solidWaste;
    arrayItem.properties.layerNo = "0";
    arrayItem.properties.isHighlighted = false;
});

prabhagGeojson.features.forEach(function (arrayItem) {
    arrayItem.properties.wetWaste = parseInt(Math.random() * 50 + 1)
    arrayItem.properties.solidWaste = parseInt(Math.random() * 300 + 1)
    // arrayItem.properties.totalWaste = arrayItem.properties.wetWaste + arrayItem.properties.solidWaste;
    if (arrayItem.properties.prabhag_no == "061" || arrayItem.properties.prabhag_no == "067" || arrayItem.properties.prabhag_no == "069" || arrayItem.properties.prabhag_no == "122" || arrayItem.properties.prabhag_no == "132") {
        arrayItem.properties.totalWaste = arrayItem.properties.wetWaste + arrayItem.properties.solidWaste;
    }
    else {
        arrayItem.properties.totalWaste = 0;
    }
    arrayItem.properties.layerNo = "1";
    arrayItem.properties.isHighlighted = false;
});
var nameOfregions = []
regionGeojson.features.forEach(function (arrayItem) {
    arrayItem.properties.wetWaste = parseInt(Math.random() * 50 + 1)
    arrayItem.properties.solidWaste = parseInt(Math.random() * 300 + 1)
    arrayItem.properties.totalWaste = arrayItem.properties.wetWaste + arrayItem.properties.solidWaste;
    arrayItem.properties.layerNo = "2";
    nameOfregions.push(arrayItem.properties.Name);
    arrayItem.properties.isHighlighted = false;
});

// console.log(nameOfregions);

var nameOfBuildings = []
buildingGeojson.features.forEach(function (arrayItem) {
    arrayItem.properties.wetWaste = parseInt(Math.random() * 50 + 1)
    arrayItem.properties.solidWaste = parseInt(Math.random() * 300 + 1)
    arrayItem.properties.totalWaste = arrayItem.properties.wetWaste + arrayItem.properties.solidWaste;
    arrayItem.properties.layerNo = "3";
    nameOfBuildings.push(arrayItem.properties.name);
    arrayItem.properties.isHighlighted = false;
});
// console.log(nameOfBuildings);



let mapOptions = {
    center: [19.076090, 72.877426],
    zoom: 11
};

// create base map
let map = L.map('map', mapOptions);

// define OSM layer to be added on map
let tiles = new L.tileLayer('http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}', {
    maxZoom: 20,
    subdomains: ['mt0', 'mt1', 'mt2', 'mt3']
});

map.addLayer(tiles);

map.doubleClickZoom.disable();

// L.geoJson(wardGeoJson).addTo(map);



// Adding Colors

function getColor(d) {
    return d > 1000 ? '#800026' :
        d > 500 ? '#BD0026' :
            d > 200 ? '#E31A1C' :
                d > 100 ? '#FC4E2A' :
                    d > 50 ? '#FD8D3C' :
                        d > 20 ? '#FEB24C' :
                            d > 10 ? '#FED976' :
                                '#FFEDA0';
}

function style(feature) {
    return {
        fillColor: getColor(feature.properties.totalWaste),
        weight: 2,
        opacity: 1,
        color: 'white',
        dashArray: '3',
        fillOpacity: 1
    };
}


var currentGeojson = wardGeoJson;
var arrayOfEs = [];

L.geoJson(currentGeojson, { style: style }).addTo(map);

const upBtn = document.querySelector("#drillUp");
const downBtn = document.getElementById('drillDown');

downBtn.addEventListener("click", function () {
    drilldown(arrayOfFeature[arrayOfFeature.length - 1]);
    console.log(arrayOfFeature[arrayOfFeature.length - 1]);
    arrayOfFeature = [];
});

upBtn.addEventListener("click", function () {
    drillUp();
    arrayOfFeature = []
});




function highlightFeatureSudo(e) {
    var layer = e.target;
    layer.setStyle({
        weight: 4,
        color: '#f9fafc',
        dashArray: '',
        fillOpacity: 0.7
    });

    if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
        layer.bringToFront();
    }
}

// Adding Interaction

function highlightFeature(e) {
    var layer = e.target;
    arrayOfFeature.push(e);
    layer.setStyle({
        weight: 7,
        color: '#f9fafc',
        dashArray: '',
        fillOpacity: 0.7
    });
    e.sourceTarget.feature.properties.isHighlighted = true;

    if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
        layer.bringToFront();
    }
    info.update(layer.feature.properties);
}


function resetHighlightSudo(e) {
    if (e.sourceTarget.feature.properties.isHighlighted == false) {
        addedLayer.resetStyle(e.target);
    }

}

function resetHighlight(e) {
    addedLayer.resetStyle(e.target);
    info.update();
    e.sourceTarget.feature.properties.isHighlighted = false;
    arrayOfFeature.pop();
}

function zoomToFeature(e) {
    map.fitBounds(e.target.getBounds());
}


var arrayOfFeature = []

function onEachFeature(feature, layer) {
    layer.on({
        mouseover: highlightFeatureSudo,
        mouseout: resetHighlightSudo,

        click: function (e) {
            addData(myChart, barChart);
            if (e.sourceTarget.feature.properties.isHighlighted == false) {
                highlightFeature(e);
                e.preventDefault();
            }
            else {
                resetHighlight(e);
                e.preventDefault();
            }
            // console.log(arrayOfFeature)
        }
    });
}

map.eachLayer(function (layer) {
    map.removeLayer(layer);
});

tiles = new L.tileLayer('http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}', {
    maxZoom: 20,
    subdomains: ['mt0', 'mt1', 'mt2', 'mt3']
});

map.addLayer(tiles);

let addedLayer = L.geoJson(wardGeoJson, {
    style: style,
    onEachFeature: onEachFeature
}).addTo(map);





// update chartjs data array
function addData(chart1, chart2) {
    var randomArray = []
    for (let index = 0; index < 12; index++) {
        randomArray.push(parseInt(Math.random() * 300 + 1));
    }
    chart1.data.datasets[0].data = randomArray
    randomArray = []
    for (let index = 0; index < 5; index++) {
        randomArray.push(parseInt(Math.random() * 300 + 1));
    }
    // console.log(randomArray);
    chart2.data.datasets[0].data = randomArray;
    chart1.update();
    chart2.update();
}

function highlightLayer(layerID) {
    map._layers['name' + layerID].setStyle(highlightFeature);
}

function drilldown(e) {
    // ward -> Prabhag -> region -> building clusters
    let nextGeojson;
    let selectedJsonIDs;
    if (e.sourceTarget.feature.properties.layerNo == "0") {

        nextGeojson = prabhagGeojson
        let selectedWardID = e.sourceTarget.feature.properties.ward_id;
        selectedJsonIDs = nextGeojson.features.filter(d => (d.properties.Ward_Id == selectedWardID));

    }
    else if (e.sourceTarget.feature.properties.layerNo == "1") {
        nextGeojson = regionGeojson
        let selectedRegionID = e.sourceTarget.feature.properties.ward;
        selectedJsonIDs = nextGeojson.features.filter(d => (d.properties.ward == "ward61"));


    }
    else if (e.sourceTarget.feature.properties.layerNo == "2") {
        nextGeojson = buildingGeojson;
        let buildingClusterID = e.sourceTarget.feature.properties.region;
        selectedJsonIDs = nextGeojson.features.filter(d => (d.properties.name == buildingClusterID));

    }

    //filtered Values
    let selectedJson = {
        "type": "FeatureCollection",
        "features": selectedJsonIDs
    }
    map.fitBounds([e.sourceTarget._bounds]);
    map.eachLayer(function (layer) {
        map.removeLayer(layer);
    });
    selectedArea = selectedJson;
    currentGeojson = nextGeojson;
    arrayOfEs.push(e);

    tiles = new L.tileLayer('http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}', {
        maxZoom: 20,
        subdomains: ['mt0', 'mt1', 'mt2', 'mt3']
    });

    map.addLayer(tiles);

    L.geoJson(selectedArea, {
        style: style,
        onEachFeature: onEachFeature
    }).addTo(map);
    // console.log(arrayOfEs);

}

function drillUp() {

    // e = [wardJson, PrabhagJson, regionJson];

    addData(myChart, barChart);
    let nextGeojson;

    if (arrayOfEs.length == 3) {
        nextGeojson = regionGeojson;
        map.fitBounds([arrayOfEs[arrayOfEs.length - 2].sourceTarget._bounds]);
        // map.removeLayer(addedLayer2);
        map.eachLayer(function (layer) {
            map.removeLayer(layer);
        });
        currentGeojson = nextGeojson; 3
        console.log(arrayOfEs);
    }

    else if (arrayOfEs.length == 2) {
        // nextGeojson = prabhagGeojson
        // let selectedRegionID = temp.sourceTarget.feature.properties.ward;
        let selectedRegionIDs = prabhagGeojson.features.filter(d => (d.properties.Ward_Name == "K WEST"));
        let selectedRegions = {
            "type": "FeatureCollection",
            "features": selectedRegionIDs
        }
        map.fitBounds([arrayOfEs[0].sourceTarget._bounds]);
        console.log(arrayOfEs);
        // map.removeLayer(addedLayer2);
        map.eachLayer(function (layer) {
            map.removeLayer(layer);
        });

        nextGeojson = selectedRegions;

    }

    else if (arrayOfEs.length == 1) {

        map.eachLayer(function (layer) {
            map.removeLayer(layer);
        });

        tiles = new L.tileLayer('http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}', {
            maxZoom: 20,
            subdomains: ['mt0', 'mt1', 'mt2', 'mt3']
        });

        map.addLayer(tiles);
        L.geoJson(wardGeoJson, {
            style: style,
            onEachFeature: onEachFeature
        }).addTo(map);
        map.setView([19.076090, 72.877426], 11);
        console.log(arrayOfEs);
        arrayOfEs = []
        return 0;
    }

    temp = arrayOfEs.pop();
    tiles = new L.tileLayer('http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}', {
        maxZoom: 20,
        subdomains: ['mt0', 'mt1', 'mt2', 'mt3']
    });

    map.addLayer(tiles);

    L.geoJson(nextGeojson, {
        style: style,
        onEachFeature: onEachFeature
    }).addTo(map);
}

//info update
var info = L.control();
info.onAdd = function (map) {
    this._div = L.DomUtil.create('div', 'info'); // create a div with a class "info"
    this.update();
    return this._div;
};

// method that we will use to update the control based on feature properties passed
info.update = function (props) {
    this._div.innerHTML = '<h6>Total Waste</h6>' + (props ?
        '<b>' + props.totalWaste + '</b> tonns<br />' + props.ward_id + ' (' + props.ward_name_ + ') ' + props.region + ' '
        : 'Hover over a state');
};

info.addTo(map);

//legend
var legend = L.control({ position: 'bottomright' });

legend.onAdd = function (map) {
    var div = L.DomUtil.create('div', 'info legend'),
        grades = [0, 10, 20, 50, 100, 200, 500, 1000],
        labels = [];

    // loop through our density intervals and generate a label with a colored square for each interval
    for (var i = 0; i < grades.length; i++) {
        div.innerHTML +=
            '<i style="background:' + getColor(grades[i] + 1) + '"></i> ' +
            grades[i] + (grades[i + 1] ? '&ndash;' + grades[i + 1] + '<br>' : '+');
    }
    return div;
};


legend.addTo(map);


// drill down

// ArrayOFEs = [eOfwards, eOfPrabhags, eOfRegion]


var ctx = document.getElementById("myChart").getContext('2d');

var valueArray = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    randomArrayOf5 = [0, 0, 0, 0, 0]
var myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: ["Jan", "Feb", "March", "May", "June", "July", "Aug", "Sep", "Oct", "Nov", "Dec"],
        datasets: [{
            label: 'Time Period', // Name the series
            data: valueArray, // Specify the data values array
            fill: false,
            borderColor: '#2196f3', // Add custom color border (Line)
            backgroundColor: '#2196f3', // Add custom color background (Points and Fill)
            borderWidth: 1, // Specify bar border width
        }]
    },
    options: {
        responsive: true, // Instruct chart js to respond nicely.
        maintainAspectRatio: false, // Add to prevent default behaviour of full-width/height 
    }
});


var barChart = new Chart(document.getElementById("bar-chart"), {
    type: 'bar',
    data: {
        labels: ["2018", "2019", "2020", "2021", "2022"],
        datasets: [
            {
                label: "Waste (tons)",
                backgroundColor: ["#3e95cd", "#8e5ea2", "#3cba9f", "#e8c3b9", "#c45850"],
                data: randomArrayOf5
            }
        ]
    },
    options: {
        legend: { display: false },
        title: {
            display: true,
            text: 'Predicted world population (millions) in 2050'
        },
        responsive: true, // Instruct chart js to respond nicely.
        maintainAspectRatio: false, // Add to prevent default behaviour of full-width/height 
    }
});



var yearDropDown = document.getElementById("dropdownYear");
var wasteDropDown = document.getElementById("dropdownWaste");

function onChangeYear() {
    var value = yearDropDown.value;
    var text = yearDropDown.options[yearDropDown.selectedIndex].text;
    console.log(value);
    addData(myChart, barChart);
}

function onChangeWaste() {
    var value = wasteDropDown.value;
    var text = wasteDropDown.options[wasteDropDown.selectedIndex].text;
    console.log(value);
    addData(myChart, barChart);
}

yearDropDown.onchange = onChangeYear;
dropdownWaste.onchange = onChangeWaste;




