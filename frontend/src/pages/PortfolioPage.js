import React, { useState, useEffect } from 'react';
import socket from '../services/websocket';

function PortfolioPage() {
  const [portfolio, setPortfolio] = useState([]);

  useEffect(() => {
    socket.on('connect', () => {
      console.log('WebSocket connected');
    });

    socket.on('portfolio_update', data => {
      console.log('Portfolio update:', data);
      // Update state with the new data
      setPortfolio(data.holdings); // Adjust 'data.holdings' based on your actual data structure
    });

    return () => {
      socket.off('connect');
      socket.off('portfolio_update');
    };
  }, []);

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl text-white mb-4">My Portfolio</h1>
      <ul>
        {portfolio.map((holding, index) => (
          <li key={index} className="text-white">
            {holding.asset.symbol}: {holding.quantity}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default PortfolioPage;
