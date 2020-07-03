import React from 'react';
import axios from 'axios';

class ChartImg extends React.Component<any, any> {
  constructor(props: any) {
    super(props)
  }

  fetchDraw(){
    var host = "http://192.168.199.249:8080";
    axios.post(host + "/date_weather", {
      'start': this.props.start,
      'end': this.props.end
    }).then(function (response) {
      var data = response.data;
    })
    .catch(function (error) {
      console.log(error);
    });
  }
  render() {
    return (
        "Test"
    );
  }
}


export default ChartImg;