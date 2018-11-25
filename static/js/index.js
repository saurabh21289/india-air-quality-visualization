nv.addGraph(function() {
var format = d3.time.format("%Y-%d-%m %H:%M:%S").parse;
var chart = nv.models.multiBarChart()
  .useInteractiveGuideline(true);;
chart.xAxis
.tickFormat(function(d) {
  return d3.time.format('%d-%m-%y %H:%M:%S')(format(d));
})
chart.yAxis
.tickFormat(d3.format('02f'));

d3.select('#averageDegreesLineChart svg')
.datum(temperatureIndexJSON)
.transition().duration(500)
.call(chart);
nv.utils.windowResize(chart.update);
return;
});

function test() {
return [

  {
    key: "gabby",
    color: "#51A351",
    values:
      [
        {'x': '2018-11-22 10:05:10', 'y': 14.43},
        {'x': '2018-11-25 10:05:10', 'y': 14.43},
        {'x': '2018-11-24 10:05:10', 'y': 21.68}
      ]
  },
  {
    key: "eric",
    color: "#BD362F",
    values:
      [
        { x : "2016-01-01 10:05:10", y : 60 },
        { x : "2016-01-02 10:05:10", y : 50 },
        { x : "2016-01-03 10:05:10", y : 70 }
      ]
  }
]

}
