import axios from 'axios';

export const fetchPortfolio = () => async dispatch => {
  try {
    const response = await axios.get('/api/portfolio/');
    dispatch({ type: 'FETCH_PORTFOLIO_SUCCESS', payload: response.data });
  } catch (error) {
    dispatch({ type: 'FETCH_PORTFOLIO_ERROR', error });
  }
};
