import API from '../../services/api';

export const fetchPortfolio = () => async dispatch => {
  dispatch({ type: 'PORTFOLIO_LOADING' });
  try {
    const response = await API.get('portfolio/');
    dispatch({ type: 'FETCH_PORTFOLIO_SUCCESS', payload: response.data.holdings });
  } catch (error) {
    dispatch({ type: 'FETCH_PORTFOLIO_ERROR', error });
  }
};
