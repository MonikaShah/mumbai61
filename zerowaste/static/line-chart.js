function drawxmr(data, box, w_type,area) {
  console.log(data,box,w_type,area)
    let sum = 0; 
let title_chart;
let line_title;
let data1=[];
    data.sort((a, b) => new Date(a.coll_date) - new Date(b.coll_date))
   if(area == "region"){
 
let unique_date = data.map(item => item.coll_date)
.filter((value, index, self) => self.indexOf(value) === index);
let unique_region =data.map(item => item.region)
.filter((value, index, self) => self.indexOf(value) === index);

let yval1 = d =>{
  if(w_type=='total_waste'){ 
    line_title = "Total Waste";
   
     return d.total_waste}
   else if(w_type == 'dry_waste_before_segregation'){
    line_title = "Dry Waste";
   
    return d.dry_waste_before_segregation}
   else if(w_type == 'wet_waste_before_segregation'){
    line_title = "Wet Waste";
   
    return d.wet_waste_before_segregation}
   else if(w_type == 'hazardous_waste'){
    line_title = "Hazardous Waste";
   
    return d.hazardous_waste}};
 
// Define Data

data1 =[];
unique_region.forEach(function(b){
let trace;
let xval = [];
let yval = [];

// unique_date.forEach(function(e) {
    data.forEach(function(f){
      if(f.region == b){
        // console.log(f,b)
xval.push(f.coll_date);
yval.push(yval1(f));
       
      }
    })
  // })
  trace = {
    type: "scatter",
    mode: "lines+markers",
    name: b,
    x: xval,
    y: yval,
    color:b
  }
  data1.push(trace)
  title_chart = "Region wise Chart" + '('+line_title+')';

})
   }
else{
  if(w_type=='total_waste'){ 
    line_title = "Total Waste";
   
  }
   else if(w_type == 'dry_waste_before_segregation'){
    line_title = "Dry Waste";
   
    }
   else if(w_type == 'wet_waste_before_segregation'){
    line_title = "Wet Waste";
   
    }
   else if(w_type == 'hazardous_waste'){
    line_title = "Hazardous Waste";
   
    };
  title_chart = "Prabhag wise Chart" + '('+line_title+')';

  var trace2 = {
    type: "scatter",
    mode: "lines+markers",
    name: "Ward 61",
    x: unpack1(data, 'coll_date'),
    y: unpack(data, w_type),
    color: w_type
  }

  
data1 = [trace2];
}
// console.log(result,'trace2');
    console.log(data1);
  function unpack(rows, key) {
    return data.map(function (row) {  return row[key]; });
  }
  var selectorOptions = {
    buttons: [{
        step: 'month',
        stepmode: 'backward',
        count: 1,
        label: '1m'
    }, {
        step: 'month',
        stepmode: 'backward',
        count: 6,
        label: '6m'
    }, {
        step: 'year',
        stepmode: 'todate',
        count: 1,
        label: 'YTD'
    }, {
        step: 'year',
        stepmode: 'backward',
        count: 1,
        label: '1y'
    }, {
        step: 'all',
    }],
};
  function unpack1(rows, key) {
    return data.map(function (row) { 
 return new Date(row[key]) });
  }
  
  
  var layout = {

    title: {text:title_chart,
      size:15
    },

    xaxis: {
      rangeselector: selectorOptions,
      rangeslider: {}
  },
yaxis: {
rangemode: 'tozero',
// tickvals:tickVals,
//       ticktext: tickVals.map(function(val){ return numberWithCommas(val); }),
      title:w_type,
    //   type: 'date',
      linewidth: 2,
      ticks: 'outside',
      tick0: 0,
      nticks:4,
      tickcolor: '#000',
},
    height: 600,
    margin: {
      t: 50,
      b: 40,
      l: 60,
       r:20,
      pad: 0
    },
    showlegend: true,

    annotations:[]
  };

  var config = { responsive: true };
  Plotly.newPlot(box, data1,layout, { displayModeBar: false },config);
}