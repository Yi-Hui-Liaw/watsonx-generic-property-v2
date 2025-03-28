import React from "react";
import "../styles/NexusOne.css"; // Reuse the same CSS
import bedIcon from "../assets/bedroom.png";
import bathIcon from "../assets/bathroom.png";
import parkingIcon from "../assets/parking-lot.png";
import lumenhImage from "../assets/lumenh-2.png"; 

const Lumenh = () => {
  return (
    <div className="nexus-container">
      {/* Left Image Section */}
      <div className="nexus-image">
        <img src={lumenhImage} alt="The Lumenh" />
      </div>

      {/* Right Content Section */}
      <div className="nexus-details">
        <h2 className="title">The Lumenh</h2>
        <p className="subtitle">A true masterpiece of green architecture - located adjacent to <strong>Mutiara Damansara.</strong></p>
        <p className="description">
          This elevated site boasts breathtaking views and a unique topography that naturally preserves the natural surroundings.  
          <br></br>Our luxurious detached villas and twin villas are designed to maximize natural light and ventilation,
          creating a sense of srenity and tranquility within each residence. With only 80 units per acre,
          residents can enjoy absolute privacy and comfort in their spacious homes.
        </p>

        {/* Features Section */}
        <div className="features">
          <h3>Up-to</h3>
          <div className="features-icons">
            <div className="feature">
              <img src={bedIcon} alt="Bedroom" />
              <p>4 Bedrooms</p>
            </div>
            <div className="feature">
              <img src={bathIcon} alt="Bathroom" />
              <p>3 Bathrooms</p>
            </div>
            <div className="feature">
              <img src={parkingIcon} alt="Parking" />
              <p>2 Parking Lots</p>
            </div>
          </div>
        </div>

        {/* Property Details */}
        <div className="property-details">
          <div className="detail"><span>Build-Up</span>From 51m² – 135m² (526ft² – 1470ft²)</div>
          <div className="detail"><span>Status</span>New Launch</div>
          <div className="detail"><span>Price</span>RM 5XX,XXX – RM8XX,XXX</div>
          <div className="detail"><span>Tenure</span>Freehold</div>
          <div className="detail"><span>Property Type</span>2-Storey Terrace</div>
        </div>
      </div>
    </div>
  );
};

export default Lumenh;
