import API from '../../services/api';

export const fetchMarketData = () => async dispatch => {
  dispatch({ type: 'MARKET_DATA_LOADING' });
  try {
    const response = await API.get('market-data/');
    dispatch({ type: 'FETCH_MARKET_DATA_SUCCESS', payload: response.data });
  } catch (error) {
    dispatch({ type: 'FETCH_MARKET_DATA_ERROR', error });
  }
};
