import React from "react";
import "../styles/NexusOne.css"; 
import bedIcon from "../assets/bedroom.png";
import bathIcon from "../assets/bathroom.png";
import parkingIcon from "../assets/parking-lot.png";
import nexusOne from "../assets/nexus-2.png";

const NexusOne = () => {
  return (
    <div className="nexus-container">
      {/* Left Image Section */}
      <div className="nexus-image">
        <img src={nexusOne} alt="The Nexus One" />
      </div>

      {/* Right Content Section */}
      <div className="nexus-details">
        <h2 className="title">The Nexus One</h2>
        <p className="subtitle">The Nexus One is now open for registration!</p>
        <p className="description">
          The pioneering project in Property A’s LUXURY Series, where practical living meets effortless convenience. 
          Nestled in Jalan 3/144A, Cheras, Kuala Lumpur, this innovative freehold development is poised to revolutionize 
          urban dwelling. With a starting price of RM350K, don’t miss this opportunity to secure your dream home.
        </p>

        {/* Features Section */}
        <div className="features">
          <h3>Up-to</h3>
          <div className="features-icons">
            <div className="feature">
              <img src={bedIcon} alt="Bedroom" />
              <p>3 Bedrooms</p>
            </div>
            <div className="feature">
              <img src={bathIcon} alt="Bathroom" />
              <p>2 Bathrooms</p>
            </div>
            <div className="feature">
              <img src={parkingIcon} alt="Parking" />
              <p>2 Parking Lots</p>
            </div>
          </div>
        </div>

        {/* Property Details */}
        <div className="property-details">
          <div className="detail"><span>Build-Up</span>From 48m² – 115m² (437ft² – 1270ft²)</div>
          <div className="detail"><span>Status</span>New Launch</div>
          <div className="detail"><span>Price</span>RM 3XX,XXX – RM8XX,XXX</div>
          <div className="detail"><span>Tenure</span>Freehold</div>
          <div className="detail"><span>Property Type</span>Condominium</div>
        </div>
      </div>
    </div>
  );
};

export default NexusOne;
