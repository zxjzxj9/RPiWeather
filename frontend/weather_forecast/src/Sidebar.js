import React from 'react';
import { Header, Icon, Menu, Segment, Sidebar } from 'semantic-ui-react';


class Index extends React.Component {
  render() {
    return (
      <Header as='h3'>Raspberry Pi Weather System</Header>
    );
  }
}

class Chart extends React.Component {

  render() {
    return (
      <Header as='h3'>Weather Data Chart</Header>
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

      <Sidebar.Pusher style={{"min-height": "100vh"}}>
        <Segment basic>
	    {this.renderSideBar()}
        </Segment>
      </Sidebar.Pusher>
    </Sidebar.Pushable>
    )
  }

}

export default MainPage;
