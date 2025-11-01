import { VscHome, VscArchive, VscAccount, VscSettingsGear } from 'react-icons/vsc';
import GradientText from '../components/ui/GradientText';
import Dock from '../components/ui/Dock';
import './Home.css';
import { useNavigate } from 'react-router-dom';

const Home = () => {
  const navigate = useNavigate();

  const items = [
    { 
      icon: <VscHome size={24} />, 
      label: 'Home', 
      onClick: () => navigate('/home') 
    },
    { 
      icon: <VscArchive size={24} />, 
      label: 'Menu', 
      onClick: () => navigate('/menu') 
    },
    { 
      icon: <VscAccount size={24} />, 
      label: 'Profile', 
      onClick: () => alert('Profile!') 
    },
    { 
      icon: <VscSettingsGear size={24} />, 
      label: 'Settings', 
      onClick: () => alert('Settings!') 
    },
  ];

  return (
    <div className="page">
      {/* Video Background */}
      <div className="video-background">
        <video
          autoPlay
          muted
          loop
          playsInline
          className="background-video"
        >
          <source src="/models/model.mp4" type="video/mp4" />
          Your browser does not support the video tag.
        </video>
        <div className="video-overlay"></div>
      </div>
      
      <Dock 
        items={items}
        panelHeight={68}
        baseItemSize={50}
        magnification={70}
      />
      
      <div className="corner-content">
        <div className="main-title">
          <h1 className="title-main">
            <GradientText
              colors={['#00aeff', '#ad2837', '#ffb700']}
              animationDuration="4s"
              fontSize="clamp(4rem, 10vw, 12rem)"
              fontWeight="900"
              className="main-title-text"
            >
              Drive Pulse
            </GradientText>
          </h1>
          <div className="title-subtitle">
            <p>
              <GradientText
                colors={['#26c3cb', '#4cb892', '#0977d1']}
                animationDuration="5s"
                fontSize="clamp(1.5rem, 4vw, 3.5rem)"
                fontWeight="400"
                className="subtitle-text"
              >
                The Pulse of Smarter Mobility
              </GradientText>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;
