    const N = 300;
    var height = 0;

    const weightColor = d3.scaleSequentialSqrt(d3.interpolateYlOrRd)
      .domain([0, 1e7]);

    const world = Globe()
      (document.getElementById('globeViz'))
      .globeImageUrl('//cdn.jsdelivr.net/npm/three-globe/example/img/earth-night.jpg')
      .bumpImageUrl('//cdn.jsdelivr.net/npm/three-globe/example/img/earth-topology.png')
      .backgroundImageUrl('//cdn.jsdelivr.net/npm/three-globe/example/img/night-sky.png')
      .hexBinPointWeight(0.1)
      .hexAltitude(.01)
      .hexBinResolution(4)
      .hexTopColor(d => weightColor(d.sumWeight))
      .hexSideColor(d => weightColor(d.sumWeight))
      .hexBinMerge(true)
      .pointAltitude(0.1)
      .enablePointerInteraction(false); // performance improvement



    fetch('http://localhost:5000/get_csv_data')
   .then(response => response.text())
   .then(csv => d3.csvParse(csv, ({ lat, lng, size }) => ({ lat: +lat, lng: +lng, size: +size })))
   .then(data =>  { 
       world.hexBinPointsData(data);
     
      // console.log(data);
   });



    // Add auto-rotation

    world.controls().autoRotate = true;
    world.controls().autoRotateSpeed = 0.1;
  
    // Gen random data


   
    window.onload = function() {
      
      var dataPoints = [];
      
      var chart = new CanvasJS.Chart("chartContainer", {
        backgroundColor: "#000000",
        animationEnabled: true,
        theme: "dark1",  
        title: {
          text: "Covid-19 Data"
        },
        data: [{
          type: "column",
          dataPoints: dataPoints
        }]
      });
      
      function addData(data) {

        console.log(data)
        for (var i = 0; i < data.length; i++) {
          dataPoints.push({
            label: data[i].label,
            y: data[i].y
          });
         
        }
         console.log(dataPoints);
        chart.render();
      
      }
      
      $.getJSON("http://localhost:5000/topten", addData);
      
      }

       fetch('http://localhost:5000/summary')
      .then((response) => {
        return response.json();
      })
      .then((data) => {

        document.getElementById('summary').innerHTML = "<span style='color:yellow'>CONFIRMED : " + data.confirmedCount + '</span><BR>' +  "<span style='color:green'>CURED : " + data.curedCount + " - " + ((data.curedCount/data.confirmedCount)*100).toFixed(2) + "%</span><BR><span style='color:red'>" +  'DEAD: ' + data.deadCount  + " - " + ((data.deadCount/data.confirmedCount)*100).toFixed(2) + "%</span>";

        var typed = new Typed('#typed', {
        stringsElement: '#typed-strings'
        });

        console.log(data);
      });