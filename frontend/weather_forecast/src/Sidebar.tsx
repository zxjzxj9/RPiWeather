import React from 'react';
import { Header, Icon, List, Menu, Segment, Sidebar, Label, Button } from 'semantic-ui-react';
import { DateTimeInput, DateTimeInputOnChangeData } from 'semantic-ui-calendar-react';

type DateTimeFormHandleChangeData = DateTimeInputOnChangeData;

class Index extends React.Component {
  render() {
    return (
      <Header as='h1'>Raspberry Pi Weather System</Header>
    );
  }
}

class Chart extends React.Component<any, any>{
  constructor(props: any) {
    super(props);
    //var date1 = new Date();
    // 8 Hours before current time
    //date1.setHours(date1.getHours() - 8);
    //var date2 = new Date();
    this.state = {
      year: '',
      month: '',
      date: '',
      time: '',
      dateTime: '',
      datesRange: '',
      monthsRange: '',
      start: '',
      end: ''
    };
  }

  private handleChange = (event: React.SyntheticEvent, { name, value }: DateTimeFormHandleChangeData) => {
    if (this.state.hasOwnProperty(name)) {
      // console.log(name, value);
      this.setState({ [name]: value });
    }
  }

  render() {
    return (
      <Segment>
      <Header as='h1'>Weather Data Chart</Header>
      <List divided relaxed>
        <List.Item>
          <Label pointing='below'> Start Datetime: </Label> 
          <DateTimeInput value={this.state.start} name='start' clearable={true} dateFormat="DD-MM-YY" timeFormat="24" iconPosition='left'
            placeholder="Start Time" onChange={this.handleChange}/>
          <br />
          <Label pointing='below'> End Datetime: </Label> 
          <DateTimeInput value={this.state.end} name='end' clearable={true} dateFormat="DD-MM-YY" timeFormat="24" iconPosition='left'
            placeholder="End Time" onChange={this.handleChange}/>
      	</List.Item>
        <br />
        <Button content="Draw" primary/>

      </List>
      </Segment>
    );
  }
}

class MainPage extends React.Component<any, any>{
    
  constructor(props: any) {
    super(props);
    this.state = {content: 'index'};
  }

  handleClick(componentName: any) {
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
