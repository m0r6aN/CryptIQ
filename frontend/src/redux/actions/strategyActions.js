import api from '../../services/api';

export const FETCH_STRATEGIES_SUCCESS = 'FETCH_STRATEGIES_SUCCESS';
export const CREATE_STRATEGY_SUCCESS = 'CREATE_STRATEGY_SUCCESS';
export const DELETE_STRATEGY_SUCCESS = 'DELETE_STRATEGY_SUCCESS';

export const fetchStrategies = () => async dispatch => {
  try {
    const response = await api.get('/portfolio/strategies/');
    dispatch({ type: FETCH_STRATEGIES_SUCCESS, payload: response.data });
  } catch (error) {
    console.error(error);
  }
};

export const createStrategy = strategy => async dispatch => {
  try {
    const response = await api.post('/portfolio/strategies/', strategy);
    dispatch({ type: CREATE_STRATEGY_SUCCESS, payload: response.data });
  } catch (error) {
    console.error(error);
  }
};

export const deleteStrategy = strategyId => async dispatch => {
  try {
    await api.delete(`/portfolio/strategies/${strategyId}/`);
    dispatch({ type: DELETE_STRATEGY_SUCCESS, payload: strategyId });
  } catch (error) {
    console.error(error);
  }
};
