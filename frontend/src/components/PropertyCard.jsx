import React from "react";
import { Link } from "react-router-dom";
import "../styles/PropertyCard.css";

const PropertyCard = ({ property }) => {
  return (
    <Link to={property.link} className="property-card-link">
      <div className="property-card">
        <img src={property.image} alt={property.title} />
        <div className="property-info">
          <h3>{property.title}</h3>
          <p className="location">{property.location}</p>
          <p className="additional-info" dangerouslySetInnerHTML={{ __html: property.additionalInfo }} />
        </div>
      </div>
    </Link>
  );
};

export default PropertyCard;
