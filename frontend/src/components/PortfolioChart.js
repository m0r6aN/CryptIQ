import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { fetchMarketData } from '../redux/actions/marketDataActions';

const PortfolioChart = () => {
  const dispatch = useDispatch();
  const marketData = useSelector(state => state.marketData.data);

  useEffect(() => {
    dispatch(fetchMarketData('bitcoin'));
  }, [dispatch]);

  return (
    <div>
      <h2>Portfolio Performance</h2>
      {/* Implement chart using marketData */}
    </div>
  );
};

export default PortfolioChart;
