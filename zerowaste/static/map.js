let mergedData;

const svg = d3.select('svg');
const transitionDuration = 500;
const width = document.body.clientWidth/2;
const height = document.body.clientHeight/1.5;
console.log(width,height)
let active = d3.select(null);
svg.attr('width', width).attr('height', height)
const g = svg.append('g');
var mercator = d3 .geoMercator() .scale(1).translate([0, 100]);
//const mercator = geoMercator().scale(30000).translate([width/2, height/2]).center([73,19.7]);
const pathGenerator = d3.geoPath().projection(mercator);
let text;
let legend_title;
//Zoom
let sampleCategoricalData = [];

let zzoom = d3.zoom().scaleExtent([1, 10]).on("zoom", zoomed);
let  ColorValue = d => {
  console.log(d,w_type,"ye");
  
  if(w_type=='total_waste'){ 
  legend_title = "Total Waste";
  // sampleCategoricalData.push(d.properties.total_waste);
   return d.properties.total_waste}
  else if(w_type == 'dry_waste_before_segregation'){
  legend_title = "Dry Waste";
  // sampleCategoricalData.push(d.properties.dry_waste);
  return d.properties.dry_waste}
  else if(w_type == 'wet_waste_before_segregation'){
  legend_title = "Wet Waste";
  // sampleCategoricalData.push(d.properties.wet_waste);
  return d.properties.wet_waste}
  else if(w_type == 'hazardous_waste'){
  legend_title = "Hazardous Waste";
  // sampleCategoricalData.push(d.properties.hazardous_waste);
  return d.properties.hazardous_waste}};


console.log(sampleCategoricalData,"color")
let Tooltipheader1 = d => area;
let Tooltipheader2 = d => legend_title;
let TooltipVal1 = d => legend_title_val(d);
let TooltipVal2 = d => ColorValue(d);
// let ColorValue = d => d.properties.tot;
function zoomed() {
    g.style("stroke-width", 1 / d3.event.transform.k + "px");
    g.attr("transform", d3.event.transform); // updated for d3 v4
  }
  let colors = [ "#00af50", "#fff000", "#ffc000", "#fe0000", "#8e0000"]
  let tooltip = d3.select("body")
  .append("div")
  .attr("class", "tooltip")
  .style("opacity", 0);
let legend_title_val = d =>{
  if(area=="ward"){
    return d.properties.ward;
  }
  else if(area=="region"){
    return d.properties.region;
  }
};

// = d3.scaleOrdinal().domain([Math.min(sampleCategoricalData),Math.max(sampleCategoricalData)])
// .range( colors);

    // let sampleCategoricalData = []
   
  //makemap
  let tooltipValue = (d) => {
    let ttv = `
        ${Tooltipheader1(d)} : ${TooltipVal1(d)} <br>
        ${Tooltipheader2(d)} :${TooltipVal2(d)} (Kgs)`;
    return ttv;
  }
  const onMouseOverPoly = d => {
    tooltip
      .transition()
      .duration(200)
      .style("opacity", 0.9);
    tooltip
      .html(tooltipValue(d))
      .style("left", d3.event.pageX + "px")
      .style("top", d3.event.pageY - 30 + "px");

  };
//selectmap
const selectMap = (geojson,location,area) => {
  console.log(area,"area");
  if(area == "ward"){
    
  if(location == "61"){
    location= 'ward61';
  }
    var selection = [];
    geojson.forEach( sel =>{
    if (sel.properties.ward == location){
    selection.push(sel);
    }
    });
    area="region";
  }
  else if(area=="region"){
    var selection = [];
    geojson.forEach( sel =>{
    if (sel.properties.region == location){
    selection.push(sel);
    }
    });
    area="cluster";
  }
   
    return selection;
} 


  // const readGeoJSON = (filename) => {
  //   let a;
  // let json = d3.json(`${filename}`).then(json =>{
  //   a=  json.features;
  // })
  // console.log(a, 'a');
  // }
  
  // let features = readGeoJSON('cluster.json');
  // var scaleCenter = calculateScaleCenter(features.features);
  // mercator.scale(scaleCenter.scale) .center(scaleCenter.center) .translate([width / 2, height / 2]);
  let dom;
  
  function calculateScaleCenter(features) {
   var bbox_path = pathGenerator.bounds(features),
  scale = 0.95 / Math.max( (bbox_path[1][0] - bbox_path[0][0]) / width, (bbox_path[1][1] - bbox_path[0][1]) / height ); 
  var bbox_feature = d3.geoBounds(features), center = [ (bbox_feature[1][0] + bbox_feature[0][0]) / 2, ((bbox_feature[1][1] + bbox_feature[0][1]) / 2)]; 
  return { 'scale': scale, 'center': center }; }

  async function legend(array_no_at_risk) {
    // console.log(array_no_at_risk,"array")
    // if (array_no_at_risk.length <= 2) {
    //   array_no_at_risk.push(0);
    // }
    array_no_at_risk.sort(function (a, b) { return a - b });
if(array_no_at_risk.length == '1'){
  dom = [0,array_no_at_risk[0]];
}
else{
  dom =  [d3.min(array_no_at_risk),d3.max(array_no_at_risk)];
}
    colorScale = d3.scaleQuantile()
      .domain(dom) // pass the whole dataset to a scaleQuantile’s domain
      .range(colors);

    localeEnIN = await fetch("https://cdn.jsdelivr.net/npm/d3-format@3/locale/en-IN.json")
      .then(d => d.json()).then(d3.formatLocale);
    // let 
    // if (underserved == true) {
    //   formatter = localeEnIN.format(",.0f");

    // }
    // else {
    //   formatter = localeEnIN.format(",.1f");


    // }
    let myLegend;

    svg.append("g")
      .attr("class", "legendQuant")
      .attr("transform", `translate(${width - 200},20)`)

    myLegend = d3.legendColor()
      // .labelFormat(formatter)
      .cells(10)
      .title(legend_title)
      .scale(colorScale);
    svg.select(".legendQuant")
      .call(myLegend);
  }