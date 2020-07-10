import React from 'react';
import axios, { AxiosResponse } from 'axios';
import * as d3 from 'd3';
import { tsv } from 'd3';


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

  fetchDraw(){
    var host = "http://192.168.199.249:8080";
    var ret;
    const thisref = this;
    return axios.post<WeatherData>(host + "/date_weather", {
             'start': this.props.start.toISOString(),
             'end': this.props.end.toISOString()
           }).then(function (response) {
             const data = response.data;
             // console.log(data);
             thisref.drawData(data);
             return data;
           })
             .catch(function (error) {
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
    const yScale_T = d3.scaleLinear().rangeRound([height, 0]);
    const yScale_P = d3.scaleLinear().rangeRound([height, 0]);
    const yScale_H = d3.scaleLinear().rangeRound([height, 0]);

    yScale_T.domain(d3.extent(data.temperature) as [number, number]);
    yScale_P.domain(d3.extent(data.pressure) as [number, number]);
    yScale_H.domain(d3.extent(data.humidity) as [number, number]);

    // xScale.domain(data.timestamp.map(item => new Date(item)));
    const datetime = data.timestamp.map(item => new Date(item))
    xScale.domain(d3.extent(datetime) as [Date, Date]);
    //xScale.domain([Date.now(), Date.now() + 24 * 60 * 60 * 1000]);
    //console.log(maxmin);

    const xAxis = d3.axisBottom(xScale);
    const yAxisT = d3.axisLeft(yScale_T);
    const yAxisP = d3.axisLeft(yScale_P);
    const yAxisH = d3.axisRight(yScale_H);

    function trans(x: number, y:number) {
      return "translate(" + (x + margin.left) + ", " + (y + margin.top) + ")";
    }

    curr.append("g")
          .attr("transform", trans(0, height))
          .call(xAxis)
          .append("text")
          .attr("class", "axis-title")
          .attr("transform", "rotate(0)")
          .attr("x", width/2)
          .attr("y", 20)
          .attr("dy", "2.00em")
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
          .style("text-anchor", "end")
          .attr("fill", "#000000")
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
          .style("text-anchor", "end")
          .attr("fill", "#000000")
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
          .style("text-anchor", "end")
          .attr("fill", "#000000")
          .text("Humidity%");
    //curr.append("g")
    //      .attr("transform", "translate(" + width + ", 0)") 
    //      .call(yAxisP);

    //curr.append("g")
    //      .attr("transform", "translate(" + width + ", 0)") 
    //      .call(yAxisH);
    //const ts = data!["timestamp"];
    //console.log(ts);
    //xScale.domain(d3.extent(ts.map(item:string => new Date(item))));
    //xScale.domain(d3.extent(data["timestamp"].map function(d){
    //    return new Date(d);}));

    // curr.append("circle")
    //      .attr("cx", Math.random()*30)
    //      .attr("cy", Math.random()*30)
    //      .attr("r", Math.random()*10);
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