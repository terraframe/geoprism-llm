import React from "react"
import Container from '@mui/material/Container';
import Grid from '@mui/material/Grid2';

import Chatbot from 'react-chatbot-kit'
import 'react-chatbot-kit/build/main.css';

import ActionProvider from './chatbot/ActionProvider';
import MessageParser from './chatbot/MessageParser';
import config from './chatbot/config';
import { Box } from '@mui/material';

import './App.css';

export default function App() {
  return (

    //Initialise
    <Container style={{ background: '#f2f6fc', height: '100vh' }} maxWidth={false} className='App'>
      <Box sx={{ flexGrow: 1 }} justifyContent='center'>
        <Grid container spacing={2}>
          <Grid size={2}>
          </Grid>
          <Grid size={8}>
            <Chatbot
              config={config}
              actionProvider={ActionProvider}
              messageParser={MessageParser}
              validator={(message) => message.length > 0} />
          </Grid>
          <Grid size={2}>
          </Grid>
        </Grid>
      </Box>
    </Container>
  );
}
