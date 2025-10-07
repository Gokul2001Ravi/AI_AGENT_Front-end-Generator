import React from 'react';
import { Link } from 'react-router-dom';
import UserMenu from './UserMenu';
import { useSelector } from 'react-redux';

function Navbar() {
  const cartItemsCount = useSelector((state) => state.cart.items.length);

  return (
    <nav className="bg-gradient-to-r from-blue-600 to-purple-700 p-4 shadow-lg sticky top-0 z-50">
      <div className="container mx-auto flex justify-between items-center">
        <Link to="/" className="text-white text-3xl font-bold hover:text-blue-200 transition duration-300">
          AI Shopper
        </Link>
        <div className="flex items-center space-x-6">
          <Link to="/" className="text-white hover:text-blue-200 text-lg transition duration-300">
            Home
          </Link>
          <Link to="/recommendations" className="text-white hover:text-blue-200 text-lg transition duration-300">
            Recommendations
          </Link>
          <Link to="/deals" className="text-white hover:text-blue-200 text-lg transition duration-300">
            Deals
          </Link>
          <Link to="/try-on" className="text-white hover:text-blue-200 text-lg transition duration-300">
            Try-On
          </Link>
          <Link to="/cart" className="relative text-white hover:text-blue-200 text-lg transition duration-300">
            Cart ({cartItemsCount})
          </Link>
          <Link to="/orders" className="text-white hover:text-blue-200 text-lg transition duration-300">
            Orders
          </Link>
          <UserMenu />
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
