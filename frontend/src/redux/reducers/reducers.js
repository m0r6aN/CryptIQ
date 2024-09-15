const initialState = {
    portfolio: [],
    loading: false,
    error: null,
  };
  
  function rootReducer(state = initialState, action) {
    switch (action.type) {
      case 'FETCH_PORTFOLIO_SUCCESS':
        return { ...state, portfolio: action.payload, loading: false };
      case 'FETCH_PORTFOLIO_ERROR':
        return { ...state, error: action.error, loading: false };
      default:
        return state;
    }
  }
  
  export default rootReducer;
  