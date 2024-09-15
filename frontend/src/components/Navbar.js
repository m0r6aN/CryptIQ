import React from 'react';
import { Link } from 'react-router-dom';

function Navbar() {
  return (
    <nav className="bg-gray-800 p-4">
      <div className="container mx-auto flex">
        <Link to="/" className="text-white mr-4">Home</Link>
        <Link to="/portfolio" className="text-white">Portfolio</Link>
      </div>
    </nav>
  );
}

export default Navbar;
