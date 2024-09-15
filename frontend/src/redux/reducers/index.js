import { combineReducers } from 'redux';
import portfolioReducer from './portfolioReducer';
import strategyReducer from './strategyReducer';
import marketDataReducer from './marketDataReducer';
import notificationReducer from './notificationReducer';
import userReducer from './userReducer';

const rootReducer = combineReducers({
  portfolio: portfolioReducer,
  strategy: strategyReducer,
  marketData: marketDataReducer,
  notifications: notificationReducer,
  user: userReducer,
  // Other reducers
});

export default rootReducer;
