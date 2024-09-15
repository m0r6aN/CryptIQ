import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { createStrategy } from '../redux/actions/strategyActions';

const RebalanceStrategyForm = () => {
  const dispatch = useDispatch();
  const [name, setName] = useState('');
  const [allocations, setAllocations] = useState('');

  const handleSubmit = e => {
    e.preventDefault();
    const allocationPairs = allocations.split(',').map(pair => pair.trim().split(':'));
    const target_allocations = {};
    allocationPairs.forEach(([symbol, percentage]) => {
      target_allocations[symbol] = parseFloat(percentage);
    });
    dispatch(createStrategy({ name, target_allocations }));
    setName('');
    setAllocations('');
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Create Strategy</h2>
      <input
        type="text"
        placeholder="Strategy Name"
        value={name}
        onChange={e => setName(e.target.value)}
        required
      />
      <input
        type="text"
        placeholder="Allocations (e.g., BTC:50,ETH:30)"
        value={allocations}
        onChange={e => setAllocations(e.target.value)}
        required
      />
      <button type="submit">Create</button>
    </form>
  );
};

export default RebalanceStrategyForm;
