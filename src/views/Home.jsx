import { VscHome, VscArchive, VscAccount, VscSettingsGear } from 'react-icons/vsc';
import GradientText from '../components/ui/GradientText';
import Dock from '../components/ui/Dock';
import './Home.css';
import { useRef, useState } from 'react';

const Home = () => {
  const [videoLoaded, setVideoLoaded] = useState(false);
  const videoRef = useRef(null);

  const items = [
    { icon: <VscHome size={24} />, label: 'Home', onClick: () => window.location.hash = '/' },
    { icon: <VscArchive size={24} />, label: 'Menu', onClick: () => window.location.hash = '/menu' },
    { icon: <VscAccount size={24} />, label: 'Profile', onClick: () => alert('Profile!') },
    { icon: <VscSettingsGear size={24} />, label: 'Settings', onClick: () => alert('Settings!') },
  ];

  const handleVideoLoad = () => {
    setVideoLoaded(true);
    if (videoRef.current) {
      videoRef.current.play().catch(console.log);
    }
  };

  return (
    <div className="page">
      {/* Video Background */}
      <div className="video-background">
        <video
          ref={videoRef}
          autoPlay
          muted
          loop
          playsInline
          preload="metadata"
          className="background-video"
          onLoadedData={handleVideoLoad}
          onError={(e) => console.error('Video error:', e)}
        >
          <source src="./models/model.mp4" type="video/mp4" />
          Your browser does not support the video tag.
        </video>
        <div className="video-overlay"></div>
        
        {/* Loading fallback */}
        {!videoLoaded && (
          <div className="video-loading-fallback">
            <div className="loading-gradient"></div>
          </div>
        )}
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
              fontSize="12rem"
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
                fontSize="3.5rem"
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
