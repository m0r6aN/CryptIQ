import React, { useState, useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import PortfolioChart from './PortfolioChart';
import { fetchPortfolio } from '../redux/actions/portfolioActions';
import { fetchMarketData } from '../redux/actions/marketDataActions';
import { Link } from 'react-router-dom';

function Dashboard() {
  const dispatch = useDispatch();
  const portfolio = useSelector(state => state.portfolio.data);
  const marketData = useSelector(state => state.marketData.data);
  const loading = useSelector(state => state.portfolio.loading || state.marketData.loading);
  const error = useSelector(state => state.portfolio.error || state.marketData.error);

  useEffect(() => {
    dispatch(fetchPortfolio());
    dispatch(fetchMarketData());
  }, [dispatch]);

  if (loading) {
    return <div className="text-white">Loading dashboard...</div>;
  }

  if (error) {
    return <div className="text-red-500">Error loading dashboard: {error.message}</div>;
  }

  // Calculate total portfolio value
  const totalValue = portfolio.reduce((acc, holding) => {
    const symbol = holding.asset.symbol;
    const marketPrice = marketData[symbol]?.price || 0;
    return acc + holding.quantity * marketPrice;
  }, 0);

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl text-white mb-6">Dashboard</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Portfolio Summary */}
        <div className="bg-gray-800 p-4 rounded">
          <h2 className="text-xl text-white mb-4">Portfolio Summary</h2>
          <p className="text-white text-2xl mb-4">${totalValue.toFixed(2)}</p>
          <PortfolioChart portfolio={portfolio} marketData={marketData} />
        </div>

        {/* Asset Allocation */}
        <div className="bg-gray-800 p-4 rounded">
          <h2 className="text-xl text-white mb-4">Asset Allocation</h2>
          <ul>
            {portfolio.map((holding) => {
              const symbol = holding.asset.symbol;
              const marketPrice = marketData[symbol]?.price || 0;
              const value = holding.quantity * marketPrice;
              const allocation = totalValue ? ((value / totalValue) * 100).toFixed(2) : 0;

              return (
                <li key={symbol} className="text-white mb-2">
                  {symbol}: {allocation}% (${value.toFixed(2)})
                </li>
              );
            })}
          </ul>
        </div>
      </div>

      {/* Recent Transactions */}
      <div className="bg-gray-800 p-4 rounded mt-6">
        <h2 className="text-xl text-white mb-4">Recent Transactions</h2>
        {/* Implement the transactions list or link to transactions page */}
        <Link to="/transactions" className="text-blue-400">View all transactions</Link>
      </div>

      {/* AI Assistant Integration */}
      <div className="bg-gray-800 p-4 rounded mt-6">
        <h2 className="text-xl text-white mb-4">AI Assistant</h2>
        <p className="text-white mb-2">Get personalized insights and recommendations.</p>
        <Link to="/ai-chat" className="text-blue-400">Chat with AI Assistant</Link>
      </div>

      {/* Notifications and Alerts */}
      <div className="bg-gray-800 p-4 rounded mt-6">
        <h2 className="text-xl text-white mb-4">Notifications and Alerts</h2>
        {/* Implement notifications or link to settings */}
        <p className="text-white">No new notifications.</p>
      </div>
    </div>
  );
}

export default Dashboard;
