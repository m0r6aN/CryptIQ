import api from '../../services/api';

export const FETCH_PREFERENCES_SUCCESS = 'FETCH_PREFERENCES_SUCCESS';
export const UPDATE_PREFERENCES_SUCCESS = 'UPDATE_PREFERENCES_SUCCESS';

export const fetchPreferences = () => async dispatch => {
  try {
    const response = await api.get('/accounts/preferences/');
    dispatch({ type: FETCH_PREFERENCES_SUCCESS, payload: response.data });
  } catch (error) {
    console.error(error);
  }
};

export const updatePreferences = preferences => async dispatch => {
  try {
    const response = await api.put('/accounts/preferences/', preferences);
    dispatch({ type: UPDATE_PREFERENCES_SUCCESS, payload: response.data });
  } catch (error) {
    console.error(error);
  }
};
