import io from 'socket.io-client';

const socket = io('ws://localhost:8000', {
  path: '/ws/portfolio/',
  transports: ['websocket'],
  auth: {
    token: localStorage.getItem('access_token'),
  },
});

export default socket;
