import React from 'react';
import { Header, Icon, List, Menu, Segment, Sidebar } from 'semantic-ui-react';
import { DateTimeInput } from 'semantic-ui-calendar-react';

class Index extends React.Component {
  render() {
    return (
      <Header as='h1'>Raspberry Pi Weather System</Header>
    );
  }
}

class Chart extends React.Component {
  constructor(props) {
    super(props);
    var date1 = new Date();
    // 8 Hours before current time
    date1.setHours(date1.getHours() - 8);
    var date2 = new Date();
    this.state = {
      date: '',
      time: '',
      dateTime: '',
      datesRange: '',
      start: date1,
      end: date2
    };
  }

  handleChange = (event, { name, value }) => {
    if (this.state.hasOwnProperty(name)) {
      this.setState({ [name]: value });
    }
  }

  render() {
    return (
      <div>
      <Header as='h1'>Weather Data Chart</Header>
      <List divided relaxed>
        <List.Item>
          <List.Header> Start datetime: </List.Header> 
          <DateTimeInput value={this.state.start} dateFormat="DD-MM-YYYY HH:MM" onChange={this.handleChange}/>
      	</List.Item>

        <List.Item> 
          <List.Header> End datetime: </List.Header> 
          <DateTimeInput value={this.state.end} dateFormat="DD-MM-YYYY HH:MM" onChange={this.handleChange}/>
      	</List.Item>
      </List>
      </div>
    );
  }
}

class MainPage extends React.Component {
    
  constructor(props) {
    super(props);
    this.state = {content: 'index'};
  }

  handleClick(componentName) {
    this.setState({content: componentName});
  }

  renderSideBar() {
    switch(this.state.content) {
      case 'index': return <Index />;
      case 'chart': return <Chart />;
      default: return <Index />;
    }
  }

  render() {
    return (
      <Sidebar.Pushable as={Segment}>
        <Sidebar
          as={Menu}
          animation='push'
          icon='labeled'
          inverted
          vertical
          visible
          width='thin'
      >
        <Menu.Item as='a' onClick={this.handleClick.bind(this, "chart")}>
          <Icon name='chart line' />
          Weather Data
        </Menu.Item>
        <Menu.Item as='a' onClick={this.handleClick.bind(this, "ml")}>
          <Icon name='microchip' />
          Machine Learning Pipeline
        </Menu.Item>
        <Menu.Item as='a' onClick={this.handleClick.bind(this, "settings")}>
          <Icon name='settings' />
          Settings
        </Menu.Item>
        <Menu.Item as='a' onClick={this.handleClick.bind(this, "info")}>
          <Icon name='info' />
          Info
        </Menu.Item>
      </Sidebar>

      <Sidebar.Pusher style={{minHeight: "100vh"}}>
        <Segment basic>
	    {this.renderSideBar()}
        </Segment>
      </Sidebar.Pusher>
    </Sidebar.Pushable>
    )
  }

}

export default MainPage;
