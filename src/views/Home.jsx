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
    { 
      icon: <VscHome size={24} />, 
      label: 'Home', 
      onClick: () => window.location.hash = '/' 
    },
    { 
      icon: <VscArchive size={24} />, 
      label: 'Menu', 
      onClick: () => window.location.hash = '/menu' 
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

  // Use public folder path for video
  const videoSrc = './models/model.mp4';

  useEffect(() => {
    // Test if video file exists
    const testVideoExists = async () => {
      try {
        const response = await fetch(videoSrc, { method: 'HEAD' });
        if (!response.ok) {
          console.error('Video file not found at:', videoSrc);
          setVideoError(true);
        }
      } catch (error) {
        console.error('Error checking video:', error);
        setVideoError(true);
      }
    };

    testVideoExists();
  }, []);

  const handleVideoLoad = () => {
    console.log('Video loaded successfully');
    setVideoLoaded(true);
    setVideoError(false);
    
    // Force play on mobile devices
    if (videoRef.current) {
      videoRef.current.play().catch(error => {
        console.log('Auto-play prevented:', error);
      });
    }
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
          onCanPlayThrough={handleVideoLoad}
        >
          <source src={videoSrc} type="video/mp4" />
          Your browser does not support the video tag.
        </video>
        
        {/* Fallback gradient background if video fails to load */}
        {(videoError || !videoLoaded) && (
          <div className="video-fallback">
            <div className="fallback-gradient"></div>
          </div>
        )}
        
        {/* Loading spinner */}
        {!videoLoaded && !videoError && (
          <div className="video-loading">
            <div className="loading-spinner"></div>
          </div>
        )}
        
        <div className="video-overlay"></div>
      </div>
      
      {/* Dock Navigation */}
      <Dock 
        items={items}
        panelHeight={68}
        baseItemSize={50}
        magnification={70}
      />
      
      {/* Main Content */}
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

      {/* Debug info - remove in production */}
      {process.env.NODE_ENV === 'development' && (
        <div style={{
          position: 'fixed',
          top: '10px',
          left: '10px',
          background: 'rgba(0,0,0,0.8)',
          color: 'white',
          padding: '10px',
          zIndex: 1000,
          fontSize: '12px',
          borderRadius: '5px'
        }}>
          Video Loaded: {videoLoaded ? '✅' : '❌'}<br/>
          Video Error: {videoError ? '✅' : '❌'}<br/>
          Video Source: {videoSrc}
        </div>
      )}
    </div>
  );
};

export default Home;
