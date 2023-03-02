import { wardGeojson } from './data/ward.js'
import { prabhagGeojson } from './data/prabhag.js'
import { regionGeojson } from './data/region.js'
import { buildingGeojson } from './data/building.js'

import { wardData } from './data/ward_data.js'
import { prabhagData } from './data/prabhag_data.js'
import { regionData } from './data/region_data.js'
import { buildingData } from './data/building_data.js'

// // console.log(buildingGeojson.layer)
let layerNo = 0  

wardGeojson.features.forEach(function (arrayItem) {
    // arrayItem.properties.wetWaste = parseInt(Math.random() * 50 + 1)
    // arrayItem.properties.solidWaste = parseInt(Math.random() * 300 + 1)
    // arrayItem.properties.totalWaste = arrayItem.properties.wetWaste + arrayItem.properties.solidWaste;
    arrayItem.properties.layerNo = "0";
    arrayItem.properties.isHighlighted = false;
});

prabhagGeojson.features.forEach(function (arrayItem) {
    // arrayItem.properties.wetWaste = parseInt(Math.random() * 50 + 1)
    // arrayItem.properties.solidWaste = parseInt(Math.random() * 300 + 1)
    // // arrayItem.properties.totalWaste = arrayItem.properties.wetWaste + arrayItem.properties.solidWaste;
    // if (arrayItem.properties.prabhag_no == "061" || arrayItem.properties.prabhag_no == "067" || arrayItem.properties.prabhag_no == "069" || arrayItem.properties.prabhag_no == "122" || arrayItem.properties.prabhag_no == "132") {
    //     arrayItem.properties.totalWaste = arrayItem.properties.wetWaste + arrayItem.properties.solidWaste;
    // }
    // else {
    //     arrayItem.properties.totalWaste = 0;
    // }
    arrayItem.properties.layerNo = "1";
    arrayItem.properties.isHighlighted = false;
});
var nameOfregions = []
regionGeojson.features.forEach(function (arrayItem) {
    // arrayItem.properties.wetWaste = parseInt(Math.random() * 50 + 1)
    // arrayItem.properties.solidWaste = parseInt(Math.random() * 300 + 1)
    // arrayItem.properties.totalWaste = arrayItem.properties.wetWaste + arrayItem.properties.solidWaste;
    arrayItem.properties.layerNo = "2";
    nameOfregions.push(arrayItem.properties.Name);
    arrayItem.properties.isHighlighted = false;
});

// // console.log(nameOfregions);

var nameOfBuildings = []
buildingGeojson.features.forEach(function (arrayItem) {
    // arrayItem.properties.wetWaste = parseInt(Math.random() * 50 + 1)
    // arrayItem.properties.solidWaste = parseInt(Math.random() * 300 + 1)
    // arrayItem.properties.totalWaste = arrayItem.properties.wetWaste + arrayItem.properties.solidWaste;
    arrayItem.properties.layerNo = "3";
    nameOfBuildings.push(arrayItem.properties.name);
    arrayItem.properties.isHighlighted = false;
});
// // console.log(nameOfBuildings);



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

// L.geoJson(wardGeojson).addTo(map);



/* 
                Input variables 
*/

var slider = document.getElementById("myRange");
var waste_type=document.getElementById("waste_type");
var output = document.getElementById("demo");
var inputdate = "2021-01-01";
///Date variabels 

var year = document.getElementById("year");
var month = document.getElementById("month");
var year_Month=document.getElementById("yearMonth");
var period=document.getElementById("time_period");
var delay_time=document.getElementById("delay");
var startDate,endDate;
var currentData=wardData;
// map to store csv values and their range
var arMap = new Map();
// to store result of csv file
var res;
// end fetch of data

//output.innerHTML = slider.value;

// initializing slider input to one because the innitial value of slider is undefine
var sliderInput = "0" + 1;
var data_type=waste_type.value;
var default_waste="weight";
var currentGeom;

// var selectedArea= wardGeojson;
// var nextData=wardData;

var sliderGeom=wardGeojson;
var SliderData=wardData;


// For Make map function to filter value based on date 
let DataforLegend

var arrayOfFeature = []



/* 
                            End input variables 
*/

/*
                           make map function
*/

