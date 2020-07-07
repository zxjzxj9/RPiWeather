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

    // From https://datawanderings.com/2019/10/28/tutorial-making-a-line-chart-in-d3-js-v-5/
    const xScale = d3.scaleTime().range([this.ref.current.style.width, 0]);
    const yScale = d3.scaleLinear().rangeRound([this.ref.current.style.height, 0]);

    // xScale.domain(data.timestamp.map(item => new Date(item)));
    const datetime = data.timestamp.map(item => new Date(item))
    const maxmin = d3.extent(datetime);

    //xScale.range([0, 100]);
    xScale.domain(maxmin as [Date, Date]);
    //xScale.domain([Date.now(), Date.now() + 24 * 60 * 60 * 1000]);
    console.log(maxmin);

    const xAxis = d3.axisBottom(xScale);

    curr.append("g")
          .call(xAxis);

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
          <svg style={{height:400, width:600}} ref={this.ref}/>
        </div>
    );
  }
}


export default ChartImg;