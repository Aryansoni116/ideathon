import { HashRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './views/Home';
import Menu from './views/Menu';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/menu" element={<Menu />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
