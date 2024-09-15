import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import HomePage from './pages/HomePage';
import PortfolioPage from './pages/PortfolioPage';
import LoginPage from './pages/LoginPage';
// import RegisterPage from './pages/RegisterPage';
import TradePage from './pages/TradePage';
import AIChatPage from './pages/AIChatPage';
import Navbar from './components/Navbar';
import StrategyPage from './pages/StrategyPage';
import SettingsPage from './pages/SettingsPage';

function App() {
  return (
    <Router>
      <Navbar />
      <Switch>
        <Route path="/portfolio" component={PortfolioPage} />
        <Route path="/trade" component={TradePage} />
        <Route path="/ai-chat" component={AIChatPage} />
        <Route path="/strategies" component={StrategyPage} />
        <Route path="/login" component={LoginPage} />
        <Route path="/settings" component={SettingsPage} />
        {/* <Route path="/register" component={RegisterPage} /> */}
        <Route path="/" component={HomePage} exact />
      </Switch>
    </Router>
  );
}

export default App;
