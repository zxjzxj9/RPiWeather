import React from 'react';
import axios from 'axios';
import * as d3 from 'd3';


class ChartImg extends React.Component<any, any>{

  private ref: any;
  constructor(props: any) {
    super(props)
    this.ref = React.createRef();
  }

  fetchData(){
    var host = "http://192.168.199.249:8080";
    var ret;
    axios.post(host + "/date_weather", {
      'start': this.props.start.toISOString(),
      'end': this.props.end.toISOString()
    }).then(function (response) {
      const data = response.data;
      console.log(data);
      //return data;
      ret = data;
    })
    .catch(function (error) {
      console.log(error);
    });
    return ret;
  }

  fetchDraw() {
    const data = this.fetchData();
    console.log(data);
    const curr = d3.select(this.ref.current);
    curr.append("circle")
          .attr("cx", 40)
          .attr("cy", 60)
          .attr("r", 10);
  }

  render() {
    return (
        <div>
          <svg style={{height:400, width:600}} ref={this.ref}/>
          {this.fetchDraw()}
        </div>
    );
  }
}


export default ChartImg;