import React from 'react';
import axios from 'axios';
import * as d3 from 'd3';
// import ReactDOM from 'react-dom';
// import { renderToStaticMarkup } from 'react-dom/server';


interface WeatherData {
    humidity: number[];
    pressure: number[];
    temperature: number[];
    timestamp: string[];
}

class ChartImg extends React.Component<any, any> {

  private ref: any;
  constructor(props: any) {
    super(props)
    this.ref = React.createRef();
  }

  download() {
    const clone = this.ref.current.cloneNode(true);
    clone.removeAttribute("style");
    const h = parseInt(this.ref.current.style.height);
    const w = parseInt(this.ref.current.style.width);
    clone.setAttribute("height", h);
    clone.setAttribute("width", w);
    clone.setAttribute("xmlns", "http://www.w3.org/2000/svg");
    clone.setAttribute("xmlns:xlink", "http://www.w3.org/1999/xlink");
    clone.setAttribute("xml:space", "preserve");

    // console.log(clone, h, w);
    const svgData = new XMLSerializer().serializeToString(clone);
    //const svgData = encodeURIComponent(renderToStaticMarkup(clone));

    var wd = (window.open("", "download") as Window);
    var c = wd.document.createElement('canvas');
    c.setAttribute('width', w.toString());
    c.setAttribute('height', h.toString());
    var ctx = c.getContext('2d');
    var img = wd.document.createElement('img');
    //console.log(img);

    var doc = wd.document;
    doc.body.appendChild(img);
    //doc.body.appendChild(c);

    img.onload = () => {
      (ctx as CanvasRenderingContext2D).drawImage(img, 0, 0, w, h);
      // `download` attr is not well supported
      // Will result in a download popup for chrome and the
      // image opening in a new tab for others.

      var a = wd.document.createElement('a');
      doc.body.appendChild(a);
      //console.log(a);
      a.setAttribute('href', c.toDataURL('image/png'))
      a.setAttribute('target', 'download')
      a.setAttribute('download', "data.png");
      a.click();
      wd.close();
    };

    img.setAttribute('src', "data:image/svg+xml;base64," + window.btoa(unescape(encodeURIComponent(svgData))));
    //img.setAttribute('src', 'data:image/svg+xml;' + btoa(svgData));

  }

  fetchDraw(){
    var host = "http://192.168.199.249:8080";
    const thisref = this;
    return axios.post<WeatherData>(host + "/date_weather", {
             'start': this.props.start.toISOString(),
             'end': this.props.end.toISOString()
           }).then(function (response) {
             const data = response.data;
             // console.log(data);
             thisref.drawData(data);
             return data;
           }).catch(function (error) {
             console.log(error);
           });
  }

  drawData(data: WeatherData) {
    //const data = this.fetchData();
    //console.log(data);
    const curr = d3.select(this.ref.current);
    curr.selectAll("svg > *").remove();

    const margin = {
      top: 50,
      bottom: 50,
      left: 50,
      right: 50
    }

    const height = parseInt(this.ref.current.style.height) - (margin.top + margin.bottom);
    const width = parseInt(this.ref.current.style.width) - (margin.left + margin.right);
    // From https://datawanderings.com/2019/10/28/tutorial-making-a-line-chart-in-d3-js-v-5/
    // console.log(this.ref.current.style.width, this.ref.current.style.height)
    const xScale = d3.scaleTime().range([0, width]);
    const yScaleT = d3.scaleLinear().rangeRound([height, 0]);
    const yScaleP = d3.scaleLinear().rangeRound([height, 0]);
    const yScaleH = d3.scaleLinear().rangeRound([height, 0]);

    yScaleT.domain(d3.extent(data.temperature) as [number, number]);
    yScaleP.domain(d3.extent(data.pressure) as [number, number]);
    yScaleH.domain(d3.extent(data.humidity) as [number, number]);

    // xScale.domain(data.timestamp.map(item => new Date(item)));
    const datetime = data.timestamp.map(item => new Date(item))
    xScale.domain(d3.extent(datetime) as [Date, Date]);
    //xScale.domain([Date.now(), Date.now() + 24 * 60 * 60 * 1000]);
    //console.log(maxmin);

    const xAxis = d3.axisBottom(xScale);
    const yAxisT = d3.axisLeft(yScaleT);
    const yAxisP = d3.axisLeft(yScaleP);
    const yAxisH = d3.axisRight(yScaleH);

    function trans(x: number, y:number) {
      return "translate(" + (x + margin.left) + ", " + (y + margin.top) + ")";
    }

    function drawLine(x: Date[], y: number[], 
      xscaler:d3.ScaleTime<number, number>, 
      yscaler:d3.ScaleLinear<number, number>, 
      color='black') {
      // zip xy
      const d = x.map(function(e, i){return {x:e, y:y[i]};});
      const line = d3.line<any>()
                     .x(d=>xscaler(d.x))
                     .y(d=>yscaler(d.y));
                     //.curve(d3.curveBasis);

      curr.append("path")
          .attr("transform", trans(0, 0))
          .datum(d)
          .attr("class", "line")
          .style("fill", "none")
          .style("stroke", color)
          .style("stroke-opacity", 0.5)
          .style("stroke-width", 2)
          .attr("d", line);
    }

    drawLine(datetime, data.temperature, xScale, yScaleT, "red");
    drawLine(datetime, data.pressure, xScale, yScaleP, "green");
    drawLine(datetime, data.humidity, xScale, yScaleH, "blue");

    // draw axis
    curr.append("g")
          .attr("transform", trans(0, height))
          .call(xAxis)
          .append("text")
          .attr("class", "axis-title")
          .attr("transform", "rotate(0)")
          .attr("x", width/2)
          .attr("y", 20)
          .attr("dy", "2.00em")
          .style("font-size", "12px")
          .style("text-anchor", "end")
          .attr("fill", "#000000")
          .text("Datetime");
    
    curr.append("g")
          .attr("transform", trans(0, 0))
          .call(yAxisT)
          .append("text")
          .attr("class", "axis-title")
          .attr("transform", "rotate(-90)")
          .attr("x", -height/2+30)
          .attr("y", -60)
          .attr("dy", "2.00em")
          .style("font-size", "12px")
          .style("text-anchor", "end")
          .attr("fill", "red")
          .text("Temperature/°C");
    
    curr.append("g")
          .attr("transform", trans(width, 0))
          .call(yAxisP)
          .append("text")
          .attr("class", "axis-title")
          .attr("x", -height/2+30)
          .attr("y", -70)
          .attr("transform", "rotate(-90)")
          .attr("dy", "2.00em")
          .style("font-size", "12px")
          .style("text-anchor", "end")
          .attr("fill", "green")
          .text("Pressure/hBar");

    curr.append("g")
          .attr("transform", trans(width, 0))
          .call(yAxisH)
          .append("text")
          .attr("class", "axis-title")
          .attr("x", height/2+30)
          .attr("y", -60)
          .attr("transform", "rotate(+90)")
          .attr("dy", "2.00em")
          .style("font-size", "12px")
          .style("text-anchor", "end")
          .attr("fill", "blue")
          .text("Humidity%");

  }

  componentDidMount() {
     this.fetchDraw();
  }

  componentDidUpdate() {
     this.fetchDraw();
  }

  render() {
    return (
        <div>
          <svg style={{height:500, width:700}} ref={this.ref}/>
        </div>
    );
  }
}


export default ChartImg;