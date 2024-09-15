const initialState = {
    data: {},
    loading: false,
    error: null,
  };
  
  export default function marketDataReducer(state = initialState, action) {
    switch (action.type) {
      case 'MARKET_DATA_LOADING':
        return { ...state, loading: true, error: null };
      case 'FETCH_MARKET_DATA_SUCCESS':
        return { ...state, data: action.payload, loading: false };
      case 'FETCH_MARKET_DATA_ERROR':
        return { ...state, error: action.error, loading: false };
      default:
        return state;
    }
  }
  