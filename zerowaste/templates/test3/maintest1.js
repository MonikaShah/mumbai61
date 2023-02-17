// import { mydata} from "./data/nwardGeojson.js";
// import { geo} from "./data/nward_we.js";
// import { } from "./data/nwardGeojson.js";
import { geo} from "./data/ward.js";
import { mydata } from "./data/dynamic.js";
console.log(mydata)


var map = L.map("map").setView([19.077924, 72.904834], 10);
map.doubleClickZoom.disable();

L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
  maxZoom: 15,
}).addTo(map);

var inputdate = "2020-09-20";



// To Fetch data from the input variabels



var slider = document.getElementById("myRange");

var waste_type=document.getElementById("waste_type");
var output = document.getElementById("demo");
const input_file = document.getElementById("fileInput");

///Date variabels 

var year = document.getElementById("year");
var month = document.getElementById("month");
var year_Month=document.getElementById("yearMonth");
var period=document.getElementById("time_period");
var delay_time=document.getElementById("delay");
var startDate,endDate;

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


Papa.parse('static/js/data/color_update.csv', {
  download: true,
  header: true,
  skipEmptyLines: true,
  complete: function(results) {
    res = results;
    getcall();
    makemap(sliderInput, inputdate);
    console.log(arMap);
  }
});



// ///  Make Map function to add the map

const makemap = (slider, inputdate) => {

  let selectedRegion = mydata.features.filter(
    (d) => d.properties.ward_date == inputdate
  );

  let selectedFeatures = {
    type: "FeatureCollection",
    features: selectedRegion,
  };

  
 
  

function returnColorCode(d)
{
  for( var key of arMap.keys())
  {
    
      if(d>key)
      {
        // console.log("d "+d+" key"+key+" value "+arMap.get(key))
        return arMap.get(key);
      }
  }
}

  function getColor(d) {
  
   
      return returnColorCode(d)
       
  }


  function style(feature) {
    const dataFeature = selectedFeatures.features.find(
      (d) => d.properties.ward_id === feature.properties.ward_id
    );
    // console.log(dataFeature.properties.dry_waste)
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
      }
      catch(err){
        swal("Data Not Found", "Data not found for date "+inputdate, "warning", {
          button: "close",}    );
      }
      
    return {
      fillColor: getColor(value_for_data),
      weight: 2,
      opacity: 1,
      color: "white",
      dashArray: "3",
      fillOpacity: 0.7,
    };
  }

  function highlightFeature(e) {
    var layer = e.target;

    layer.setStyle({
      weight: 5,
      color: "#666",
      dashArray: "",
      fillOpacity: 0.7,
    });

    layer.bringToFront();
  }

  function resetHighlight(e) {
    geojson.resetStyle(e.target);
  }

  function onEachFeature(feature, layer) {
    layer.on({
      mouseover: highlightFeature,
      mouseout: resetHighlight,
      
    });
  }

  var geojson = L.geoJSON(geo, {
    style: style,
     onEachFeature: onEachFeature,
  });
// console.log(data_type)
//   geojson.eachLayer(function(layer) {
//     console.log(selectedFeatures.features.filter(
//       (d) => d.properties.id == layer.feature.properties.id
//     ))
//     if ( selectedFeatures.features.filter((d) => d.properties.id == layer.feature.properties.id) ) {
//       // layer.setStyle({fillColor: "red"});
//       layer.setStyle({fillColor:getColor(data_type,selectedFeatures.features.filter((d) => d.properties.weight))});
//     }
//   });

  geojson.addTo(map);
};

/// end make map function 

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
        console.log(arMap);
}


/// calling make map function to see default output

// makemap(sliderInput, inputdate);


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
  console.log(month.value);
  inputdate = year.value + "-" + month.value + "-" + sliderInput;
  makemap(sliderInput, inputdate);
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
  makemap(sliderInput, inputdate);
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

  // console.log(year.value+"-"+month.value+"-"+ sliderInput);

    inputdate = year.value + "-" + month.value + "-" + sliderInput;
    
  makemap(sliderInput, inputdate);

  
};


/////                         To Read Data From csv file for color codes






/// end all types of event



/* 
                              Jquery 
                              Code 
*/


$( "#year" ).yearpicker({
  year: 2020,
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
                
                makemap(sliderInput, inputdate);



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