const dat= [ {
    "total_waste_key": "500",
    "total_waste_value": "#003f5c",
    "dry_waste_key": "0.16",
    "dry_waste_value": "#b30000",
    "wet_waste_key": "0.19",
    "wet_waste_value": "#003f5c",
    "weight_key": "0.29",
    "weight_value": "#a073de"
  },
  {
    "total_waste_key": "6000",
    "total_waste_value": "#2f4b7c",
    "dry_waste_key": "0.44",
    "dry_waste_value": "#7c1158",
    "wet_waste_key": "0.25",
    "wet_waste_value": "#2f4b7c",
    "weight_key": "0.28",
    "weight_value": "#F94A29"
  },
  {
    "total_waste_key": "250",
    "total_waste_value": "#665191",
    "dry_waste_key": "3",
    "dry_waste_value": "#4421af",
    "wet_waste_key": "12",
    "wet_waste_value": "#665191",
    "weight_key": "0.27",
    "weight_value": "#39479e"
  },
  {
    "total_waste_key": "1000",
    "total_waste_value": "#a05195",
    "dry_waste_key": "16",
    "dry_waste_value": "#1a53ff",
    "wet_waste_key": "32",
    "wet_waste_value": "#a05195",
    "weight_key": "0.25",
    "weight_value": "#c04680"
  },
  {
    "total_waste_key": "2000",
    "total_waste_value": "#d45087",
    "dry_waste_key": "29",
    "dry_waste_value": "#0d88e6",
    "wet_waste_key": "66",
    "wet_waste_value": "#d45087",
    "weight_key": "0.24",
    "weight_value": "#FD8D3C"
  },
  {
    "total_waste_key": "4500",
    "total_waste_value": "#f95d6a",
    "dry_waste_key": "47",
    "dry_waste_value": "#00b7c7",
    "wet_waste_key": "88",
    "wet_waste_value": "#f95d6a",
    "weight_key": "0.23",
    "weight_value": "#e0aaec"
  },
  {
    "total_waste_key": "100",
    "total_waste_value": "#ff7c43",
    "dry_waste_key": "66",
    "dry_waste_value": "#5ad45a",
    "wet_waste_key": "209",
    "wet_waste_value": "#ff7c43",
    "weight_key": "0.22",
    "weight_value": "#f4e8a4"
  }
];
const result = {
  data: dat
};
res=result;

// Adding Colors

function returnColorCode(d)
{
  for( var key of arMap.keys())
  {
    
      if(d>key)
      {
        // // console.log("d "+d+" key"+key+" value "+arMap.get(key))
        return arMap.get(key);
      }
  }
}

  function getColor(d) {
  
   
      return returnColorCode(d)
       
  }


////




////










const makemap = (geo, mydata) => {


  //  console.log(geo)
  //  console.log(mydata.features)
    var selectedData = mydata.features.filter(
      (d) => d.properties.date == inputdate
    );

    DataforLegend=selectedData;

    let selectedFeatures = {
      type: "FeatureCollection",
      features: selectedData,
    };
  
    
   
    
  
 
  
  
    function style(feature) {
      const dataFeature = selectedFeatures.features.find(
        (d) => d.properties.primary_id === feature.properties.primary_id
      );
        // console.log(dataFeature)
       var value_for_data;
        
       try{
          if (data_type === 'dryWaste') {
            
            value_for_data= dataFeature.properties.dry_waste;
          } else if (data_type === 'wetWaste') {
            value_for_data=dataFeature.properties.wet_waste;
          } else if (data_type === 'totalWaste') {
            value_for_data=dataFeature.properties.total_waste;
          } else if (data_type === 'weight') {
            value_for_data= dataFeature.properties.weight;
          }
          //  console.log(value_for_data)
        }
        catch(err){
          // console.log(data_type,value_for_data)
          
          // swal("Data Not Found", "Data not found for date "+inputdate, "warning", {
          //   button: "close",}    );
          // console.log("data not found for this date "+inputdate)
        }
        
      return {
        fillColor: getColor(value_for_data),
        weight: 2,
        opacity: 1,
        color: "white",
        dashArray: "3",
        fillOpacity: 0.9,
      };
    }

    // function highlightFeature(e) {
    //   var layer = e.target;
  
    //   layer.setStyle({
    //     weight: 5,
    //     color: "#666",
    //     dashArray: "",
    //     fillOpacity: 0.7,
    //   });
  
    //   layer.bringToFront();
    // }

    // function resetHighlight(e) {
    //   geojson.resetStyle(e.target);
    // }
  
    // function onEachFeature(feature, layer) {
    //   layer.on({
    //     mouseover: highlightFeature,
    //     mouseout: resetHighlight,
        
    //   });
    // }


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
          geojson.resetStyle(e.target);
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
    
    
   
    
    function onEachFeature(feature, layer) {
      layer.on({
          mouseover: highlightFeatureSudo,
          mouseout: resetHighlightSudo,
    
          click: function (e) {
             
              if (e.sourceTarget.feature.properties.isHighlighted == false) {
                  highlightFeature(e);
                  //  e.preventDefault();
              }
              else {
                  resetHighlight(e);
                  // e.preventDefault();
              }
              // // console.log(arrayOfFeature)
          }
      });
    }

   

  
    var geojson = L.geoJSON(geo, {
      style: style,
       onEachFeature: onEachFeature,
    }).addTo(map);
 
  
   

  };


  function getcall() {
    arMap.clear();
    if (data_type === 'dryWaste') 
          {
            
            for(var i = 0; i < res.data.length; i++){
              arMap.set(res.data[i].dry_waste_key,res.data[i].dry_waste_value);
             }
          }
          else if (data_type === 'wetWaste') 
          {
            for(var i = 0; i < res.data.length; i++){
              arMap.set(res.data[i].wet_waste_key,res.data[i].wet_waste_value);
             }
          } 
      
          else if (data_type === 'totalWaste') {
            for(var i = 0; i < res.data.length; i++){
              arMap.set(res.data[i].total_waste_key,res.data[i].total_waste_value);
             }
          }
          else if (data_type === 'weight') {
           
            for(var i = 0; i < res.data.length; i++){
              arMap.set(res.data[i].weight_key,res.data[i].weight_value);
             }
          }
          // console.log(arMap);
  }


  getcall();
  /*

                                            End Makemap function  
  */







