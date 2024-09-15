import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import {
  fetchStrategies,
  deleteStrategy,
} from '../redux/actions/strategyActions';
import RebalanceStrategyForm from '../components/RebalanceStrategyForm';

const StrategyPage = () => {
  const dispatch = useDispatch();
  const strategies = useSelector(state => state.strategy.strategies);

  const [editingStrategy, setEditingStrategy] = useState(null);

  useEffect(() => {
    dispatch(fetchStrategies());
  }, [dispatch]);

  const handleEdit = strategy => {
    // Set the strategy to be edited in the component's state
    setEditingStrategy(strategy);
    // Possibly open a modal or navigate to an edit page
  };

  const handleDelete = strategyId => {
    dispatch(deleteStrategy(strategyId));
  };

  return (
    <div>
      <h1>Rebalancing Strategies</h1>
      <RebalanceStrategyForm />
      <ul>
        {strategies.map(strategy => (
          <li key={strategy.id}>
            {strategy.name}
            <button onClick={() => handleEdit(strategy)}>Edit</button>
            <button onClick={() => handleDelete(strategy.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default StrategyPage;
