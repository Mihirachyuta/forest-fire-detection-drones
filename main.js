var layout = {
  dragmode: "zoom",
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

var config = {
  mapboxAccessToken:
    "pk.eyJ1IjoibWloaXJhY2h5dXRhIiwiYSI6ImNrdzBhNzJmMTBkc3kyd3BxZ2Qwcm12YmEifQ.oqfDCGJ9A8F4OLMzcgR7JA",
};

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
          size: 15,
          symbol: "airport",
        },
        text: data.id,
        textposition: "bottom right",
      },
    ];
    console.log(data);
    Plotly.newPlot("myDiv", dataFrame, layout, config);
  });
