const initialState = {
    data: [],
    loading: false,
    error: null,
  };
  
  export default function portfolioReducer(state = initialState, action) {
    switch (action.type) {
      case 'PORTFOLIO_LOADING':
        return { ...state, loading: true, error: null };
      case 'FETCH_PORTFOLIO_SUCCESS':
        return { ...state, data: action.payload, loading: false };
      case 'FETCH_PORTFOLIO_ERROR':
        return { ...state, error: action.error, loading: false };
      default:
        return state;
    }
  }
  