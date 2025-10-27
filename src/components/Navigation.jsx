import { Link, useLocation } from 'react-router-dom';

const Navigation = () => {
  const location = useLocation();

  return (
    <nav className="navbar">
      <ul className="nav-links">
        <li>
          <Link 
            to="/" 
            className={location.pathname === '/' ? 'active' : ''}
          >
            Home
          </Link>
        </li>
        <li>
          <Link 
            to="/menu" 
            className={location.pathname === '/menu' ? 'active' : ''}
          >
            Menu
          </Link>
        </li>
      </ul>
    </nav>
  );
};

export default Navigation;