import React from 'react';
import { useSelector } from 'react-redux';
import Notification from './Notification';

const NotificationCenter = () => {
  const notifications = useSelector(state => state.notifications.items);

  return (
    <div className="notification-center">
      {notifications.map((notif, index) => (
        <Notification key={index} message={notif.message} />
      ))}
    </div>
  );
};

export default NotificationCenter;
