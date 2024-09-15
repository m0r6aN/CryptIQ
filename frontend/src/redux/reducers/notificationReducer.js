import { ADD_NOTIFICATION, CLEAR_NOTIFICATIONS } from '../actions/notificationActions';

const initialState = {
  items: [],
};

const notificationReducer = (state = initialState, action) => {
  switch (action.type) {
    case ADD_NOTIFICATION:
      return { ...state, items: [...state.items, action.payload] };
    case CLEAR_NOTIFICATIONS:
      return { ...state, items: [] };
    default:
      return state;
  }
};

export default notificationReducer;
