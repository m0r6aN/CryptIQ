import React, { useState, useEffect } from 'react';

const TradePage = () => {
  const [portfolio, setPortfolio] = useState([]);
  const [selectedCoin, setSelectedCoin] = useState('');
  const [amount, setAmount] = useState('');
  const [tradeHistory, setTradeHistory] = useState([]);

  useEffect(() => {
    // Fetch portfolio and trade history when component mounts
    fetchPortfolio();
    fetchTradeHistory();
  }, []);

  const fetchPortfolio = async () => {
    // Call backend API to get portfolio data
    const response = await fetch('/api/portfolio');
    const data = await response.json();
    setPortfolio(data);
  };

  const fetchTradeHistory = async () => {
    // Call backend API to get trade history
    const response = await fetch('/api/trade-history');
    const data = await response.json();
    setTradeHistory(data);
  };

  const handleTrade = async (type) => {
    if (!selectedCoin || !amount) return;

    const response = await fetch('/api/trade', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ coin: selectedCoin, amount, type })
    });

    if (response.ok) {
      alert(`${type} order placed successfully!`);
      fetchPortfolio(); // Refresh portfolio after trade
    } else {
      alert('Error placing trade');
    }
  };

  return (
    <div>
      <h2>TradePage</h2>

      {/* Portfolio Overview */}
      <h3>Portfolio</h3>
      <ul>
        {portfolio.map((coin) => (
          <li key={coin.symbol}>
            {coin.symbol}: {coin.amount} units (${coin.price})
          </li>
        ))}
      </ul>

      {/* Order Form */}
      <h3>Place Trade</h3>
      <select value={selectedCoin} onChange={(e) => setSelectedCoin(e.target.value)}>
        <option value="">Select Coin</option>
        {portfolio.map((coin) => (
          <option key={coin.symbol} value={coin.symbol}>
            {coin.symbol}
          </option>
        ))}
      </select>
      <input
        type="number"
        value={amount}
        placeholder="Amount"
        onChange={(e) => setAmount(e.target.value)}
      />
      <button onClick={() => handleTrade('buy')}>Buy</button>
      <button onClick={() => handleTrade('sell')}>Sell</button>

      {/* Trade History */}
      <h3>Trade History</h3>
      <ul>
        {tradeHistory.map((trade) => (
          <li key={trade.id}>
            {trade.type.toUpperCase()} {trade.amount} {trade.coin} at ${trade.price}
          </li>
        ))}
      </ul>

      {/* Additional features like chart, order book will be added here */}
    </div>
  );
};

export default TradePage;
