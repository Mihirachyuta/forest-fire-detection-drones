var dataFrame;
fetch("http://127.0.0.1:5000/drones")
  .then((response) => response.json())
  .then((data) => {
    dataFrame = [
      {
        type: "scattermapbox",
        mode: "markers+text",
        lat: data.lat,
        lon: data.long,
        marker: {
          size: 15,
          symbol: "airport",
        },
        text: data.id,
        textposition: "bottom right",
      },
    ];
  });
var layout = {
  dragmode: "closest",
  mapbox: {
    style: "outdoors",
    zoom: 8,
    center: {
      lat: -2.314755,
      lon: -62.650526,
    },
  },
  showlegend: false,
  height: "720",
  width: "1280",
  autosize: true,
};
plot = Plotly.newPlot("myDiv", dataFrame, layout, config);
var config = {
  mapboxAccessToken:
    "pk.eyJ1IjoibWloaXJhY2h5dXRhIiwiYSI6ImNrdzBhNzJmMTBkc3kyd3BxZ2Qwcm12YmEifQ.oqfDCGJ9A8F4OLMzcgR7JA",
};

function fetch_data() {
  fetch("http://127.0.0.1:5000/drones")
    .then((response) => response.json())
    .then((data) => {
      var dataFrame = [
        {
          type: "scattermapbox",
          mode: "markers+text",
          lat: data.lat,
          lon: data.long,
          marker: {
            size: data.size,
            symbol: data.symbol,
          },
          text: data.id,
          textposition: "bottom right",
        },
      ];
      console.log(data);
      Plotly.newPlot("myDiv", dataFrame, layout, config);
      //Plotly.update(graphDiv, data_update, layout_update, 0);

      //plot.dataFrame = dataFrame;
    });
}
fetch_data();
setInterval(fetch_data, 5000);
