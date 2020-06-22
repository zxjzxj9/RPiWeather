import React from 'react';
// import logo from './logo.svg';
import './App.css';
//import {Rating} from 'semantic-ui-react';
// import d3 from 'd3';
import { Header, Icon, Image, Menu, Segment, Sidebar } from 'semantic-ui-react'

const SidebarExampleVisible = () => (
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
      <Menu.Item as='a'>
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
        <Header as='h3'>Application Content</Header>
        <Image src='https://react.semantic-ui.com/images/wireframe/paragraph.png' />
      </Segment>
    </Sidebar.Pusher>
  </Sidebar.Pushable>
)


// color scheme: https://coolors.co/ffa69e-faf3dd-b8f2e6-aed9e0-5e6472
function App() {
  return (
    <SidebarExampleVisible />
  );
}

export default App;
