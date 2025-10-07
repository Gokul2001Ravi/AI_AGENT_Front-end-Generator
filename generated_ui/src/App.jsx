import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import ChatbotWidget from './components/ChatbotWidget';

// Import Screens
import Home from './screens/Home';
import SmartRecommendations from './screens/SmartRecommendations';
import DealsHub from './screens/DealsHub';
import VirtualTryOn from './screens/VirtualTryOn';
import CartCheckout from './screens/CartCheckout';
import OrderTracking from './screens/OrderTracking';
import Profile from './screens/Profile';

function App() {
  return (
    <div className="flex flex-col min-h-screen">
      <Navbar />
      <main className="flex-grow">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/recommendations" element={<SmartRecommendations />} />
          <Route path="/deals" element={<DealsHub />} />
          <Route path="/try-on" element={<VirtualTryOn />} />
          <Route path="/cart" element={<CartCheckout />} />
          <Route path="/orders" element={<OrderTracking />} />
          <Route path="/profile" element={<Profile />} />
        </Routes>
      </main>
      <ChatbotWidget />
      <Footer />
    </div>
  );
}

export default App;
