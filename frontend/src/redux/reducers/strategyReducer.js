import {
  FETCH_STRATEGIES_SUCCESS,
  CREATE_STRATEGY_SUCCESS,
  DELETE_STRATEGY_SUCCESS,
} from '../actions/strategyActions';

const initialState = {
  strategies: [],
};

const strategyReducer = (state = initialState, action) => {
  switch (action.type) {
    case FETCH_STRATEGIES_SUCCESS:
      return { ...state, strategies: action.payload };
    case CREATE_STRATEGY_SUCCESS:
      return { ...state, strategies: [...state.strategies, action.payload] };
    case DELETE_STRATEGY_SUCCESS:
      return {
        ...state,
        strategies: state.strategies.filter(
          strategy => strategy.id !== action.payload
        ),
      };
    default:
      return state;
  }
};

export default strategyReducer;
