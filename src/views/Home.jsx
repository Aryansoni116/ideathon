import { VscHome, VscArchive, VscAccount, VscSettingsGear } from 'react-icons/vsc';
import GradientText from '../components/ui/GradientText';
import Dock from '../components/ui/Dock';
import './Home.css';

const Home = () => {
  const items = [
    { icon: <VscHome size={24} />, label: 'Home', onClick: () => window.location.href = '/' },
    { icon: <VscArchive size={24} />, label: 'Menu', onClick: () => window.location.href = '/menu' },
    { icon: <VscAccount size={24} />, label: 'Profile', onClick: () => alert('Profile!') },
    { icon: <VscSettingsGear size={24} />, label: 'Settings', onClick: () => alert('Settings!') },
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
              colors={['#00aeffff', '#ad2837ea', '#ffb700ff']}
              animationDuration="4s"
              fontSize="12rem"  // Direct font size
              fontWeight="900"
              className="main-title-text"
            >
              Drive Pulse
            </GradientText>
          </h1>
          <div className="title-subtitle">
            <p>
              <GradientText
                colors={['#26c3cbc0', '#4cb892ff', '#0977d1ff']}
                animationDuration="5s"
                fontSize="3.5rem"  // Direct font size
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