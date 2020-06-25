import React from 'react';
import { Header, Icon, Menu, Segment, Sidebar } from 'semantic-ui-react';


class Index extends React.Component {
  render() {
    return (
      <Header as='h3'>Raspberry Pi Weather System</Header>
    );
  }
}

class MainPage extends React.Component {
    
  constructor(props) {
    super(props);
      this.content = <Index />;
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
        <Menu.Item as='a' onClick={function() {alert('Click!');}}>
          <Icon name='chart line' />
          Weather Data
        </Menu.Item>
        <Menu.Item as='a'>
          <Icon name='microchip' />
          Machine Learning Pipeline
        </Menu.Item>
        <Menu.Item as='a'>
          <Icon name='settings' />
          Settings
        </Menu.Item>
        <Menu.Item as='a'>
          <Icon name='info' />
          Info
        </Menu.Item>
      </Sidebar>

      <Sidebar.Pusher style={{"min-height": "100vh"}}>
        <Segment basic>
	    {this.content}
        </Segment>
      </Sidebar.Pusher>
    </Sidebar.Pushable>
    )
  }

}

export default MainPage;
