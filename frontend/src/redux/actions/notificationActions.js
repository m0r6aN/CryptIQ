export const ADD_NOTIFICATION = 'ADD_NOTIFICATION';
export const CLEAR_NOTIFICATIONS = 'CLEAR_NOTIFICATIONS';

export const addNotification = message => ({
  type: ADD_NOTIFICATION,
  payload: { message },
});

export const clearNotifications = () => ({
  type: CLEAR_NOTIFICATIONS,
});
