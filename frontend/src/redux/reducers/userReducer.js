import {
    FETCH_PREFERENCES_SUCCESS,
    UPDATE_PREFERENCES_SUCCESS,
  } from '../actions/userActions';
  
  const initialState = {
    preferences: {},
  };
  
  const userReducer = (state = initialState, action) => {
    switch (action.type) {
      case FETCH_PREFERENCES_SUCCESS:
      case UPDATE_PREFERENCES_SUCCESS:
        return { ...state, preferences: action.payload };
      default:
        return state;
    }
  };
  
  export default userReducer;