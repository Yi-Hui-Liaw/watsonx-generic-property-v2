import React from "react";
import "../styles/NexusOne.css"; // Reuse the same CSS
import bedIcon from "../assets/bedroom.png";
import bathIcon from "../assets/bathroom.png";
import parkingIcon from "../assets/parking-lot.png";
import ABCImage from "../assets/abc-2.png"; 

const ABC = () => {
  return (
    <div className="nexus-container">
      {/* Left Image Section */}
      <div className="nexus-image">
        <img src={ABCImage} alt="ABC Residence" />
      </div>

      {/* Right Content Section */}
      <div className="nexus-details">
        <h2 className="title">ABC Residence</h2>
        <p className="subtitle">A perfect tale about <strong>urbanity meets nature.</strong></p>
        <p className="description">
          ABC Residence is the new phase in Damansara Bay, Kepong, Kuala Lumpur.
          Different and bold, this trendy high-rise development showcases flexible living features with
          exciting indoor and outdoor living spaces. <br></br>
          Brimming with features and highly attainable, ABC Residence offers urban liveability a mere 
          7-minute walk to The Beat and Kepong Metro Park Lakeside.
        </p>

        {/* Features Section */}
        <div className="features">
          <h3>Up-to</h3>
          <div className="features-icons">
            <div className="feature">
              <img src={bedIcon} alt="Bedroom" />
              <p>5 Bedrooms</p>
            </div>
            <div className="feature">
              <img src={bathIcon} alt="Bathroom" />
              <p>4 Bathrooms</p>
            </div>
            <div className="feature">
              <img src={parkingIcon} alt="Parking" />
              <p>2 Parking Lots</p>
            </div>
          </div>
        </div>

        {/* Property Details */}
        <div className="property-details">
          <div className="detail"><span>Build-Up</span>From 56m² – 145m² (547ft² – 1870ft²)</div>
          <div className="detail"><span>Status</span>New Launch</div>
          <div className="detail"><span>Price</span>RM 8XX,XXX – RM1,2XX,XXX</div>
          <div className="detail"><span>Tenure</span>Freehold</div>
          <div className="detail"><span>Property Type</span>2-Storey Semi-D</div>
        </div>
      </div>
    </div>
  );
};

export default ABC;