var currentGeojson = wardGeojson;
var arrayOfEs = [];

// L.geoJson(currentGeojson, { style: style }).addTo(map);

const upBtn = document.querySelector("#drillUp");
const downBtn = document.getElementById('drillDown');

downBtn.addEventListener("click", function () {
    drilldown(arrayOfFeature[arrayOfFeature.length - 1]);
    // console.log(arrayOfFeature[arrayOfFeature.length - 1]);
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



map.eachLayer(function (layer) {
    map.removeLayer(layer);
});

tiles = new L.tileLayer('http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}', {
    maxZoom: 20,
    subdomains: ['mt0', 'mt1', 'mt2', 'mt3']
});

map.addLayer(tiles);

let addedLayer = L.geoJson(wardGeojson);

makemap(currentGeojson,currentData)







function highlightLayer(layerID) {
    map._layers['name' + layerID].setStyle(highlightFeature);
}



function drilldown(e) {
  var selectedArea;
  var nextData;
  let nextGeojson;
    let selectedJsonIDs;
    
    // ward -> Prabhag -> region -> building clusters
    
    if (e.sourceTarget.feature.properties.layerNo == "0") {
        currentData=wardData;
        nextData=prabhagData;

        

        currentGeom="ward";
        nextGeojson = prabhagGeojson
        let selectedWardID = e.sourceTarget.feature.properties.ward_id;
        selectedJsonIDs = nextGeojson.features.filter(d => (d.properties.Ward_Id == selectedWardID));

    }
    else if (e.sourceTarget.feature.properties.layerNo == "1") {
        currentData=prabhagData;
        nextData=regionData;
        currentGeom="prabhag";

        

        nextGeojson = regionGeojson
        let selectedRegionID = e.sourceTarget.feature.properties.prabhag_no;
        selectedJsonIDs = nextGeojson.features.filter(d => (d.properties.ward == selectedRegionID));


    }
    else if (e.sourceTarget.feature.properties.layerNo == "2") {
        currentData=regionData;
        nextData=buildingData;

       

        currentGeom="region";
        nextGeojson = buildingGeojson;
        let buildingClusterID = e.sourceTarget.feature.properties.region;
        selectedJsonIDs = nextGeojson.features.filter(d => (d.properties.name == buildingClusterID));

    }
    else{

      // sliderGeom=buildingGeojson;
      // SliderData=buildingData;

        currentGeom="building"
        currentData=buildingData
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

    // L.geoJson(selectedArea, {
    //     style: style,
    //     onEachFeature: onEachFeature
    // }).addTo(map);
    // // console.log(arrayOfEs);
    makemap(selectedArea,nextData);
    sliderGeom=selectedArea;
    SliderData=nextData;
    // console.log(selectedArea,currentData);
    console.log("drill down "+arrayOfEs.length);
}

function drillUp() {

    // e = [wardJson, PrabhagJson, regionJson];

    

    let nextGeojson;
    let nextData;
    let temp;
    console.log(arrayOfEs);
    if (arrayOfEs.length == 3) {
        nextGeojson = regionGeojson;
        nextData=regionData;
        map.fitBounds([arrayOfEs[arrayOfEs.length - 2].sourceTarget._bounds]);
        // map.removeLayer(addedLayer2);
        map.eachLayer(function (layer) {
            map.removeLayer(layer);
        });
        currentGeojson = nextGeojson;
        // console.log(arrayOfEs);
    }

    else if (arrayOfEs.length == 2) {
        // nextGeojson = prabhagGeojson
        // let selectedRegionID = temp.sourceTarget.feature.properties.ward;
        let selectedRegionIDs = prabhagGeojson.features.filter(d => (d.properties.Ward_Name == arrayOfEs[1].sourceTarget.feature.properties.Ward_Name))
        let selectedRegions = {
            "type": "FeatureCollection",
            "features": selectedRegionIDs
        }
    
        map.fitBounds([arrayOfEs[0].sourceTarget._bounds]);
        // console.log(arrayOfEs);
        // map.removeLayer(addedLayer2);
        map.eachLayer(function (layer) {
            map.removeLayer(layer);
        });
        

        nextGeojson = selectedRegions;
        nextData=prabhagData

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
        // L.geoJson(wardGeojson, {
        //     style: style,
        //     onEachFeature: onEachFeature
        // }).addTo(map);
        // map.setView([19.076090, 72.877426], 11);
        sliderGeom=wardGeojson;
        SliderData=wardData;
        makemap(wardGeojson,wardData)
        // console.log(arrayOfEs);
        arrayOfEs = []
        return 0;
    }

    temp = arrayOfEs.pop();
    tiles = new L.tileLayer('http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}', {
        maxZoom: 20,
        subdomains: ['mt0', 'mt1', 'mt2', 'mt3']
    });

    map.addLayer(tiles);

    // L.geoJson(nextGeojson, {
    //     style: style,
    //     onEachFeature: onEachFeature
    // }).addTo(map);
    sliderGeom=nextGeojson;
    SliderData=nextData
    //console.log(nextGeojson,nextData)
    console.log("drill up "+arrayOfEs.length);
    makemap(nextGeojson,nextData)
}

/*                      To fetch data for legend 

*/



//info update
var info = L.control();
info.onAdd = function (map) {
    this._div = L.DomUtil.create('div', 'info'); // create a div with a class "info"
    console.log("daa")
    this.update();
    return this._div;
};


var legendValue;

// method that we will use to update the control based on feature properties passed
info.update = function (props) {
  if(props)
  {
      let dataforlegend=DataforLegend.filter(
    (d) => d.properties.primary_id==props.primary_id);
    
    try{
        if (data_type === 'dryWaste') {
          
          legendValue=dataforlegend[0].properties.dry_waste;
        } else if (data_type === 'wetWaste') {
          legendValue=dataforlegend[0].properties.wet_waste;
        } else if (data_type === 'totalWaste') {
          legendValue=dataforlegend[0].properties.total_waste;
        } else if (data_type === 'weight') {
          legendValue=dataforlegend[0].properties.weight;
        }
         
      }
      catch(err){
       
        // console.log("data not found for this date "+inputdate)
      }
     console.log(props) 
  }


    this._div.innerHTML = '<h6>'+data_type+'</h6>' + (props ?
        '<b>' + legendValue + '</b> tonns<br />' + props.primary_id + ' (' + props.ward_name_ + ')'
        : 'Hover over a state');
};

info.addTo(map);

//legend
var legend = L.control({ position: 'bottomright' });

var divforupdate;
legend.onAdd = function (map) {
   var div = L.DomUtil.create('div', 'info legend'),
        grades = [0],
        labels = [];
        div.setAttribute('id', 'my-legend');
     return div;  
     this.update();
};

legend.update=function(map){
 
  var updateLegnd=document.getElementById("my-legend");
  updateLegnd.innerHTML='';
  var grades = [0],
  labels = [];
  for( var key of arMap.keys())
  {
      grades.push(key)
      
        //return arMap.get(key);
      
  }

// loop through our density intervals and generate a label with a colored square for each interval
for (var i = 0; i < grades.length; i++) {
  updateLegnd.innerHTML +=
      '<i style="background:' + getColor(grades[i] + 1) + '"></i> ' +
      grades[i] + (grades[i + 1] ? '&ndash;' + grades[i + 1] + '<br>' : '+');
}

};

legend.addTo(map);
legend.update()

// drill down

// ArrayOFEs = [eOfwards, eOfPrabhags, eOfRegion]


/*
///
                          All  types of event
                          which occurs
                          on input changes
////
 */
// on year change event
/*
year.onchange = () => {
  inputdate = year.value + "-" + month.value + "-" + sliderInput;

  makemap(sliderInput, year.value, month.value);
};

// month change event
*/
month.onchange = () => {
    // console.log(month.value);
    inputdate = year.value + "-" + month.value + "-" + sliderInput;
    makemap(sliderGeom,SliderData);
  };
  
  // Year and month 
  
  // year_Month.onchange = () => {
  //   inputdate = year.value + "-" + month.value + "-" + sliderInput
  //   makemap(sliderInput, inputdate);
  // };
  
  
  
  // On type of event change 
  
  waste_type.onchange = () => {
    data_type=waste_type.value;
    getcall()
    legend.update();
    makemap(sliderGeom,SliderData);
  };
  
  
  // on Timeperiod change 
  
  period.onchange = () => {
      if(period.value==="none")
      {
      document.getElementById("month_data").style.display = "block"; 
    } 
    else if(period.value==="rainy")
    {
      
      startDate="06";
      endDate="09";
      for (let i = month.options.length - 1; i >= 0; i--) {
        let value = month.options[i].value;
        if (value < startDate ||  value > endDate ) {
          month.remove(i);
        }
      }
    }
    else if(period.value==="autum")
    {
      
      startDate="10";
      endDate="11";
      for (let i = month.options.length - 1; i >= 0; i--) {
        let value = month.options[i].value;
        if (value < startDate ||  value > endDate ) {
          month.remove(i);
        }
      }
  
    }
    else if(period.value==="winter")
    {
  
      startDate="12";
      endDate="02";
      for (let i = month.options.length - 1; i >= 0; i--) {
        let value = month.options[i].value;
        if (value > endDate &&  value < startDate ) {
          month.remove(i);
        }
      }
    }
    else if(period.value==="summer")
    {
  
      startDate="03";
      endDate="05";
      for (let i = month.options.length - 1; i >= 0; i--) {
        let value = month.options[i].value;
        if (value < startDate ||  value > endDate ) {
          month.remove(i);
        }
      }
    }
  
    
  
  
  };
  
  //  On change slider event
  
  slider.oninput = function () {
   
    if (parseInt(this.value, 10) < 10)
      sliderInput = this.value = "0" + this.value;
    else sliderInput = this.value;
    output.innerHTML = this.value;
  
    // // console.log(year.value+"-"+month.value+"-"+ sliderInput);
  
      inputdate = year.value + "-" + month.value + "-" + sliderInput;
      // console.log(selectedArea,nextData)
      makemap(sliderGeom,SliderData);
      
    
  };
  
  
  /////                         To Read Data From csv file for color codes
  
  
  
  
  
  
  /// end all types of event
  
  
  
  /* 
                                Jquery 
                                Code 
  */
  
  
  $( "#year" ).yearpicker({
    year: 2021,
    startYear: 2012,
    endYear: 2030
  });
  
  
  
  var but=document.getElementById("au");
  let timerId;
  but.onclick=function fun()
  {
    
          if (but.value=="start") 
          {
              let value = slider.value;
              let delay = delay_time.value *1000; 
          // Function to change the value of the slider after a certain delay
              function changeValue()
              {
                    value++;
                    if (value > slider.max) {
                      value = slider.min;
                    }
                    slider.value = value;
  
  
                  if (parseInt(slider.value, 10) < 10)
                      sliderInput = slider.value = "0" + slider.value;
                  else 
                      sliderInput = slider.value;
                  
                  output.innerHTML = sliderInput;
                  inputdate = year.value + "-" + month.value + "-" + sliderInput;
                  
                  makemap(sliderGeom,SliderData);
  
  
  
                  timerId =setTimeout(changeValue, delay);
          }
  
          // Call the function to start the automatic change
          timerId =setTimeout(changeValue, delay);
  
          // Event listener to change the value when it's automated
          slider.addEventListener("input", function() {
            value = slider.value;
          
          });
          
          but.value = "stop";
          }
        else 
        {
          clearTimeout(timerId); // Stop the timeout using the ID
          but.value = "start";
        }
  
  }










