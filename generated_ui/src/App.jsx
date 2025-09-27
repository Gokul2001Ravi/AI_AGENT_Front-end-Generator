import React from 'react';
import { Provider } from 'react-redux'; // Assuming Redux is used
import store from './store/configureStore';
import NavigationBar from './components/NavigationBar';
import Routes from './Routes'; // Assuming react-router-dom is used for routing

const App = () => {
  return (
    <Provider store={store}>
      <div className="flex flex-col min-h-screen bg-gray-100">
        <NavigationBar />
        <Routes />
      </div>
    </Provider>
  );
};

export default App;