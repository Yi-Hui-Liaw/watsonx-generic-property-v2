import React from "react";
import { Link } from "react-router-dom";
import "../styles/PropertyCard.css";

const PropertyCard = ({ property }) => {
  return (
    <div className="property-card">
      <img src={property.image} alt={property.title} />
      <div className="property-info">
        <h3>{property.title}</h3>
        <p>{property.location}</p>
        <Link to={property.link}>View Details</Link>
      </div>
    </div>
  );
};

export default PropertyCard;
