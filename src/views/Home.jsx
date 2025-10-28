import { VscHome, VscArchive, VscAccount, VscSettingsGear } from 'react-icons/vsc';
import GradientText from '../components/ui/GradientText';
import Dock from '../components/ui/Dock';
import './Home.css';
import { useRef, useState, useEffect } from 'react';

const Home = () => {
  const [videoLoaded, setVideoLoaded] = useState(false);
  const [videoError, setVideoError] = useState(false);
  const videoRef = useRef(null);

  const items = [
    { icon: <VscHome size={24} />, label: 'Home', onClick: () => window.location.hash = '/' },
    { icon: <VscArchive size={24} />, label: 'Menu', onClick: () => window.location.hash = '/menu' },
    { icon: <VscAccount size={24} />, label: 'Profile', onClick: () => alert('Profile!') },
    { icon: <VscSettingsGear size={24} />, label: 'Settings', onClick: () => alert('Settings!') },
  ];

  // Try multiple video paths
  const videoPaths = [
    './models/model.mp4',
    '/models/model.mp4',
    'models/model.mp4'
  ];

  useEffect(() => {
    // Test if video exists
    const testVideoLoad = async () => {
      for (const path of videoPaths) {
        try {
          const response = await fetch(path, { method: 'HEAD' });
          if (response.ok) {
            console.log('Video found at:', path);
            return;
          }
        } catch (error) {
          console.log('Video not found at:', path);
        }
      }
      setVideoError(true);
    };

    testVideoLoad();
  }, []);

  const handleVideoLoad = () => {
    console.log('Video loaded successfully');
    setVideoLoaded(true);
    setVideoError(false);
  };

  const handleVideoError = (e) => {
    console.error('Video failed to load:', e);
    setVideoError(true);
    setVideoLoaded(false);
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
          preload="auto"
          className="background-video"
          onLoadedData={handleVideoLoad}
          onError={handleVideoError}
        >
          {videoPaths.map((path, index) => (
            <source key={index} src={path} type="video/mp4" />
          ))}
          Your browser does not support the video tag.
        </video>
        
        {/* Fallback background if video fails */}
        {(videoError || !videoLoaded) && (
          <div className="fallback-background">
            <div className="animated-gradient-fallback"></div>
          </div>
        )}
        
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
